"""Explicit, additive assessment fixtures; never called during application startup."""

from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from workshops.models import PrivateResourceBlob, Resource, Workshop

DEMO_OWNER = "skillseat-assessment-demo"
DEMO_DESCRIPTION = (
    "Fictional assessment demonstration: not a real scheduled event. "
    "Bookings and Stripe sandbox payments are for testing only; no real money is taken. "
)
CATALOGUE = (
    (
        "DEMO: Your first lines of Python",
        0,
        "Explore variables and loops with friendly coding exercises. No experience needed.",
    ),
    (
        "DEMO: Everyday drawing for beginners",
        0,
        "Practise pencil sketches, shapes and observation with everyday objects.",
    ),
    (
        "DEMO: Find your eye for photography",
        100,
        "Explore composition and natural light. Includes a downloadable fictional practice handout after verified test payment.",
    ),
    (
        "DEMO: Clay, coffee & creativity",
        250,
        "Explore hand-built ceramics, texture and form with a fictional pottery exercise.",
    ),
)
HANDOUT = (
    b"SkillSeat fictional photography practice handout\n"
    b"Assessment demonstration only - no real scheduled event.\n\n"
    b"1. Frame an everyday object using the rule of thirds.\n"
    b"2. Compare the same scene in soft window light and shade.\n"
    b"3. Write down how your framing changes the story.\n"
)


class Command(BaseCommand):
    help = "Add four permanent fictional assessment workshops, preserving all existing records."

    def add_arguments(self, parser):
        parser.add_argument("--confirm", help="Required acknowledgement: skillseat-assessment-demo")

    @transaction.atomic
    def handle(self, *args, **options):
        if options.get("confirm") != DEMO_OWNER:
            raise CommandError("Explicit --confirm skillseat-assessment-demo is required.")
        if not settings.STRIPE_TEST_KEY.startswith(("sk_test_", "rk_test_")):
            raise CommandError("A Stripe sandbox key is required; live payments are forbidden.")
        if not settings.STRIPE_WEBHOOK_SECRET:
            raise CommandError("Configure signed Stripe webhook verification before seeding.")
        if settings.PRIVATE_RESOURCE_BACKEND != "database":
            raise CommandError("Durable database private-resource storage is required.")

        owner, created = get_user_model().objects.get_or_create(
            username=DEMO_OWNER,
            defaults={
                "first_name": "Fictional Assessment",
                "last_name": "Demo Host",
                "password": "!",
            },
        )
        # Serialize simultaneous invocations through the unique, dedicated owner row.
        owner = get_user_model().objects.select_for_update().get(pk=owner.pk)
        if not created and (
            owner.has_usable_password()
            or owner.is_staff
            or owner.is_superuser
            or owner.first_name != "Fictional Assessment"
            or owner.last_name != "Demo Host"
            or owner.user_permissions.exists()
            or owner.groups.exists()
        ):
            raise CommandError("Dedicated demo username is occupied; no account was modified.")

        for index, (title, price, description) in enumerate(CATALOGUE):
            start = (timezone.now() + timedelta(days=730 + index)).replace(
                hour=10, minute=0, second=0, microsecond=0
            )
            item, _ = Workshop.objects.get_or_create(
                owner=owner,
                title=title,
                defaults={
                    "description": DEMO_DESCRIPTION + description,
                    "location": "Fictional Demo Studio, London - assessment only",
                    "starts_at": start,
                    "ends_at": start + timedelta(hours=2),
                    "capacity": 30,
                    "price_pence": price,
                    "published": True,
                },
            )
            if not item.published or item.price_pence != price or item.starts_at <= timezone.now():
                raise CommandError(
                    "Existing demo listing has changed or expired; review it manually. No records were overwritten."
                )
            if price == 100:
                name = f"assessment/photography-{item.pk}.txt"
                blob, _ = PrivateResourceBlob.objects.get_or_create(
                    name=name, defaults={"content": HANDOUT}
                )
                if bytes(blob.content) != HANDOUT:
                    raise CommandError(
                        "Existing demo resource differs; no resource was overwritten."
                    )
                resource, _ = Resource.objects.get_or_create(
                    workshop=item,
                    title="Fictional photography practice handout",
                    defaults={"file": name},
                )
                if resource.file.name != name:
                    raise CommandError(
                        "Existing demo resource reference differs; no data was overwritten."
                    )
            self.stdout.write(
                f"{item.pk}: {item.title} | {item.price_display} | {item.available_seats}/{item.capacity} available | {item.starts_at.isoformat()}"
            )
        self.stdout.write(
            "Four permanent fictional demos ready. Existing accounts, bookings and payment audit records preserved."
        )
