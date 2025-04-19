"""Tests for Moire main module."""

from typing import Any

from moire.moire import Moire, Tag, serialize

converter: Moire = Moire()


def check_parsing(moire_code: str, intermediate_representation: Any) -> None:
    """Check the intermediate representation of the Moire code.

    :param moire_code: Moire code
    :param intermediate_representation: expected intermediate representation
    """
    assert converter.get_ir(moire_code) == intermediate_representation


def check_serialization(
    intermediate_representation: Any, moire_code: str
) -> None:
    """Check the Moire code serialization.

    :param intermediate_representation: intermediate representation
    :param moire_code: expected Moire code
    """
    assert serialize(intermediate_representation) == moire_code


def test_text_parsing() -> None:
    """Test text parsing."""
    check_parsing("text", ["text"])


def test_text_serialization() -> None:
    """Test text serialization."""
    check_serialization(["text"], "text")


def test_tag_parsing() -> None:
    """Test tag parsing."""
    check_parsing("\\tag{text}", [Tag("tag", [["text"]])])


def test_tag_serialization() -> None:
    """Test tag serialization."""
    check_serialization([Tag("tag", [["text"]])], "\\tag {text}")


def test_text_and_tag() -> None:
    """Test text and tag."""
    check_parsing("\\tag{text}text", [Tag("tag", [["text"]]), "text"])


def test_text_and_space() -> None:
    """Test text and space."""
    check_parsing(" text ", [" text "])


def test_text_and_spaces() -> None:
    """Test text and spaces."""
    check_parsing("  text  ", ["  text  "])


def test_tag_and_space() -> None:
    """Test tag and space."""
    check_parsing("\\tag {text}", [Tag("tag", [["text"]])])


def test_tag_in_tag_parsing() -> None:
    """Test tag in tag parsing."""
    check_parsing(
        "\\tag{text\\tag2{text}text}",
        [Tag("tag", [["text", Tag("tag2", [["text"]]), "text"]])],
    )


def test_tag_in_tag_serialization() -> None:
    """Test tag in tag serialization."""
    check_serialization(
        [Tag("tag", [["text", Tag("tag2", [["text"]]), "text"]])],
        "\\tag {text\\tag2 {text}text}",
    )


def test_table_parsing() -> None:
    """Test table parsing."""
    check_parsing(
        "\\table{{a}{b}}{{c}{d}}",
        [Tag("table", [[["a"], ["b"]], [["c"], ["d"]]])],
    )


def test_table_serialization() -> None:
    """Test table serialization."""
    check_serialization(
        [Tag("table", [[["a"], ["b"]], [["c"], ["d"]]])],
        "\\table {{a} {b}} {{c} {d}}",
    )


def test_tag_in_table_serialization() -> None:
    """Test tag in table serialization."""
    check_serialization(
        [Tag("table", [[["a", Tag("nbs", [""]), "a"], ["b"]], [["c"], ["d"]]])],
        "\\table {{a\\nbs {}a} {b}} {{c} {d}}",
    )
