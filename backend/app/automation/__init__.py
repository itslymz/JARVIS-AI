"""Automation package."""

from app.automation.windows_control import WindowsControl
from app.automation.browser import BrowserAutomation

__all__ = [
    "WindowsControl",
    "BrowserAutomation",
]
