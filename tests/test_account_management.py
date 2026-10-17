from django.contrib.auth import get_user_model
from django.test import TestCase


class AccountManagementTests(TestCase):
    def test_registration_hashes_password_and_ignores_privileges(self):
        response = self.client.post(
            "/accounts/register/",
            {
                "username": "newlearner",
                "password1": "Unusual-river-92!",
                "password2": "Unusual-river-92!",
                "is_staff": "true",
                "is_superuser": "true",
            },
        )
        self.assertEqual(response.status_code, 302)
        person = get_user_model().objects.get(username="newlearner")
        self.assertTrue(person.check_password("Unusual-river-92!"))
        self.assertFalse(person.is_staff)
        self.assertFalse(person.is_superuser)

    def test_weak_password_rejected(self):
        response = self.client.post(
            "/accounts/register/",
            {"username": "newlearner", "password1": "123", "password2": "123"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(get_user_model().objects.filter(username="newlearner").exists())

    def test_edit_only_own_profile_and_no_privilege_assignment(self):
        person = get_user_model().objects.create_user(
            username="person", password="Unusual-river-92!"
        )
        other = get_user_model().objects.create_user(username="other")
        self.client.force_login(person)
        response = self.client.post(
            "/accounts/edit/",
            {
                "first_name": "Alex",
                "last_name": "Example",
                "email": "alex@example.com",
                "id": other.pk,
                "is_staff": "true",
            },
        )
        self.assertEqual(response.status_code, 302)
        person.refresh_from_db()
        other.refresh_from_db()
        self.assertEqual(person.first_name, "Alex")
        self.assertFalse(person.is_staff)
        self.assertEqual(other.first_name, "")

    def test_anonymous_edit_and_password_change_protected(self):
        for path in ("/accounts/edit/", "/accounts/password/"):
            self.assertEqual(self.client.get(path).status_code, 302)

    def test_password_change_checks_old_password_and_preserves_session(self):
        person = get_user_model().objects.create_user(
            username="person", password="Unusual-river-92!"
        )
        self.client.force_login(person)
        data = {
            "old_password": "wrong",
            "new_password1": "Different-forest-82!",
            "new_password2": "Different-forest-82!",
        }
        self.assertEqual(self.client.post("/accounts/password/", data).status_code, 200)
        data["old_password"] = "Unusual-river-92!"
        self.assertEqual(self.client.post("/accounts/password/", data).status_code, 302)
        person.refresh_from_db()
        self.assertTrue(person.check_password("Different-forest-82!"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), person.pk)
