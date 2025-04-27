"""Tests for Markdown."""

from textwrap import dedent

from moire.default import DefaultMarkdown

__author__ = "Sergey Vartanov"
__email__ = "me@enzet.ru"


def check(code: str, result: str, is_html: bool = True) -> None:
    """Check the result of the conversion.

    :param code: Moire code
    :param result: expected result
    """
    assert DefaultMarkdown(is_html=is_html).convert(code, wrap=False) == result


def test_markdown_header() -> None:
    """Test headers."""
    check("\\1 {Header}", "# Header")
    check("\\6 {Header}", "###### Header")


def test_markdown_bold() -> None:
    """Test bold text."""
    check("\\b {text}", "**text**")


def test_markdown_italic() -> None:
    """Test italic text."""
    check("\\i {text}", "*text*")


def test_markdown_underline() -> None:
    """Test underline text."""
    check("\\u {text}", "<u>text</u>")


def test_markdown_underline_no_html() -> None:
    """Test underline text without HTML."""
    check("\\u {text}", "text", is_html=False)


def test_markdown_deleted() -> None:
    """Test deleted text."""
    check("\\del {text}", "<del>text</del>")


def test_markdown_deleted_no_html() -> None:
    """Test deleted text without HTML."""
    check("\\del {text}", "text", is_html=False)


def test_markdown_monospace() -> None:
    """Test monospace text."""
    check("\\m {text}", "`text`")


def test_markdown_small_caps() -> None:
    """Test small caps text."""
    check("\\sc {text}", '<span style="font-variant: small-caps;">text</span>')


def test_markdown_small_caps_no_html() -> None:
    """Test small caps text without HTML."""
    check("\\sc {text}", "text", is_html=False)


def test_markdown_subscript() -> None:
    """Test subscript text."""
    check("\\sub {text}", "<sub>text</sub>")


def test_markdown_subscript_no_html() -> None:
    """Test subscript text without HTML."""
    check("\\sub {text}", "text", is_html=False)


def test_markdown_superscript() -> None:
    """Test superscript text."""
    check("\\super {text}", "<sup>text</sup>")


def test_markdown_superscript_no_html() -> None:
    """Test superscript text without HTML."""
    check("\\super {text}", "text", is_html=False)


def test_markdown_list() -> None:
    """Test list."""
    check(
        "List: \\list {item 1,} {item 2.}",
        dedent(
            """\
            List: 
              * item 1,
              * item 2.
            """  # noqa: W291
        )[:-1],
    )
