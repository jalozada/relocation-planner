"""Shared fixtures for browser-based end-to-end tests."""

import os

import pytest


os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")


@pytest.fixture
def app_url(live_server):
    """Return the base URL for the Django live test server."""
    return live_server.url
