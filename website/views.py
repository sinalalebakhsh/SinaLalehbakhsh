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

    related_topic_ids = set()

    for project in projects:
        related_topic_ids.update(
            project.tags.values_list("id", flat=True)
        )

    for article in articles:
        related_topic_ids.update(
            article.tags.values_list("id", flat=True)
        )

    related_topics = (
        Tag.objects
        .filter(id__in=related_topic_ids)
        .exclude(id=tag.id)
        .order_by("name")
    )

    return render(
        request,
        "website/topic_detail.html",
        {
            "tag": tag,
            "projects": projects,
            "articles": articles,
            "related_topics": related_topics,
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


