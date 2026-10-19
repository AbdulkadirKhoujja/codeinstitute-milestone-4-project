"""Django foundation behaviour, separate from future workshop features."""

import importlib

from django.apps import apps
from django.conf import settings
from django.db import connection
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import resolve, reverse


class ProjectWiringTests(SimpleTestCase):
    def test_settings_load_the_root_configuration(self):
        self.assertEqual(settings.ROOT_URLCONF, "config.urls")
        self.assertEqual(settings.WSGI_APPLICATION, "config.wsgi.application")
        self.assertEqual(settings.ASGI_APPLICATION, "config.asgi.application")

    def test_core_app_is_registered(self):
        self.assertEqual(apps.get_app_config("core").name, "core")

    def test_root_resolves_to_named_core_home(self):
        self.assertEqual(reverse("core:home"), "/")
        self.assertEqual(resolve("/").view_name, "core:home")

    def test_home_is_public_and_leads_to_workshop_discovery(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")
        self.assertContains(response, "SkillSeat")
        self.assertContains(response, 'href="/workshops/"')

    @override_settings(DEBUG=False, ALLOWED_HOSTS=["skillseat.example.com"])
    def test_unapproved_host_is_rejected(self):
        self.assertEqual(self.client.get("/", HTTP_HOST="attacker.example").status_code, 400)

    def test_missing_route_returns_404(self):
        self.assertEqual(self.client.get("/not-a-route/").status_code, 404)

    def test_wsgi_and_asgi_applications_load(self):
        for module in ("config.wsgi", "config.asgi"):
            with self.subTest(module=module):
                self.assertTrue(callable(importlib.import_module(module).application))


class DatabaseFoundationTests(TestCase):
    def test_database_connects_and_django_migrations_exist(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            self.assertEqual(cursor.fetchone(), (1,))
        self.assertIn("django_migrations", connection.introspection.table_names())

    def test_local_database_uses_sqlite(self):
        expected = (
            "postgresql"
            if settings.DATABASES["default"]["ENGINE"].endswith("postgresql")
            else "sqlite"
        )
        self.assertEqual(connection.vendor, expected)
