"""Authentication and permission foundations, not registration or booking."""

from django.contrib.auth import authenticate, get_user_model
from django.db import connection
from django.test import Client, TestCase
from django.urls import reverse


class UserModelTests(TestCase):
    def test_custom_user_is_configured_before_initial_migration(self):
        self.assertEqual(get_user_model()._meta.label, "accounts.User")
        tables = connection.introspection.table_names()
        self.assertIn("accounts_user", tables)
        self.assertNotIn("auth_user", tables)

    def test_new_user_has_hashed_password_and_no_privileged_role(self):
        user = get_user_model().objects.create_user(username="attendee", password="test-password-73!")
        self.assertTrue(user.check_password("test-password-73!"))
        self.assertNotEqual(user.password, "test-password-73!")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.has_perm("accounts.change_user"))

    def test_superuser_manager_preserves_django_admin_contract(self):
        user = get_user_model().objects.create_superuser(username="administrator", password="test-password-73!")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)


class AuthenticationBoundaryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="attendee", password="test-password-73!")

    def test_anonymous_profile_access_redirects_to_login(self):
        self.assertRedirects(
            self.client.get(reverse("accounts:profile")),
            reverse("accounts:login") + "?next=" + reverse("accounts:profile"),
        )

    def test_login_page_has_csrf_token(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_valid_login_grants_access_to_own_account_page(self):
        response = self.client.post(reverse("accounts:login"), {"username": "attendee", "password": "test-password-73!"})
        self.assertRedirects(response, reverse("accounts:profile"))
        self.assertContains(self.client.get(reverse("accounts:profile")), "attendee")

    def test_bad_password_does_not_authenticate(self):
        self.client.post(reverse("accounts:login"), {"username": "attendee", "password": "incorrect"})
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_inactive_user_cannot_authenticate(self):
        self.user.is_active = False
        self.user.save()
        self.assertIsNone(authenticate(username="attendee", password="test-password-73!"))

    def test_login_cannot_redirect_to_an_external_site(self):
        response = self.client.post(reverse("accounts:login") + "?next=https://attacker.example/", {"username": "attendee", "password": "test-password-73!"})
        self.assertRedirects(response, reverse("accounts:profile"))

    def test_login_post_requires_csrf(self):
        client = Client(enforce_csrf_checks=True)
        response = client.post(reverse("accounts:login"), {"username": "attendee", "password": "test-password-73!"})
        self.assertEqual(response.status_code, 403)
        self.assertNotIn("_auth_user_id", client.session)

    def test_logout_requires_post_and_csrf_and_ends_session(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.user)
        self.assertEqual(client.get(reverse("accounts:logout")).status_code, 405)
        self.assertEqual(client.post(reverse("accounts:logout")).status_code, 403)
        client.get(reverse("accounts:profile"))
        response = client.post(reverse("accounts:logout"), {"csrfmiddlewaretoken": client.cookies["csrftoken"].value})
        self.assertRedirects(response, reverse("core:home"))
        self.assertNotIn("_auth_user_id", client.session)

    def test_regular_attendee_cannot_access_admin(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("admin:login")))
