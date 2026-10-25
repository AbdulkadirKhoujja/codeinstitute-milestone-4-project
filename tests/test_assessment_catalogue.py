from datetime import timedelta
from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone

from tests.test_workshops import workshop
from workshops.models import (
    Booking,
    PaymentAttempt,
    PaymentEvent,
    PrivateResourceBlob,
    Resource,
    Workshop,
)


@override_settings(
    PRODUCTION=True,
    STRIPE_TEST_KEY="sk_test_fictional_regression",
    STRIPE_WEBHOOK_SECRET="whsec_fictional_regression",
    PRIVATE_RESOURCE_BACKEND="database",
)
class AssessmentCatalogueTests(TestCase):
    def seed(self, **options):
        call_command(
            "seed_assessment", confirm="skillseat-assessment-demo", stdout=StringIO(), **options
        )

    def test_original_development_seed_still_refuses_production(self):
        with self.assertRaises(CommandError):
            call_command("seed_demo", stdout=StringIO())

    def test_explicit_confirmation_and_sandbox_durable_storage_are_required(self):
        with self.assertRaises(CommandError):
            call_command("seed_assessment", stdout=StringIO())
        for values in (
            {"STRIPE_TEST_KEY": "sk_live_invalid"},
            {"STRIPE_TEST_KEY": ""},
            {"STRIPE_WEBHOOK_SECRET": ""},
            {"PRIVATE_RESOURCE_BACKEND": "filesystem"},
        ):
            with (
                self.subTest(values=values),
                override_settings(**values),
                self.assertRaises(CommandError),
            ):
                self.seed()
        self.assertFalse(Workshop.objects.exists())
        self.assertFalse(get_user_model().objects.exists())

    def test_four_persistent_fictional_listings_search_filters_and_protected_resource(self):
        self.seed()
        initial = list(Workshop.objects.values())
        self.seed()
        self.assertEqual(list(Workshop.objects.values()), initial)
        self.assertEqual(Workshop.objects.count(), 4)
        self.assertEqual(Workshop.objects.filter(price_pence=0).count(), 2)
        self.assertEqual(Workshop.objects.filter(price_pence__gt=0).count(), 2)
        for item in Workshop.objects.select_related("owner"):
            self.assertTrue(item.published)
            self.assertGreater(item.starts_at, timezone.now() + timedelta(days=365))
            self.assertGreaterEqual(item.available_seats, 20)
            self.assertIn("DEMO", item.title)
            self.assertIn("not a real scheduled event", item.description)
            self.assertFalse(item.owner.has_usable_password())
            self.assertFalse(item.owner.is_staff)
            self.assertFalse(item.owner.user_permissions.exists())
            self.assertContains(
                self.client.get(reverse("workshops:detail", args=[item.pk])),
                "not a real scheduled event",
            )
        listing = self.client.get(reverse("workshops:list"))
        self.assertEqual(len(listing.context["workshops"]), 4)
        for price, count in [("free", 2), ("paid", 2)]:
            self.assertEqual(
                len(
                    self.client.get(reverse("workshops:list"), {"price": price}).context[
                        "workshops"
                    ]
                ),
                count,
            )
        for term in ["Python", "photography", "clay", "drawing"]:
            self.assertEqual(
                len(self.client.get(reverse("workshops:list"), {"q": term}).context["workshops"]), 1
            )
        self.assertEqual(Resource.objects.count(), 1)
        resource = Resource.objects.get()
        self.assertGreater(resource.workshop.price_pence, 0)
        self.assertEqual(PrivateResourceBlob.objects.count(), 1)
        with resource.file.open() as content:
            self.assertIn(b"fictional", content.read())
        self.assertEqual(
            self.client.get(reverse("workshops:download", args=[resource.pk])).status_code, 302
        )
        learner = get_user_model().objects.create_user(username="unpaid-reviewer")
        self.client.force_login(learner)
        self.assertEqual(
            self.client.get(reverse("workshops:download", args=[resource.pk])).status_code, 403
        )

    def test_existing_users_bookings_and_payment_audit_are_untouched(self):
        existing = workshop(price_pence=100)
        learner = get_user_model().objects.create_user(username="existing-learner")
        booking = Booking.objects.create(
            workshop=existing, attendee=learner, status="confirmed", amount_pence=100, paid=True
        )
        PaymentAttempt.objects.create(
            booking=booking, session_id="cs_test_existing", state="succeeded"
        )
        PaymentEvent.objects.create(
            event_id="evt_existing", event_type="checkout.session.completed"
        )
        models = [get_user_model(), Workshop, Booking, PaymentAttempt, PaymentEvent]
        before = {model: list(model.objects.values()) for model in models}
        self.seed()
        for model, records in before.items():
            for record in records:
                self.assertEqual(model.objects.values().get(pk=record["id"]), record)

    def test_owner_name_collision_aborts_without_modifying_any_account(self):
        owner = get_user_model().objects.create_user(
            username="skillseat-assessment-demo", password="fictional-existing-password"
        )
        with self.assertRaises(CommandError):
            self.seed()
        owner.refresh_from_db()
        self.assertTrue(owner.has_usable_password())
        self.assertFalse(Workshop.objects.exists())
