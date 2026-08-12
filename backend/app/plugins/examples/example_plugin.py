"""Example plugin demonstrating the plugin API."""

from typing import Dict, Any
from app.plugins.manager import BasePlugin, PluginPermission


class ExamplePlugin(BasePlugin):
    """Example plugin."""

    @property
    def name(self) -> str:
        """Get plugin name."""
        return "Example Plugin"

    @property
    def version(self) -> str:
        """Get plugin version."""
        return "1.0.0"

    @property
    def description(self) -> str:
        """Get plugin description."""
        return "Example plugin demonstrating the plugin API"

    async def initialize(self) -> bool:
        """Initialize plugin.
        
        Returns:
            True if initialization successful
        """
        print(f"Initializing {self.name}")
        self.permissions = [
            PluginPermission.FILESYSTEM_READ,
            PluginPermission.NETWORK,
        ]
        return True

    async def execute(self, action: str, params: Dict[str, Any]) -> Any:
        """Execute plugin action.
        
        Args:
            action: Action name
            params: Action parameters
            
        Returns:
            Action result
        """
        if action == "greet":
            name = params.get("name", "World")
            return {"message": f"Hello, {name}!"}
        elif action == "add":
            a = params.get("a", 0)
            b = params.get("b", 0)
            return {"result": a + b}
        else:
            return {"error": f"Unknown action: {action}"}

    async def shutdown(self) -> bool:
        """Shutdown plugin.
        
        Returns:
            True if shutdown successful
        """
        print(f"Shutting down {self.name}")
        return True
