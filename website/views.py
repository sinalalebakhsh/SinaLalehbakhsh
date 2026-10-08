from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from taggit.models import Tag

from .models import ArticlePage, ProjectPage


def topic_index(request):
    tags = Tag.objects.order_by("name")

    return render(
        request,
        "website/topic_index.html",
        {
            "tags": tags,
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
        projects = (
            ProjectPage.objects.live()
            .filter(
                Q(title__icontains=query)
                | Q(short_description__icontains=query)
                | Q(description__icontains=query)
                | Q(technologies__icontains=query)
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


