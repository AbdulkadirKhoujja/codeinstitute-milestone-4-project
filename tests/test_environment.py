"""Configuration contracts runnable before Django starts."""

import unittest

from django.core.exceptions import ImproperlyConfigured

from config.environment import load_environment

SECRET = "unit-test-only-key-" + "aB7!" * 16


class EnvironmentTests(unittest.TestCase):
    def development(self, **overrides):
        return load_environment(
            {"DJANGO_ENV": "development", "DJANGO_SECRET_KEY": SECRET, **overrides}
        )

    def production(self, **overrides):
        return load_environment(
            {
                "DJANGO_SECRET_KEY": SECRET,
                "DJANGO_ALLOWED_HOSTS": "skillseat.example.com",
                **overrides,
            }
        )

    def test_default_environment_is_production_with_debug_off(self):
        config = self.production()
        self.assertEqual(config.name, "production")
        self.assertFalse(config.debug)

    def test_explicit_development_supports_loopback_hosts(self):
        config = self.development()
        self.assertTrue(config.debug)
        self.assertEqual(config.allowed_hosts, ["localhost", "127.0.0.1", "[::1]"])

    def test_development_can_disable_debug(self):
        self.assertFalse(self.development(DJANGO_DEBUG="false").debug)

    def test_secret_is_required_in_both_environments(self):
        for name in ("development", "production"):
            with self.subTest(name=name), self.assertRaises(ImproperlyConfigured):
                load_environment({"DJANGO_ENV": name})

    def test_weak_or_placeholder_secrets_are_rejected(self):
        for secret in ("", "short", "a" * 60, "django-insecure-" + SECRET, "replace-me-" + SECRET):
            with self.subTest(secret=secret), self.assertRaises(ImproperlyConfigured):
                self.development(DJANGO_SECRET_KEY=secret)

    def test_unknown_environment_is_rejected(self):
        with self.assertRaises(ImproperlyConfigured):
            self.development(DJANGO_ENV="prodution")

    def test_invalid_debug_values_are_rejected(self):
        for value in ("yes", "", "Falsee"):
            with self.subTest(value=value), self.assertRaises(ImproperlyConfigured):
                self.development(DJANGO_DEBUG=value)

    def test_production_debug_is_rejected(self):
        with self.assertRaises(ImproperlyConfigured):
            self.production(DJANGO_DEBUG="true")

    def test_production_requires_explicit_hosts(self):
        for value in ("", " , "):
            with self.subTest(value=value), self.assertRaises(ImproperlyConfigured):
                self.production(DJANGO_ALLOWED_HOSTS=value)

    def test_invalid_or_wildcard_hosts_are_rejected(self):
        for host in (
            "*",
            ".example.com",
            "https://example.com",
            "example.com:443",
            "bad host",
            "-bad.com",
        ):
            with self.subTest(host=host), self.assertRaises(ImproperlyConfigured):
                self.production(DJANGO_ALLOWED_HOSTS=host)

    def test_host_list_is_trimmed(self):
        config = self.production(DJANGO_ALLOWED_HOSTS=" skillseat.example.com, www.example.com ")
        self.assertEqual(config.allowed_hosts, ["skillseat.example.com", "www.example.com"])

    def test_configuration_does_not_expose_secret_in_repr(self):
        self.assertNotIn(SECRET, repr(self.development()))
