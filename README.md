# Relocation Planner

Open-source, local-first relocation planning platform.

## Running browser tests

Browser tests use `pytest`, `pytest-django`, and `pytest-playwright` with Django's
`live_server` fixture.

Install the Chromium browser used by Playwright:

```bash
uv run playwright install chromium
```

Run the browser tests:

```bash
uv run pytest tests/e2e --browser chromium
```
