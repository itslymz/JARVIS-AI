"""Unit tests for plugin manager."""

import pytest
from app.plugins.manager import (
    PluginManager,
    BasePlugin,
    PluginPermission,
    PluginStatus,
)


class MockPlugin(BasePlugin):
    """Mock plugin for testing."""

    @property
    def name(self) -> str:
        return "Mock Plugin"

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def description(self) -> str:
        return "Mock plugin for testing"

    async def initialize(self) -> bool:
        self.status = PluginStatus.ACTIVE
        return True

    async def execute(self, action: str, params):
        return {"action": action, "params": params}

    async def shutdown(self) -> bool:
        return True


@pytest.fixture
def plugin_manager():
    """Create plugin manager instance."""
    return PluginManager()


@pytest.mark.asyncio
async def test_grant_permission(plugin_manager):
    """Test granting permissions."""
    plugin = MockPlugin()
    plugin_manager.loaded_plugins[plugin.id] = plugin
    
    result = await plugin_manager.grant_permission(
        plugin.id,
        PluginPermission.FILESYSTEM_READ,
    )
    assert result is True


@pytest.mark.asyncio
async def test_has_permission(plugin_manager):
    """Test checking permissions."""
    plugin = MockPlugin()
    plugin_manager.loaded_plugins[plugin.id] = plugin
    
    await plugin_manager.grant_permission(
        plugin.id,
        PluginPermission.NETWORK,
    )
    
    has_permission = await plugin_manager.has_permission(
        plugin.id,
        PluginPermission.NETWORK,
    )
    assert has_permission is True


@pytest.mark.asyncio
async def test_revoke_permission(plugin_manager):
    """Test revoking permissions."""
    plugin = MockPlugin()
    plugin_manager.loaded_plugins[plugin.id] = plugin
    
    await plugin_manager.grant_permission(
        plugin.id,
        PluginPermission.SYSTEM,
    )
    
    result = await plugin_manager.revoke_permission(
        plugin.id,
        PluginPermission.SYSTEM,
    )
    assert result is True


@pytest.mark.asyncio
async def test_enable_disable_plugin(plugin_manager):
    """Test enabling and disabling plugins."""
    plugin = MockPlugin()
    plugin_manager.loaded_plugins[plugin.id] = plugin
    
    # Enable
    result = await plugin_manager.enable_plugin(plugin.id)
    assert result is True
    assert plugin.enabled is True
    
    # Disable
    result = await plugin_manager.disable_plugin(plugin.id)
    assert result is True
    assert plugin.enabled is False


@pytest.mark.asyncio
async def test_list_plugins(plugin_manager):
    """Test listing plugins."""
    plugin = MockPlugin()
    plugin_manager.loaded_plugins[plugin.id] = plugin
    
    plugins = await plugin_manager.list_plugins()
    assert len(plugins) == 1
    assert plugins[0]["name"] == "Mock Plugin"
