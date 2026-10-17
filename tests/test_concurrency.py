from concurrent.futures import ThreadPoolExecutor
from threading import Barrier

from django.core.exceptions import ValidationError
from django.db import close_old_connections, connections
from django.test import TransactionTestCase

from tests.test_workshops import user, workshop
from workshops.models import Booking, Workshop
from workshops.services import cancel_booking, reserve


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
