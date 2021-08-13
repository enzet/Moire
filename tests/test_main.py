from moire.moire import Moire, Tag


converter: Moire = Moire()


def test_tag() -> None:
    assert converter.full_parse("\\b{text}") == [Tag("b", [["text"]])]


def test_simple() -> None:
    assert converter.full_parse("text") == ["text"]
