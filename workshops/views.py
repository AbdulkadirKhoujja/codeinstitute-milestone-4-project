from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

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
