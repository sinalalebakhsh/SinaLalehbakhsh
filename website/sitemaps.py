from django.contrib.sitemaps import Sitemap

from website.models import HomePage, ProjectPage


class PortfolioSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return [
            HomePage.objects.live().first(),
            *ProjectPage.objects.live(),
        ]

    def location(self, obj):
        if isinstance(obj, HomePage):
            return "/"

        return f"/{obj.slug}/"

    def lastmod(self, obj):
        return obj.last_published_at