from django.contrib.sitemaps import Sitemap
from wagtail.models import Page


class WagtailSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Page.objects.live().public().specific()

    def location(self, obj):
        return obj.url