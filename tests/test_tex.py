"""Tests for Moire markup parsing."""

from moire.default import DefaultTeX

__author__ = "Sergey Vartanov"
__email__ = "me@enzet.ru"


converter: DefaultTeX = DefaultTeX()


def check(code: str, result: str) -> None:
    """Check the result of the conversion.

    :param code: Moire code
    :param result: expected result
    """
    assert converter.convert(code, wrap=False, in_block=False) == result


def test_tex_header() -> None:
    """Test header."""
    check("\\1 {header}", "\\section{header}")


def test_tex_bold() -> None:
    """Test bold."""
    check("\\b {text}", "{\\bf text}")


def test_tex_italic() -> None:
    """Test italic."""
    check("\\i {text}", "{\\em text}")


def test_tex_underscore() -> None:
    """Test underscore."""
    check("_", "\\_")
