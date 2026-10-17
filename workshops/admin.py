from django.contrib import admin

from .models import Booking, PaymentAttempt, PaymentEvent, Review


class AuditAdmin(admin.ModelAdmin):
    """Financial and capacity state may only change through domain operations."""

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser


@admin.register(Booking)
class BookingAdmin(AuditAdmin):
    list_display = ("id", "workshop", "attendee", "status", "paid", "refund_required")
    list_filter = ("status", "refund_required")


admin.site.register(PaymentAttempt, AuditAdmin)
admin.site.register(PaymentEvent, AuditAdmin)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("workshop", "attendee", "rating", "visible")
    readonly_fields = ("workshop", "attendee", "rating", "body", "created_at")
    fields = readonly_fields + ("visible",)

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser
