"""Unit tests for Windows control."""

import pytest
import sys

if sys.platform == "win32":
    from app.automation.windows_control import WindowsControl

    @pytest.fixture
    def windows_control():
        """Create Windows control instance."""
        return WindowsControl()

    @pytest.mark.asyncio
    async def test_mouse_position(windows_control):
        """Test getting mouse position."""
        pos = await windows_control.get_mouse_position()
        assert isinstance(pos, tuple)
        assert len(pos) == 2

    @pytest.mark.asyncio
    async def test_wait(windows_control):
        """Test wait function."""
        import time
        start = time.time()
        await windows_control.wait(0.1)
        elapsed = time.time() - start
        assert elapsed >= 0.1

    @pytest.mark.asyncio
    async def test_hotkey(windows_control):
        """Test hotkey press."""
        # Just test it doesn't crash
        result = await windows_control.press_key("space")
        assert result is True

else:
    # Skip tests on non-Windows systems
    pytestmark = pytest.mark.skip(reason="Windows only")
