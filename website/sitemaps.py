from django.contrib.sitemaps import Sitemap
from wagtail.models import Page

from website.models import (
    HomePage,
    ProjectPage,
    ArticlesIndexPage,
    ArticlePage,
)


class PortfolioSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return (
            Page.objects.live()
            .public()
            .type(
                HomePage,
                ProjectPage,
                ArticlesIndexPage,
                ArticlePage,
            )
            .specific()
            .order_by("path")
        )

    def location(self, obj):
        return obj.get_url()

    def lastmod(self, obj):
        return obj.last_published_at