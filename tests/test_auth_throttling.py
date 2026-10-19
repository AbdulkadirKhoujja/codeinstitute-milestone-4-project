from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from accounts.models import AuthThrottle


class AuthenticationThrottleTests(TestCase):
    def test_five_failed_attempts_block_further_login_then_expire(self):
        get_user_model().objects.create_user(username="learner", password="Correct-forest-83!")
        for _ in range(5):
            self.assertEqual(
                self.client.post(
                    "/accounts/login/", {"username": "learner", "password": "wrong"}
                ).status_code,
                200,
            )
        response = self.client.post(
            "/accounts/login/", {"username": "learner", "password": "Correct-forest-83!"}
        )
        self.assertEqual(response.status_code, 429)
        self.assertIn("Retry-After", response)
        self.assertNotIn("_auth_user_id", self.client.session)
        AuthThrottle.objects.update(expires_at=timezone.now() - timedelta(seconds=1))
        self.assertEqual(
            self.client.post(
                "/accounts/login/", {"username": "learner", "password": "Correct-forest-83!"}
            ).status_code,
            302,
        )

    def test_local_forwarded_ip_cannot_bypass_and_other_ip_is_independent(self):
        for _ in range(5):
            self.client.post("/accounts/login/", {"username": "unknown", "password": "wrong"})
        self.assertEqual(
            self.client.post(
                "/accounts/login/",
                {"username": "unknown", "password": "wrong"},
                HTTP_X_FORWARDED_FOR="203.0.113.99",
            ).status_code,
            429,
        )
        self.assertEqual(
            self.client.post(
                "/accounts/login/",
                {"username": "unknown", "password": "wrong"},
                REMOTE_ADDR="203.0.113.98",
            ).status_code,
            200,
        )
        for bucket in AuthThrottle.objects.all():
            self.assertNotIn("unknown", bucket.key)
            self.assertNotIn("127.0.0.1", bucket.key)
