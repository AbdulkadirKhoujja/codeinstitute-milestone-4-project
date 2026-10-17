import tempfile
from datetime import timedelta

from django.contrib.auth.models import Permission
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.utils import timezone

from tests.test_workshops import user, workshop
from workshops.models import Booking, Resource, Review, Workshop
from workshops.services import reserve


class ResourceReviewTests(TestCase):
    def test_expired_and_cancelled_states_deny_even_with_a_paid_flag(self):
        self.client.force_login(self.person)
        for state in ("expired", "cancelled", "pending"):
            Booking.objects.filter(pk=self.booking.pk).update(status=state, paid=True)
            self.assertEqual(
                self.client.get(f"/workshops/resources/{self.resource.pk}/").status_code, 404
            )

    def test_owner_resource_delete_checks_ownership_and_removes_file(self):
        other = user("otherhost")
        other.user_permissions.add(Permission.objects.get(codename="add_workshop"))
        self.client.force_login(other)
        path = f"/workshops/resources/{self.resource.pk}/delete/"
        self.assertEqual(self.client.post(path).status_code, 404)
        storage, filename = self.resource.file.storage, self.resource.file.name
        self.assertTrue(storage.exists(filename))
        self.client.force_login(self.item.owner)
        self.assertEqual(self.client.post(path).status_code, 302)
        self.assertFalse(storage.exists(filename))
        self.assertFalse(Resource.objects.exists())

    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.setting = override_settings(PRIVATE_RESOURCE_ROOT=self.directory.name)
        self.setting.enable()
        self.addCleanup(self.setting.disable)
        self.item = workshop(price_pence=1200)
        self.item.owner.user_permissions.add(Permission.objects.get(codename="add_workshop"))
        self.person = user("learner")
        self.booking = reserve(self.item.pk, self.person)
        self.resource = Resource.objects.create(
            workshop=self.item,
            title="Course notes",
            file=SimpleUploadedFile("notes.txt", b"Private course notes"),
        )

    def test_private_file_denied_until_verified_and_revoked_on_cancel(self):
        path = f"/workshops/resources/{self.resource.pk}/"
        self.assertEqual(self.client.get(path).status_code, 302)
        self.client.force_login(self.person)
        self.assertEqual(self.client.get(path).status_code, 404)
        Booking.objects.filter(pk=self.booking.pk).update(paid=True, status="confirmed")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b"".join(response.streaming_content), b"Private course notes")
        self.assertEqual(response["Content-Type"], "application/octet-stream")
        Booking.objects.filter(pk=self.booking.pk).update(status="cancelled")
        self.assertEqual(self.client.get(path).status_code, 404)
        self.assertEqual(self.client.get("/media/notes.txt").status_code, 404)

    def test_unrelated_user_and_forged_resource_denied(self):
        self.client.force_login(user("outsider"))
        for path in (
            f"/workshops/resources/{self.resource.pk}/",
            "/workshops/resources/9999/",
            "/workshops/resources/../../notes.txt",
        ):
            self.assertEqual(self.client.get(path).status_code, 404)

    def test_owner_can_upload_but_cross_owner_cannot(self):
        path = f"/workshops/studio/{self.item.pk}/resources/"
        other = user("otherhost")
        other.user_permissions.add(Permission.objects.get(codename="add_workshop"))
        self.client.force_login(other)
        self.assertEqual(self.client.post(path, {"title": "Forged"}).status_code, 404)
        self.client.force_login(self.item.owner)
        self.assertEqual(
            self.client.post(
                path, {"title": "Extra notes", "file": SimpleUploadedFile("extra.txt", b"example")}
            ).status_code,
            302,
        )
        self.assertEqual(Resource.objects.filter(workshop=self.item).count(), 2)

    def test_review_requires_completion_attendance_and_confirmed_booking(self):
        self.client.force_login(self.person)
        path = f"/workshops/{self.item.pk}/review/"
        data = {"rating": 5, "body": "A thoughtful practical session."}
        self.assertEqual(self.client.post(path, data).status_code, 403)
        Booking.objects.filter(pk=self.booking.pk).update(
            paid=True, status="confirmed", attended=True
        )
        self.assertEqual(self.client.post(path, data).status_code, 403)
        Workshop.objects.filter(pk=self.item.pk).update(
            starts_at=timezone.now() - timedelta(hours=3),
            ends_at=timezone.now() - timedelta(hours=1),
        )
        self.assertEqual(self.client.post(path, data).status_code, 302)
        self.assertEqual(self.client.post(path, data).status_code, 302)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get().attendee, self.person)
        self.assertContains(self.client.get(f"/workshops/{self.item.pk}/"), data["body"])

    def test_review_invalid_content_and_unrelated_attendee(self):
        Workshop.objects.filter(pk=self.item.pk).update(
            starts_at=timezone.now() - timedelta(hours=3),
            ends_at=timezone.now() - timedelta(hours=1),
        )
        Booking.objects.filter(pk=self.booking.pk).update(
            paid=True, status="confirmed", attended=True
        )
        self.client.force_login(self.person)
        path = f"/workshops/{self.item.pk}/review/"
        self.assertEqual(self.client.post(path, {"rating": 6, "body": " "}).status_code, 200)
        self.assertFalse(Review.objects.exists())
        self.client.force_login(user("outsider"))
        self.assertEqual(
            self.client.post(path, {"rating": 5, "body": "Forged review"}).status_code, 403
        )

    def test_only_owner_marks_attendance_after_end(self):
        path = f"/workshops/studio/bookings/{self.booking.pk}/attend/"
        self.client.force_login(self.person)
        self.assertEqual(self.client.post(path).status_code, 403)
        self.client.force_login(self.item.owner)
        self.assertEqual(self.client.post(path).status_code, 400)
        Workshop.objects.filter(pk=self.item.pk).update(
            starts_at=timezone.now() - timedelta(hours=3),
            ends_at=timezone.now() - timedelta(hours=1),
        )
        Booking.objects.filter(pk=self.booking.pk).update(paid=True, status="confirmed")
        self.assertEqual(self.client.post(path).status_code, 302)
        self.booking.refresh_from_db()
        self.assertTrue(self.booking.attended)
