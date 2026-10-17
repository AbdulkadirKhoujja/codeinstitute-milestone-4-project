"""Transactional domain operations. Start with a write to serialize SQLite writers."""

import time
from datetime import timedelta
from functools import wraps

from django.core.exceptions import ValidationError
from django.db import IntegrityError, OperationalError, transaction
from django.db.models import F
from django.utils import timezone

from .models import Booking, Workshop


def retry_contention(function):
    """Retry whole transactions only for transient SQLite lock contention."""

    @wraps(function)
    def wrapped(*args, **kwargs):
        for attempt in range(8):
            try:
                return function(*args, **kwargs)
            except OperationalError as exc:
                if "locked" not in str(exc).lower():
                    raise
                if attempt == 7:
                    raise ValidationError("The service is busy. Please try again.") from exc
                time.sleep(0.01 * (attempt + 1))

    return wrapped


def _release(booking_id, state, now):
    """Caller owns a transaction; conditional transition releases exactly once."""
    query = Booking.objects.filter(pk=booking_id, status__in=["pending", "confirmed"])
    if state == "expired":
        query = query.filter(status="pending", expires_at__lte=now)
    if query.update(status=state):
        booking = Booking.objects.get(pk=booking_id)
        Workshop.objects.filter(pk=booking.workshop_id).update(reserved=F("reserved") - 1)
        if booking.paid:
            Booking.objects.filter(pk=booking_id).update(refund_required=True)
        return 1
    return 0


@retry_contention
def expire_bookings():
    now = timezone.now()
    ids = list(
        Booking.objects.filter(status="pending", expires_at__lte=now).values_list("pk", flat=True)
    )
    count = 0
    for pk in ids:
        with transaction.atomic():
            count += _release(pk, "expired", now)
    return count


@retry_contention
def reserve(workshop_id, attendee):
    expire_bookings()
    now = timezone.now()
    try:
        with transaction.atomic():
            changed = Workshop.objects.filter(
                pk=workshop_id, published=True, starts_at__gt=now, reserved__lt=F("capacity")
            ).update(reserved=F("reserved") + 1)
            if not changed:
                raise ValidationError("This workshop is no longer available.")
            item = Workshop.objects.get(pk=workshop_id)
            if Booking.objects.filter(
                workshop=item, attendee=attendee, status__in=["pending", "confirmed"]
            ).exists():
                raise ValidationError("You already have a place at this workshop.")
            return Booking.objects.create(
                workshop=item,
                attendee=attendee,
                amount_pence=item.price_pence,
                status="pending" if item.price_pence else "confirmed",
                expires_at=now + timedelta(minutes=35) if item.price_pence else None,
            )
    except IntegrityError as exc:
        raise ValidationError("A place could not be reserved. Please check your bookings.") from exc


@retry_contention
def cancel_booking(booking_id, attendee):
    now = timezone.now()
    with transaction.atomic():
        # A no-op write obtains the database's write lock before reading state.
        Booking.objects.filter(pk=booking_id, attendee=attendee).update(status=F("status"))
        try:
            booking = Booking.objects.select_related("workshop").get(
                pk=booking_id, attendee=attendee
            )
        except Booking.DoesNotExist as exc:
            raise ValidationError("Booking unavailable.") from exc
        if booking.status in ("cancelled", "expired"):
            return
        if booking.workshop.starts_at <= now:
            raise ValidationError("Bookings cannot be cancelled after the workshop starts.")
        _release(booking_id, "cancelled", now)
