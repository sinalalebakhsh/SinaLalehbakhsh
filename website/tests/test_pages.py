from django.test import TestCase
from wagtail.models import Page, Site

from website.models import (
    ArticlePage,
    ArticlesIndexPage,
    HomePage,
    ProjectPage,
)


class PageTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        root_page = Page.objects.get(depth=1)

        cls.home_page = root_page.add_child(
            instance=HomePage(
                title="Sina Lalehbakhsh",
                slug="test-homepage",
                intro="<p>Software Developer</p>",
            )
        )

        cls.site, _ = Site.objects.update_or_create(
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
                short_description="<p>Django project</p>",
            )
        )

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
                intro="A guide to Django REST APIs.",
                body="<p>API development</p>",
            )
        )

        for page in (
            cls.home_page,
            cls.project,
            cls.articles_index,
            cls.article,
        ):
            page.save_revision().publish()

    def test_homepage_returns_success(self):
        response = self.client.get("/", HTTP_HOST="localhost")

        self.assertEqual(response.status_code, 200)

    def test_project_page_returns_success(self):
        response = self.client.get(
            self.project.get_url(),
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 200)

    def test_articles_index_returns_success(self):
        response = self.client.get(
            self.articles_index.get_url(),
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 200)

    def test_article_page_returns_success(self):
        response = self.client.get(
            self.article.get_url(),
            HTTP_HOST="localhost",
        )

        self.assertEqual(response.status_code, 200)

    def test_homepage_lists_live_projects(self):
        projects = self.home_page.get_projects()

        self.assertIn(self.project, projects)

    def test_articles_index_lists_live_articles(self):
        articles = self.articles_index.get_articles()

        self.assertIn(self.article, articles)