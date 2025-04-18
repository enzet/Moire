from typing import Any

from moire.moire import Moire, Tag, serialize

converter: Moire = Moire()


def check_parsing(moire_code: str, intermediate_representation: Any) -> None:
    assert converter.get_ir(moire_code) == intermediate_representation


def check_serialization(
    intermediate_representation: Any, moire_code: str
) -> None:
    assert serialize(intermediate_representation) == moire_code


def test_text_parsing() -> None:
    check_parsing("text", ["text"])


def test_text_serialization() -> None:
    check_serialization(["text"], "text")


def test_tag_parsing() -> None:
    check_parsing("\\tag{text}", [Tag("tag", [["text"]])])


def test_tag_serialization() -> None:
    check_serialization([Tag("tag", [["text"]])], "\\tag {text}")


def test_text_and_tag() -> None:
    check_parsing("\\tag{text}text", [Tag("tag", [["text"]]), "text"])


def test_text_and_space() -> None:
    check_parsing(" text ", [" text "])


def test_text_and_spaces() -> None:
    check_parsing("  text  ", ["  text  "])


def test_tag_and_space() -> None:
    check_parsing("\\tag {text}", [Tag("tag", [["text"]])])


def test_tag_in_tag_parsing() -> None:
    check_parsing(
        "\\tag{text\\tag2{text}text}",
        [Tag("tag", [["text", Tag("tag2", [["text"]]), "text"]])],
    )


def test_tag_in_tag_serialization() -> None:
    check_serialization(
        [Tag("tag", [["text", Tag("tag2", [["text"]]), "text"]])],
        "\\tag {text\\tag2 {text}text}",
    )


def test_table_parsing() -> None:
    check_parsing(
        "\\table{{a}{b}}{{c}{d}}",
        [Tag("table", [[["a"], ["b"]], [["c"], ["d"]]])],
    )


def test_table_serialization() -> None:
    check_serialization(
        [Tag("table", [[["a"], ["b"]], [["c"], ["d"]]])],
        "\\table {{a} {b}} {{c} {d}}",
    )


def test_tag_in_table_serialization() -> None:
    check_serialization(
        [Tag("table", [[["a", Tag("nbs", [""]), "a"], ["b"]], [["c"], ["d"]]])],
        "\\table {{a\\nbs {}a} {b}} {{c} {d}}",
    )
