from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page


class HomePage(Page):
    max_count = 1
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
        help_text="Main projects and portfolio.",
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

    class Meta:
        verbose_name = "Home Page"
        verbose_name_plural = "Home Page"



        