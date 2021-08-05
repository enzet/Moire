"""
Tests for Moire markup parsing.
"""

from moire.default import DefaultHTML, DefaultRTF, DefaultTeX

__author__ = "Sergey Vartanov"
__email__ = "me@enzet.ru"


converter_html = DefaultHTML()


def check(converter, code: str, result: str, _):
    assert converter.convert(code, wrap=False) == result


def check_html(code: str, result: str, _):
    check(converter_html, code, result, _)


def check_rtf(code: str, result: str, _):
    check(converter_rtf, code, result, _)


def check_tex(code: str, result: str, _):
    check(converter_tex, code, result, _)


def test_html_text():
    check_html("plain text", "plain text", "Plain text")


def test_html_text_with_2_spaces():
    check_html("plain  text", "plain text", "Double space in plain text")


def test_html_spaces_around_text():
    check_html("  plain  text  ", " plain text ", "Spaces around plain text")


def test_html_tag() -> None:
    check_html("\\b{bold}", "<b>bold</b>", "Simple tag")


def test_html_tag_with_space() -> None:
    check_html("\\b {bold}", "<b>bold</b>", "Simple tag with space")


def test_html_tag_with_2_spaces() -> None:
    check_html("\\b  {bold}", "<b>bold</b>", "Simple tag with two spaces")


def test_html_tag_with_spaces_inside_parameter() -> None:
    check_html("\\b {  bold  }", "<b> bold </b>", "Simple tag with spaces")


def test_html_tag_with_text() -> None:
    check_html("\\b {bold}text", "<b>bold</b>text", "Simple tag and plain text")


def test_html_code_tag() -> None:
    check_html("\\code {code}", "<pre><tt>code</tt></pre>", "Verbatim")


def test_html_escaped_tag() -> None:
    check_html("\\\\b \\{\\}", "\\b {}", "Escaped tags")


def test_html_escaped_in_tag() -> None:
    check_html("\\b {\\}}", "<b>}</b>", "Escaped tags in tag")


def test_html_escaped_symbol() -> None:
    check_html("<&>", "&lt;&amp;&gt;", "Escaped symbols")


def test_html_escaped_symbol_2() -> None:
    check_html("&nbsp;", "&amp;nbsp;", "Escaped")


def test_html_text_around_tag() -> None:
    check_html("text\\b {bold}text", "text<b>bold</b>text", "Text around tag")


def test_html_2_tags() -> None:
    check_html("\\b{bold}\\i{italic}", "<b>bold</b><i>italic</i>", "Two tags")


def test_html_n14() -> None:
    check_html(
        "\\code {<&>&nbsp;}",
        "<pre><tt>&lt;&amp;&gt;&amp;nbsp;</tt></pre>",
        "Escaped in code",
    )


def test_html_tag_with_text_and_space() -> None:
    check_html(
        "\\b {bold} text",
        "<b>bold</b> text",
        "Simple tag and plain text with space",
    )


def test_html_text_around_tag_and_spaces() -> None:
    check_html(
        "text \\b {bold} text",
        "text <b>bold</b> text",
        "Text around tag with spaces",
    )


def test_html_nested_tags_and_spaces() -> None:
    check_html(
        "\\block {a\n\nt \\m {tt} t\n\na}",
        "<p>a</p><p>t <tt>tt</tt> t</p><p>a</p>",
        "Text around two tags with spaces",
    )


def test_html_nested_tags_and_spaces_around() -> None:
    check_html(
        "\\block {a\n\n t \\m {tt} t \n\na}",
        "<p>a</p><p>t <tt>tt</tt> t</p><p>a</p>",
        "Text around two tags with spaces",
    )


def test_html_nested_tags_and_multiple_spaces() -> None:
    check_html(
        "\\block {a\n\n t  \\m {tt}  t \n\na}",
        "<p>a</p><p>t <tt>tt</tt> t</p><p>a</p>",
        "Text around two tags with spaces",
    )


def test_html_2_tags_and_space() -> None:
    check_html(
        "\\b{bold} \\i{italic}",
        "<b>bold</b> <i>italic</i>",
        "Two tags with space",
    )


def test_html_nested_tags() -> None:
    check_html(
        "\\b{\\i{bold italic}}",
        "<b><i>bold italic</i></b>",
        "Tag inside tag",
    )


def test_html_tag_with_2_parameters() -> None:
    check_html(
        "\\ref{link}{text}",
        '<a href="link">text</a>',
        "Tag with multiple parameters",
    )


def test_html_text_around_tag_with_2_parameters() -> None:
    check_html(
        "text \\ref{link}{text} text",
        'text <a href="link">text</a> text',
        "Text around tag with multiple parameters",
    )


def test_html_text_around_tag_with_2_parameters_and_spaces() -> None:
    check_html(
        "text \\ref {link} {text} text",
        'text <a href="link">text</a> text',
        "Text around tag with multiple parameters",
    )


def test_html_tag_2_parameters_with_spaces() -> None:
    check_html(
        "\\ref {  link  } {  text  }",
        '<a href="  link  "> text </a>',
        "Tag with multiple parameters with spaces",
    )


def test_html_table_1_cell() -> None:
    check_html(
        "\\table{{td}}",
        "<table><tr><td><p>td</p></td></tr></table>",
        "Tag with nested parameters",
    )


def test_html_table_tag() -> None:
    check_html(
        "\\table{{\\i {td}}}",
        "<table><tr><td><p><i>td</i></p></td></tr></table>",
        "Tag in tag with nested parameters",
    )


def test_html_table_2_cells() -> None:
    check_html(
        "\\table{{td}{td}}",
        "<table><tr><td><p>td</p></td><td><p>td</p></td></tr></table>",
        "Tag with more nested parameters",
    )
