from unittest.mock import patch

from django.db import OperationalError
from django.test import SimpleTestCase

from workshops.services import retry_contention


class TransactionRetryTests(SimpleTestCase):
    @patch("workshops.services.time.sleep")
    def test_serialization_failure_retries_whole_operation(self, sleep):
        class DatabaseFailure(Exception):
            sqlstate = "40001"

        failure = OperationalError("serialization conflict")
        failure.__cause__ = DatabaseFailure()
        calls = []

        @retry_contention
        def operation():
            calls.append(1)
            if len(calls) == 1:
                raise failure
            return "committed"

        self.assertEqual(operation(), "committed")
        self.assertEqual(len(calls), 2)

    def test_unrelated_database_errors_are_not_swallowed(self):
        @retry_contention
        def operation():
            raise OperationalError("unavailable database")

        with self.assertRaises(OperationalError):
            operation()
