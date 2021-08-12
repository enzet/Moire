"""
Tests for RTF.
"""

from moire.default import DefaultRTF

__author__ = "Sergey Vartanov"
__email__ = "me@enzet.ru"


converter: DefaultRTF = DefaultRTF()


def check(code: str, result: str):
    assert converter.convert(code, wrap=False) == result


def test_rtf() -> None:
    check("АБВ", "\\u1040  \\u1041  \\u1042  ")
