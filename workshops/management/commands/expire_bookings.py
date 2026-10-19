from django.core.management.base import BaseCommand
from django.utils import timezone

from accounts.models import AuthThrottle
from workshops.services import expire_bookings


class Command(BaseCommand):
    help = "Release expired unpaid booking holds. Safe to run repeatedly."

    def handle(self, *args, **options):
        self.stdout.write(f"Expired {expire_bookings()} booking holds.")
        count, _ = AuthThrottle.objects.filter(expires_at__lte=timezone.now()).delete()
        self.stdout.write(f"Removed {count} expired authentication throttle buckets.")
