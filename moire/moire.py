"""
Moire library.  This file is a part of Moire project—light markup language.

See http://github.com/enzet/Moire
"""

import sys

from typing import List, Dict

__author__: str = "Sergey Vartanov"
__email__: str = "me@enzet.ru"

# Global variables

# Constants

comment_begin = "/*"
comment_end = "*/"

paragraph_delimiter = "\n\n"


def error(message):
    print(" [ERROR] " + str(message) + ".")


class Tag:
    """
    Moire tag definition. Tag has name and parameters:
    \<tag name> {<parameter 1>} ... {<parameter N>}.
    """

    def __init__(self, tag_id, parameters):
        self.id = tag_id
        self.parameters = parameters

    def __str__(self):
        s = self.id + " {" + str(self.parameters) + "}"
        return s

    def __repr__(self):
        s = self.id + " {" + str(self.parameters) + "}"
        return s

    def is_header(self):
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


def is_space(c):
    return c in " \n\t\r"


def trim_inside(s):
    """
    Replace all space symbol sequences with one space character.
    """
    ret = ""
    i = 0
    while i < len(s):
        if is_space(s[i]):
            ret += " "
            while i < len(s) and is_space(s[i]):
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
        if text[i : i + 2] == comment_begin:
            adding = False
            i += 1
        elif text[i : i + 2] == comment_end:
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
    in_tag = False  # Lexer position in tag name
    in_space = True  # Lexer position in space between tag name and first "{"
    lexemes: List[Lexeme] = []
    positions: List[int] = []
    tag_name: str = ""
    word: str = ""

    index: int = 0

    while index < len(text):
        char = text[index]
        if char == "\\":
            if index == len(text) - 1:
                print("Error: backslash at the end of string.")
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
        elif char == "{":
            if in_tag or in_space:
                in_tag = False
                if tag_name != "":
                    lexemes.append(Lexeme("tag", tag_name))
                    positions.append(index)
            lexemes.append(Lexeme("parameter_begin"))
            positions.append(index)
            tag_name = ""
            word = ""
        elif char == "}":
            if word != "":
                lexemes.append(Lexeme("text", word))
                positions.append(index)
            word = ""
            lexemes.append(Lexeme("parameter_end"))
            positions.append(index)
        elif is_space(char):
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
                print("Lexer error at " + str(position) + ".")
                # print input_file[position - 10:position + 10]\
                #        .replace("\n", " ").replace("\t", " ")
                # print "          ^"
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
        self.parse(intermediate_representation, inblock=False, depth=0, mode="pre_")
        result: str = self.parse(intermediate_representation)
        self.finish()

        return result

    def parse(
        self, text, inblock=False, depth=0, mode="",
        spec=None
    ) -> str:
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
                return "<NO TAG>"
        elif isinstance(text, list):
            s = ""
            inner_block = []
            for item in text:
                if inblock:
                    if (
                        isinstance(item, Tag) and item.id in self.block_tags
                    ):
                        if inner_block:
                            s += self.process_inner_block(inner_block)
                            inner_block = []
                        s += str(
                            self.parse(
                                item, inblock=inblock, depth=depth + 1,
                                mode=mode, spec=spec,
                            )
                        )
                    else:
                        inner_block.append(item)
                else:
                    s += str(
                        self.parse(
                            item, inblock=inblock, depth=depth + 1, mode=mode,
                            spec=spec,
                        )
                    )
            if inner_block:
                s += self.process_inner_block(inner_block)
            return s
        else:
            assert False

    def clear(self, text):
        if isinstance(text, list):
            s = ""
            for item in text:
                if isinstance(item, str):
                    s += item
            return self.escape(s)
        return self.escape(text)

    def full_parse(self, text: str, offset: int = 0, prefix: str = ""):
        text = comments_preprocessing(text)
        lexemes, positions = lexer(text)
        index, raw_IR = get_intermediate(lexemes, positions, 0, 0)

        resulted_IR = []

        for item in raw_IR:
            if isinstance(item, Tag):
                if item.is_header() and (offset or prefix):
                    new_item = Tag(str(int(item.id) + offset), item.parameters)
                    resulted_IR.append(new_item)
                else:
                    resulted_IR.append(item)
            else:
                resulted_IR.append(item)

        return resulted_IR

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
                delimiter = item.find(paragraph_delimiter)
                while delimiter != -1:
                    content = item[previous:delimiter]
                    if content != "" or previous == 0:
                        paragraph.append(content)
                        paragraphs.append(paragraph)
                        paragraph = []
                    previous = delimiter + len(paragraph_delimiter)
                    delimiter = item.find(paragraph_delimiter, delimiter + 1)
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
