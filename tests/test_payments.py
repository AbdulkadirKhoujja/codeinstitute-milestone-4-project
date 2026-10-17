import hashlib
import hmac
import json
import time
from datetime import timedelta
from types import SimpleNamespace
from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings
from django.utils import timezone

from tests.test_workshops import user, workshop
from workshops.models import Booking, PaymentAttempt, PaymentEvent
from workshops.payments import initiate_checkout, process_event
from workshops.services import cancel_booking, expire_bookings, reserve


@override_settings(
    STRIPE_TEST_KEY="rk_test_simulated",
    STRIPE_WEBHOOK_SECRET="whsec_simulated",
    PAYMENT_ORIGIN="http://localhost:8000",
)
class PaymentTests(TestCase):
    def setUp(self):
        self.item = workshop(price_pence=2500, capacity=1)
        self.person = user("learner")
        self.booking = reserve(self.item.pk, self.person)

    def attempt(self):
        return PaymentAttempt.objects.create(booking=self.booking, session_id="cs_test_simulated")

    def event(self, event_id="evt_simulated", **changes):
        obj = dict(
            id="cs_test_simulated",
            livemode=False,
            mode="payment",
            payment_status="paid",
            amount_total=2500,
            currency="gbp",
            client_reference_id=str(self.booking.pk),
        )
        obj.update(changes)
        return {
            "id": event_id,
            "type": "checkout.session.completed",
            "livemode": False,
            "data": {"object": obj},
        }

    @patch("workshops.payments.stripe.StripeClient")
    def test_checkout_uses_snapshot_server_price_and_idempotency(self, client):
        client.return_value.v1.checkout.sessions.create.return_value = SimpleNamespace(
            id="cs_test_simulated",
            url="https://checkout.stripe.com/c/pay/simulated",
            livemode=False,
        )
        self.assertTrue(
            initiate_checkout(self.booking.pk, self.person).startswith(
                "https://checkout.stripe.com/"
            )
        )
        call = client.return_value.v1.checkout.sessions.create.call_args
        self.assertEqual(call.args[0]["line_items"][0]["price_data"]["unit_amount"], 2500)
        self.assertIn("idempotency_key", call.kwargs["options"])
        self.assertNotIn("payment_method_types", call.args[0])
        self.assertEqual(PaymentAttempt.objects.get().session_id, "cs_test_simulated")

    def test_other_account_and_live_key_rejected(self):
        with self.assertRaises(ValidationError):
            initiate_checkout(self.booking.pk, user("intruder"))
        with (
            override_settings(STRIPE_TEST_KEY="sk_live_FORBIDDEN"),
            self.assertRaises(ValidationError),
        ):
            initiate_checkout(self.booking.pk, self.person)

    def test_verified_payment_and_replay_confirm_exactly_once(self):
        self.attempt()
        process_event(self.event())
        process_event(self.event())
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "confirmed")
        self.assertTrue(self.booking.paid)
        self.assertEqual(PaymentEvent.objects.count(), 1)
        self.item.refresh_from_db()
        self.assertEqual(self.item.reserved, 1)

    def test_unpaid_event_does_not_confirm_async_success_can(self):
        self.attempt()
        process_event(self.event(payment_status="unpaid"))
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "pending")
        event = self.event(event_id="evt_async")
        event["type"] = "checkout.session.async_payment_succeeded"
        process_event(event)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "confirmed")

    def test_wrong_amount_currency_reference_or_live_mode_never_grants_access(self):
        self.attempt()
        for changes in (
            {"amount_total": 1},
            {"currency": "usd"},
            {"client_reference_id": "999"},
            {"livemode": True},
        ):
            with self.subTest(changes=changes):
                try:
                    process_event(self.event(event_id="evt_" + str(changes), **changes))
                except ValidationError:
                    pass
                self.booking.refresh_from_db()
                self.assertNotEqual(self.booking.status, "confirmed")

    def test_expired_hold_late_success_never_restores_seat(self):
        self.attempt()
        Booking.objects.filter(pk=self.booking.pk).update(
            expires_at=timezone.now() - timedelta(seconds=1)
        )
        expire_bookings()
        process_event(self.event())
        self.booking.refresh_from_db()
        self.item.refresh_from_db()
        self.assertEqual(self.booking.status, "expired")
        self.assertTrue(self.booking.refund_required)
        self.assertEqual(self.item.reserved, 0)

    def test_cancelled_late_payment_and_reordered_expiration(self):
        self.attempt()
        cancel_booking(self.booking.pk, self.person)
        process_event(self.event())
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "cancelled")
        self.assertTrue(self.booking.refund_required)

    def test_expiration_after_success_does_not_downgrade(self):
        self.attempt()
        process_event(self.event())
        event = self.event("evt_expired", payment_status="unpaid")
        event["type"] = "checkout.session.expired"
        process_event(event)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "confirmed")

    def test_webhook_rejects_bad_signature_and_accepts_real_sdk_signature(self):
        self.attempt()
        payload = json.dumps(self.event()).encode()
        endpoint = "/workshops/payments/webhook/"
        self.assertEqual(
            self.client.post(
                endpoint, payload, content_type="application/json", HTTP_STRIPE_SIGNATURE="bad"
            ).status_code,
            400,
        )
        stamp = str(int(time.time()))
        signature = hmac.new(
            b"whsec_simulated", stamp.encode() + b"." + payload, hashlib.sha256
        ).hexdigest()
        response = self.client.post(
            endpoint,
            payload,
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE=f"t={stamp},v1={signature}",
        )
        self.assertEqual(response.status_code, 200)
        self.booking.refresh_from_db()
        self.assertTrue(self.booking.paid)

    def test_success_url_cannot_confirm_payment(self):
        self.client.force_login(self.person)
        self.client.get("/workshops/bookings/?success=true&paid=true")
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "pending")

    @patch("workshops.payments.stripe.StripeClient")
    def test_repeated_checkout_reuses_session_and_server_price_snapshot(self, client):
        client.return_value.v1.checkout.sessions.create.return_value = SimpleNamespace(
            id="cs_test_repeat", url="https://checkout.stripe.com/c/pay/repeat", livemode=False
        )
        from workshops.models import Workshop

        Workshop.objects.filter(pk=self.item.pk).update(price_pence=9000)
        first = initiate_checkout(self.booking.pk, self.person)
        self.assertEqual(initiate_checkout(self.booking.pk, self.person), first)
        self.assertEqual(client.return_value.v1.checkout.sessions.create.call_count, 1)
        self.assertEqual(
            client.return_value.v1.checkout.sessions.create.call_args.args[0]["line_items"][0][
                "price_data"
            ]["unit_amount"],
            2500,
        )

    def test_signed_but_stale_webhook_rejected(self):
        payload = json.dumps(self.event()).encode()
        signature = hmac.new(b"whsec_simulated", b"1." + payload, hashlib.sha256).hexdigest()
        response = self.client.post(
            "/workshops/payments/webhook/",
            payload,
            content_type="application/json",
            HTTP_STRIPE_SIGNATURE=f"t=1,v1={signature}",
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(PaymentEvent.objects.exists())
