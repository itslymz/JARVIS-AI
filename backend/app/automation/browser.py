"""Browser automation with Playwright."""

from typing import Optional, List, Dict, Any
from playwright.async_api import (
    async_playwright,
    Browser,
    BrowserContext,
    Page,
    Locator,
)
import asyncio


class BrowserAutomation:
    """Browser automation using Playwright.
    
    Supports Chrome, Firefox, and WebKit browsers.
    """

    def __init__(self, browser_type: str = "chromium", headless: bool = False):
        """Initialize browser automation.
        
        Args:
            browser_type: Browser type (chromium, firefox, webkit)
            headless: Run in headless mode
        """
        self.browser_type = browser_type
        self.headless = headless
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    async def start(self) -> bool:
        """Start browser session.
        
        Returns:
            True if successful
        """
        try:
            self.playwright = await async_playwright().start()
            
            if self.browser_type == "chromium":
                self.browser = await self.playwright.chromium.launch(
                    headless=self.headless
                )
            elif self.browser_type == "firefox":
                self.browser = await self.playwright.firefox.launch(
                    headless=self.headless
                )
            elif self.browser_type == "webkit":
                self.browser = await self.playwright.webkit.launch(
                    headless=self.headless
                )
            else:
                raise ValueError(f"Unknown browser type: {self.browser_type}")
            
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
            return True
        except Exception as e:
            print(f"Failed to start browser: {e}")
            return False

    async def stop(self) -> bool:
        """Stop browser session.
        
        Returns:
            True if successful
        """
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            return True
        except Exception as e:
            print(f"Failed to stop browser: {e}")
            return False

    # Navigation

    async def goto(self, url: str, wait_until: str = "networkidle") -> bool:
        """Navigate to URL.
        
        Args:
            url: URL to navigate to
            wait_until: Wait strategy (load, domcontentloaded, networkidle)
            
        Returns:
            True if successful
        """
        try:
            if not self.page:
                return False
            await self.page.goto(url, wait_until=wait_until)
            return True
        except Exception as e:
            print(f"Failed to navigate: {e}")
            return False

    async def go_back(self) -> bool:
        """Go back to previous page.
        
        Returns:
            True if successful
        """
        try:
            if not self.page:
                return False
            await self.page.go_back()
            return True
        except Exception as e:
            print(f"Failed to go back: {e}")
            return False

    async def go_forward(self) -> bool:
        """Go forward to next page.
        
        Returns:
            True if successful
        """
        try:
            if not self.page:
                return False
            await self.page.go_forward()
            return True
        except Exception as e:
            print(f"Failed to go forward: {e}")
            return False

    async def reload(self) -> bool:
        """Reload current page.
        
        Returns:
            True if successful
        """
        try:
            if not self.page:
                return False
            await self.page.reload()
            return True
        except Exception as e:
            print(f"Failed to reload: {e}")
            return False

    # Interaction

    async def click(self, selector: str) -> bool:
        """Click element by selector.
        
        Args:
            selector: CSS selector
            
        Returns:
            True if successful
        """
        try:
            if not self.page:
                return False
            await self.page.click(selector)
            return True
        except Exception as e:
            print(f"Failed to click: {e}")
            return False

    async def fill(self, selector: str, text: str) -> bool:
        """Fill input field.
        
        Args:
            selector: CSS selector
            text: Text to fill
            
        Returns:
            True if successful
        """
        try:
            if not self.page:
                return False
            await self.page.fill(selector, text)
            return True
        except Exception as e:
            print(f"Failed to fill input: {e}")
            return False

    async def type_text(self, selector: str, text: str, delay: int = 50) -> bool:
        """Type text slowly (character by character).
        
        Args:
            selector: CSS selector
            text: Text to type
            delay: Delay between keystrokes in ms
            
        Returns:
            True if successful
        """
        try:
            if not self.page:
                return False
            await self.page.locator(selector).type(text, delay=delay)
            return True
        except Exception as e:
            print(f"Failed to type text: {e}")
            return False

    async def select_option(self, selector: str, value: str) -> bool:
        """Select option in dropdown.
        
        Args:
            selector: CSS selector
            value: Option value
            
        Returns:
            True if successful
        """
        try:
            if not self.page:
                return False
            await self.page.select_option(selector, value)
            return True
        except Exception as e:
            print(f"Failed to select option: {e}")
            return False

    async def check_checkbox(self, selector: str) -> bool:
        """Check checkbox.
        
        Args:
            selector: CSS selector
            
        Returns:
            True if successful
        """
        try:
            if not self.page:
                return False
            await self.page.check(selector)
            return True
        except Exception as e:
            print(f"Failed to check checkbox: {e}")
            return False

    async def uncheck_checkbox(self, selector: str) -> bool:
        """Uncheck checkbox.
        
        Args:
            selector: CSS selector
            
        Returns:
            True if successful
        """
        try:
            if not self.page:
                return False
            await self.page.uncheck(selector)
            return True
        except Exception as e:
            print(f"Failed to uncheck checkbox: {e}")
            return False

    # Content Extraction

    async def get_text(self, selector: str) -> Optional[str]:
        """Get text content of element.
        
        Args:
            selector: CSS selector
            
        Returns:
            Text content or None
        """
        try:
            if not self.page:
                return None
            return await self.page.locator(selector).text_content()
        except Exception as e:
            print(f"Failed to get text: {e}")
            return None

    async def get_attribute(self, selector: str, name: str) -> Optional[str]:
        """Get attribute of element.
        
        Args:
            selector: CSS selector
            name: Attribute name
            
        Returns:
            Attribute value or None
        """
        try:
            if not self.page:
                return None
            return await self.page.locator(selector).get_attribute(name)
        except Exception as e:
            print(f"Failed to get attribute: {e}")
            return None

    async def get_html(self, selector: Optional[str] = None) -> Optional[str]:
        """Get HTML content.
        
        Args:
            selector: Optional CSS selector for element HTML
            
        Returns:
            HTML content or None
        """
        try:
            if not self.page:
                return None
            if selector:
                return await self.page.locator(selector).inner_html()
            else:
                return await self.page.content()
        except Exception as e:
            print(f"Failed to get HTML: {e}")
            return None

    async def get_page_title(self) -> Optional[str]:
        """Get page title.
        
        Returns:
            Page title or None
        """
        try:
            if not self.page:
                return None
            return self.page.title()
        except Exception as e:
            print(f"Failed to get title: {e}")
            return None

    async def get_current_url(self) -> Optional[str]:
        """Get current URL.
        
        Returns:
            Current URL or None
        """
        try:
            if not self.page:
                return None
            return self.page.url
        except Exception as e:
            print(f"Failed to get URL: {e}")
            return None

    # Screenshots & PDFs

    async def take_screenshot(self, filepath: str) -> bool:
        """Take screenshot of page.
        
        Args:
            filepath: Path to save screenshot
            
        Returns:
            True if successful
        """
        try:
            if not self.page:
                return False
            await self.page.screenshot(path=filepath)
            return True
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
            return False

    async def save_pdf(self, filepath: str) -> bool:
        """Save page as PDF.
        
        Args:
            filepath: Path to save PDF
            
        Returns:
            True if successful
        """
        try:
            if not self.page:
                return False
            await self.page.pdf(path=filepath)
            return True
        except Exception as e:
            print(f"Failed to save PDF: {e}")
            return False

    # Wait Methods

    async def wait_for_selector(self, selector: str, timeout: int = 30000) -> bool:
        """Wait for element to appear.
        
        Args:
            selector: CSS selector
            timeout: Timeout in milliseconds
            
        Returns:
            True if element appeared
        """
        try:
            if not self.page:
                return False
            await self.page.wait_for_selector(selector, timeout=timeout)
            return True
        except Exception as e:
            print(f"Failed to wait for selector: {e}")
            return False

    async def wait_for_url(self, url_pattern: str, timeout: int = 30000) -> bool:
        """Wait for URL to match pattern.
        
        Args:
            url_pattern: URL pattern
            timeout: Timeout in milliseconds
            
        Returns:
            True if URL matched
        """
        try:
            if not self.page:
                return False
            await self.page.wait_for_url(url_pattern, timeout=timeout)
            return True
        except Exception as e:
            print(f"Failed to wait for URL: {e}")
            return False

    async def wait_for_load_state(self, state: str = "networkidle", timeout: int = 30000) -> bool:
        """Wait for page load state.
        
        Args:
            state: Load state (load, domcontentloaded, networkidle)
            timeout: Timeout in milliseconds
            
        Returns:
            True if state reached
        """
        try:
            if not self.page:
                return False
            await self.page.wait_for_load_state(state, timeout=timeout)
            return True
        except Exception as e:
            print(f"Failed to wait for load state: {e}")
            return False
