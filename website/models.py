from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


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

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("tagline"),
        FieldPanel("about"),
        FieldPanel("skills"),
        FieldPanel("projects"),
        FieldPanel("experience"),
        FieldPanel("contact"),
    ]


class ProjectPage(Page):
    template = "website/project_page.html"
    parent_page_types = ["website.HomePage"]
    
    short_description = RichTextField(
        blank=True,
        help_text="Short project description.",
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

    content_panels = Page.content_panels + [
        FieldPanel("short_description"),
        FieldPanel("technologies"),
        FieldPanel("project_url"),
        FieldPanel("github_url"),
    ]

    class Meta:
        verbose_name = "Project"
        verbose_name_plural = "Projects"

