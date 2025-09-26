from __future__ import annotations

from .client import LspHtmlPlugin

__all__ = (
    # ST: core
    "plugin_loaded",
    "plugin_unloaded",
    # ST: commands
    # ST: listeners
    # ...
    "LspHtmlPlugin",
)


def plugin_loaded() -> None:
    """Executed when this plugin is loaded."""
    LspHtmlPlugin.setup()


def plugin_unloaded() -> None:
    """Executed when this plugin is unloaded."""
    LspHtmlPlugin.cleanup()
