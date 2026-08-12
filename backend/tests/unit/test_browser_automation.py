"""Unit tests for browser automation."""

import pytest
from app.automation.browser import BrowserAutomation


@pytest.fixture
async def browser():
    """Create browser instance."""
    b = BrowserAutomation(headless=True)
    await b.start()
    yield b
    await b.stop()


@pytest.mark.asyncio
async def test_browser_start(browser):
    """Test browser startup."""
    assert browser.browser is not None
    assert browser.page is not None


@pytest.mark.asyncio
async def test_navigate(browser):
    """Test navigation to URL."""
    result = await browser.goto("https://example.com")
    assert result is True


@pytest.mark.asyncio
async def test_get_title(browser):
    """Test getting page title."""
    await browser.goto("https://example.com")
    title = await browser.get_page_title()
    assert title is not None
    assert len(title) > 0


@pytest.mark.asyncio
async def test_get_url(browser):
    """Test getting current URL."""
    await browser.goto("https://example.com")
    url = await browser.get_current_url()
    assert url is not None
    assert "example.com" in url
