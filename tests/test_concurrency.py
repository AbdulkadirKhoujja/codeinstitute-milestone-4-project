from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from threading import Barrier

from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.db import close_old_connections, connections
from django.test import TransactionTestCase
from django.utils import timezone

from tests.test_workshops import user, workshop
from workshops.models import Booking, PaymentAttempt
from workshops.payments import process_event
from workshops.services import cancel_booking, expire_bookings, reserve, update_workshop


class CapacityConcurrencyTests(TransactionTestCase):
    def race(self, operations):
        barrier = Barrier(len(operations))

        def run(operation):
            close_old_connections()
            try:
                barrier.wait(timeout=10)
                operation()
                return "ok"
            except ValidationError:
                return "rejected"
            finally:
                connections.close_all()

        with ThreadPoolExecutor(max_workers=len(operations)) as pool:
            return list(pool.map(run, operations))

    def test_final_seat_two_connections_never_oversell(self):
        item = workshop(capacity=1)
        people = [user("first"), user("second")]
        results = self.race([lambda person=person: reserve(item.pk, person) for person in people])
        self.assertCountEqual(results, ["ok", "rejected"])
        item.refresh_from_db()
        self.assertEqual(item.reserved, 1)
        self.assertEqual(Booking.objects.filter(status="confirmed").count(), 1)

    def test_duplicate_simultaneous_requests_one_booking(self):
        item = workshop(capacity=2)
        person = user("learner")
        results = self.race([lambda: reserve(item.pk, person)] * 2)
        self.assertCountEqual(results, ["ok", "rejected"])
        item.refresh_from_db()
        self.assertEqual(item.reserved, 1)

    def test_cancel_race_releases_exactly_once(self):
        item = workshop(capacity=1)
        person = user("learner")
        booking = reserve(item.pk, person)
        self.assertEqual(self.race([lambda: cancel_booking(booking.pk, person)] * 2), ["ok", "ok"])
        item.refresh_from_db()
        self.assertEqual(item.reserved, 0)

    def test_capacity_reduction_races_booking_safely(self):
        item = workshop(capacity=2)
        item.owner.user_permissions.add(Permission.objects.get(codename="add_workshop"))
        reserve(item.pk, user("first"))
        second = user("second")
        result = self.race(
            [
                lambda: update_workshop(item.pk, item.owner, {"capacity": 1}),
                lambda: reserve(item.pk, second),
            ]
        )
        self.assertCountEqual(result, ["ok", "rejected"])
        item.refresh_from_db()
        self.assertLessEqual(item.reserved, item.capacity)
        self.assertEqual(item.reserved, Booking.objects.filter(status="confirmed").count())

    def test_expiry_race_releases_once(self):
        item = workshop(capacity=1, price_pence=1000)
        booking = reserve(item.pk, user("learner"))
        Booking.objects.filter(pk=booking.pk).update(
            expires_at=timezone.now() - timedelta(seconds=1)
        )
        self.assertEqual(self.race([expire_bookings] * 2), ["ok", "ok"])
        item.refresh_from_db()
        self.assertEqual(item.reserved, 0)

    def test_payment_and_cancellation_race_requires_refund_without_seat(self):
        item = workshop(capacity=1, price_pence=1000)
        person = user("learner")
        booking = reserve(item.pk, person)
        PaymentAttempt.objects.create(booking=booking, session_id="cs_test_race")
        event = {
            "id": "evt_race",
            "livemode": False,
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test_race",
                    "livemode": False,
                    "mode": "payment",
                    "payment_status": "paid",
                    "amount_total": 1000,
                    "currency": "gbp",
                    "client_reference_id": str(booking.pk),
                }
            },
        }
        self.assertEqual(
            self.race([lambda: process_event(event), lambda: cancel_booking(booking.pk, person)]),
            ["ok", "ok"],
        )
        booking.refresh_from_db()
        item.refresh_from_db()
        self.assertEqual(booking.status, "cancelled")
        self.assertTrue(booking.refund_required)
        self.assertEqual(item.reserved, 0)

    def test_duplicate_payment_events_race_confirm_once(self):
        item = workshop(capacity=1, price_pence=1000)
        person = user("learner")
        booking = reserve(item.pk, person)
        PaymentAttempt.objects.create(booking=booking, session_id="cs_test_race")
        event = {
            "id": "evt_race",
            "livemode": False,
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test_race",
                    "livemode": False,
                    "mode": "payment",
                    "payment_status": "paid",
                    "amount_total": 1000,
                    "currency": "gbp",
                    "client_reference_id": str(booking.pk),
                }
            },
        }
        self.assertEqual(self.race([lambda: process_event(event)] * 2), ["ok", "ok"])
        booking.refresh_from_db()
        self.assertEqual(booking.status, "confirmed")
        item.refresh_from_db()
        self.assertEqual(item.reserved, 1)
