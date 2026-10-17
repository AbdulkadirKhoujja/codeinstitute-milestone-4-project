from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from workshops.models import Workshop


def user(name="host"):
    return get_user_model().objects.create_user(username=name)


def workshop(owner=None, **kwargs):
    values = dict(
        owner=owner or user(),
        title="Practical pottery",
        description="Learn by doing",
        location="London studio",
        starts_at=timezone.now() + timedelta(days=2),
        ends_at=timezone.now() + timedelta(days=2, hours=2),
        capacity=2,
        published=True,
    )
    values.update(kwargs)
    return Workshop.objects.create(**values)


class WorkshopModelTests(TestCase):
    def test_paid_prices_have_a_practical_minimum_and_provider_safe_maximum(self):
        item = workshop()
        for value in (1, 49, 100000000):
            item.price_pence = value
            with self.subTest(price=value), self.assertRaises(ValidationError):
                item.full_clean()
        for value in (0, 50, 99999999):
            item.price_pence = value
            item.full_clean()

    def test_price_and_availability(self):
        item = workshop(price_pence=2500)
        self.assertEqual(item.price_display, "£25.00")
        self.assertEqual(item.available_seats, 2)

    def test_dates_must_be_ordered(self):
        item = workshop()
        item.ends_at = item.starts_at
        with self.assertRaises(ValidationError):
            item.full_clean()

    def test_database_rejects_over_capacity_and_zero_capacity(self):
        item = workshop()
        for values in ({"reserved": 3}, {"capacity": 0}):
            with (
                self.subTest(values=values),
                self.assertRaises(IntegrityError),
                transaction.atomic(),
            ):
                Workshop.objects.filter(pk=item.pk).update(**values)


class DiscoveryTests(TestCase):
    def test_discovery_lists_upcoming_workshops_without_advertising_past_seats(self):
        item = workshop(
            title="Past fictional workshop",
            starts_at=timezone.now() - timedelta(hours=3),
            ends_at=timezone.now() - timedelta(hours=1),
        )
        self.assertNotContains(self.client.get("/workshops/"), item.title)
        response = self.client.get(f"/workshops/{item.pk}/")
        self.assertContains(response, item.title)
        self.assertNotContains(response, "places available")

    def test_public_discovery_hides_drafts(self):
        item = workshop()
        draft = workshop(owner=item.owner, title="Private draft", published=False)
        response = self.client.get("/workshops/")
        self.assertContains(response, item.title)
        self.assertNotContains(response, draft.title)
        self.assertEqual(self.client.get(f"/workshops/{draft.pk}/").status_code, 404)

    def test_detail_and_invalid_identifiers(self):
        item = workshop(price_pence=1250)
        response = self.client.get(f"/workshops/{item.pk}/")
        for text in (
            item.title,
            item.description,
            item.location,
            "£12.50",
            "2",
            item.owner.username,
        ):
            self.assertContains(response, text)
        for path in ("/workshops/9999/", "/workshops/invalid/"):
            self.assertEqual(self.client.get(path).status_code, 404)
