"""
Moire library.

See http://github.com/enzet/Moire
"""

import logging
import sys
from io import StringIO

from typing import List, Dict

__author__: str = "Sergey Vartanov"
__email__: str = "me@enzet.ru"

# Constants

COMMENT_BEGIN: str = "/*"
COMMENT_END: str = "*/"
TAG_MARKER: str = "\\"
ARGUMENT_START: str = "{"
ARGUMENT_END: str = "}"
SPACES: str = " \n\t\r"
PARAGRAPH_DELIMITER: str = "\n\n"


class Tag:
    """
    Moire tag definition. Tag has name and parameters:
    <backslash><tag name> {<parameter 1>} ... {<parameter N>}.
    """

    def __init__(self, tag_id: str, parameters: List):
        self.id: str = tag_id
        self.parameters: List = parameters

    def __repr__(self) -> str:
        s = f"{self.id}{{{self.parameters}}}"
        return s

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


class Lexeme:
    def __init__(self, lexeme_type, content=None):
        self.type = lexeme_type
        self.content = content

    def __repr__(self):
        s = self.type
        if self.content:
            s += " {" + str(self.content.replace("\n", " ")) + "}"
        return s


class Tree:
    def __init__(self, parent, children, element):
        self.element = element
        self.parent = parent
        self.children = children
        self.number = 0

    def pr(self):
        print(self.element)
        for child in self.children:
            child.pr()

    def find(self, text):
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


class Argument:
    def __init__(self, array, spec):
        self.array = array
        self.spec = spec

    def __getitem__(self, key):
        return self.array[key]

    def __len__(self):
        return len(self.array)

    def spec(self):
        return self.spec


def trim_inside(s):
    """
    Replace all space symbol sequences with one space character.
    """
    ret = ""
    i = 0
    while i < len(s):
        if s[i] in SPACES:
            ret += " "
            while i < len(s) and s[i] in SPACES:
                i += 1
            continue
        else:
            ret += s[i]
        i += 1
    return ret


def comments_preprocessing(text):
    """
    Text to text processing: comments removing.
    """
    preprocessed = ""
    adding = True
    i = 0
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


def is_letter_or_digit(char):
    return "a" <= char <= "z" or "A" <= char <= "Z" or "0" <= char <= "9"


def lexer(text) -> (List[Lexeme], List[int]):
    """
    Parse formatted preprocessed text to a list of lexemes.
    """
    in_tag: bool = False  # Lexer position in tag name
    # Lexer position in space between tag name and first "{"
    in_space: bool = True
    lexemes: List[Lexeme] = []
    positions: List[int] = []
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
    """
    Get intermediate representation.
    """
    tag = None
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
                logging.error("Lexer error at " + str(position) + ".")
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
    block_tags = []
    escape_symbols: Dict[str, str] = {}

    def __init__(self):
        self.index = 0
        self.status = {"missing_tags": set()}

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

    def get_ids(self, content: str) -> List[str]:
        """
        Get all header identifiers.

        :param content: input content in the Moire format
        """
        ids: List[str] = []
        intermediate_representation = self.full_parse(content)
        for element in intermediate_representation:
            if isinstance(element, Tag) and element.is_header():
                if len(element.parameters) >= 2:
                    ids.append(element.parameters[1][0])
        return ids

    def convert(self, input_data: str, wrap: bool = True):
        """
        Convert Moire text without includes but with comments artifacts to
        selected format.
        """
        intermediate_representation = self.full_parse(input_data)

        # Construct content table

        tree = Tree(None, [], Tag("0", ["_", "_"]))
        content_root = tree
        for k in intermediate_representation:
            if isinstance(k, Tag) and k.id in "123456":
                element = Tree(tree, [], k)
                if int(k.id) > int(tree.element.id):
                    tree.children.append(element)
                    element.number = len(tree.children) - 1
                    tree = tree.children[-1]
                else:
                    while int(k.id) <= int(tree.element.id):
                        tree = tree.parent
                    tree.children.append(element)
                    element.number = len(tree.children) - 1
                    element.parent = tree
                    tree = tree.children[-1]
        self.status["tree"] = content_root

        # Wrap whole text with "body" tag

        if wrap:
            intermediate_representation = Tag(
                "body", [intermediate_representation, content_root]
            )

        self.init()
        self.parse(
            intermediate_representation, inblock=False, depth=0, mode="pre_"
        )
        result: str = self.parse(intermediate_representation)
        self.finish()

        return result

    def parse(self, text, inblock=False, depth=0, mode="", spec=None) -> str:
        """
        Element parsing into formatted text. Element may be plain text, tag, or
        list of elements.
        """
        if spec is None:
            spec = {}

        if not text:
            return ""
        elif isinstance(text, str):
            if "full_escape" in spec and spec["full_escape"]:
                return self._full_escape(self.escape(text))
            if "trim" in spec and not spec["trim"]:
                return self.escape(text)
            else:
                return self.escape(trim_inside(text))
        elif isinstance(text, Tag):
            key = "header" if (text.id in "123456") else text.id
            method = None
            try:
                method = getattr(self, mode + key)
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
                    assert False, f"Unknown tag {mode}{key}"
                else:
                    return ""
        elif isinstance(text, list):
            builder = StringIO()
            inner_block = []
            for item in text:
                if inblock:
                    if isinstance(item, Tag) and item.id in self.block_tags:
                        if inner_block:
                            builder.write(self.process_inner_block(inner_block))
                            inner_block = []
                        builder.write(
                            self.parse(
                                item,
                                inblock=inblock,
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
                        inblock=inblock,
                        depth=depth + 1,
                        mode=mode,
                        spec=spec,
                    )
                    builder.write(parsed)
            if inner_block:
                builder.write(self.process_inner_block(inner_block))
            return builder.getvalue()
        else:
            assert False

    def clear(self, text) -> str:
        if isinstance(text, list):
            return self.escape("".join([x for x in text if isinstance(x, str)]))
        return self.escape(text)

    def full_parse(self, text: str, offset: int = 0, prefix: str = ""):
        text = comments_preprocessing(text)
        lexemes, positions = lexer(text)
        index, raw_ir = get_intermediate(lexemes, positions, 0, 0)

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

    def process_inner_block(self, inner_block):
        """
        Wrap parts of inner block element with text tag.
        """
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
