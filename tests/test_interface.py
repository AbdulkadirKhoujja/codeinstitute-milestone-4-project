from django.test import TestCase


class InterfaceTests(TestCase):
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
