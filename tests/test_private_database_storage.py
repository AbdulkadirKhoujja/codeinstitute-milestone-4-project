from django.core.files.base import ContentFile
from django.test import TestCase, override_settings

from workshops.models import PrivateResourceBlob
from workshops.storage import PrivateStorage


@override_settings(PRIVATE_RESOURCE_BACKEND="database")
class PersistentResourceStorageTests(TestCase):
    def test_bytes_survive_new_storage_instance_and_have_no_public_url(self):
        storage = PrivateStorage()
        name = storage.save("resources/fictional.txt", ContentFile(b"Private persistent handout"))
        self.assertEqual(PrivateResourceBlob.objects.count(), 1)
        restarted = PrivateStorage()
        self.assertTrue(restarted.exists(name))
        self.assertEqual(restarted.open(name).read(), b"Private persistent handout")
        self.assertEqual(restarted.size(name), 26)
        with self.assertRaises(ValueError):
            restarted.url(name)
        restarted.delete(name)
        self.assertFalse(storage.exists(name))

    def test_rejects_oversize_content_and_missing_files(self):
        storage = PrivateStorage()
        with self.assertRaises(ValueError):
            storage.save("resources/too-large.bin", ContentFile(b"x" * (5 * 1024 * 1024 + 1)))
        with self.assertRaises(FileNotFoundError):
            storage.open("resources/missing")
