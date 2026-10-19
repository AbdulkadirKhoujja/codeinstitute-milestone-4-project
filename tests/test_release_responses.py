from unittest.mock import patch

from django.db import DatabaseError
from django.test import TestCase, override_settings


class ReleaseResponseTests(TestCase):
    def test_health_is_read_only_and_checks_database(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"status": "ok"})
        self.assertIn("no-store", response["Cache-Control"])
        self.assertEqual(self.client.post("/health/").status_code, 405)

    @patch("core.views.connection.cursor", side_effect=DatabaseError("private connection detail"))
    def test_health_failure_is_generic(self, cursor):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json(), {"status": "unavailable"})
        self.assertNotContains(response, "private connection detail", status_code=503)

    @override_settings(DEBUG=False)
    def test_missing_page_retains_useful_navigation(self):
        response = self.client.get("/missing-release-check/")
        self.assertContains(response, "Find your next workshop", status_code=404)
