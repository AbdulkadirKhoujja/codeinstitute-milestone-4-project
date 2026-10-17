import uuid
from pathlib import Path

from django.conf import settings
from django.core.files.storage import FileSystemStorage


class PrivateStorage(FileSystemStorage):
    @property
    def base_location(self):
        return settings.PRIVATE_RESOURCE_ROOT

    def url(self, name):
        raise ValueError("Private resources have no public URL.")


def resource_path(instance, filename):
    return f"resources/{uuid.uuid4().hex}{Path(filename).suffix[:12]}"
