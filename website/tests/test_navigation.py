from django.test import TestCase
from wagtail.models import Page, Site
from taggit.models import Tag

from website.models import (
    ArticlePage,
    ArticlesIndexPage,
    HomePage,
    ProjectPage,
)


class NavigationTests(TestCase):
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
                short_description="<p>Django REST API</p>",
            )
        )

        cls.project.tags.add("django")

        cls.articles_index = cls.home_page.add_child(
            instance=ArticlesIndexPage(
                title="Articles",
                slug="articles",
            )
        )

        cls.article = cls.articles_index.add_child(
            instance=ArticlePage(
                title="Building APIs with Django",
                slug="building-apis-with-django",
                intro="Learn Django REST API development.",
                body="<p>Django and REST API</p>",
            )
        )

        cls.article.tags.add("django")

        for page in (
            cls.home_page,
            cls.project,
            cls.articles_index,
            cls.article,
        ):
            page.save_revision().publish()

    def test_topics_index_returns_success(self):
        response = self.client.get(
            "/topics/",
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 200)

    def test_topic_detail_returns_success(self):
        tag = Tag.objects.get(slug="django")

        response = self.client.get(
            f"/topics/{tag.slug}/",
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 200)

    def test_unknown_topic_returns_404(self):
        response = self.client.get(
            "/topics/unknown-topic/",
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 404)

    def test_search_page_returns_success(self):
        response = self.client.get(
            "/search/",
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 200)

    def test_search_finds_project_by_title(self):
        response = self.client.get(
            "/search/",
            {"q": "ACRON"},
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ACRON")

    def test_search_finds_article(self):
        response = self.client.get(
            "/search/",
            {"q": "Building APIs"},
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Building APIs")

    def test_search_with_empty_query_returns_success(self):
        response = self.client.get(
            "/search/",
            {"q": "   "},
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 200)