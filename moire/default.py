"""Default tag definitions."""

import logging
import sys
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from dataclasses import dataclass, field
from pathlib import Path
from textwrap import dedent
from typing import Any, ClassVar, override

from moire.moire import Moire

__author__ = "Sergey Vartanov"
__email__ = "me@enzet.ru"

logger: logging.Logger = logging.getLogger(__name__)

depth: int = 0
status: dict[str, Any] = {}
BLOCK_TAGS: set[str] = {
    "block", "body", "code", "title", "number", "list", "image", "table"
}  # fmt: skip
Arguments = list[Any]


class TagNotImplementedError(NotImplementedError):
    """Tag is not implemented in the parser."""

    def __init__(self, tag: str = "") -> None:
        self.tag: str = tag

    def __str__(self) -> str:
        return rf"Tag \{self.tag} is not implemented in the parser"


@dataclass
class Default(Moire, ABC):
    """Default tag declaration."""

    # Main methods.

    @abstractmethod
    def body(self, arg: Arguments) -> str:
        """Body of the document."""
        raise TagNotImplementedError(Default.body.__name__)

    # Metadata tags.

    @abstractmethod
    def title(self, arg: Arguments) -> str:
        """Specify title of the document.

        This is metadata tag and is not displayed in the document.
        """
        raise TagNotImplementedError(Default.title.__name__)

    @abstractmethod
    def author(self, arg: Arguments) -> str:
        """Specify author of the document.

        This is metadata tag and is not displayed in the document.
        """
        raise TagNotImplementedError(Default.author.__name__)

    @abstractmethod
    def date(self, arg: Arguments) -> str:
        """Specify date of the document.

        This is metadata tag and is not displayed in the document.
        """
        raise TagNotImplementedError(Default.date.__name__)

    # Hyperlinks.

    @staticmethod
    @abstractmethod
    def _get_ref(link: str, text: str) -> str:
        """Get reference to a link."""
        raise NotImplementedError

    @abstractmethod
    def ref(self, arg: Arguments) -> str:
        r"""Hypertext reference.

        Arguments: <reference> <text>?

        If reference starts with `#`, Moire will try to create a reference to
        the declared header or label with this identifier. E.g. if we have a
        header `\3 {Header} {test}` or label `\label {test}`, valid references
        for both of them will be `\ref {#test} {reference text}`.
        """
        raise TagNotImplementedError(Default.ref.__name__)

    # Main formatting tags.

    @abstractmethod
    def header(self, arg: Arguments, level: int) -> str:
        """Add header with specified level.

        Arguments: <header text> <header identifier>?
        """
        raise TagNotImplementedError(Default.header.__name__)

    @abstractmethod
    def e(self, arg: Arguments) -> str:
        """Emphasize text."""
        raise TagNotImplementedError(Default.e.__name__)

    @abstractmethod
    def s(self, arg: Arguments) -> str:
        """Strongly emphasize text."""
        raise TagNotImplementedError(Default.s.__name__)

    def b(self, arg: Arguments) -> str:
        r"""Make text bold.

        This tag is deprecated. Now it is an alias for `\s`.
        """
        return self.s(arg)

    def i(self, arg: Arguments) -> str:
        r"""Make text italic.

        This tag is deprecated. Now it is an alias for `\e`.
        """
        return self.e(arg)

    @abstractmethod
    def c(self, arg: Arguments) -> str:
        """Mark text as code."""
        raise TagNotImplementedError(Default.c.__name__)

    def m(self, arg: Arguments) -> str:
        r"""Make text monospaced.

        This tag is deprecated. Now it is an alias for `\c`.
        """
        return self.c(arg)

    @abstractmethod
    def del__(self, arg: Arguments) -> str:
        """Mark text as deleted."""
        raise TagNotImplementedError(Default.del__.__name__)

    @abstractmethod
    def sub(self, arg: Arguments) -> str:
        """Make text a subscript."""
        raise TagNotImplementedError(Default.sub.__name__)

    @abstractmethod
    def super(self, arg: Arguments) -> str:
        """Make text a superscript."""
        raise TagNotImplementedError(Default.super.__name__)

    # Main block tags.

    @abstractmethod
    def list__(self, arg: Arguments) -> str:
        """Create a list of items."""
        raise TagNotImplementedError(Default.list__.__name__)

    @abstractmethod
    def table(self, arg: Arguments) -> str:
        r"""Create a simple table with rows and columns.

        Format: \table {{<cell>} {<cell>} ...} {{<cell>} {<cell>} ...} ...

        This simple table does not support header, border style, text alignment,
        or cell merging.
        """
        raise TagNotImplementedError(Default.table.__name__)

    @abstractmethod
    def image(self, arg: Arguments) -> str:
        r"""Image.

        Format: \image {<image source>} {<image title>}?
        """
        raise TagNotImplementedError(Default.image.__name__)

    def _parse_code_arguments(self, arg: Arguments) -> tuple[str, str]:
        """Parse trimmed code and possible language identifier."""
        if len(arg) == 1:
            return self.trim(self.parse(arg[0], spec={"trim": False})), ""

        return (
            self.trim(self.parse(arg[1], spec={"trim": False})),
            self.clear(arg[0]),
        )

    @abstractmethod
    def code(self, arg: Arguments) -> str:
        """Code block.

        Arguments: <language identifier>? <code>

        Examples of language identifiers: `cpp` for C++, `python` for Python,
        `js` or `javascript` for JavaScript.
        """
        raise TagNotImplementedError(Default.code.__name__)

    def nospell(self, arg: Arguments) -> str:
        """Text that shouldn't be checked for spelling.

        This method will do nothing and just resume the process of parsing its
        content, it is an indication to the Moire code viewer or editor not to
        check the content for spelling with automatic tools.
        """
        return self.parse(arg[0])


@dataclass
class DefaultHTML(Default):
    """Default HTML format."""

    name: ClassVar[str] = "HTML"
    id_: ClassVar[str] = "html"
    extensions: ClassVar[list[str]] = ["html", "htm"]
    escape_symbols: ClassVar[dict[str, str]] = {"<": "&lt;", ">": "&gt;"}
    block_tags: ClassVar[set[str]] = BLOCK_TAGS

    # Parser methods.

    @override
    def escape(self, text: str) -> str:
        return super().escape(text.replace("&", "&amp;"))

    # Main methods.

    @override
    def body(self, arg: Arguments) -> str:
        status["content"] = []
        s: str = dedent(
            """
            <html>
                <head>
                    <meta http-equiv="Content-Type" content="text/html;
                        charset=utf-8">
                    <link rel="stylesheet" href="style.css">
                </head>
                <body>
            """
        )
        s += self.parse(arg[0], in_block=True)
        s += dedent(
            """
                </body>
            </html>
            """
        )
        return s

    # Metadata tags.

    @override
    def title(self, arg: Arguments) -> str:
        return f"<title>{self.parse(arg[0])}</title>"

    @override
    def author(self, arg: Arguments) -> str:
        return f'<meta name="author" content="{self.parse(arg[0])}">'

    @override
    def date(self, arg: Arguments) -> str:
        return f'<meta name="date" content="{self.parse(arg[0])}">'

    # Hyperlinks.

    @override
    @staticmethod
    def _get_ref(link: str, text: str) -> str:
        return f'<a href="{link}">{text}</a>'

    @override
    def ref(self, arg: Arguments) -> str:
        link: str = self.parse(arg[0])
        return DefaultHTML._get_ref(
            link, link if len(arg) == 1 else self.parse(arg[1])
        )

    # Main formatting tags.

    @override
    def header(self, arg: Arguments, level: int) -> str:
        id_: str = "" if len(arg) <= 1 else f' id="{self.clear(arg[1])}"'
        return f"<h{level}{id_}>{self.parse(arg[0])}</h{level}>"

    @override
    def s(self, arg: Arguments) -> str:
        return f"<b>{self.parse(arg[0])}</b>"

    @override
    def e(self, arg: Arguments) -> str:
        return f"<i>{self.parse(arg[0])}</i>"

    @override
    def c(self, arg: Arguments) -> str:
        return f"<code>{self.parse(arg[0])}</code>"

    @override
    def del__(self, arg: Arguments) -> str:
        return f"<del>{self.parse(arg[0])}</del>"

    @override
    def sub(self, arg: Arguments) -> str:
        return f"<sub>{self.parse(arg[0])}</sub>"

    @override
    def super(self, arg: Arguments) -> str:
        return f"<sup>{self.parse(arg[0])}</sup>"

    # Main block tags.

    @override
    def list__(self, arg: Arguments) -> str:
        items: str = "".join(f"<li>{self.parse(x)}</li>" for x in arg)
        return f"<ul>{items}</ul>"

    @override
    def table(self, arg: Arguments) -> str:
        result: str = ""

        for row in arg:
            cells: str = "".join(
                [f"<td>{self.parse(cell, in_block=True)}</td>" for cell in row]
            )
            result += f"<tr>{cells}</tr>"

        return f"<table>{result}</table>"

    @override
    def image(self, arg: Arguments) -> str:
        title: str = f' alt="{self.parse(arg[1])}"' if len(arg) > 1 else ""
        return f'<img src="{self.clear(arg[0])}"{title} />'

    @override
    def code(self, arg: Arguments) -> str:
        code_, _ = self._parse_code_arguments(arg)
        return f"<pre><tt>{code_}</tt></pre>"

    @staticmethod
    def br(_: Arguments) -> str:
        """Add line break."""
        return "<br />"

    def size(self, arg: Arguments) -> str:
        """Set font size."""
        return f'<span style="font-size: {arg[0]}">{self.parse(arg[1])}</span>'

    def text(self, arg: Arguments) -> str:
        """Wrap text in a paragraph."""
        return f"<p>{self.parse(arg[0])}</p>"

    def quote(self, arg: Arguments) -> str:
        """Mark text as a block quote."""
        return f"<blockquote>{self.parse(arg[0])}</blockquote>"


@dataclass
class DefaultText(Default):
    """Plain text."""

    name: ClassVar[str] = "Text"
    id_: ClassVar[str] = "text"
    extension: ClassVar[str] = "txt"
    escape_symbols: ClassVar[dict[str, str]] = {}

    # Main methods.

    @override
    def body(self, arg: Arguments) -> str:
        return self.parse(arg[0], in_block=True, depth=1) + "\n"

    # Metadata tags.

    @override
    def title(self, arg: Arguments) -> str:
        # Tag is ignored.
        return ""

    @override
    def author(self, arg: Arguments) -> str:
        # Tag is ignored.
        return ""

    @override
    def date(self, arg: Arguments) -> str:
        # Tag is ignored.
        return ""

    # Hyperlinks.

    @override
    @staticmethod
    def _get_ref(link: str, text: str) -> str:
        return f"{text} ({link})"

    @override
    def ref(self, arg: Arguments) -> str:
        return DefaultText._get_ref(self.clear(arg[0]), self.parse(arg[1]))

    # Main formatting tags.

    @override
    def header(self, arg: Arguments, level: int) -> str:
        return "  " * (level - 1) + self.parse(arg[0], depth=depth + 1)

    @override
    def s(self, arg: Arguments) -> str:
        return self.parse(arg[0], depth=depth + 1)

    @override
    def e(self, arg: Arguments) -> str:
        return self.parse(arg[0], depth=depth + 1)

    @override
    def c(self, arg: Arguments) -> str:
        return self.parse(arg[0], depth=depth + 1)

    @override
    def del__(self, arg: Arguments) -> str:
        return self.parse(arg[0], depth=depth + 1)

    @override
    def sub(self, arg: Arguments) -> str:
        return self.parse(arg[0], depth=depth + 1)

    @override
    def super(self, arg: Arguments) -> str:
        return self.parse(arg[0], depth=depth + 1)

    # Main block tags.

    @override
    def list__(self, arg: Arguments) -> str:
        result: str = ""
        for item in arg:
            if isinstance(item, list):
                result += "  * " + self.parse(
                    item, in_block=True, depth=depth + 1
                )
        return result

    @override
    def table(self, arg: Arguments) -> str:
        widths: list[int] = []
        for row in arg:
            cells: list[str] = [self.parse(cell) for cell in row]
            for index, cell in enumerate(cells):
                if len(widths) - 1 < index:
                    widths.append(len(cell))
                else:
                    widths[index] = max(widths[index], len(cell))

        ruler: str = "+" + "+".join(["-" * (x + 2) for x in widths]) + "+"

        result: str = ruler + "\n"
        for row in arg:
            result += "|"
            for index, cell in enumerate(row):
                parsed: str = self.parse(cell)
                result += f" {parsed} " * (widths[index] - len(parsed)) + " |"
            result += "\n"
        result += ruler + "\n"

        return result

    @override
    def image(self, arg: Arguments) -> str:
        return f"[{self.parse(arg[1]) if len(arg) > 1 else ''}]"

    @override
    def code(self, arg: Arguments) -> str:
        code_, _ = self._parse_code_arguments(arg)
        return code_ + "\n"


@dataclass
class DefaultMarkdown(Default):
    """Markdown.

    Markdown formatter based on CommonMark specification 0.31.2 (28 January
    2024).

    See https://spec.commonmark.org/0.31.2/
    """

    name: ClassVar[str] = "Markdown"
    id_: ClassVar[str] = "markdown"
    extensions: ClassVar[list[str]] = ["md", "markdown"]
    block_tags: ClassVar[set[str]] = BLOCK_TAGS

    def __init__(
        self, *, is_html: bool = True, is_github_flavored: bool = False
    ) -> None:
        super().__init__()
        self.list_level: int = 0

        self.is_html: bool = is_html
        """If true, use HTML for tags that are not supported by CommonMark.

        If false, these tags will be ignored.
        """

        self.is_github_flavored: bool = is_github_flavored
        """If true, use GitHub Flavored Markdown extensions."""

    # Main methods.

    @override
    def body(self, arg: Arguments) -> str:
        # TODO(enzet): rewrite.
        return (
            self.parse(arg[0], in_block=True)
            .replace("\n\n\n", "\n\n")
            .replace("\n\n\n", "\n\n")
        )

    # Metadata tags.

    @override
    def title(self, arg: Arguments) -> str:
        # Tag is ignored.
        return ""

    @override
    def author(self, arg: Arguments) -> str:
        # Tag is ignored.
        return ""

    @override
    def date(self, arg: Arguments) -> str:
        # Tag is ignored.
        return ""

    # Hyperlinks.

    @override
    @staticmethod
    def _get_ref(link: str, text: str) -> str:
        return f"[{text}]({link})"

    @override
    def ref(self, arg: Arguments) -> str:
        return DefaultMarkdown._get_ref(self.parse(arg[0]), self.parse(arg[1]))

    # Main formatting tags.

    @override
    def header(self, arg: Arguments, level: int) -> str:
        """We use simplest possible ATX header style."""

        # CommonMark specification allows headers from level 1 to 6.
        # TODO(enzet): add warning if level is greater than 6.
        level = min(level, 6)

        return f"{level * '#'} {self.parse(arg[0])}"

    @override
    def s(self, arg: Arguments) -> str:
        # TODO(enzet): add weak warning, bold is actually "strong emphasis" in
        # CommonMark.
        return f"**{self.parse(arg[0])}**"

    @override
    def e(self, arg: Arguments) -> str:
        # TODO(enzet): add weak warning, italic is actually "emphasis" in
        # CommonMark.
        return f"*{self.parse(arg[0])}*"

    @override
    def c(self, arg: Arguments) -> str:
        return f"`{self.parse(arg[0])}`"

    @override
    def del__(self, arg: Arguments) -> str:
        if self.is_github_flavored:
            return f"~~{self.parse(arg[0])}~~"
        if self.is_html:
            return f"<del>{self.parse(arg[0])}</del>"
        # TODO(enzet): add warning, tag is ignored.
        return self.parse(arg[0])

    @override
    def sub(self, arg: Arguments) -> str:
        if self.is_html:
            return f"<sub>{self.parse(arg[0])}</sub>"
        # TODO(enzet): add warning, tag is ignored.
        return self.parse(arg[0])

    @override
    def super(self, arg: Arguments) -> str:
        if self.is_html:
            return f"<sup>{self.parse(arg[0])}</sup>"
        # TODO(enzet): add warning, tag is ignored.
        return self.parse(arg[0])

    # Main block tags.

    @override
    def list__(self, arg: Arguments) -> str:
        self.list_level += 1
        result: str = "".join(
            ("\n" + "  " * self.list_level + f"* {self.parse(item)}")
            for item in arg
        )
        self.list_level -= 1
        return result

    @override
    def table(self, arg: Arguments) -> str:
        result: str = ""
        for index, row in enumerate(arg):
            if isinstance(row, list):
                result += "|"
                for cell in row:
                    if isinstance(cell, list):
                        result += f" {self.parse(cell)} |"
                result += "\n"
                if index == 0:
                    result += "|"
                    for cell in row:
                        if isinstance(cell, list):
                            result += "---|"
                    result += "\n"
        return result

    @override
    def image(self, arg: Arguments) -> str:
        if len(arg) > 1:
            return f"![{self.parse(arg[1])}]({self.parse(arg[0])})"
        return f"![{self.parse(arg[0])}]({self.parse(arg[0])})"

    @override
    def code(self, arg: Arguments) -> str:
        code_, language = self._parse_code_arguments(arg)
        return f"```{language}\n{code_}\n```"

    def quote(self, arg: Arguments) -> str:
        """Mark text as a block quote."""
        return f"> {self.parse(arg[0])}"


@dataclass
class DefaultWiki(Default):
    """Wiki syntax of Wikipedia."""

    name: ClassVar[str] = "Wiki"
    id_: ClassVar[str] = "wiki"
    extensions: ClassVar[list[str]] = ["wiki"]
    block_tags: ClassVar[set[str]] = BLOCK_TAGS

    # Main methods.

    @override
    def body(self, arg: Arguments) -> str:
        return (
            self.parse(arg[0], in_block=True)
            .replace("\n\n\n", "\n\n")
            .replace("\n\n\n", "\n\n")
        )

    # Metadata tags.

    @override
    def title(self, arg: Arguments) -> str:
        # Tag is ignored.
        return ""

    @override
    def author(self, arg: Arguments) -> str:
        # Tag is ignored.
        return ""

    @override
    def date(self, arg: Arguments) -> str:
        # Tag is ignored.
        return ""

    # Hyperlinks.

    @override
    @staticmethod
    def _get_ref(link: str, text: str) -> str:
        return f"[[{link}|{text}]]"

    @override
    def ref(self, arg: Arguments) -> str:
        return DefaultWiki._get_ref(self.clear(arg[0]), self.parse(arg[1]))

    # Main formatting tags.

    @override
    def header(self, arg: Arguments, level: int) -> str:
        return f"{level * '='} {self.parse(arg[0])} {level * '='}"

    @override
    def s(self, arg: Arguments) -> str:
        return f"'''{self.parse(arg[0])}'''"

    @override
    def e(self, arg: Arguments) -> str:
        return f"''{self.parse(arg[0])}''"

    @override
    def c(self, arg: Arguments) -> str:
        return f"`{self.parse(arg[0])}`"

    @override
    def del__(self, arg: Arguments) -> str:
        return f"~~{self.parse(arg[0])}~~"

    @override
    def sub(self, arg: Arguments) -> str:
        return DefaultHTML.sub(self, arg[0])  # type: ignore[arg-type]

    @override
    def super(self, arg: Arguments) -> str:
        return DefaultHTML.super(self, arg[0])  # type: ignore[arg-type]

    # Main block tags.

    @override
    def list__(self, arg: Arguments) -> str:
        result: str = ""
        for item in arg:
            if isinstance(item, list):
                result += f"* {self.parse(item)}\n"
        return result

    @override
    def table(self, arg: Arguments) -> str:
        result: str = (
            '{| class="wikitable" border="1" cellspacing="0" cellpadding="2"\n'
            "! Tag || Rendering\n"
        )
        for row in arg:
            result += "|-\n"
            for cell in row:
                result += f"| {self.parse(cell)}\n"
        return result + "|}\n"

    @override
    def image(self, arg: Arguments) -> str:
        if len(arg) > 1:
            return f"[[File:{self.parse(arg[0])}|thumb|{self.parse(arg[1])}]]"
        return f"[[File:{self.parse(arg[0])}|thumb]]"

    @override
    def code(self, arg: Arguments) -> str:
        code_, language = self._parse_code_arguments(arg)
        if language:
            return (
                f'<syntaxhighlight lang="{language}">'
                f"\n{code_}\n</syntaxhighlight>"
            )
        return f"<pre><tt>{code_}\n</tt></pre>"

    def quote(self, arg: Arguments) -> str:
        """Mark text as a block quote."""
        return f">{self.parse(arg[0])}"


@dataclass
class DefaultTeX(Default):
    """TeX syntax."""

    name: ClassVar[str] = "Tex"
    id_: ClassVar[str] = "tex"
    extension: ClassVar[str] = "tex"

    escape_symbols: ClassVar[dict[str, str]] = {"_": r"\_"}
    block_tags: ClassVar[set[str]] = BLOCK_TAGS
    headers: ClassVar[list[str]] = [
        "section",
        "subsection",
        "subsubsection",
        "paragraph",
        "subparagraph",
    ]

    packages: list[tuple[str, str]] = field(default_factory=list)

    # Main methods.

    @override
    def body(self, arg: Arguments) -> str:
        result: str = dedent(
            r"""\
            \documentclass[twoside,psfig]{article}
            \usepackage[utf8]{inputenc}
            \usepackage[russian]{babel}
            \usepackage{enumitem}
            \usepackage{float}
            \usepackage[margin=3cm,hmarginratio=1:1,top=32mm,columnsep=20pt]
                {geometry}
            \usepackage{graphicx}
            \usepackage{hyperref}
            \usepackage{multicol}
            \begin{document}
            """
        )
        result += self.parse(arg[0], in_block=True)
        result += r"\end{document}"
        return result

    # Metadata tags.

    @override
    def title(self, arg: Arguments) -> str:
        result: str = f"\\title{{{self.parse(arg[0])}}}\n"
        result += r"\maketitle"
        return result

    @override
    def author(self, arg: Arguments) -> str:
        return rf"\author{{{self.parse(arg[0])}}}"

    @override
    def date(self, arg: Arguments) -> str:
        return rf"\date{{{self.parse(arg[0])}}}"

    # Hyperlinks.

    @override
    @staticmethod
    def _get_ref(link: str, text: str) -> str:
        return rf"\href{{{link}}}{{{text}}}"

    @override
    def ref(self, arg: Arguments) -> str:
        result: str = ""
        link = self.clear(arg[0])
        if link[0] == "#":
            link = link[1:]
        if len(arg) == 1:
            result += DefaultTeX._get_ref(link, link)
        else:
            result += DefaultTeX._get_ref(link, self.parse(arg[1]))
        return result

    # Main formatting tags.

    @override
    def header(self, arg: Arguments, level: int) -> str:
        if level <= len(self.headers):
            return rf"\{self.headers[level - 1]}{{{self.parse(arg[0])}}}"
        return self.parse(arg[0])

    @override
    def s(self, arg: Arguments) -> str:
        return rf"{{\bf {self.parse(arg[0])}}}"

    @override
    def e(self, arg: Arguments) -> str:
        return rf"{{\em {self.parse(arg[0])}}}"

    @override
    def c(self, arg: Arguments) -> str:
        return rf"{{\tt {self.parse(arg[0])}}}"

    @override
    def del__(self, arg: Arguments) -> str:
        # TODO(enzet): implement.
        raise TagNotImplementedError(Default.del__.__name__)

    @override
    def sub(self, arg: Arguments) -> str:
        return f"${{{self.parse(arg[0])}}}$"

    @override
    def super(self, arg: Arguments) -> str:
        return rf"\textsuperscript{{{self.parse(arg[0])}}}"

    # Main block tags.

    @override
    def list__(self, arg: Arguments) -> str:
        result: str = "\\begin{itemize}\n"
        for item in arg:
            result += f"\\item {self.parse(item)}\n\n"
        result += "\\end{itemize}\n"
        return result

    @override
    def table(self, arg: Arguments) -> str:
        result: str = "\\begin{table}[h]\n\\begin{center}\n\\begin{tabular}"

        max_columns: int = 0
        for tr in arg:
            if isinstance(tr, list):
                column_count: int = 0
                for td in tr:
                    if isinstance(td, list):
                        column_count += 1
                max_columns = max(max_columns, column_count)

        result += f"{{|{('l|' * max_columns)}}}\n\\hline\n"

        for row in arg:
            if isinstance(row, list):
                columns: list[list[Any]] = [
                    column for column in row if isinstance(column, list)
                ]
                for column in columns[:-1]:
                    result += self.parse(column) + " & "
                result += self.parse(columns[-1])
                result += " \\\\\n\\hline\n"

        result += "\\end{tabular}\n\\end{center}\n\\end{table}\n"

        return result

    @override
    def image(self, arg: Arguments) -> str:
        result: str = (
            r"\begin{figure}[h]\begin{center}\includegraphics{"
            + self.parse(arg[0])
            + r"}\end{center}"
        )
        if len(arg) > 1:
            result += rf"\caption{{ {self.parse(arg[1])}}}"
        result += r"\end{figure}"
        return result

    @override
    def code(self, arg: Arguments) -> str:
        code_, _ = self._parse_code_arguments(arg)
        return rf"\begin{{verbatim}}{code_}\end{{verbatim}}"

    def ordered(self, arg: Arguments) -> str:
        """Create an ordered list."""
        result: str = "\\begin{ordered}\n"
        for item in arg[0]:
            if isinstance(item, list):
                result += f"\\item {self.parse(item[0])}\n\n"
        result += "\\end{ordered}\n"
        return result

    def abstract(self, arg: Arguments) -> str:
        """Create an abstract."""
        return (
            "\\begin{abstract}\n\n"
            + self.parse(arg[0], in_block=True)
            + "\\end{abstract}\n\n"
        )

    def books(self, arg: Arguments) -> str:
        """Create a bibliography."""
        result: str = "\\begin{thebibliography}{0}\n\n"
        for item in arg[0]:
            if not isinstance(item, list):
                continue
            result += (
                f"\\bibitem{{{self.clear(item[0])}}} {self.parse(item[1])}\n\n"
            )
        result += "\\end{thebibliography}\n\n"
        return result

    @staticmethod
    def br(_: Arguments) -> str:
        """Add line break."""
        return r"\\"

    def cite(self, arg: Arguments) -> str:
        """Add a citation."""
        return rf"\cite{{{self.clear(arg[0])}}}"

    @staticmethod
    def math(arg: Arguments) -> str:
        """Add inline math."""
        return f"${''.join(arg[0])}$"

    @staticmethod
    def mathblock(arg: Arguments) -> str:
        """Add math block."""
        return rf"\[{''.join(arg[0])}\]"

    def item(self, arg: Arguments) -> str:
        """Add an item to a list."""
        return rf"\item{{{self.parse(arg[0])}}}"

    def size(self, _: Arguments) -> str:
        """Set font size."""
        raise TagNotImplementedError(DefaultTeX.size.__name__)

    def quote(self, _: Arguments) -> str:
        """Mark text as a block quote."""
        raise TagNotImplementedError(DefaultTeX.quote.__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser: ArgumentParser = ArgumentParser()

    parser.add_argument("-i", "--input", help="Moire input file", required=True)
    parser.add_argument("-o", "--output", help="output file", required=True)
    parser.add_argument("-f", "--format", help="output format", required=True)

    options: Namespace = parser.parse_args(sys.argv[1:])
    path: Path = Path(options.input)

    with path.open(encoding="utf-8") as input_file:
        converter: Moire = getattr(sys.modules[__name__], options.format)()
        output: str = converter.convert(input_file.read())

    if not output:
        logger.fatal("No output produced.")
        sys.exit(1)

    with path.with_suffix(options.output).open(
        "w+", encoding="utf-8"
    ) as output_file:
        output_file.write(output)
        logger.info("Converted to %s.", path.with_suffix(options.output))
