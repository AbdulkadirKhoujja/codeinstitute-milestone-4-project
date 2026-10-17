from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from workshops.models import Workshop


class Command(BaseCommand):
    help = "Create three explicitly fictional workshops for local development only."

    def handle(self, *args, **options):
        if settings.PRODUCTION:
            raise CommandError("Demo data is available only in explicit development mode.")
        owner, created = get_user_model().objects.get_or_create(
            username="fictional-skillseat-host",
            defaults={"first_name": "SkillSeat", "last_name": "Demo Studio"},
        )
        if created:
            owner.set_unusable_password()
            owner.save()
        for index, (title, price, description) in enumerate(
            [
                (
                    "Clay, coffee & a little creativity",
                    2500,
                    "Shape your first hand-built ceramic piece. Explore texture, form and the joy of making with clay.",
                ),
                (
                    "Find your eye for photography",
                    1800,
                    "See familiar streets differently. Learn composition and natural light with the camera you already have.",
                ),
                (
                    "Your first lines of Python",
                    0,
                    "A friendly introduction to solving small problems with code. Bring curiosity and a laptop; no experience needed.",
                ),
            ]
        ):
            start = (timezone.now() + timedelta(days=7 + index)).replace(
                hour=10, minute=0, second=0, microsecond=0
            )
            Workshop.objects.get_or_create(
                owner=owner,
                title=title,
                defaults={
                    "description": "Fictional development workshop. " + description,
                    "location": "Demo Studio · London (fictional)",
                    "starts_at": start,
                    "ends_at": start + timedelta(hours=2),
                    "capacity": 8,
                    "price_pence": price,
                    "published": True,
                },
            )
        self.stdout.write(
            "Fictional demo workshops ready. No customer accounts, transactions or login passwords created."
        )
