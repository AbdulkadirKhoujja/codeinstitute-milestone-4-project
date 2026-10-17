from io import StringIO

from django.core.management import call_command
from django.test import TestCase

from workshops.models import Workshop


class DemoDataTests(TestCase):
    def test_explicit_fictional_seed_is_idempotent_and_has_no_login_password(self):
        call_command("seed_demo", stdout=StringIO())
        call_command("seed_demo", stdout=StringIO())
        self.assertEqual(Workshop.objects.count(), 3)
        for item in Workshop.objects.select_related("owner"):
            self.assertIn("Fictional", item.description)
            self.assertFalse(item.owner.has_usable_password())
            self.assertFalse(item.owner.is_staff)
