"""Verify startup policy and security responses in both configuration modes."""

import json
import os
import subprocess
import sys

from django.conf import settings
from django.test import SimpleTestCase, override_settings

from tests.test_environment import SECRET


class StartupPolicyTests(SimpleTestCase):
    def run_settings(self, **values):
        environment = {key: value for key, value in os.environ.items() if not key.startswith("DJANGO_")}
        environment.update(values)
        return subprocess.run(
            [sys.executable, "-c", "import json; from config import settings as s; print(json.dumps({key: getattr(s, key) for key in ('DEBUG', 'SESSION_COOKIE_SECURE', 'CSRF_COOKIE_SECURE', 'SECURE_SSL_REDIRECT', 'SECURE_HSTS_SECONDS', 'SECURE_HSTS_INCLUDE_SUBDOMAINS', 'SECURE_HSTS_PRELOAD')}))"],
            env=environment,
            text=True,
            capture_output=True,
            timeout=30,
            check=False,
        )

    def test_production_settings_enable_transport_and_cookie_security(self):
        result = self.run_settings(DJANGO_SECRET_KEY=SECRET, DJANGO_ALLOWED_HOSTS="skillseat.example.com")
        self.assertEqual(result.returncode, 0, result.stderr)
        policy = json.loads(result.stdout)
        self.assertFalse(policy.pop("DEBUG"))
        self.assertGreaterEqual(policy.pop("SECURE_HSTS_SECONDS"), 31536000)
        self.assertTrue(all(policy.values()))

    def test_development_settings_support_local_http_without_hsts(self):
        result = self.run_settings(DJANGO_ENV="development", DJANGO_SECRET_KEY=SECRET)
        self.assertEqual(result.returncode, 0, result.stderr)
        policy = json.loads(result.stdout)
        self.assertTrue(policy.pop("DEBUG"))
        self.assertFalse(any(policy.values()))

    def test_unconfigured_startup_fails_without_exposing_a_key(self):
        result = self.run_settings()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("DJANGO_SECRET_KEY", result.stderr)

    def test_invalid_configuration_prevents_settings_loading(self):
        for overrides in (
            {"DJANGO_ENV": "unknown"},
            {"DJANGO_DEBUG": "true"},
            {"DJANGO_ALLOWED_HOSTS": "*"},
        ):
            with self.subTest(overrides=overrides):
                values = {"DJANGO_SECRET_KEY": SECRET, "DJANGO_ALLOWED_HOSTS": "skillseat.example.com", **overrides}
                result = self.run_settings(**values)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn(SECRET, result.stderr)


class SecurityResponseTests(SimpleTestCase):
    def test_security_middleware_sets_frame_and_content_type_protection(self):
        response = self.client.get("/")
        self.assertEqual(response.headers["X-Frame-Options"], "DENY")
        self.assertEqual(response.headers["X-Content-Type-Options"], "nosniff")

    @override_settings(SECURE_SSL_REDIRECT=True)
    def test_production_http_requests_redirect_to_https(self):
        response = self.client.get("/accounts/login/?next=/accounts/")
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, "https://testserver/accounts/login/?next=/accounts/")

    @override_settings(SECURE_HSTS_SECONDS=31536000, SECURE_HSTS_INCLUDE_SUBDOMAINS=True, SECURE_HSTS_PRELOAD=True)
    def test_https_response_has_hsts(self):
        response = self.client.get("/", secure=True)
        self.assertEqual(response.headers["Strict-Transport-Security"], "max-age=31536000; includeSubDomains; preload")

    def test_sessions_are_http_only_and_same_site(self):
        self.assertTrue(settings.SESSION_COOKIE_HTTPONLY)
        self.assertEqual(settings.SESSION_COOKIE_SAMESITE, "Lax")
        self.assertEqual(settings.CSRF_COOKIE_SAMESITE, "Lax")

    def test_proxy_headers_are_not_trusted_without_deployment_configuration(self):
        self.assertIsNone(settings.SECURE_PROXY_SSL_HEADER)
        self.assertFalse(settings.USE_X_FORWARDED_HOST)
