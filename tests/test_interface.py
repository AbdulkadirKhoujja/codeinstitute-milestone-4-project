from django.test import TestCase


class InterfaceTests(TestCase):
    def test_owner_forms_have_unique_resource_labels(self):
        from django.contrib.auth.models import Permission

        from tests.test_workshops import workshop

        item = workshop()
        item.owner.user_permissions.add(Permission.objects.get(codename="add_workshop"))
        self.client.force_login(item.owner)
        response = self.client.get(f"/workshops/studio/{item.pk}/")
        self.assertEqual(response.content.count(b'id="id_title"'), 1)
        self.assertContains(response, 'for="resource_title"')

    def test_full_or_ended_detail_explains_unavailability(self):
        from tests.test_workshops import workshop

        item = workshop(capacity=1, reserved=1)
        self.client.force_login(item.owner)
        response = self.client.get(f"/workshops/{item.pk}/")
        self.assertContains(response, "Booking is currently unavailable")
        self.assertNotContains(response, "Reserve a place")
        self.assertNotContains(response, "Write or edit your review")

    def test_home_leads_to_discovery_and_registration(self):
        response = self.client.get("/")
        for text in (
            'href="/workshops/"',
            'href="/accounts/register/"',
            'href="#main-content"',
            'id="main-content"',
            "SkillSeat",
            "Make room for your next skill",
        ):
            self.assertContains(response, text)

    def test_shared_navigation_status_and_styles(self):
        for path in ("/", "/workshops/", "/accounts/register/", "/accounts/login/"):
            response = self.client.get(path)
            self.assertContains(response, 'aria-label="Main navigation"')
            self.assertContains(response, 'name="viewport"')
            self.assertContains(response, "skillseat.css")
            self.assertContains(response, "<footer")

    def test_registration_uses_block_help_and_programmatic_descriptions(self):
        response = self.client.get("/accounts/register/")
        self.assertContains(response, '<div class="helptext" id="id_password1_helptext">')
        self.assertContains(response, 'aria-describedby="id_password1_helptext"')
