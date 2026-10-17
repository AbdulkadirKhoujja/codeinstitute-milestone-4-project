from django.core.management.base import BaseCommand

from workshops.services import expire_bookings


class Command(BaseCommand):
    help = "Release expired unpaid booking holds. Safe to run repeatedly."

    def handle(self, *args, **options):
        self.stdout.write(f"Expired {expire_bookings()} booking holds.")
