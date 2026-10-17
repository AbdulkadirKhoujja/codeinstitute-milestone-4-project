from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q

from .storage import PrivateStorage, resource_path


class Workshop(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=140)
    description = models.TextField(max_length=10000)
    location = models.CharField(max_length=240)
    starts_at = models.DateTimeField(db_index=True)
    ends_at = models.DateTimeField()
    capacity = models.PositiveIntegerField()
    reserved = models.PositiveIntegerField(default=0, editable=False)
    price_pence = models.PositiveIntegerField(default=0)
    published = models.BooleanField(default=False, db_index=True)

    class Meta:
        ordering = ["starts_at", "pk"]
        constraints = [
            models.CheckConstraint(
                condition=Q(price_pence=0) | Q(price_pence__gte=50, price_pence__lte=99999999),
                name="supported_workshop_price",
            ),
            models.CheckConstraint(condition=Q(capacity__gte=1), name="positive_capacity"),
            models.CheckConstraint(
                condition=Q(reserved__lte=F("capacity")), name="within_capacity"
            ),
            models.CheckConstraint(condition=Q(ends_at__gt=F("starts_at")), name="ordered_dates"),
        ]

    def clean(self):
        if self.starts_at and self.ends_at and self.ends_at <= self.starts_at:
            raise ValidationError({"ends_at": "End must be after start."})

    @property
    def available_seats(self):
        return self.capacity - self.reserved

    @property
    def price_display(self):
        return f"£{Decimal(self.price_pence) / 100:.2f}" if self.price_pence else "Free"

    def __str__(self):
        return self.title


class Booking(models.Model):
    STATES = [(value, value.title()) for value in ("pending", "confirmed", "cancelled", "expired")]
    workshop = models.ForeignKey(Workshop, on_delete=models.PROTECT, related_name="bookings")
    attendee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    status = models.CharField(max_length=12, choices=STATES)
    amount_pence = models.PositiveIntegerField()
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    paid = models.BooleanField(default=False, editable=False)
    refund_required = models.BooleanField(default=False, editable=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workshop", "attendee"],
                condition=Q(status__in=["pending", "confirmed"]),
                name="one_active_booking",
            ),
            models.CheckConstraint(
                condition=Q(status__in=["pending", "confirmed", "cancelled", "expired"]),
                name="valid_booking_state",
            ),
            models.CheckConstraint(
                condition=~Q(status="pending") | Q(expires_at__isnull=False, amount_pence__gt=0),
                name="pending_has_hold",
            ),
            models.CheckConstraint(
                condition=~Q(status="confirmed") | Q(amount_pence=0) | Q(paid=True),
                name="paid_confirmation_verified",
            ),
        ]
        indexes = [models.Index(fields=["status", "expires_at"])]


class Resource(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="resources")
    title = models.CharField(max_length=140)
    file = models.FileField(storage=PrivateStorage(), upload_to=resource_path)


class PaymentAttempt(models.Model):
    booking = models.OneToOneField(
        Booking, on_delete=models.PROTECT, related_name="payment_attempt"
    )
    session_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    checkout_url = models.URLField(max_length=2048, blank=True)
    state = models.CharField(
        max_length=20,
        default="created",
        choices=[(value, value.title()) for value in ("created", "succeeded", "failed", "review")],
    )
    updated_at = models.DateTimeField(auto_now=True)


class PaymentEvent(models.Model):
    event_id = models.CharField(max_length=255, unique=True)
    event_type = models.CharField(max_length=100)
    received_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, related_name="reviews")
    attendee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    rating = models.PositiveSmallIntegerField()
    body = models.TextField(max_length=2000)
    visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workshop", "attendee"], name="one_review_per_attendee"
            ),
            models.CheckConstraint(
                condition=Q(rating__gte=1, rating__lte=5), name="valid_review_rating"
            ),
        ]
