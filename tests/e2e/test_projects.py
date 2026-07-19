from django.urls import reverse
from playwright.sync_api import expect


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
    expect(page.get_by_role("link", name="Dashboard")).to_be_visible()
    expect(page.get_by_text("Created by the Playwright browser test.")).to_be_visible()
