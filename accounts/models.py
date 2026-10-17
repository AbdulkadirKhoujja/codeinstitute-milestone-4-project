from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Django's username-based user; extension point for future account needs."""
