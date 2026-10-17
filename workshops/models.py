from decimal import Decimal

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import F, Q


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
