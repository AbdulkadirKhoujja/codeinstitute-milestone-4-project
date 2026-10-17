import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.http import FileResponse, Http404, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import ResourceForm, ReviewForm, WorkshopForm
from .models import Booking, Resource, Review, Workshop
from .payments import initiate_checkout, process_event
from .services import cancel_booking, expire_bookings, reserve, update_workshop


def listing(request):
    expire_bookings()
    return render(
        request,
        "workshops/list.html",
        {"workshops": Workshop.objects.filter(published=True).select_related("owner")},
    )


def detail(request, pk):
    expire_bookings()
    item = get_object_or_404(Workshop.objects.select_related("owner"), pk=pk, published=True)
    can_access = request.user.is_authenticated and (
        request.user.is_superuser
        or (item.owner_id == request.user.pk and request.user.has_perm("workshops.add_workshop"))
        or Booking.objects.filter(
            workshop=item, attendee=request.user, status="confirmed", paid=True
        ).exists()
    )
    return render(
        request,
        "workshops/detail.html",
        {
            "workshop": item,
            "reviews": item.reviews.filter(visible=True).select_related("attendee"),
            "resources": item.resources.all() if can_access else [],
            "booking_open": item.starts_at > timezone.now() and item.available_seats > 0,
            "review_eligible": request.user.is_authenticated
            and item.ends_at <= timezone.now()
            and Booking.objects.filter(
                workshop=item, attendee=request.user, status="confirmed", attended=True
            ).exists(),
        },
    )


@login_required
@require_POST
def book(request, pk):
    get_object_or_404(Workshop, pk=pk, published=True)
    try:
        reserve(pk, request.user)
        messages.success(request, "Your place is reserved. Check your booking status below.")
    except ValidationError as exc:
        messages.error(request, exc.messages[0])
    return redirect("workshops:bookings")


@login_required
def bookings(request):
    expire_bookings()
    items = (
        Booking.objects.filter(attendee=request.user)
        .select_related("workshop")
        .order_by("-created_at")
    )
    return render(request, "workshops/bookings.html", {"bookings": items})


@login_required
@require_POST
def cancel(request, pk):
    get_object_or_404(Booking, pk=pk, attendee=request.user)
    try:
        cancel_booking(pk, request.user)
        messages.success(
            request, "Booking cancelled. Any verified payment requires manual refund review."
        )
    except ValidationError as exc:
        messages.error(request, exc.messages[0])
    return redirect("workshops:bookings")


def owned_workshops(person):
    if not person.has_perm("workshops.add_workshop"):
        raise PermissionDenied
    return Workshop.objects.all() if person.is_superuser else Workshop.objects.filter(owner=person)


@login_required
def studio(request):
    return render(request, "workshops/studio.html", {"workshops": owned_workshops(request.user)})


@login_required
def edit_workshop(request, pk=None):
    allowed = owned_workshops(request.user)
    item = get_object_or_404(allowed, pk=pk) if pk else Workshop(owner=request.user)
    form = WorkshopForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        if pk:
            # Conditional UPDATE closes the validation-to-save booking race.
            values = {field: form.cleaned_data[field] for field in form.Meta.fields}
            try:
                update_workshop(pk, request.user, values)
            except ValidationError as exc:
                form.add_error("capacity", exc.messages[0])
            else:
                messages.success(request, "Workshop updated.")
                return redirect("workshops:edit", pk=pk)
        else:
            form.save()
            messages.success(request, "Workshop created.")
            return redirect("workshops:edit", pk=item.pk)
    return render(
        request,
        "workshops/edit.html",
        {
            "form": form,
            "workshop": item,
            "roster": item.bookings.select_related("attendee") if pk else [],
            "resource_form": ResourceForm(auto_id="resource_%s"),
            "resources": item.resources.all() if pk else [],
        },
    )


@login_required
def download(request, pk):
    resource = get_object_or_404(Resource.objects.select_related("workshop"), pk=pk)
    item = resource.workshop
    host = request.user.is_superuser or (
        item.owner_id == request.user.pk and request.user.has_perm("workshops.add_workshop")
    )
    if (
        not host
        and not Booking.objects.filter(
            workshop=item, attendee=request.user, status="confirmed", paid=True
        ).exists()
    ):
        raise Http404
    try:
        response = FileResponse(
            resource.file.open("rb"),
            as_attachment=True,
            filename=resource.file.name.rsplit("/", 1)[-1],
            content_type="application/octet-stream",
        )
    except FileNotFoundError:
        raise Http404 from None
    response["Cache-Control"] = "private, no-store"
    return response


@login_required
@require_POST
def upload_resource(request, pk):
    item = get_object_or_404(owned_workshops(request.user), pk=pk)
    form = ResourceForm(request.POST, request.FILES)
    if form.is_valid():
        resource = form.save(commit=False)
        resource.workshop = item
        resource.save()
        messages.success(request, "Private resource added.")
    else:
        messages.error(request, "Resource not saved. Provide a title and a file of at most 5 MB.")
    return redirect("workshops:edit", pk=pk)


@login_required
@require_POST
def delete_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk, workshop__in=owned_workshops(request.user))
    workshop_id = resource.workshop_id
    resource.file.delete(save=False)
    resource.delete()
    messages.success(request, "Resource removed.")
    return redirect("workshops:edit", pk=workshop_id)


@login_required
@require_POST
def attend(request, pk):
    booking = get_object_or_404(
        Booking.objects.select_related("workshop"),
        pk=pk,
        workshop__in=owned_workshops(request.user),
    )
    if booking.status != "confirmed" or booking.workshop.ends_at > timezone.now():
        return HttpResponseBadRequest(
            "Attendance can be recorded only for confirmed bookings after the workshop ends."
        )
    Booking.objects.filter(pk=pk, status="confirmed").update(attended=True)
    messages.success(request, "Attendance recorded.")
    return redirect("workshops:edit", pk=booking.workshop_id)


@login_required
def review(request, pk):
    item = get_object_or_404(Workshop, pk=pk)
    if (
        item.ends_at > timezone.now()
        or not Booking.objects.filter(
            workshop=item, attendee=request.user, status="confirmed", attended=True
        ).exists()
    ):
        raise PermissionDenied(
            "Reviews require attendance recorded by your host after the workshop ends."
        )
    existing = Review.objects.filter(workshop=item, attendee=request.user).first()
    form = ReviewForm(request.POST or None, instance=existing)
    if request.method == "POST" and form.is_valid():
        record = form.save(commit=False)
        record.workshop = item
        record.attendee = request.user
        record.save()
        messages.success(request, "Your review was saved.")
        return redirect("workshops:detail", pk=pk)
    return render(request, "accounts/form.html", {"form": form, "heading": "Review your workshop"})


@login_required
@require_POST
def delete_review(request, pk):
    record = get_object_or_404(Review, pk=pk, attendee=request.user)
    workshop_id = record.workshop_id
    record.delete()
    messages.success(request, "Your review was removed.")
    return redirect("workshops:detail", pk=workshop_id)


@login_required
@require_POST
def checkout(request, pk):
    get_object_or_404(Booking, pk=pk, attendee=request.user)
    try:
        return redirect(initiate_checkout(pk, request.user))
    except ValidationError as exc:
        messages.error(request, exc.messages[0])
        return redirect("workshops:bookings")


@csrf_exempt
@require_POST
def webhook(request):
    if not settings.STRIPE_WEBHOOK_SECRET:
        return HttpResponse(status=503)
    if len(request.body) > 256 * 1024:
        return HttpResponse(status=400)
    try:
        event = stripe.Webhook.construct_event(
            request.body,
            request.headers.get("Stripe-Signature", ""),
            settings.STRIPE_WEBHOOK_SECRET,
        )
        process_event(event.to_dict())
    except (ValueError, stripe.SignatureVerificationError, ValidationError):
        return HttpResponse(status=400)
    return HttpResponse(status=200)
