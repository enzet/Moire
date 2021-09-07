from moire.moire import Moire, Tag
from typing import Any


converter: Moire = Moire()


def check(moire_code: str, intermediate_representation: Any) -> None:
    assert converter.get_ir(moire_code) == intermediate_representation


def test_text() -> None:
    check("text", ["text"])


def test_tag() -> None:
    check("\\tag{text}", [Tag("tag", [["text"]])])


def test_text_and_tag() -> None:
    check("\\tag{text}text", [Tag("tag", [["text"]]), "text"])


def test_text_and_space() -> None:
    check(" text ", [" text "])


def test_text_and_spaces() -> None:
    check("  text  ", ["  text  "])


def test_tag_and_space() -> None:
    check("\\tag {text}", [Tag("tag", [["text"]])])
