from django.shortcuts import get_object_or_404, render
from taggit.models import Tag

from .models import ProjectPage


def topic_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)

    projects = (
        ProjectPage.objects.live()
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
        },
    )


    