from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from website.sitemaps import PortfolioSitemap
from website import views


sitemaps = {
    "pages": PortfolioSitemap,
}


urlpatterns = [
    path("django-admin/", admin.site.urls),

    path(
        "topics/<str:slug>/",
        views.topic_detail,
        name="topic_detail",
    ),

    path("topics/", views.topic_index, name="topic_index"),
    path("search/", views.search, name="search"),

    path("admin/", include(wagtailadmin_urls)),

    path("documents/", include(wagtaildocs_urls)),

    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain",
        ),
    ),

    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="sitemap",
    ),

    path("", include(wagtail_urls)),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )