from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import WorkshopForm
from .models import Booking, Workshop
from .services import cancel_booking, expire_bookings, reserve


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
    return render(request, "workshops/detail.html", {"workshop": item})


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
            if not allowed.filter(pk=pk, reserved__lte=values["capacity"]).update(**values):
                form.add_error(
                    "capacity", "Reservations changed. Reload and choose sufficient capacity."
                )
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
        },
    )
