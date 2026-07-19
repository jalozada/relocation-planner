from django.urls import reverse
from playwright.sync_api import expect

from apps.core.models import (
    DocumentType,
    RelocationTemplate,
    RelocationTemplateDocument,
    RelocationTemplateTask,
)


def ensure_standard_relocation_template():
    """Create the template data needed by the browser tests."""
    document_type, _created = DocumentType.objects.get_or_create(name="Passport")
    template, _created = RelocationTemplate.objects.get_or_create(
        name="Standard Relocation",
        defaults={
            "description": "Browser test template.",
            "active": True,
        },
    )
    RelocationTemplateDocument.objects.get_or_create(
        template=template,
        document_type=document_type,
    )
    RelocationTemplateTask.objects.get_or_create(
        template=template,
        title="Review required documents",
    )


def test_create_project_shows_success_and_dashboard(page, app_url):
    """A project can be created through the browser UI."""
    project_name = "Browser Test Project"

    page.goto(f"{app_url}{reverse('core:project-list')}")
    page.get_by_role("link", name="New Project").first.click()

    page.get_by_label("Name").fill(project_name)
    page.get_by_label("Description").fill("Created by the Playwright browser test.")
    page.get_by_role("button", name="Save").click()

    expect(page.get_by_text("Project created successfully.")).to_be_visible()
    expect(page.get_by_role("heading", name=project_name)).to_be_visible()

    page.get_by_role("link", name="View Project").click()

    expect(page.get_by_role("heading", name=project_name)).to_be_visible()
    expect(page.locator("#main-content").get_by_role("link", name="Dashboard")).to_be_visible()
    expect(page.get_by_text("Created by the Playwright browser test.")).to_be_visible()


def test_create_project_from_template_populates_dashboard(page, app_url):
    """A project can be initialized from a relocation template in the browser."""
    project_name = "Browser Template Project"
    ensure_standard_relocation_template()

    page.goto(f"{app_url}{reverse('core:project-create')}")
    page.get_by_label("Name").fill(project_name)
    page.get_by_label("Description").fill("Created from the standard template.")
    page.get_by_label("Relocation template").select_option(label="Standard Relocation")
    page.get_by_role("button", name="Save").click()

    expect(page.get_by_text("Project created successfully.")).to_be_visible()
    expect(page.get_by_role("heading", name=project_name)).to_be_visible()

    page.get_by_role("link", name="View Project").click()

    expect(page.get_by_role("heading", name=project_name)).to_be_visible()
    expect(page.get_by_text("Passport")).to_be_visible()
    expect(page.get_by_text("Review required documents")).to_be_visible()


def test_create_project_milestone_updates_dashboard(page, app_url):
    """A milestone can be added to a project in the browser."""
    project_name = "Browser Milestone Project"
    milestone_title = "Arrive in destination city"

    page.goto(f"{app_url}{reverse('core:project-create')}")
    page.get_by_label("Name").fill(project_name)
    page.get_by_label("Description").fill("Project with a milestone.")
    page.get_by_role("button", name="Save").click()

    page.get_by_role("link", name="View Project").click()
    page.get_by_role("link", name="Add Milestone").click()

    page.get_by_label("Title").fill(milestone_title)
    page.get_by_label("Target date").fill("2026-08-15")
    page.get_by_label("Description").fill("Land and get settled.")
    page.get_by_role("button", name="Save").click()

    expect(page.get_by_text("Milestone added successfully.")).to_be_visible()
    expect(page.get_by_role("heading", name=milestone_title)).to_be_visible()

    page.get_by_role("link", name="Back to milestones").click()
    expect(page.get_by_text(milestone_title)).to_be_visible()

    page.locator("#main-content").get_by_role("link", name="Dashboard", exact=True).click()
    expect(page.get_by_text(milestone_title)).to_be_visible()
