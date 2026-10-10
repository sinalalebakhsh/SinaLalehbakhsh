# Sina Lalehbakhsh — Personal Website

Personal portfolio and publishing website for **Sina Lalehbakhsh**, a software developer focused on Python, Django, backend development, REST APIs, and modern web applications.

The website brings together professional information, selected projects, technical articles, and ways to get in touch.

## About

This project is being developed as a simple, maintainable personal website and knowledge hub. It is intended to present professional experience and projects while providing a place to publish technical articles and ideas.

## Technology Stack

- **Python 3.14**
- **Django 6.1**
- **Wagtail 8**
- **SQLite** for local development
- **Pipenv** for Python environment and dependency management
- **HTML and CSS** for page templates and styling

## Features

The project currently includes code for:

- A portfolio homepage with introduction, tagline, about, skills, experience, and contact sections
- Project pages with descriptions, technologies, project links, role, status, and tags
- An article archive and individual article pages
- Related articles and projects based on shared tags
- Topic/tag index and topic detail pages
- Search across published projects and articles
- Wagtail CMS for managing website content
- `robots.txt` and a sitemap endpoint at `/sitemap.xml`

The availability and completeness of content on the live website depend on which pages have been created and published in the CMS.

## Project Repository

- GitHub: <https://github.com/sinalalebakhsh/SinaLalehbakhsh>

## Run Locally

### Requirements

Install a compatible Python version and Pipenv. The project’s current environment is configured for Python 3.14.

### Setup

Clone the repository and enter the project directory:

```bash
git clone https://github.com/sinalalebakhsh/SinaLalehbakhsh.git
cd SinaLalehbakhsh
```

Install the project dependencies:

```bash
pipenv install
```

Apply database migrations:

```bash
pipenv run python manage.py migrate
```

Create an administrator account for Wagtail:

```bash
pipenv run python manage.py createsuperuser
```

Start the development server:

```bash
pipenv run python manage.py runserver
```

Open the website at <http://127.0.0.1:8000/> and the Wagtail admin at <http://127.0.0.1:8000/admin/>.

> These instructions assume the repository includes the required Pipenv files and migrations. If dependencies are managed differently in the current checkout, follow the files committed to the repository.

## Content Management

Website content is managed through Wagtail. The current models support homepage content, project pages, an article index, article pages, images, URLs, and tags.

## Contact

**Sina Lalehbakhsh**

- Email: <mailto:sinalalehbakhsh@gmail.com>
- Phone: [+98 912 650 7649](tel:+989126507649)
- LinkedIn: <https://www.linkedin.com/in/sina-lalebakhsh/>
- GitHub: <https://github.com/sinalalebakhsh>
- YouTube — Main channel: <https://www.youtube.com/@sinalalehbakhsh>
- YouTube — Second channel: <https://www.youtube.com/@sinalalebakhsh>

For professional opportunities, collaborations, or questions about the project, please use one of the contact links above.

## Project Status

This is an evolving personal website project. Features and content may change as development continues.

## License

No license has been specified yet. Unless a license file is added to the repository, all rights are reserved by the copyright holder and reuse, redistribution, or modification should not be assumed to be permitted.
