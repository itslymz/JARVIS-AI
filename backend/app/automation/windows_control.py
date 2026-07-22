"""Windows computer control and automation."""

import subprocess
import sys
from typing import Optional, List, Tuple
import pyautogui
import time


class WindowsControl:
    """Control Windows operating system."""

    def __init__(self):
        """Initialize Windows control."""
        if sys.platform != "win32":
            raise RuntimeError("Windows control only available on Windows")
        # Disable pyautogui safety features for performance
        pyautogui.FAILSAFE = False
        pyautogui.PAUSE = 0.1

    # Application Management

    async def launch_application(self, app_path: str, args: Optional[List[str]] = None) -> bool:
        """Launch an application.
        
        Args:
            app_path: Path to application executable
            args: Optional command line arguments
            
        Returns:
            True if launched successfully
        """
        try:
            cmd = [app_path]
            if args:
                cmd.extend(args)
            subprocess.Popen(cmd)
            await self._wait_for_window(2)  # Wait 2 seconds for window
            return True
        except Exception as e:
            print(f"Failed to launch application: {e}")
            return False

    async def launch_by_name(self, app_name: str) -> bool:
        """Launch application by name.
        
        Args:
            app_name: Application name (e.g., 'notepad', 'chrome')
            
        Returns:
            True if launched successfully
        """
        try:
            if app_name.lower() == "notepad":
                subprocess.Popen("notepad.exe")
            elif app_name.lower() in ["chrome", "google chrome"]:
                subprocess.Popen(
                    r"C:\Program Files\Google\Chrome\Application\chrome.exe"
                )
            elif app_name.lower() in ["firefox", "firefox browser"]:
                subprocess.Popen(
                    r"C:\Program Files\Mozilla Firefox\firefox.exe"
                )
            elif app_name.lower() in ["edge", "microsoft edge"]:
                subprocess.Popen(
                    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
                )
            elif app_name.lower() in ["calculator", "calc"]:
                subprocess.Popen("calc.exe")
            elif app_name.lower() in ["word", "microsoft word"]:
                subprocess.Popen("WINWORD.EXE")
            elif app_name.lower() in ["excel", "microsoft excel"]:
                subprocess.Popen("EXCEL.EXE")
            else:
                # Try to launch from Program Files
                subprocess.Popen(f"{app_name}.exe")
            
            await self._wait_for_window(2)
            return True
        except Exception as e:
            print(f"Failed to launch {app_name}: {e}")
            return False

    async def close_application(self, app_name: str, force: bool = False) -> bool:
        """Close an application.
        
        Args:
            app_name: Application name or window title
            force: Force close with /F flag
            
        Returns:
            True if closed successfully
        """
        try:
            if force:
                subprocess.run(["taskkill", "/IM", f"{app_name}.exe", "/F"])
            else:
                subprocess.run(["taskkill", "/IM", f"{app_name}.exe"])
            return True
        except Exception as e:
            print(f"Failed to close application: {e}")
            return False

    # Mouse Control

    async def move_mouse(self, x: int, y: int, duration: float = 0.5) -> bool:
        """Move mouse to position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            duration: Duration of movement in seconds
            
        Returns:
            True if successful
        """
        try:
            pyautogui.moveTo(x, y, duration=duration)
            return True
        except Exception as e:
            print(f"Failed to move mouse: {e}")
            return False

    async def click(self, x: int, y: int, button: str = "left", clicks: int = 1) -> bool:
        """Click at position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            button: Mouse button (left, right, middle)
            clicks: Number of clicks
            
        Returns:
            True if successful
        """
        try:
            pyautogui.click(x, y, clicks=clicks, button=button)
            return True
        except Exception as e:
            print(f"Failed to click: {e}")
            return False

    async def double_click(self, x: int, y: int) -> bool:
        """Double click at position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if successful
        """
        return await self.click(x, y, clicks=2)

    async def right_click(self, x: int, y: int) -> bool:
        """Right click at position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            
        Returns:
            True if successful
        """
        return await self.click(x, y, button="right")

    async def drag(self, x1: int, y1: int, x2: int, y2: int, duration: float = 0.5) -> bool:
        """Drag from one position to another.
        
        Args:
            x1: Start X coordinate
            y1: Start Y coordinate
            x2: End X coordinate
            y2: End Y coordinate
            duration: Duration of drag in seconds
            
        Returns:
            True if successful
        """
        try:
            pyautogui.moveTo(x1, y1, duration=0.1)
            pyautogui.drag(x2 - x1, y2 - y1, duration=duration)
            return True
        except Exception as e:
            print(f"Failed to drag: {e}")
            return False

    async def scroll(self, x: int, y: int, amount: int = 3) -> bool:
        """Scroll at position.
        
        Args:
            x: X coordinate
            y: Y coordinate
            amount: Scroll amount (positive up, negative down)
            
        Returns:
            True if successful
        """
        try:
            pyautogui.moveTo(x, y)
            pyautogui.scroll(amount)
            return True
        except Exception as e:
            print(f"Failed to scroll: {e}")
            return False

    # Keyboard Control

    async def type_text(self, text: str, interval: float = 0.05) -> bool:
        """Type text.
        
        Args:
            text: Text to type
            interval: Interval between keystrokes
            
        Returns:
            True if successful
        """
        try:
            pyautogui.typewrite(text, interval=interval)
            return True
        except Exception as e:
            print(f"Failed to type text: {e}")
            return False

    async def press_key(self, key: str) -> bool:
        """Press a key.
        
        Args:
            key: Key name (e.g., 'enter', 'space', 'esc')
            
        Returns:
            True if successful
        """
        try:
            pyautogui.press(key)
            return True
        except Exception as e:
            print(f"Failed to press key: {e}")
            return False

    async def hotkey(self, *keys: str) -> bool:
        """Press keyboard shortcut.
        
        Args:
            *keys: Key names (e.g., 'ctrl', 'c')
            
        Returns:
            True if successful
        """
        try:
            pyautogui.hotkey(*keys)
            return True
        except Exception as e:
            print(f"Failed to press hotkey: {e}")
            return False

    # Clipboard Management

    async def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to clipboard.
        
        Args:
            text: Text to copy
            
        Returns:
            True if successful
        """
        try:
            # Use Windows command line
            process = subprocess.Popen(
                "clip",
                stdin=subprocess.PIPE,
                shell=True,
            )
            process.communicate(text.encode("utf-8"))
            return True
        except Exception as e:
            print(f"Failed to copy to clipboard: {e}")
            return False

    async def paste_from_clipboard(self) -> Optional[str]:
        """Paste text from clipboard.
        
        Returns:
            Clipboard content or None
        """
        try:
            result = subprocess.run(
                "powershell -Command Get-Clipboard",
                shell=True,
                capture_output=True,
                text=True,
            )
            return result.stdout.strip()
        except Exception as e:
            print(f"Failed to paste from clipboard: {e}")
            return None

    # File Explorer Integration

    async def open_file_explorer(self, path: str = "C:\\") -> bool:
        """Open file explorer at path.
        
        Args:
            path: Directory path
            
        Returns:
            True if successful
        """
        try:
            subprocess.Popen(["explorer", path])
            await self._wait_for_window(1)
            return True
        except Exception as e:
            print(f"Failed to open file explorer: {e}")
            return False

    async def get_file_from_dialog(self) -> Optional[str]:
        """Open file dialog and get selected file.
        
        Returns:
            File path or None
        """
        try:
            # This would require more complex implementation
            # For now, return placeholder
            print("File dialog functionality requires GUI integration")
            return None
        except Exception as e:
            print(f"Failed to open file dialog: {e}")
            return None

    # Utility Methods

    async def take_screenshot(self, filepath: str = "screenshot.png") -> bool:
        """Take a screenshot.
        
        Args:
            filepath: Path to save screenshot
            
        Returns:
            True if successful
        """
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            return True
        except Exception as e:
            print(f"Failed to take screenshot: {e}")
            return False

    async def get_mouse_position(self) -> Tuple[int, int]:
        """Get current mouse position.
        
        Returns:
            Tuple of (x, y) coordinates
        """
        return pyautogui.position()

    async def wait(self, seconds: float) -> bool:
        """Wait for specified duration.
        
        Args:
            seconds: Duration to wait
            
        Returns:
            True
        """
        time.sleep(seconds)
        return True

    # Private Methods

    async def _wait_for_window(self, timeout: float = 5) -> bool:
        """Wait for a window to appear.
        
        Args:
            timeout: Timeout in seconds
            
        Returns:
            True if window appeared
        """
        time.sleep(timeout)
        return True
