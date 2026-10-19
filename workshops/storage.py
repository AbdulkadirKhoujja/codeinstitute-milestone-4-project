import os
import uuid
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage


class PrivateStorage(FileSystemStorage):
    @property
    def database_backed(self):
        return getattr(settings, "PRIVATE_RESOURCE_BACKEND", "filesystem") == "database"

    def _open(self, name, mode="rb"):
        if not self.database_backed:
            return super()._open(name, mode)
        model = apps.get_model("workshops", "PrivateResourceBlob")
        try:
            blob = model.objects.get(pk=name)
        except model.DoesNotExist:
            raise FileNotFoundError(name) from None
        return ContentFile(bytes(blob.content), name=name)

    def _save(self, name, content):
        if not self.database_backed:
            return super()._save(name, content)
        data = content.read(5 * 1024 * 1024 + 1)
        if len(data) > 5 * 1024 * 1024:
            raise ValueError("Private files must be 5 MB or smaller.")
        apps.get_model("workshops", "PrivateResourceBlob").objects.create(name=name, content=data)
        return name

    def exists(self, name):
        if self.database_backed:
            return (
                apps.get_model("workshops", "PrivateResourceBlob").objects.filter(pk=name).exists()
            )
        return super().exists(name)

    def delete(self, name):
        if self.database_backed:
            apps.get_model("workshops", "PrivateResourceBlob").objects.filter(pk=name).delete()
        else:
            super().delete(name)

    def size(self, name):
        if self.database_backed:
            with self._open(name) as content:
                return content.size
        return super().size(name)

    def path(self, name):
        if self.database_backed:
            raise NotImplementedError("Database resources have no filesystem path.")
        return super().path(name)

    @property
    def base_location(self):
        return settings.PRIVATE_RESOURCE_ROOT

    @property
    def location(self):
        return os.path.abspath(self.base_location)

    def url(self, name):
        raise ValueError("Private resources have no public URL.")


def resource_path(instance, filename):
    return f"resources/{uuid.uuid4().hex}{Path(filename).suffix[:12]}"
