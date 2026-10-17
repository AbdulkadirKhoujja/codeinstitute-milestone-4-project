from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from tests.test_workshops import user, workshop
from workshops.models import Booking, Workshop
from workshops.services import cancel_booking, expire_bookings, reserve


class BookingTests(TestCase):
    def setUp(self):
        self.item = workshop(capacity=1)
        self.attendee = user("learner")

    def test_existing_booking_detail_links_to_management(self):
        reserve(self.item.pk, self.attendee)
        self.client.force_login(self.attendee)
        response = self.client.get(f"/workshops/{self.item.pk}/")
        self.assertContains(response, "Manage your booking")
        self.assertNotContains(response, "Reserve a place")

    def test_free_confirmed_and_duplicate_rejected(self):
        booking = reserve(self.item.pk, self.attendee)
        self.assertEqual(booking.status, "confirmed")
        with self.assertRaises(ValidationError):
            reserve(self.item.pk, self.attendee)
        self.assertEqual(Booking.objects.count(), 1)
        self.assertEqual(Workshop.objects.get(pk=self.item.pk).reserved, 1)

    def test_full_and_unpublished_and_started_rejected(self):
        reserve(self.item.pk, self.attendee)
        with self.assertRaises(ValidationError):
            reserve(self.item.pk, user("second"))
        for values in ({"published": False}, {"starts_at": timezone.now() - timedelta(hours=1)}):
            Workshop.objects.filter(pk=self.item.pk).update(**values)
            with self.assertRaises(ValidationError):
                reserve(self.item.pk, self.attendee)

    def test_paid_hold_expires_and_releases_seat(self):
        Workshop.objects.filter(pk=self.item.pk).update(price_pence=1000)
        booking = reserve(self.item.pk, self.attendee)
        self.assertEqual(booking.status, "pending")
        self.assertEqual(booking.amount_pence, 1000)
        Booking.objects.filter(pk=booking.pk).update(
            expires_at=timezone.now() - timedelta(seconds=1)
        )
        self.assertEqual(expire_bookings(), 1)
        self.assertEqual(expire_bookings(), 0)
        booking.refresh_from_db()
        self.item.refresh_from_db()
        self.assertEqual(booking.status, "expired")
        self.assertEqual(self.item.reserved, 0)
        self.assertEqual(reserve(self.item.pk, self.attendee).status, "pending")

    def test_cancel_is_owned_idempotent_and_releases_capacity(self):
        booking = reserve(self.item.pk, self.attendee)
        with self.assertRaises(ValidationError):
            cancel_booking(booking.pk, user("intruder"))
        cancel_booking(booking.pk, self.attendee)
        cancel_booking(booking.pk, self.attendee)
        self.item.refresh_from_db()
        self.assertEqual(self.item.reserved, 0)

    def test_cannot_cancel_started_workshop(self):
        booking = reserve(self.item.pk, self.attendee)
        Workshop.objects.filter(pk=self.item.pk).update(
            starts_at=timezone.now() - timedelta(minutes=1)
        )
        with self.assertRaises(ValidationError):
            cancel_booking(booking.pk, self.attendee)

    def test_booking_endpoints_require_login_post_and_ownership(self):
        path = f"/workshops/{self.item.pk}/book/"
        self.assertEqual(self.client.post(path).status_code, 302)
        self.client.force_login(self.attendee)
        self.assertEqual(self.client.get(path).status_code, 405)
        self.assertEqual(self.client.post(path).status_code, 302)
        booking = Booking.objects.get()
        self.assertContains(self.client.get("/workshops/bookings/"), self.item.title)
        self.client.force_login(user("intruder"))
        self.assertNotContains(self.client.get("/workshops/bookings/"), self.item.title)
        self.assertEqual(
            self.client.post(f"/workshops/bookings/{booking.pk}/cancel/").status_code, 404
        )
