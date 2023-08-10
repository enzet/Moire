"""
Tests for Moire markup parsing.
"""

from moire.default import DefaultHTML

__author__ = "Sergey Vartanov"
__email__ = "me@enzet.ru"


converter = DefaultHTML()


def check(code: str, result: str, message: str):
    assert converter.convert(code, wrap=False) == result, message


def test_html_text():
    check("plain text", "plain text", "Plain text")


def test_html_text_with_2_spaces():
    check("plain  text", "plain text", "Double space in plain text")


def test_html_spaces_around_text():
    check("  plain  text  ", " plain text ", "Spaces around plain text")


def test_html_tag() -> None:
    check("\\b{bold}", "<b>bold</b>", "Simple tag")


def test_html_tag_with_space() -> None:
    check("\\b {bold}", "<b>bold</b>", "Simple tag with space")


def test_html_tag_with_2_spaces() -> None:
    check("\\b  {bold}", "<b>bold</b>", "Simple tag with two spaces")


def test_html_tag_with_spaces_inside_parameter() -> None:
    check("\\b {  bold  }", "<b> bold </b>", "Simple tag with spaces")


def test_html_tag_with_text() -> None:
    check("\\b {bold}text", "<b>bold</b>text", "Simple tag and plain text")


def test_html_code_tag() -> None:
    check("\\code {code}", "<pre><tt>code</tt></pre>", "Verbatim")


def test_html_escaped_tag() -> None:
    check("\\\\b \\{\\}", "\\b {}", "Escaped tags")


def test_html_escaped_in_tag() -> None:
    check("\\b {\\}}", "<b>}</b>", "Escaped tags in tag")


def test_html_escaped_symbol() -> None:
    check("<&>", "&lt;&amp;&gt;", "Escaped symbols")


def test_html_escaped_symbol_2() -> None:
    check("&nbsp;", "&amp;nbsp;", "Escaped")


def test_html_text_around_tag() -> None:
    check("text\\b {bold}text", "text<b>bold</b>text", "Text around tag")


def test_html_2_tags() -> None:
    check("\\b{bold}\\i{italic}", "<b>bold</b><i>italic</i>", "Two tags")


def test_html_n14() -> None:
    check(
        "\\code {<&>&nbsp;}",
        "<pre><tt>&lt;&amp;&gt;&amp;nbsp;</tt></pre>",
        "Escaped in code",
    )


def test_html_tag_with_text_and_space() -> None:
    check(
        "\\b {bold} text",
        "<b>bold</b> text",
        "Simple tag and plain text with space",
    )


def test_html_text_around_tag_and_spaces() -> None:
    check(
        "text \\b {bold} text",
        "text <b>bold</b> text",
        "Text around tag with spaces",
    )


def test_html_nested_tags_and_spaces() -> None:
    check(
        "\\block {a\n\nt \\m {tt} t\n\na}",
        "<p>a</p><p>t <code>tt</code> t</p><p>a</p>",
        "Text around two tags with spaces",
    )


def test_html_nested_tags_and_spaces_around() -> None:
    check(
        "\\block {a\n\n t \\m {tt} t \n\na}",
        "<p>a</p><p>t <code>tt</code> t</p><p>a</p>",
        "Text around two tags with spaces",
    )


def test_html_nested_tags_and_multiple_spaces() -> None:
    check(
        "\\block {a\n\n t  \\m {tt}  t \n\na}",
        "<p>a</p><p>t <code>tt</code> t</p><p>a</p>",
        "Text around two tags with spaces",
    )


def test_html_2_tags_and_space() -> None:
    check(
        "\\b{bold} \\i{italic}",
        "<b>bold</b> <i>italic</i>",
        "Two tags with space",
    )


def test_html_nested_tags() -> None:
    check(
        "\\b{\\i{bold italic}}",
        "<b><i>bold italic</i></b>",
        "Tag inside tag",
    )


def test_html_tag_with_2_parameters() -> None:
    check(
        "\\ref{link}{text}",
        '<a href="link">text</a>',
        "Tag with multiple parameters",
    )


def test_html_text_around_tag_with_2_parameters() -> None:
    check(
        "text \\ref{link}{text} text",
        'text <a href="link">text</a> text',
        "Text around tag with multiple parameters",
    )


def test_html_text_around_tag_with_2_parameters_and_spaces() -> None:
    check(
        "text \\ref {link} {text} text",
        'text <a href="link">text</a> text',
        "Text around tag with multiple parameters",
    )


def test_html_tag_2_parameters_with_spaces() -> None:
    check(
        "\\ref {  link  } {  text  }",
        '<a href="  link  "> text </a>',
        "Tag with multiple parameters with spaces",
    )


def test_html_table_1_cell() -> None:
    check(
        "\\table{{td}}",
        "<table><tr><td><p>td</p></td></tr></table>",
        "Tag with nested parameters",
    )


def test_html_table_tag() -> None:
    check(
        "\\table{{\\i {td}}}",
        "<table><tr><td><p><i>td</i></p></td></tr></table>",
        "Tag in tag with nested parameters",
    )


def test_html_table_2_cells() -> None:
    check(
        "\\table{{td}{td}}",
        "<table><tr><td><p>td</p></td><td><p>td</p></td></tr></table>",
        "Tag with more nested parameters",
    )


def __test_html_table_with_wrong_data() -> None:
    check(
        "\\table data1{data2{td}data3{td}data4}",
        "<table><tr><td><p>td</p></td><td><p>td</p></td></tr></table>",
        "Tag with incorrectly placed data",
    )
