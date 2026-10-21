import importlib
from datetime import timedelta
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import SimpleTestCase, TransactionTestCase
from django.utils import timezone

from accounts.models import User
from workshops.models import Booking, Workshop


class ScheduledExpiryTests(SimpleTestCase):
    def test_runs_command_on_each_tick_and_closes_connections(self):
        from workshops.maintenance import run_expiry

        stop = Mock()
        stop.is_set.return_value = False
        stop.wait.side_effect = [False, True]
        with (
            patch("workshops.maintenance.call_command") as command,
            patch("workshops.maintenance.connections") as connections,
        ):
            run_expiry(stop)
        self.assertEqual(command.call_count, 2)
        self.assertTrue(all(c.args == ("expire_bookings",) for c in command.call_args_list))
        self.assertEqual(connections.close_all.call_count, 2)
        self.assertEqual(stop.wait.call_args_list[0].args, (60,))

    def test_failed_tick_is_logged_without_exception_details_and_retried(self):
        from workshops.maintenance import run_expiry

        stop = Mock()
        stop.is_set.return_value = False
        stop.wait.side_effect = [False, True]
        with (
            patch(
                "workshops.maintenance.call_command", side_effect=[RuntimeError("private"), None]
            ),
            patch("workshops.maintenance.connections") as connections,
            self.assertLogs("skillseat.maintenance", level="INFO") as logs,
        ):
            run_expiry(stop)
        self.assertIn("retry", " ".join(logs.output))
        self.assertNotIn("private", " ".join(logs.output))
        self.assertEqual(connections.close_all.call_count, 2)

    def test_stopped_worker_does_not_start_a_command(self):
        from workshops.maintenance import run_expiry

        stop = Mock()
        stop.is_set.return_value = True
        with patch("workshops.maintenance.call_command") as command:
            run_expiry(stop)
        command.assert_not_called()

    def test_gunicorn_starts_after_worker_init_and_stops_on_exit(self):
        hooks = importlib.import_module("config.gunicorn")
        worker = SimpleNamespace(log=Mock())
        with patch("workshops.maintenance.Thread") as thread_class:
            hooks.post_worker_init(worker)
            thread_class.return_value.start.assert_called_once()
            self.assertTrue(thread_class.call_args.kwargs["daemon"])
            hooks.worker_exit(None, worker)
            self.assertTrue(worker.hold_expiry_stop.is_set())
            thread_class.return_value.join.assert_called_once_with(timeout=5)
        hooks.worker_exit(None, SimpleNamespace())
        self.assertIn("--config config/gunicorn.py", Path("Procfile").read_text())


class ScheduledExpiryDatabaseTests(TransactionTestCase):
    def test_scheduled_command_releases_only_expired_pending_holds_once(self):
        from workshops.maintenance import run_expiry

        owner = User.objects.create_user(username="timer-owner")
        now = timezone.now()
        workshop = Workshop.objects.create(
            owner=owner,
            title="Fictional timer test",
            location="Test room",
            starts_at=now + timedelta(days=1),
            ends_at=now + timedelta(days=1, hours=1),
            capacity=3,
            reserved=3,
            price_pence=100,
        )
        bookings = []
        for name, status, paid, expiry in (
            ("expired", "pending", False, now - timedelta(seconds=1)),
            ("future", "pending", False, now + timedelta(minutes=20)),
            ("paid", "confirmed", True, now - timedelta(seconds=1)),
        ):
            bookings.append(
                Booking.objects.create(
                    workshop=workshop,
                    attendee=User.objects.create_user(username=name),
                    status=status,
                    paid=paid,
                    amount_pence=100,
                    expires_at=expiry,
                )
            )
        stop = Mock()
        stop.is_set.return_value = False
        stop.wait.side_effect = [False, True]
        run_expiry(stop)
        workshop.refresh_from_db()
        for booking in bookings:
            booking.refresh_from_db()
        self.assertEqual([b.status for b in bookings], ["expired", "pending", "confirmed"])
        self.assertEqual(workshop.reserved, 2)
        self.assertTrue(bookings[2].paid)
