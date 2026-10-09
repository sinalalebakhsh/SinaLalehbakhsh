from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from taggit.models import Tag

from .models import ArticlePage, ProjectPage


def topic_index(request):
    tags = Tag.objects.order_by("name")
    topic_data = []

    for tag in tags:
        projects_count = (
            ProjectPage.objects.live()
            .filter(tags=tag)
            .count()
        )

        articles_count = (
            ArticlePage.objects.live()
            .filter(tags=tag)
            .count()
        )

        # موضوعی که هیچ محتوای منتشرشده‌ای ندارد، نمایش داده نشود.
        if projects_count == 0 and articles_count == 0:
            continue

        topic_data.append(
            {
                "tag": tag,
                "projects_count": projects_count,
                "articles_count": articles_count,
            }
        )

    return render(
        request,
        "website/topic_index.html",
        {
            "topic_data": topic_data,
        },
    )


def topic_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)

    projects = (
        ProjectPage.objects.live()
        .filter(tags=tag)
        .specific()
        .order_by("-first_published_at")
    )

    articles = (
        ArticlePage.objects.live()
        .filter(tags=tag)
        .specific()
        .order_by("-first_published_at")
    )

    return render(
        request,
        "website/topic_detail.html",
        {
            "tag": tag,
            "projects": projects,
            "articles": articles,
        },
    )
def search(request):
    query = request.GET.get("q", "").strip()

    projects = ProjectPage.objects.none()
    articles = ArticlePage.objects.none()

    if query:
        matching_tags = Tag.objects.filter(
            name__icontains=query
        )

        projects = (
            ProjectPage.objects.live()
            .filter(
                Q(title__icontains=query)
                | Q(short_description__icontains=query)
                | Q(description__icontains=query)
                | Q(technologies__icontains=query)
                | Q(tags__in=matching_tags)
            )
            .specific()
            .distinct()
        )

        articles = (
            ArticlePage.objects.live()
            .filter(
                Q(title__icontains=query)
                | Q(intro__icontains=query)
                | Q(body__icontains=query)
                | Q(tags__in=matching_tags)
            )
            .specific()
            .distinct()
        )

    return render(
        request,
        "website/search.html",
        {
            "query": query,
            "projects": projects,
            "articles": articles,
        },
    )

