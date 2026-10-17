from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.test import Client, TestCase
from django.utils import timezone

from tests.test_workshops import user, workshop
from workshops.forms import WorkshopForm
from workshops.models import Booking, PaymentAttempt, Review, Workshop
from workshops.payments import initiate_checkout, process_event
from workshops.services import reserve


class SecurityRegressionTests(TestCase):
    def setUp(self):
        self.item = workshop()
        self.person = user("learner")

    def test_booking_and_management_posts_require_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.person)
        self.assertEqual(client.post(f"/workshops/{self.item.pk}/book/").status_code, 403)
        self.item.owner.user_permissions.add(Permission.objects.get(codename="add_workshop"))
        client.force_login(self.item.owner)
        self.assertEqual(client.post(f"/workshops/studio/{self.item.pk}/", {}).status_code, 403)

    def test_state_changing_routes_are_post_only(self):
        booking = reserve(self.item.pk, self.person)
        self.client.force_login(self.person)
        for path in (
            f"/workshops/bookings/{booking.pk}/cancel/",
            f"/workshops/bookings/{booking.pk}/checkout/",
            "/workshops/payments/webhook/",
            "/workshops/reviews/999/delete/",
            "/workshops/resources/999/delete/",
        ):
            self.assertEqual(self.client.get(path).status_code, 405)

    def test_xss_is_escaped_in_public_content(self):
        Workshop.objects.filter(pk=self.item.pk).update(title='<script>alert("x")</script>')
        response = self.client.get(f"/workshops/{self.item.pk}/")
        self.assertNotContains(response, '<script>alert("x")</script>')
        self.assertContains(response, "&lt;script&gt;")

    def test_reviews_cannot_modify_or_delete_other_attendees(self):
        other = user("other")
        record = Review.objects.create(
            workshop=self.item, attendee=other, rating=5, body="Another attendee review"
        )
        self.client.force_login(self.person)
        self.assertEqual(
            self.client.post(f"/workshops/reviews/{record.pk}/delete/").status_code, 404
        )
        self.assertEqual(
            self.client.post(
                f"/workshops/{self.item.pk}/review/",
                {"id": record.pk, "rating": 1, "body": "Forged modification"},
            ).status_code,
            403,
        )
        record.refresh_from_db()
        self.assertEqual(record.rating, 5)

    def test_hidden_review_stays_hidden_after_own_edit_and_delete_works(self):
        booking = reserve(self.item.pk, self.person)
        Booking.objects.filter(pk=booking.pk).update(attended=True)
        Workshop.objects.filter(pk=self.item.pk).update(
            starts_at=timezone.now() - timedelta(hours=3),
            ends_at=timezone.now() - timedelta(hours=1),
        )
        record = Review.objects.create(
            workshop=self.item,
            attendee=self.person,
            rating=5,
            body="Moderated review",
            visible=False,
        )
        self.client.force_login(self.person)
        self.assertEqual(
            self.client.post(
                f"/workshops/{self.item.pk}/review/", {"rating": 4, "body": "Updated own review"}
            ).status_code,
            302,
        )
        self.assertNotContains(self.client.get(f"/workshops/{self.item.pk}/"), "Updated own review")
        self.assertEqual(
            self.client.post(f"/workshops/reviews/{record.pk}/delete/").status_code, 302
        )
        self.assertFalse(Review.objects.exists())

    def test_workshop_invalid_values_rejected_by_form(self):
        data = dict(
            title="Test",
            description="Description",
            location="Studio",
            starts_at=self.item.starts_at.isoformat(),
            ends_at=self.item.ends_at.isoformat(),
            capacity=1,
            price_pence=0,
        )
        for changes in (
            {"capacity": -1},
            {"capacity": 0},
            {"price_pence": -1},
            {"ends_at": self.item.starts_at.isoformat()},
        ):
            with self.subTest(changes=changes):
                self.assertFalse(WorkshopForm(data | changes).is_valid())

    def test_csp_and_private_pages_prevent_shared_caching(self):
        self.client.force_login(self.person)
        response = self.client.get("/workshops/bookings/")
        self.assertIn("no-store", response.get("Cache-Control", ""))
        self.assertIn("default-src 'self'", response.get("Content-Security-Policy", ""))


class PaymentFailureTests(TestCase):
    def setUp(self):
        self.item = workshop(price_pence=1000)
        self.person = user("learner")
        self.booking = reserve(self.item.pk, self.person)

    @patch("workshops.payments.stripe.StripeClient")
    def test_network_failure_leaves_hold_and_no_attempt_committed(self, client):
        import stripe
        from django.test import override_settings

        client.return_value.v1.checkout.sessions.create.side_effect = stripe.APIConnectionError(
            "simulated"
        )
        with (
            override_settings(
                STRIPE_TEST_KEY="rk_test_simulated", PAYMENT_ORIGIN="http://localhost:8000"
            ),
            self.assertRaises(ValidationError),
        ):
            initiate_checkout(self.booking.pk, self.person)
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.status, "pending")
        self.assertFalse(PaymentAttempt.objects.exists())

    def test_async_failure_releases_once_and_unknown_session_rolls_back_receipt(self):
        from workshops.models import PaymentEvent

        PaymentAttempt.objects.create(booking=self.booking, session_id="cs_test_failure")
        event = {
            "id": "evt_failure",
            "livemode": False,
            "type": "checkout.session.async_payment_failed",
            "data": {"object": {"id": "cs_test_failure", "livemode": False, "mode": "payment"}},
        }
        process_event(event)
        process_event(event)
        self.item.refresh_from_db()
        self.assertEqual(self.item.reserved, 0)
        event["id"] = "evt_unknown"
        event["data"]["object"]["id"] = "cs_test_unknown"
        with self.assertRaises(ValidationError):
            process_event(event)
        self.assertFalse(PaymentEvent.objects.filter(event_id="evt_unknown").exists())
