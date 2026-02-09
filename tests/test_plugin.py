"""Tests for the Moire plugin system."""

from moire.default import DefaultHTML, DefaultMarkdown
from moire.moire import Argument
from moire.plugin import MoirePlugin, get_plugin_method


class GreetPlugin(MoirePlugin):
    """Test plugin with a simple tag."""

    def greet(self, fmt: DefaultHTML, arg: Argument) -> str:
        """Greet tag for all formats."""
        return f"Hello, {fmt.parse(arg[0])}!"


class FormatSpecificPlugin(MoirePlugin):
    """Test plugin with format-specific tags."""

    def color(self, fmt: DefaultHTML, arg: Argument) -> str:
        """Default color handler."""
        return fmt.parse(arg[0])

    def color__html(self, fmt: DefaultHTML, arg: Argument) -> str:
        """HTML-specific color handler."""
        return f'<span style="color: {fmt.clear(arg[0])};"></span>'

    def color__markdown(self, fmt: DefaultMarkdown, arg: Argument) -> str:
        """Markdown-specific color handler."""
        return f"`{fmt.clear(arg[0])}`"


class HeaderPlugin(MoirePlugin):
    """Test plugin with header override."""

    def header(self, fmt: DefaultHTML, arg: Argument, level: int) -> str:
        """Custom header."""
        return f"[h{level}: {fmt.parse(arg[0])}]"


# --- get_plugin_method tests ---


def test_get_plugin_method_generic() -> None:
    """Test generic plugin method lookup."""
    plugin = GreetPlugin()
    result = get_plugin_method([plugin], "greet", "html")
    assert result is not None
    assert result[0] is plugin


def test_get_plugin_method_format_specific() -> None:
    """Test format-specific method takes priority."""
    plugin = FormatSpecificPlugin()
    result = get_plugin_method([plugin], "color", "html")
    assert result is not None
    _, method = result
    assert method.__name__ == "color__html"


def test_get_plugin_method_fallback() -> None:
    """Test fallback to generic when no format-specific method exists."""
    plugin = FormatSpecificPlugin()
    result = get_plugin_method([plugin], "color", "tex")
    assert result is not None
    _, method = result
    assert method.__name__ == "color"


def test_get_plugin_method_not_found() -> None:
    """Test None returned for unknown tags."""
    plugin = GreetPlugin()
    result = get_plugin_method([plugin], "unknown", "html")
    assert result is None


def test_get_plugin_method_skips_private() -> None:
    """Test that private methods are not matched."""
    plugin = GreetPlugin()
    result = get_plugin_method([plugin], "_internal", "html")
    assert result is None


# --- Integration tests ---


def test_plugin_tag_html() -> None:
    """Test plugin tag renders in HTML."""
    converter = DefaultHTML()
    converter.plugins = [GreetPlugin()]
    result = converter.convert(r"\greet{World}", wrap=False)
    assert result == "Hello, World!"


def test_plugin_tag_markdown() -> None:
    """Test plugin tag renders in Markdown."""
    converter = DefaultMarkdown()
    converter.plugins = [GreetPlugin()]
    result = converter.convert(r"\greet{World}", wrap=False)
    assert result == "Hello, World!"


def test_plugin_format_specific_html() -> None:
    """Test format-specific plugin method for HTML."""
    converter = DefaultHTML()
    converter.plugins = [FormatSpecificPlugin()]
    result = converter.convert(r"\color{red}", wrap=False)
    assert result == '<span style="color: red;"></span>'


def test_plugin_format_specific_markdown() -> None:
    """Test format-specific plugin method for Markdown."""
    converter = DefaultMarkdown()
    converter.plugins = [FormatSpecificPlugin()]
    result = converter.convert(r"\color{red}", wrap=False)
    assert result == "`red`"


def test_plugin_format_fallback() -> None:
    """Test generic fallback when no format-specific method exists."""
    from moire.default import DefaultTeX

    converter = DefaultTeX()
    converter.plugins = [FormatSpecificPlugin()]
    result = converter.convert(r"\color{red}", wrap=False)
    assert result == "red"


def test_plugin_header_does_not_override_builtin() -> None:
    """Test that built-in header takes precedence over plugin header."""
    converter = DefaultHTML()
    converter.plugins = [HeaderPlugin()]
    result = converter.convert(r"\2{Section}", wrap=False)
    # Built-in header wins over plugin.
    assert result == "<h2>Section</h2>"


def test_plugin_header_level_parameter() -> None:
    """Test plugin header receives the level parameter."""
    plugin = HeaderPlugin()
    plugins = [plugin]
    result = get_plugin_method(plugins, "header", "html")
    assert result is not None
    _, method = result
    # Verify the method is callable with level argument.
    from moire.moire import Argument

    arg = Argument([["Section"]], {})
    assert method(DefaultHTML(), arg, 2) == "[h2: Section]"


def test_plugin_does_not_override_builtin() -> None:
    """Test that built-in tags take precedence over plugins."""

    class OverridePlugin(MoirePlugin):
        def s(self, fmt: DefaultHTML, arg: Argument) -> str:
            return f"PLUGIN:{fmt.parse(arg[0])}"

    converter = DefaultHTML()
    converter.plugins = [OverridePlugin()]
    result = converter.convert(r"\s{text}", wrap=False)
    # Built-in <b> should win, not the plugin.
    assert result == "<b>text</b>"


def test_plugin_mixed_with_builtin() -> None:
    """Test plugin tags mixed with built-in tags."""
    converter = DefaultHTML()
    converter.plugins = [GreetPlugin()]
    result = converter.convert(r"\s{Hello} \greet{World}", wrap=False)
    assert result == "<b>Hello</b> Hello, World!"


def test_multiple_plugins() -> None:
    """Test multiple plugins coexist."""
    converter = DefaultHTML()
    converter.plugins = [GreetPlugin(), FormatSpecificPlugin()]
    result = converter.convert(
        r"\greet{World} \color{red}", wrap=False
    )
    assert result == 'Hello, World! <span style="color: red;"></span>'
