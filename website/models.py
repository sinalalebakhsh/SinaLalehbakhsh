from wagtail.images import get_image_model
from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page

from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase





class HomePage(Page):
    max_count = 1
    subpage_types = ["website.ProjectPage"]
    template = "website/home_page.html"

    intro = RichTextField(
        blank=True,
        help_text="Short introduction shown on the homepage.",
    )

    tagline = RichTextField(
        blank=True,
        help_text="Short tagline shown below the main title.",
    )

    about = RichTextField(
        blank=True,
        help_text="About section shown on the homepage.",
    )

    skills = RichTextField(
        blank=True,
        help_text="Skills and technologies.",
    )

    projects = RichTextField(
        blank=True,
        help_text="Short introduction for the projects section.",
    )

    experience = RichTextField(
        blank=True,
        help_text="Professional experience.",
    )

    contact = RichTextField(
        blank=True,
        help_text="Contact information.",
    )

    profile_image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Profile image shown on the homepage.",
    )

    cv_url = models.URLField(
        blank=True,
        help_text="CV or resume URL.",
    )

    linkedin_url = models.URLField(
        blank=True,
        help_text="LinkedIn profile URL.",
    )

    github_url = models.URLField(
        blank=True,
        help_text="GitHub profile URL.",
    )
    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("tagline"),
        FieldPanel("about"),
        FieldPanel("skills"),
        FieldPanel("projects"),
        FieldPanel("experience"),
        FieldPanel("contact"),
        FieldPanel("cv_url"),
        FieldPanel("linkedin_url"),
        FieldPanel("github_url"),
        FieldPanel("profile_image"),
    ]


class ProjectPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "website.ProjectPage",
        on_delete=models.CASCADE,
        related_name="tagged_items",
    )


class ProjectPage(Page):
    parent_page_types = ["website.HomePage"]
    template = "website/project_page.html"

    short_description = RichTextField(
        blank=True,
        help_text="Short project description.",
    )

    description = RichTextField(
        blank=True,
        help_text="Detailed project description.",
    )

    technologies = RichTextField(
        blank=True,
        help_text="Technologies used in this project.",
    )

    project_url = models.URLField(
        blank=True,
        help_text="Live project URL.",
    )

    github_url = models.URLField(
        blank=True,
        help_text="GitHub repository URL.",
    )

    image = models.ForeignKey(
        get_image_model(),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text="Project cover image.",
    )

    role = models.CharField(
        max_length=100,
        blank=True,
        help_text="Your role in this project.",
    )

    project_type = models.CharField(
        max_length=100,
        blank=True,
        help_text="Type of project, for example Personal Project or Client Project.",
    )

    status = models.CharField(
        max_length=100,
        blank=True,
        help_text="Current project status.",
    )


    tags = ClusterTaggableManager(
        through="website.ProjectPageTag",
        blank=True,
        help_text="Add tags such as Django, Python, AI, REST API.",
    )


    content_panels = Page.content_panels + [
        FieldPanel("short_description"),
        FieldPanel("description"),
        FieldPanel("technologies"),
        FieldPanel("role"),
        FieldPanel("project_type"),
        FieldPanel("status"),
        FieldPanel("project_url"),
        FieldPanel("github_url"),
        FieldPanel("image"),
        FieldPanel("tags"),
    ]


    @property
    def previous_project(self):
        return (
            self.get_siblings()
            .live()
            .specific()
            .filter(path__lt=self.path)
            .order_by("-path")
            .first()
        )

    @property
    def next_project(self):
        return (
            self.get_siblings()
            .live()
            .specific()
            .filter(path__gt=self.path)
            .order_by("path")
            .first()
        )
