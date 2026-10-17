"""Test-mode Stripe Checkout. Fulfillment comes only from signed webhooks."""

import hashlib
from datetime import timedelta
from urllib.parse import urlsplit

import stripe
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from django.db.models import F
from django.utils import timezone

from .models import Booking, PaymentAttempt, PaymentEvent
from .services import _release, expire_bookings, retry_contention


@retry_contention
def initiate_checkout(booking_id, person):
    key = settings.STRIPE_TEST_KEY
    if not key.startswith(("rk_test_", "sk_test_")):
        raise ValidationError(
            "Stripe test payments are not configured. Your hold will expire automatically."
        )
    origin = urlsplit(settings.PAYMENT_ORIGIN)
    if (
        not origin.netloc
        or origin.query
        or origin.fragment
        or origin.path not in ("", "/")
        or origin.scheme not in ("http", "https")
        or (settings.PRODUCTION and origin.scheme != "https")
    ):
        raise ValidationError("The payment return address is not configured.")
    expire_bookings()
    with transaction.atomic():
        Booking.objects.filter(pk=booking_id, attendee=person).update(status=F("status"))
        try:
            booking = Booking.objects.get(pk=booking_id, attendee=person)
        except Booking.DoesNotExist as exc:
            raise ValidationError("Booking unavailable.") from exc
        if booking.status != "pending" or booking.expires_at <= timezone.now():
            raise ValidationError("This booking is not awaiting payment.")
        attempt, _ = PaymentAttempt.objects.get_or_create(booking=booking)
        if attempt.session_id:
            return attempt.checkout_url
        if booking.expires_at < timezone.now() + timedelta(minutes=31):
            raise ValidationError(
                "Too little time remains to start Checkout. Cancel and reserve again."
            )
        suffix = "".join(
            chr(97 + byte % 26) for byte in hashlib.sha256(str(booking.pk).encode()).digest()[:8]
        )
        return_url = settings.PAYMENT_ORIGIN.rstrip("/") + "/workshops/bookings/"
        client = stripe.StripeClient(key, max_network_retries=2, stripe_version="2026-09-30.endive")
        try:
            session = client.v1.checkout.sessions.create(
                {
                    "mode": "payment",
                    "client_reference_id": str(booking.pk),
                    "integration_identifier": "skillseat_" + suffix,
                    "line_items": [
                        {
                            "quantity": 1,
                            "price_data": {
                                "currency": "gbp",
                                "unit_amount": booking.amount_pence,
                                "product_data": {
                                    "name": f"SkillSeat workshop booking {booking.pk}"
                                },
                            },
                        }
                    ],
                    "expires_at": int(booking.expires_at.timestamp()),
                    "success_url": return_url,
                    "cancel_url": return_url,
                },
                options={"idempotency_key": f"skillseat-booking-{booking.pk}"},
            )
        except stripe.StripeError as exc:
            raise ValidationError(
                "Stripe is unavailable. Please try again while your hold is active."
            ) from exc
        if (
            session.livemode
            or not session.id.startswith("cs_test_")
            or urlsplit(session.url).scheme != "https"
            or urlsplit(session.url).hostname != "checkout.stripe.com"
        ):
            raise ValidationError("Stripe returned an invalid test Checkout session.")
        attempt.session_id = session.id
        attempt.checkout_url = session.url
        attempt.save()
        return session.url


@retry_contention
def process_event(event):
    if event.get("livemode") is not False:
        raise ValidationError("Only test-mode events are accepted.")
    event_type = event.get("type", "")
    supported = (
        "checkout.session.completed",
        "checkout.session.async_payment_succeeded",
        "checkout.session.expired",
        "checkout.session.async_payment_failed",
    )
    if event_type not in supported:
        return
    obj = event.get("data", {}).get("object", {})
    if obj.get("livemode") is not False or obj.get("mode") != "payment":
        raise ValidationError("Invalid test payment session.")
    if not event.get("id") or len(event["id"]) > 255:
        raise ValidationError("Invalid event identifier.")
    with transaction.atomic():
        # Unique event INSERT serializes writers before any state reads.
        _, created = PaymentEvent.objects.get_or_create(
            event_id=event["id"], defaults={"event_type": event_type}
        )
        if not created:
            return
        try:
            attempt = PaymentAttempt.objects.get(session_id=obj.get("id"))
        except PaymentAttempt.DoesNotExist as exc:
            # Roll back receipt: Stripe may retry if initiation has not committed yet.
            raise ValidationError("Unknown Checkout session.") from exc
        # Serialize different events against cancellation/expiry on the same booking.
        Booking.objects.filter(pk=attempt.booking_id).update(status=F("status"))
        booking = Booking.objects.get(pk=attempt.booking_id)
        now = timezone.now()
        if event_type in ("checkout.session.expired", "checkout.session.async_payment_failed"):
            if booking.status == "pending":
                _release(
                    booking.pk,
                    "cancelled" if event_type.endswith("failed") else "expired",
                    now if event_type.endswith("failed") else max(now, booking.expires_at),
                )
                attempt.state = "failed"
                attempt.save()
            return
        if obj.get("payment_status") != "paid":
            return
        matching = (
            obj.get("amount_total") == booking.amount_pence
            and obj.get("currency") == "gbp"
            and obj.get("client_reference_id") == str(booking.pk)
        )
        if not matching:
            if booking.status == "pending":
                _release(booking.pk, "cancelled", now)
            Booking.objects.filter(pk=booking.pk).update(refund_required=True)
            attempt.state = "review"
        elif booking.status == "confirmed" and booking.paid:
            return
        elif booking.status == "pending" and booking.expires_at > now:
            Booking.objects.filter(pk=booking.pk, status="pending").update(
                status="confirmed", paid=True
            )
            attempt.state = "succeeded"
        else:
            if booking.status == "pending":
                _release(booking.pk, "expired", now)
            Booking.objects.filter(pk=booking.pk).update(paid=True, refund_required=True)
            attempt.state = "review"
        attempt.save()
