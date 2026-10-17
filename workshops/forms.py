from django import forms
from django.utils import timezone

from .models import Workshop


class WorkshopForm(forms.ModelForm):
    class Meta:
        model = Workshop
        fields = (
            "title",
            "description",
            "location",
            "starts_at",
            "ends_at",
            "capacity",
            "price_pence",
            "published",
        )
        widgets = {
            name: forms.DateTimeInput(format="%Y-%m-%dT%H:%M", attrs={"type": "datetime-local"})
            for name in ("starts_at", "ends_at")
        }
        labels = {
            "price_pence": "Price in GBP pence (0 for free)",
            "starts_at": "Starts at (UTC)",
            "ends_at": "Ends at (UTC)",
        }

    def clean(self):
        data = super().clean()
        if not self.instance.pk and data.get("starts_at") and data["starts_at"] <= timezone.now():
            self.add_error("starts_at", "Choose a future start time.")
        if data.get("capacity", 0) < self.instance.reserved:
            self.add_error("capacity", "Capacity cannot be below reserved places.")
        return data
