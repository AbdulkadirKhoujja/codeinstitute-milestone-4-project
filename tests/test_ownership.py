from django.contrib.auth.models import Permission
from django.test import TestCase

from tests.test_workshops import user, workshop
from workshops.models import Workshop


class OwnerTests(TestCase):
    def setUp(self):
        self.owner = user()
        self.owner.user_permissions.add(Permission.objects.get(codename="add_workshop"))
        self.item = workshop(owner=self.owner)
        self.data = dict(
            title="New title",
            description="Workshop details",
            location="Studio",
            starts_at=self.item.starts_at.isoformat(),
            ends_at=self.item.ends_at.isoformat(),
            capacity=3,
            price_pence=0,
            published="on",
        )

    def test_attendee_and_anonymous_cannot_manage(self):
        self.assertEqual(self.client.get("/workshops/studio/").status_code, 302)
        self.client.force_login(user("attendee"))
        for path in (
            "/workshops/studio/",
            "/workshops/studio/new/",
            f"/workshops/studio/{self.item.pk}/",
        ):
            self.assertEqual(self.client.get(path).status_code, 403)
            self.assertEqual(self.client.post(path, self.data).status_code, 403)

    def test_owner_creation_assigns_owner_server_side(self):
        self.client.force_login(self.owner)
        self.data["owner"] = user("forged").pk
        self.assertEqual(self.client.post("/workshops/studio/new/", self.data).status_code, 302)
        self.assertEqual(Workshop.objects.get(title="New title").owner, self.owner)

    def test_cross_owner_and_invalid_id_denied(self):
        other = user("otherhost")
        other.user_permissions.add(Permission.objects.get(codename="add_workshop"))
        self.client.force_login(other)
        for pk in (self.item.pk, 9999):
            path = f"/workshops/studio/{pk}/"
            self.assertEqual(self.client.get(path).status_code, 404)
            self.assertEqual(self.client.post(path, self.data).status_code, 404)

    def test_owner_can_publish_unpublish_and_edit(self):
        self.client.force_login(self.owner)
        self.data.pop("published")
        self.assertEqual(
            self.client.post(f"/workshops/studio/{self.item.pk}/", self.data).status_code, 302
        )
        self.item.refresh_from_db()
        self.assertFalse(self.item.published)
        self.assertEqual(self.item.title, "New title")

    def test_capacity_reduction_below_reservations_rejected(self):
        Workshop.objects.filter(pk=self.item.pk).update(reserved=2)
        self.client.force_login(self.owner)
        self.data["capacity"] = 1
        self.assertEqual(
            self.client.post(f"/workshops/studio/{self.item.pk}/", self.data).status_code, 200
        )
        self.item.refresh_from_db()
        self.assertEqual(self.item.capacity, 2)

    def test_superuser_can_manage_other_owners(self):
        admin = user("admin")
        admin.is_superuser = True
        admin.save()
        self.client.force_login(admin)
        self.assertEqual(self.client.get(f"/workshops/studio/{self.item.pk}/").status_code, 200)
