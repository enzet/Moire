"""Moire plugin system.

Plugins allow extending Moire with custom tags without subclassing formatter
classes. Plugins are discovered automatically via Python entry points.

To create a plugin:

1. Create a class inheriting from ``MoirePlugin``::

    from moire.plugin import MoirePlugin

    class MyPlugin(MoirePlugin):
        def my_tag(self, fmt, arg):
            return f"custom: {fmt.parse(arg[0])}"

        def my_tag__html(self, fmt, arg):
            return f'<div class="custom">{fmt.parse(arg[0])}</div>'

2. Register it as an entry point in your ``pyproject.toml``::

    [project.entry-points."moire.plugins"]
    my-plugin = "my_package.plugin:MyPlugin"

3. Install your package. The ``moire`` CLI will discover and use the
   plugin automatically.

Tag methods receive the formatter instance (``fmt``) and an ``Argument``
object (``arg``), and return a string. For format-specific implementations,
append ``__<format_id>`` to the method name. The lookup order is:

1. ``tag__<format_id>`` (format-specific)
2. ``tag`` (generic fallback)

For header tags (``\\1`` through ``\\6``), define a ``header`` method that
accepts an additional ``level`` parameter::

    def header(self, fmt, arg, level):
        return f"{'#' * level} {fmt.parse(arg[0])}"
"""

from __future__ import annotations

import logging
from importlib.metadata import entry_points
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Callable

    from moire.moire import Moire

__author__: str = "Sergey Vartanov"
__email__: str = "me@enzet.ru"

logger: logging.Logger = logging.getLogger(__name__)

ENTRY_POINT_GROUP: str = "moire.plugins"


class MoirePlugin:
    """Base class for Moire plugins.

    Define methods named after tags. Each method receives the formatter
    instance and an :class:`~moire.moire.Argument` object::

        def my_tag(self, fmt: Moire, arg: Argument) -> str:
            return fmt.parse(arg[0])

    For format-specific implementations, append ``__<format_id>`` to the
    method name::

        def my_tag__html(self, fmt: Moire, arg: Argument) -> str:
            return f"<div>{fmt.parse(arg[0])}</div>"
    """


def discover_plugins() -> list[MoirePlugin]:
    """Discover and instantiate plugins registered via entry points."""
    plugins: list[MoirePlugin] = []
    eps = entry_points(group=ENTRY_POINT_GROUP)

    for ep in eps:
        try:
            plugin_obj: Any = ep.load()
            if isinstance(plugin_obj, type) and issubclass(
                plugin_obj, MoirePlugin
            ):
                plugins.append(plugin_obj())
            else:
                logger.warning(
                    "Entry point `%s` is not a MoirePlugin subclass.",
                    ep.name,
                )
        except Exception:
            logger.exception("Failed to load plugin `%s`.", ep.name)

    return plugins


def get_plugin_method(
    plugins: list[MoirePlugin],
    tag_name: str,
    format_id: str,
) -> tuple[MoirePlugin, Callable[..., str]] | None:
    """Find a plugin method for the given tag and format.

    Lookup order:
    1. ``tag_name__format_id`` (format-specific)
    2. ``tag_name`` (generic fallback)

    :returns: ``(plugin_instance, bound_method)`` or ``None``.
    """
    # First pass: format-specific method.
    format_key: str = f"{tag_name}__{format_id}"
    for plugin in plugins:
        method: Callable[..., str] | None = getattr(plugin, format_key, None)
        if method is not None:
            return plugin, method

    # Second pass: generic method.
    for plugin in plugins:
        method = getattr(plugin, tag_name, None)
        if method is not None and not tag_name.startswith("_"):
            return plugin, method

    return None
