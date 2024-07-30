"""
Tests for Markdown.
"""

from textwrap import dedent

from moire.default import DefaultMarkdown

__author__ = "Sergey Vartanov"
__email__ = "me@enzet.ru"


converter: DefaultMarkdown = DefaultMarkdown()


def check(code: str, result: str):
    assert converter.convert(code, wrap=False) == result


def test_markdown() -> None:
    check("\\m {text}", "`text`")


def test_markdown_list() -> None:
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
