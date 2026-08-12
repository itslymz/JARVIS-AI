"""Plugin framework for dynamic plugin loading and management."""

from typing import Optional, List, Dict, Any, Callable, Type
from pathlib import Path
from abc import ABC, abstractmethod
import importlib.util
import sys
import uuid
from datetime import datetime
from enum import Enum


class PluginPermission(str, Enum):
    """Plugin permissions enumeration."""
    FILESYSTEM_READ = "filesystem:read"
    FILESYSTEM_WRITE = "filesystem:write"
    NETWORK = "network:access"
    SYSTEM = "system:execute"
    MEMORY = "memory:access"
    CLIPBOARD = "clipboard:access"
    SCREEN = "screen:capture"


class PluginStatus(str, Enum):
    """Plugin status enumeration."""
    INACTIVE = "inactive"
    ACTIVE = "active"
    DISABLED = "disabled"
    ERROR = "error"


class BasePlugin(ABC):
    """Base class for all plugins."""

    def __init__(self):
        """Initialize plugin."""
        self.id = str(uuid.uuid4())
        self.status = PluginStatus.INACTIVE
        self.permissions: List[PluginPermission] = []
        self.enabled = False

    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize plugin.
        
        Returns:
            True if initialization successful
        """
        pass

    @abstractmethod
    async def execute(self, action: str, params: Dict[str, Any]) -> Any:
        """Execute plugin action.
        
        Args:
            action: Action name
            params: Action parameters
            
        Returns:
            Action result
        """
        pass

    @abstractmethod
    async def shutdown(self) -> bool:
        """Shutdown plugin.
        
        Returns:
            True if shutdown successful
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Get plugin name."""
        pass

    @property
    @abstractmethod
    def version(self) -> str:
        """Get plugin version."""
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        """Get plugin description."""
        pass


class PluginMetadata:
    """Plugin metadata information."""

    def __init__(
        self,
        name: str,
        version: str,
        description: str,
        author: str,
        permissions: Optional[List[PluginPermission]] = None,
    ):
        """Initialize plugin metadata.
        
        Args:
            name: Plugin name
            version: Plugin version
            description: Plugin description
            author: Plugin author
            permissions: Required permissions
        """
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.permissions = permissions or []
        self.created_at = datetime.utcnow()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "author": self.author,
            "permissions": [p.value for p in self.permissions],
            "created_at": self.created_at.isoformat(),
        }


class PluginManager:
    """Manages plugin loading, execution, and lifecycle."""

    def __init__(self, plugins_dir: str = "plugins"):
        """Initialize plugin manager.
        
        Args:
            plugins_dir: Directory containing plugins
        """
        self.plugins_dir = Path(plugins_dir)
        self.plugins_dir.mkdir(exist_ok=True)
        self.loaded_plugins: Dict[str, BasePlugin] = {}
        self.plugin_metadata: Dict[str, PluginMetadata] = {}
        self.granted_permissions: Dict[str, List[PluginPermission]] = {}

    async def load_plugin(self, plugin_path: str) -> Optional[BasePlugin]:
        """Load a plugin from file.
        
        Args:
            plugin_path: Path to plugin file
            
        Returns:
            Loaded plugin or None
        """
        try:
            path = Path(plugin_path)
            if not path.exists():
                print(f"Plugin file not found: {plugin_path}")
                return None

            # Load module
            spec = importlib.util.spec_from_file_location(path.stem, path)
            if not spec or not spec.loader:
                return None

            module = importlib.util.module_from_spec(spec)
            sys.modules[path.stem] = module
            spec.loader.exec_module(module)

            # Find BasePlugin subclass
            plugin_class: Optional[Type[BasePlugin]] = None
            for item_name in dir(module):
                item = getattr(module, item_name)
                if (
                    isinstance(item, type)
                    and issubclass(item, BasePlugin)
                    and item is not BasePlugin
                ):
                    plugin_class = item
                    break

            if not plugin_class:
                print(f"No plugin class found in {plugin_path}")
                return None

            # Instantiate plugin
            plugin = plugin_class()
            if not await plugin.initialize():
                print(f"Plugin initialization failed: {plugin.name}")
                return None

            self.loaded_plugins[plugin.id] = plugin
            return plugin

        except Exception as e:
            print(f"Failed to load plugin: {e}")
            return None

    async def unload_plugin(self, plugin_id: str) -> bool:
        """Unload a plugin.
        
        Args:
            plugin_id: Plugin ID
            
        Returns:
            True if unloaded successfully
        """
        if plugin_id not in self.loaded_plugins:
            return False

        try:
            plugin = self.loaded_plugins[plugin_id]
            await plugin.shutdown()
            del self.loaded_plugins[plugin_id]
            return True
        except Exception as e:
            print(f"Failed to unload plugin: {e}")
            return False

    async def enable_plugin(self, plugin_id: str) -> bool:
        """Enable a plugin.
        
        Args:
            plugin_id: Plugin ID
            
        Returns:
            True if enabled
        """
        if plugin_id not in self.loaded_plugins:
            return False

        plugin = self.loaded_plugins[plugin_id]
        plugin.enabled = True
        plugin.status = PluginStatus.ACTIVE
        return True

    async def disable_plugin(self, plugin_id: str) -> bool:
        """Disable a plugin.
        
        Args:
            plugin_id: Plugin ID
            
        Returns:
            True if disabled
        """
        if plugin_id not in self.loaded_plugins:
            return False

        plugin = self.loaded_plugins[plugin_id]
        plugin.enabled = False
        plugin.status = PluginStatus.DISABLED
        return True

    async def grant_permission(
        self,
        plugin_id: str,
        permission: PluginPermission,
    ) -> bool:
        """Grant permission to plugin.
        
        Args:
            plugin_id: Plugin ID
            permission: Permission to grant
            
        Returns:
            True if granted
        """
        if plugin_id not in self.loaded_plugins:
            return False

        if plugin_id not in self.granted_permissions:
            self.granted_permissions[plugin_id] = []

        if permission not in self.granted_permissions[plugin_id]:
            self.granted_permissions[plugin_id].append(permission)

        return True

    async def revoke_permission(
        self,
        plugin_id: str,
        permission: PluginPermission,
    ) -> bool:
        """Revoke permission from plugin.
        
        Args:
            plugin_id: Plugin ID
            permission: Permission to revoke
            
        Returns:
            True if revoked
        """
        if plugin_id not in self.granted_permissions:
            return False

        if permission in self.granted_permissions[plugin_id]:
            self.granted_permissions[plugin_id].remove(permission)
            return True

        return False

    async def has_permission(
        self,
        plugin_id: str,
        permission: PluginPermission,
    ) -> bool:
        """Check if plugin has permission.
        
        Args:
            plugin_id: Plugin ID
            permission: Permission to check
            
        Returns:
            True if plugin has permission
        """
        if plugin_id not in self.granted_permissions:
            return False
        return permission in self.granted_permissions[plugin_id]

    async def execute_plugin(
        self,
        plugin_id: str,
        action: str,
        params: Optional[Dict[str, Any]] = None,
    ) -> Optional[Any]:
        """Execute plugin action.
        
        Args:
            plugin_id: Plugin ID
            action: Action name
            params: Action parameters
            
        Returns:
            Action result or None
        """
        if plugin_id not in self.loaded_plugins:
            return None

        plugin = self.loaded_plugins[plugin_id]
        if not plugin.enabled:
            return None

        try:
            return await plugin.execute(action, params or {})
        except Exception as e:
            print(f"Plugin execution error: {e}")
            plugin.status = PluginStatus.ERROR
            return None

    async def list_plugins(self) -> List[Dict[str, Any]]:
        """List all loaded plugins.
        
        Returns:
            List of plugin information
        """
        return [
            {
                "id": plugin.id,
                "name": plugin.name,
                "version": plugin.version,
                "status": plugin.status.value,
                "enabled": plugin.enabled,
            }
            for plugin in self.loaded_plugins.values()
        ]

    async def get_plugin_info(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        """Get plugin information.
        
        Args:
            plugin_id: Plugin ID
            
        Returns:
            Plugin information or None
        """
        if plugin_id not in self.loaded_plugins:
            return None

        plugin = self.loaded_plugins[plugin_id]
        permissions = self.granted_permissions.get(plugin_id, [])

        return {
            "id": plugin.id,
            "name": plugin.name,
            "version": plugin.version,
            "description": plugin.description,
            "status": plugin.status.value,
            "enabled": plugin.enabled,
            "granted_permissions": [p.value for p in permissions],
        }
