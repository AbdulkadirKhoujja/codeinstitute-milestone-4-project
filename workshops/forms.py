from django import forms
from django.utils import timezone

from .models import Resource, Review, Workshop


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


class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        fields = ("title", "file")

    def clean_file(self):
        file = self.cleaned_data["file"]
        if file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Files must be 5 MB or smaller.")
        return file


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1, max_value=5, help_text="Choose 1 (poor) to 5 (excellent)."
    )
    body = forms.CharField(
        min_length=10, max_length=2000, widget=forms.Textarea, label="Your review"
    )

    class Meta:
        model = Review
        fields = ("rating", "body")
