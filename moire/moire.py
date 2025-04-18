"""
Moire, a simple extensible markup language.

See http://github.com/enzet/Moire
"""

import logging
import sys
from collections.abc import Callable
from dataclasses import dataclass
from io import StringIO
from typing import Any, Optional

__author__: str = "Sergey Vartanov"
__email__: str = "me@enzet.ru"

# Constants

COMMENT_BEGIN: str = "/*"
COMMENT_END: str = "*/"
TAG_MARKER: str = "\\"
ARGUMENT_START: str = "{"
ARGUMENT_END: str = "}"
PARAGRAPH_DELIMITER: str = "\n\n"

SPACES: str = " \n\t\r"


class Root:
    def __init__(self):
        self.elements: list = []

    def add(self, element) -> None:
        self.elements.append(element)

    def serialize(self) -> str:
        return "\n".join(serialize(x) for x in self.elements)


@dataclass
class Tag:
    """Moire tag definition.

    Tag has name and parameters:
        <backslash><tag name> {<parameter 1>} ... {<parameter N>}.
    """

    id: str
    parameters: list

    def __eq__(self, other: "Tag") -> bool:
        if not isinstance(other, type(self)):
            return False
        if self.id != other.id:
            return False
        if len(self.parameters) != len(other.parameters):
            return False
        for i in range(len(self.parameters)):
            if self.parameters[i] != other.parameters[i]:
                return False
        return True

    def is_header(self) -> bool:
        return self.id in "123456"

    def serialize(self) -> str:
        """Serialize the tag into a text form."""
        return f"\\{self.id} " + " ".join(
            "{" + serialize(x) + "}" for x in self.parameters
        )


@dataclass
class Lexeme:
    type: str
    content: Optional[str] = None


class Tree:
    def __init__(self, parent, children, element) -> None:
        self.element = element
        self.parent = parent
        self.children = children
        self.number = 0

    def pr(self) -> None:
        print(self.element)
        for child in self.children:
            child.pr()

    def find(self, text: str) -> Optional["Tree"]:
        if (
            len(self.element.parameters) > 1
            and self.element.parameters[1][0] == text
        ):
            return self
        for child in self.children:
            a = child.find(text)
            if a:
                return a
        return None


@dataclass
class Argument:
    array: list
    spec: dict[str, Any]

    def __getitem__(self, key: int):
        return self.array[key]

    def __len__(self):
        return len(self.array)


def trim_inside(text: str) -> str:
    """Replace all space symbol sequences with one space character."""
    result: str = ""
    index: int = 0
    while index < len(text):
        if text[index] in SPACES:
            result += " "
            while index < len(text) and text[index] in SPACES:
                index += 1
            continue
        else:
            result += text[index]
        index += 1
    return result


def preprocess_comments(text: str):
    """Text to text processing: comments removing."""
    preprocessed: str = ""
    adding: bool = True
    i: int = 0
    while i < len(text):
        if text[i : i + len(COMMENT_BEGIN)] == COMMENT_BEGIN:
            adding = False
            i += 1
        elif text[i : i + len(COMMENT_END)] == COMMENT_END:
            adding = True
            i += 1
        else:
            if adding:
                preprocessed += text[i]
        i += 1
    return preprocessed


def is_letter_or_digit(char: str) -> bool:
    return "a" <= char <= "z" or "A" <= char <= "Z" or "0" <= char <= "9"


def lexer(text: str) -> tuple[list[Lexeme], list[int]]:
    """Parse formatted preprocessed text to a list of lexemes."""

    in_tag: bool = False  # Lexer position in tag name

    # Lexer position in space between tag name and first "{"
    in_space: bool = True
    lexemes: list[Lexeme] = []
    positions: list[int] = []
    tag_name: str = ""
    word: str = ""

    index: int = 0

    while index < len(text):
        char = text[index]
        if char == TAG_MARKER:
            if index == len(text) - 1:
                logging.error("Backslash at the end of string.")
            elif not is_letter_or_digit(text[index + 1]):
                if word != "":
                    lexemes.append(Lexeme("text", word))
                    positions.append(index)
                word = ""
                lexemes.append(Lexeme("symbol", text[index + 1]))
                positions.append(index + 1)
                index += 1
            else:
                if word != "":
                    lexemes.append(Lexeme("text", word))
                    positions.append(index)
                word = ""
                in_tag = True
                tag_name = ""
        elif char == ARGUMENT_START:
            if in_tag or in_space:
                in_tag = False
                if tag_name != "":
                    lexemes.append(Lexeme("tag", tag_name))
                    positions.append(index)
            lexemes.append(Lexeme("parameter_begin"))
            positions.append(index)
            tag_name = ""
            word = ""
        elif char == ARGUMENT_END:
            if word != "":
                lexemes.append(Lexeme("text", word))
                positions.append(index)
            word = ""
            lexemes.append(Lexeme("parameter_end"))
            positions.append(index)
        elif char in SPACES:
            if in_tag:
                in_tag = False
                in_space = True
            else:
                word += char
        else:
            if in_tag:
                tag_name += char
            else:
                word += char
        index += 1
    if word != "":
        lexemes.append(Lexeme("text", word))
        positions.append(index)

    return lexemes, positions


def get_intermediate(lexemes, positions, level, index=0):
    """Get intermediate representation."""

    tag: Optional[Tag] = None
    result = []
    while index < len(lexemes):
        item = lexemes[index]
        if item.type == "tag":
            if tag:
                result.append(tag)
            tag = Tag(item.content, [])
        elif item.type == "parameter_begin":
            level += 1
            if not tag:
                index += 1
                index, res = get_intermediate(lexemes, positions, level, index)
                result.append(res)
            else:
                index += 1
                index, res = get_intermediate(lexemes, positions, level, index)
                tag.parameters.append(res)
            index += 1
            continue
        elif item.type == "parameter_end":
            level -= 1
            if level < 0:
                position = positions[index]
                logging.error(f"Lexer error at {position}.")
                index += 1
                sys.exit(1)
            if tag:
                result.append(tag)
            return index, result
        elif item.type == "text":
            if tag:
                result.append(tag)
                tag = None
            result.append(item.content)
        elif item.type == "symbol":
            if tag:
                result.append(tag)
                tag = None
            result.append(item.content)
        index += 1
    if tag:
        result.append(tag)
    return index, result


class Moire:
    name: str = "Empty format"
    block_tags: list[str] = []
    escape_symbols: dict[str, str] = {}

    def __init__(self, file_name: Optional[str] = None):
        self.index: int = 0
        self.status: dict[str, Any] = {"missing_tags": set()}
        self.file_name: Optional[str] = file_name

    def init(self):
        """Some preliminary actions."""
        pass

    def finish(self):
        """Some finish actions."""
        pass

    def escape(self, text: str) -> str:
        for key in self.escape_symbols:
            text = text.replace(key, self.escape_symbols[key])
        return text

    def trim(self, text: str) -> str:
        if text.startswith("\n"):
            text = text[1:]
        if text.endswith("\n"):
            text = text[:-1]
        return text

    def get_ids(self, content: str) -> list[tuple[str, int]]:
        """Get all header identifiers.

        :param content: input content in the Moire format
        :return: list of tuples (id, level), level is 0 for labels
        """
        ids: list[tuple[str, int]] = []
        intermediate_representation = self.get_ir(content)
        for element in intermediate_representation:
            if isinstance(element, Tag):
                if element.is_header() and len(element.parameters) >= 2:
                    ids.append((element.parameters[1][0], int(element.id)))
                if element.id == "label":
                    ids.append((element.parameters[0][0], 0))
        return ids

    def convert(
        self, input_data: str, wrap: bool = True, in_block: bool = False
    ) -> str:
        """Convert Moire text without includes but with comments artifacts to
        selected format.
        """
        ir = self.get_ir(input_data)

        # Construct content table

        tree: Tree = Tree(None, [], Tag("0", ["_", "_"]))
        content_root: Tree = tree
        for part in ir:
            if not isinstance(part, Tag) or part.id not in "123456":
                continue
            element: Tree = Tree(tree, [], part)
            if int(part.id) > int(tree.element.id):
                tree.children.append(element)
                element.number = len(tree.children) - 1
                tree = tree.children[-1]
            else:
                while int(part.id) <= int(tree.element.id):
                    tree = tree.parent
                tree.children.append(element)
                element.number = len(tree.children) - 1
                element.parent = tree
                tree = tree.children[-1]
        self.status["tree"] = content_root

        # Wrap whole text with "body" tag

        if wrap:
            ir = Tag("body", [ir, content_root])

        self.init()
        self.parse(ir, mode="pre_")
        result: str = self.parse(ir, in_block=in_block)
        self.finish()

        return result

    def parse(
        self,
        text,
        in_block: bool = False,
        depth: int = 0,
        mode: str = "",
        spec: Optional[dict[str, Any]] = None,
    ) -> str:
        """Element parsing into formatted text.

        Element may be plain text, tag, or list of elements.
        """
        if spec is None:
            spec = {}

        if not text:
            return ""
        elif isinstance(text, str):
            if "trim" in spec and not spec["trim"]:
                return self.escape(text)
            else:
                return self.escape(trim_inside(text))
        elif isinstance(text, Tag):
            key: str = "header" if (text.id in "123456") else text.id
            method: Optional[Callable] = None
            try:
                method = getattr(self, mode + key)
            except AttributeError:
                pass
            if method is None:
                try:
                    method = getattr(self, mode + key + "__")
                except AttributeError:
                    pass
            if method is not None:
                arg = Argument(text.parameters, spec)
                if key == "header":
                    return method(arg, int(text.id))
                else:
                    return method(arg)
            else:
                if mode == "":
                    self.status["missing_tags"].add(key)
                    assert False, (
                        f"Unknown tag `{mode}{key}`"
                        + (f" in `{self.file_name}`" if self.file_name else "")
                        + "."
                    )
                else:
                    return ""
        elif isinstance(text, list):
            builder = StringIO()
            inner_block: list[Any] = []
            for item in text:
                if in_block:
                    if isinstance(item, Tag) and item.id in self.block_tags:
                        if inner_block:
                            builder.write(self.process_inner_block(inner_block))
                            inner_block = []
                        builder.write(
                            self.parse(
                                item,
                                in_block=in_block,
                                depth=depth + 1,
                                mode=mode,
                                spec=spec,
                            )
                        )
                    else:
                        inner_block.append(item)
                else:
                    parsed = self.parse(
                        item,
                        in_block=in_block,
                        depth=depth + 1,
                        mode=mode,
                        spec=spec,
                    )
                    if parsed is not None:
                        builder.write(parsed)
            if inner_block:
                builder.write(self.process_inner_block(inner_block))
            return builder.getvalue()
        else:
            assert False, f"Part is of type {type(text)}"

    def clear(self, text) -> str:
        if isinstance(text, list):
            return self.escape("".join([x for x in text if isinstance(x, str)]))
        return self.escape(text)

    def get_ir(self, text: str, offset: int = 0, prefix: str = ""):
        """Get intermediate representation."""

        # Remove comments.
        text = preprocess_comments(text)

        # Parse text into lexemes.
        lexemes, positions = lexer(text)

        # Get intermediate representation.
        index, raw_ir = get_intermediate(lexemes, positions, 0)

        resulted_ir = []

        for item in raw_ir:
            if isinstance(item, Tag):
                if item.is_header() and (offset or prefix):
                    new_item = Tag(str(int(item.id) + offset), item.parameters)
                    resulted_ir.append(new_item)
                else:
                    resulted_ir.append(item)
            else:
                resulted_ir.append(item)

        return resulted_ir

    def process_inner_block(self, inner_block: list[Any]) -> str:
        """Wrap parts of inner block element with text tag."""
        if len(inner_block) == 1 and inner_block[0] == "":
            return ""
        paragraphs = []
        paragraph = []
        for item in inner_block:
            if isinstance(item, str):
                previous = 0
                delimiter = item.find(PARAGRAPH_DELIMITER)
                while delimiter != -1:
                    content = item[previous:delimiter]
                    if content != "" or previous == 0:
                        paragraph.append(content)
                        paragraphs.append(paragraph)
                        paragraph = []
                    previous = delimiter + len(PARAGRAPH_DELIMITER)
                    delimiter = item.find(PARAGRAPH_DELIMITER, delimiter + 1)
                paragraph.append(item[previous:])
            else:
                paragraph.append(item)
        paragraphs.append(paragraph)
        s = ""
        for paragraph in paragraphs:
            if isinstance(paragraph[0], str):
                paragraph[0] = paragraph[0].lstrip()
            if isinstance(paragraph[-1], str):
                paragraph[-1] = paragraph[-1].rstrip()
            s += str(self.parse(Tag("text", [paragraph])))
        return s


def serialize(object_: Any) -> str:
    """Serialize Moire elements into a text form."""

    if isinstance(object_, str):
        return object_

    if isinstance(object_, list):
        if object_:
            if isinstance(object_[0], list):
                return " ".join("{" + serialize(x) + "}" for x in object_)
            else:
                return "".join(serialize(x) for x in object_)
        else:
            return ""

    if isinstance(object_, Tag):
        return object_.serialize()

    raise ValueError(f"Unknown object type: {type(object_)}.")
