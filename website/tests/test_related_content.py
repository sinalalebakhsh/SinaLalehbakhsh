from django.test import TestCase
from wagtail.models import Page, Site

from website.models import (
    ArticlePage,
    ArticlesIndexPage,
    HomePage,
    ProjectPage,
)


class RelatedContentTests(TestCase):
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
        cls.project.tags.add("django", "rest-api")

        cls.other_project = cls.home_page.add_child(
            instance=ProjectPage(
                title="Another Django Project",
                slug="another-django-project",
            )
        )
        cls.other_project.tags.add("django")

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
            )
        )
        cls.article.tags.add("django", "python")

        cls.other_article = cls.articles_index.add_child(
            instance=ArticlePage(
                title="Django REST Guide",
                slug="django-rest-guide",
            )
        )
        cls.other_article.tags.add("django")

        for page in (
            cls.home_page,
            cls.project,
            cls.other_project,
            cls.articles_index,
            cls.article,
            cls.other_article,
        ):
            page.save_revision().publish()

    def test_article_finds_related_projects_by_tag(self):
        related_projects = self.article.get_related_projects()

        self.assertIn(self.project, related_projects)
        self.assertIn(self.other_project, related_projects)

    def test_article_does_not_return_unrelated_projects(self):
        unrelated_project = self.home_page.add_child(
            instance=ProjectPage(
                title="Piura",
                slug="piura",
            )
        )
        unrelated_project.tags.add("water")
        unrelated_project.save_revision().publish()

        related_projects = self.article.get_related_projects()

        self.assertNotIn(unrelated_project, related_projects)

    def test_article_finds_related_articles_by_tag(self):
        related_articles = self.article.get_related_articles()

        self.assertIn(self.other_article, related_articles)
        self.assertNotIn(self.article, related_articles)

    def test_project_finds_related_projects_by_tag(self):
        related_projects = self.project.get_related_projects()

        self.assertIn(self.other_project, related_projects)
        self.assertNotIn(self.project, related_projects)

    def test_project_finds_related_articles_by_tag(self):
        related_articles = self.project.get_related_articles()

        self.assertIn(self.article, related_articles)
        self.assertIn(self.other_article, related_articles)

    def test_content_without_tags_has_no_related_items(self):
        untagged_article = self.articles_index.add_child(
            instance=ArticlePage(
                title="Untagged Article",
                slug="untagged-article",
            )
        )
        untagged_article.save_revision().publish()

        self.assertEqual(
            untagged_article.get_related_articles().count(),
            0,
        )
        self.assertEqual(
            untagged_article.get_related_projects().count(),
            0,
        )