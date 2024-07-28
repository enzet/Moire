"""
Tests for Markdown.
"""

from moire.default import DefaultMarkdown

__author__ = "Sergey Vartanov"
__email__ = "me@enzet.ru"


converter: DefaultMarkdown = DefaultMarkdown()


def check(code: str, result: str):
    assert converter.convert(code, wrap=False, in_block=False) == result


def test_markdown() -> None:
    check("\\m {text}", "`text`")
