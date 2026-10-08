from django.contrib.sitemaps import Sitemap

from website.models import (
    ArticlePage,
    ArticlesIndexPage,
    HomePage,
    ProjectPage,
)


class PortfolioSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return (
            list(HomePage.objects.live())
            + list(ProjectPage.objects.live())
            + list(ArticlesIndexPage.objects.live())
            + list(ArticlePage.objects.live())
        )

    def location(self, obj):
        return obj.get_url()

    def lastmod(self, obj):
        return obj.last_published_at

        