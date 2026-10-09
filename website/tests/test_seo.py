from django.test import TestCase
from wagtail.models import Page, Site

from website.models import HomePage, ProjectPage


class SeoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        root_page = Page.objects.get(depth=1)

        cls.home_page = root_page.add_child(
            instance=HomePage(
                title="Sina Lalehbakhsh",
                slug="test-homepage",
            )
        )

        Site.objects.update_or_create(
            hostname="localhost",
            port=80,
            defaults={
                "root_page": cls.home_page,
                "is_default_site": True,
            },
        )

        cls.project = cls.home_page.add_child(
            instance=ProjectPage(
                title="ACRON",
                slug="acron",
            )
        )

        for page in (cls.home_page, cls.project):
            page.save_revision().publish()

    def test_robots_txt_returns_success(self):
        response = self.client.get(
            "/robots.txt",
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 200)

    def test_sitemap_xml_returns_success(self):
        response = self.client.get(
            "/sitemap.xml",
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 200)

    def test_sitemap_uses_xml_content_type(self):
        response = self.client.get(
            "/sitemap.xml",
            HTTP_HOST="localhost",
        )

        self.assertIn(
            "xml",
            response.headers.get("Content-Type", "").lower(),
        )

    def test_sitemap_contains_homepage(self):
        response = self.client.get(
            "/sitemap.xml",
            HTTP_HOST="localhost",
        )

        self.assertContains(response, self.home_page.get_url())