"""
Tests for Moire markup parsing.
"""

from moire.default import DefaultTeX

__author__ = "Sergey Vartanov"
__email__ = "me@enzet.ru"


converter: DefaultTeX = DefaultTeX()


def check(code: str, result: str):
    assert converter.convert(code, wrap=False, in_block=False) == result


def test_tex() -> None:
    check("_", "\\_")
