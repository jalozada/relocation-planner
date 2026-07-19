from playwright.sync_api import expect


def test_homepage_loads(page, app_url):
    """The homepage loads in Chromium."""
    page.goto(app_url)

    expect(page).to_have_title("Home | Relocation Planner")
    expect(page.get_by_role("heading", name="Relocation Planner")).to_be_visible()
