from django.core.exceptions import ImproperlyConfigured
from django.test import SimpleTestCase

from config.release import load_release


class ReleaseConfigurationTests(SimpleTestCase):
    def test_local_default_keeps_sqlite_and_distrusts_proxy(self):
        policy = load_release({}, production=False)
        self.assertIsNone(policy.database)
        self.assertIsNone(policy.proxy_header)
        self.assertEqual(policy.storage_backend, "filesystem")

    def test_postgres_url_is_parsed_without_revealing_password(self):
        policy = load_release(
            {"DATABASE_URL": "postgresql://sample:private@localhost:5432/skillseat"},
            production=False,
        )
        self.assertEqual(policy.database["ENGINE"], "django.db.backends.postgresql")
        self.assertEqual(policy.database["NAME"], "skillseat")
        self.assertNotIn("private", repr(policy))

    def test_heroku_requires_production_database_and_explicit_https_origin(self):
        base = {"DJANGO_DEPLOYMENT": "heroku"}
        for changes in (
            {},
            {"DATABASE_URL": "sqlite:///tmp/test.db"},
            {"DATABASE_URL": "postgres://sample:private@host/db"},
        ):
            with self.subTest(changes=changes), self.assertRaises(ImproperlyConfigured):
                load_release(base | changes, production=True)

    def test_heroku_policy_uses_tls_proxy_and_persistent_private_storage(self):
        policy = load_release(
            {
                "DJANGO_DEPLOYMENT": "heroku",
                "DATABASE_URL": "postgres://sample:private@host/db?sslmode=disable",
                "DJANGO_CSRF_TRUSTED_ORIGINS": "https://skillseat-example.herokuapp.com",
            },
            production=True,
        )
        self.assertEqual(policy.database["OPTIONS"]["sslmode"], "require")
        self.assertEqual(policy.proxy_header, ("HTTP_X_FORWARDED_PROTO", "https"))
        self.assertEqual(policy.storage_backend, "database")

    def test_dyno_cannot_silently_use_local_policy(self):
        with self.assertRaises(ImproperlyConfigured):
            load_release({"DYNO": "web.1"}, production=True)

    def test_rejects_unsafe_origins_and_unknown_deployment(self):
        for origin in (
            "http://example.com",
            "https://*.example.com",
            "https://example.com/path",
            "https://user:pass@example.com",
        ):
            with self.subTest(origin=origin), self.assertRaises(ImproperlyConfigured):
                load_release({"DJANGO_CSRF_TRUSTED_ORIGINS": origin}, production=True)
        with self.assertRaises(ImproperlyConfigured):
            load_release({"DJANGO_DEPLOYMENT": "unknown"}, production=True)
