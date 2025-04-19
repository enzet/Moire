"""Tests for Moire markup parsing."""

import pytest

from moire.default import DefaultHTML

__author__ = "Sergey Vartanov"
__email__ = "me@enzet.ru"


converter = DefaultHTML()


def check(code: str, result: str, message: str) -> None:
    """Check the result of the conversion.

    :param code: Moire code
    :param result: expected result
    :param message: test explanation
    """
    assert (
        converter.convert(code, wrap=False, in_block=False) == result
    ), message


def test_html_text() -> None:
    """Test plain text."""
    check("plain text", "plain text", "Plain text")


def test_html_text_with_2_spaces() -> None:
    """Test double space in plain text."""
    check("plain  text", "plain text", "Double space in plain text")


def test_html_spaces_around_text() -> None:
    """Test spaces around plain text."""
    check("  plain  text  ", " plain text ", "Spaces around plain text")


def test_html_tag() -> None:
    """Test simple tag."""
    check("\\b{bold}", "<b>bold</b>", "Simple tag")


def test_html_tag_with_space() -> None:
    """Test simple tag with space."""
    check("\\b {bold}", "<b>bold</b>", "Simple tag with space")


def test_html_tag_with_2_spaces() -> None:
    """Test simple tag with two spaces."""
    check("\\b  {bold}", "<b>bold</b>", "Simple tag with two spaces")


def test_html_tag_with_spaces_inside_parameter() -> None:
    """Test simple tag with spaces inside parameter."""
    check("\\b {  bold  }", "<b> bold </b>", "Simple tag with spaces")


def test_html_tag_with_text() -> None:
    """Test simple tag with text."""
    check("\\b {bold}text", "<b>bold</b>text", "Simple tag and plain text")


def test_html_code_tag() -> None:
    """Test verbatim tag."""
    check("\\code {code}", "<pre><tt>code</tt></pre>", "Verbatim")


def test_html_escaped_tag() -> None:
    """Test escaped tags."""
    check("\\\\b \\{\\}", "\\b {}", "Escaped tags")


def test_html_escaped_in_tag() -> None:
    """Test escaped tags in tag."""
    check("\\b {\\}}", "<b>}</b>", "Escaped tags in tag")


def test_html_escaped_symbol() -> None:
    """Test escaped symbols."""
    check("<&>", "&lt;&amp;&gt;", "Escaped symbols")


def test_html_escaped_symbol_2() -> None:
    """Test escaped symbol."""
    check("&nbsp;", "&amp;nbsp;", "Escaped symbol")


def test_html_text_around_tag() -> None:
    """Test text around tag."""
    check("text\\b {bold}text", "text<b>bold</b>text", "Text around tag")


def test_html_2_tags() -> None:
    """Test two tags."""
    check("\\b{bold}\\i{italic}", "<b>bold</b><i>italic</i>", "Two tags")


def test_html_n14() -> None:
    """Test escaped in code."""
    check(
        "\\code {<&>&nbsp;}",
        "<pre><tt>&lt;&amp;&gt;&amp;nbsp;</tt></pre>",
        "Escaped in code",
    )


def test_html_tag_with_text_and_space() -> None:
    """Test simple tag and plain text with space."""
    check(
        "\\b {bold} text",
        "<b>bold</b> text",
        "Simple tag and plain text with space",
    )


def test_html_text_around_tag_and_spaces() -> None:
    """Test text around tag with spaces."""
    check(
        "text \\b {bold} text",
        "text <b>bold</b> text",
        "Text around tag with spaces",
    )


def test_html_nested_tags_and_spaces() -> None:
    """Test text around two tags with spaces."""
    check(
        "\\block {a\n\nt \\m {tt} t\n\na}",
        "<p>a</p><p>t <code>tt</code> t</p><p>a</p>",
        "Text around two tags with spaces",
    )


def test_html_nested_tags_and_spaces_around() -> None:
    """Test text around two tags with spaces."""
    check(
        "\\block {a\n\n t \\m {tt} t \n\na}",
        "<p>a</p><p>t <code>tt</code> t</p><p>a</p>",
        "Text around two tags with spaces",
    )


def test_html_nested_tags_and_multiple_spaces() -> None:
    """Test text around two tags with multiple spaces."""
    check(
        "\\block {a\n\n t  \\m {tt}  t \n\na}",
        "<p>a</p><p>t <code>tt</code> t</p><p>a</p>",
        "Text around two tags with multiple spaces",
    )


def test_html_2_tags_and_space() -> None:
    """Test two tags with space."""
    check(
        "\\b{bold} \\i{italic}",
        "<b>bold</b> <i>italic</i>",
        "Two tags with space",
    )


def test_html_nested_tags() -> None:
    """Test tag inside tag."""
    check(
        "\\b{\\i{bold italic}}", "<b><i>bold italic</i></b>", "Tag inside tag"
    )


def test_html_tag_with_2_parameters() -> None:
    """Test tag with multiple parameters."""
    check(
        "\\ref{link}{text}",
        '<a href="link">text</a>',
        "Tag with multiple parameters",
    )


def test_html_text_around_tag_with_2_parameters() -> None:
    """Test text around tag with multiple parameters."""
    check(
        "text \\ref{link}{text} text",
        'text <a href="link">text</a> text',
        "Text around tag with multiple parameters",
    )


def test_html_text_around_tag_with_2_parameters_and_spaces() -> None:
    """Test text around tag with multiple parameters and spaces."""
    check(
        "text \\ref {link} {text} text",
        'text <a href="link">text</a> text',
        "Text around tag with multiple parameters and spaces",
    )


def test_html_tag_2_parameters_with_spaces() -> None:
    """Test tag with multiple parameters with spaces."""
    check(
        "\\ref {  link  } {  text  }",
        '<a href=" link "> text </a>',
        "Tag with multiple parameters with spaces",
    )


def test_html_table_1_cell() -> None:
    """Test tag with nested parameters."""
    check(
        "\\table{{td}}",
        "<table><tr><td><p>td</p></td></tr></table>",
        "Tag with nested parameters",
    )


def test_html_table_tag() -> None:
    """Test tag in tag with nested parameters."""
    check(
        "\\table{{\\i {td}}}",
        "<table><tr><td><p><i>td</i></p></td></tr></table>",
        "Tag in tag with nested parameters",
    )


def test_html_table_2_cells() -> None:
    """Test tag with more nested parameters."""
    check(
        "\\table{{td}{td}}",
        "<table><tr><td><p>td</p></td><td><p>td</p></td></tr></table>",
        "Tag with more nested parameters",
    )


@pytest.mark.skip(reason="Not implemented")
def test_html_table_with_wrong_data() -> None:
    """Test tag with incorrectly placed data."""
    check(
        "\\table data1{data2{td}data3{td}data4}",
        "<table><tr><td><p>td</p></td><td><p>td</p></td></tr></table>",
        "Tag with incorrectly placed data",
    )
