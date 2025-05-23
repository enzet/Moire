"""Default tag definitions."""

import logging
import sys
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from pathlib import Path
from textwrap import dedent
from typing import Any, ClassVar, override

from moire.moire import Moire

__author__ = "Sergey Vartanov"
__email__ = "me@enzet.ru"

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
        return f"Tag \\{self.tag} is not implemented in the parser"


class Default(Moire, ABC):
    """Default tag declaration."""

    def __init__(self) -> None:
        super().__init__()

    # Main methods.

    @abstractmethod
    def body(self, arg: Arguments) -> str:
        """Body of the document."""
        raise TagNotImplementedError("body")

    # Metadata tags.

    @abstractmethod
    def title(self, arg: Arguments) -> str:
        """Title of the document.

        This is metadata tag and is not displayed in the document.
        """
        raise TagNotImplementedError("title")

    @abstractmethod
    def author(self, arg: Arguments) -> str:
        """Author of the document.

        This is metadata tag and is not displayed in the document.
        """
        raise TagNotImplementedError("author")

    @abstractmethod
    def date(self, arg: Arguments) -> str:
        """Date of the document.

        This is metadata tag and is not displayed in the document.
        """
        raise TagNotImplementedError("date")

    # Main formatting tags.

    @abstractmethod
    def header(self, arg: Arguments, level: int) -> str:
        """Header.

        Arguments: <header text> <header identifier>?
        """
        raise TagNotImplementedError("header")

    @abstractmethod
    def e(self, arg: Arguments) -> str:
        """Emphasized text."""
        raise TagNotImplementedError("e")

    @abstractmethod
    def s(self, arg: Arguments) -> str:
        """Strong emphasized text."""
        raise TagNotImplementedError("s")

    def b(self, arg: Arguments) -> str:
        """Bold text.

        This tag is deprecated. Now it is an alias for `\\s`.
        """
        return self.s(arg)

    def i(self, arg: Arguments) -> str:
        """Italic text.

        This tag is deprecated. Now it is an alias for `\\e`.
        """
        return self.e(arg)

    @abstractmethod
    def c(self, arg: Arguments) -> str:
        """Inline code."""
        raise TagNotImplementedError("c")

    def m(self, arg: Arguments) -> str:
        """Monospaced text.

        This tag is deprecated. Now it is an alias for `\\c`.
        """
        return self.c(arg)

    @abstractmethod
    def del__(self, arg: Arguments) -> str:
        """Deleted text."""
        raise TagNotImplementedError("del")

    @abstractmethod
    def sub(self, arg: Arguments) -> str:
        """Subscript."""
        raise TagNotImplementedError("sub")

    @abstractmethod
    def super(self, arg: Arguments) -> str:
        """Superscript."""
        raise TagNotImplementedError("super")

    # Main block tags.

    @abstractmethod
    def list__(self, arg: Arguments) -> str:
        """List of items."""
        raise TagNotImplementedError("list")

    @abstractmethod
    def table(self, arg: Arguments) -> str:
        """Simple table with rows and columns.

        Format: \\table {{<cell>} {<cell>} ...} {{<cell>} {<cell>} ...} ...

        This simple table does not support header, border style, text alignment,
        or cell merging.
        """
        raise TagNotImplementedError("table")

    @abstractmethod
    def image(self, arg: Arguments) -> str:
        """Image.

        Format: \\image {<image source>} {<image title>}?
        """
        raise TagNotImplementedError("image")

    @abstractmethod
    def code(self, arg: Arguments) -> str:
        """Code block.

        Arguments: <language identifier>? <code>

        Examples of language identifiers: `cpp` for C++, `python` for Python,
        `js` or `javascript` for JavaScript.
        """
        raise TagNotImplementedError("code")

    def formal(self, arg: Arguments) -> str:
        """Formal argument inside code.

        E.g. in text "Run command `ssh <username>@<host>`", the `<username>`
        and `<host>` are formal arguments.

        By default, the formal argument is wrapped in with `<` and `>`.
        """
        return f"<{self.parse(arg[0])}>"

    def _parse_code_arguments(self, arg: Arguments) -> tuple[str, str]:
        """Parse trimmed code and possible language identifier."""
        if len(arg) == 1:
            return self.trim(self.parse(arg[0], spec={"trim": False})), ""

        return (
            self.trim(self.parse(arg[1], spec={"trim": False})),
            self.clear(arg[0]),
        )

    @abstractmethod
    def ref(self, arg: Arguments) -> str:
        """Hypertext reference.

        Arguments: <reference> <text>?

        If reference starts with `#`, Moire will try to create a reference to
        the declared header or label with this identifier. E.g. if we have a
        header `\\3 {Header} {test}` or label `\\label {test}`, valid references
        for both of them will be `\\ref {#test} {reference text}`.
        """
        raise TagNotImplementedError("ref")

    def nospell(self, arg: Arguments) -> str:
        """Text that shouldn't be checked for spelling.

        This method will do nothing and just resume the process of parsing its
        content, it is an indication to the Moire code viewer or editor not to
        check the content for spelling with automatic tools.
        """
        return self.parse(arg[0])

    def ignore(self, arg: Arguments) -> str:
        """Return only the first argument of a tag."""
        return self.clear(arg[0])

    @staticmethod
    def _get_ref(link: str, text: str) -> str:
        """Get reference to a link."""
        raise NotImplementedError


class DefaultHTML(Default):
    """Default HTML format."""

    name: str = "HTML"
    id_: str = "html"
    extensions: ClassVar[list[str]] = ["html", "htm"]
    escape_symbols: ClassVar[dict[str, str]] = {"<": "&lt;", ">": "&gt;"}
    block_tags: ClassVar[set[str]] = BLOCK_TAGS

    def __init__(self) -> None:
        super().__init__()

    # Parser methods.

    @override
    def escape(self, text: str) -> str:
        return super().escape(text.replace("&", "&amp;"))

    # Main methods.

    @override
    def body(self, arg: Arguments) -> str:
        """Body of the document."""

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
        title: str = f' alt="{self.parse(arg[1])}"' if len(arg) >= 2 else ""
        return f'<img src="{self.clear(arg[0])}"{title} />'

    @override
    def code(self, arg: Arguments) -> str:
        code_, _ = self._parse_code_arguments(arg)
        return f"<pre><tt>{code_}</tt></pre>"

    @staticmethod
    def br(_: Arguments) -> str:
        """Line break."""
        return "<br />"

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

    def size(self, arg: Arguments) -> str:
        """Font size."""
        return f'<span style="font-size: {arg[0]}">{self.parse(arg[1])}</span>'

    def text(self, arg: Arguments) -> str:
        """Paragraph."""
        return f"<p>{self.parse(arg[0])}</p>"

    def quote(self, arg: Arguments) -> str:
        """Block quote."""
        return f"<blockquote>{self.parse(arg[0])}</blockquote>"


class DefaultText(Default):
    """Plain text."""

    name: str = "Text"
    id_: str = "text"
    extension: str = "txt"
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

    @override
    @staticmethod
    def _get_ref(link: str, text: str) -> str:
        return f"{text} ({link})"

    @override
    def ref(self, arg: Arguments) -> str:
        return DefaultText._get_ref(self.clear(arg[0]), self.parse(arg[1]))


class DefaultMarkdown(Default):
    """Markdown.

    Markdown formatter based on CommonMark specification 0.31.2 (28 January
    2024).

    See https://spec.commonmark.org/0.31.2/
    """

    name: str = "Markdown"
    id_: str = "markdown"
    extensions: ClassVar[list[str]] = ["md", "markdown"]
    block_tags: ClassVar[set[str]] = BLOCK_TAGS

    def __init__(
        self, is_html: bool = True, is_github_flavored: bool = False
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
        # FIXME: rewrite.
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

    # Main formatting tags.

    @override
    def header(self, arg: Arguments, level: int) -> str:
        """We use simplest possible ATX header style."""

        # CommonMark specification allows headers from level 1 to 6.
        # TODO: add warning if level is greater than 6.
        level = min(level, 6)

        return f"{level * '#'} {self.parse(arg[0])}"

    @override
    def s(self, arg: Arguments) -> str:
        # TODO: add weak warning, bold is actually "strong emphasis" in
        # CommonMark.
        return f"**{self.parse(arg[0])}**"

    @override
    def e(self, arg: Arguments) -> str:
        # TODO: add weak warning, italic is actually "emphasis" in CommonMark.
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
        # TODO: add warning, tag is ignored.
        return self.parse(arg[0])

    @override
    def sub(self, arg: Arguments) -> str:
        if self.is_html:
            return f"<sub>{self.parse(arg[0])}</sub>"
        # TODO: add warning, tag is ignored.
        return self.parse(arg[0])

    @override
    def super(self, arg: Arguments) -> str:
        if self.is_html:
            return f"<sup>{self.parse(arg[0])}</sup>"
        # TODO: add warning, tag is ignored.
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

    @override
    @staticmethod
    def _get_ref(link: str, text: str) -> str:
        return f"[{text}]({link})"

    def ref(self, arg: Arguments) -> str:
        return DefaultMarkdown._get_ref(self.parse(arg[0]), self.parse(arg[1]))

    def text(self, arg: Arguments) -> str:
        return self.parse(arg[0]) + "\n\n"

    def quote(self, arg: Arguments) -> str:
        return f"> {self.parse(arg[0])}"


class DefaultWiki(Default):
    """Wiki syntax of Wikipedia."""

    name = "Wiki"
    id_: str = "wiki"
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
        return DefaultHTML.sub(self, arg[0])  # type: ignore

    @override
    def super(self, arg: Arguments) -> str:
        return DefaultHTML.super(self, arg[0])  # type: ignore

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
        else:
            return f"<pre><tt>{code_}\n</tt></pre>"

    @override
    @staticmethod
    def _get_ref(link: str, text: str) -> str:
        return f"[[{link}|{text}]]"

    def ref(self, arg: Arguments) -> str:
        return DefaultWiki._get_ref(self.clear(arg[0]), self.parse(arg[1]))

    def text(self, arg: Arguments) -> str:
        return self.parse(arg[0]) + "\n\n"

    def quote(self, arg: Arguments) -> str:
        return f">{self.parse(arg[0])}"


class DefaultTeX(Default):
    """TeX syntax."""

    name = "Tex"
    id_: str = "tex"
    extension = "tex"

    escape_symbols: ClassVar[dict[str, str]] = {"_": "\\_"}
    block_tags: ClassVar[set[str]] = BLOCK_TAGS
    headers: ClassVar[list[str]] = [
        "section", "subsection", "subsubsection", "paragraph", "subparagraph"
    ]  # fmt: skip

    # Main methods.

    @override
    def body(self, arg: Arguments) -> str:
        result: str = dedent(
            """\
            \\documentclass[twoside,psfig]{article}
            \\usepackage[utf8]{inputenc}
            \\usepackage[russian]{babel}
            \\usepackage{enumitem}
            \\usepackage{float}
            \\usepackage[margin=3cm,hmarginratio=1:1,top=32mm,columnsep=20pt]
                {geometry}
            \\usepackage{graphicx}
            \\usepackage{hyperref}
            \\usepackage{multicol}
            \\begin{document}
            """
        )
        result += self.parse(arg[0], in_block=True)
        result += "\\end {document}"
        return result

    # Metadata tags.

    @override
    def title(self, arg: Arguments) -> str:
        result: str = f"\\title{{{self.parse(arg[0])}}}\n"
        result += "\\maketitle"
        return result

    @override
    def author(self, arg: Arguments) -> str:
        return f"\\author{{{self.parse(arg[0])}}}"

    @override
    def date(self, arg: Arguments) -> str:
        return f"\\date{{{self.parse(arg[0])}}}"

    # Main formatting tags.

    @override
    def header(self, arg: Arguments, level: int) -> str:
        if level < 6:
            return f"\\{self.headers[level - 1]}{{{self.parse(arg[0])}}}"
        return self.parse(arg[0])

    @override
    def s(self, arg: Arguments) -> str:
        return f"{{\\bf {self.parse(arg[0])}}}"

    @override
    def e(self, arg: Arguments) -> str:
        return f"{{\\em {self.parse(arg[0])}}}"

    @override
    def c(self, arg: Arguments) -> str:
        return f"{{\\tt {self.parse(arg[0])}}}"

    @override
    def del__(self, arg: Arguments) -> str:
        raise TagNotImplementedError("del")

    @override
    def sub(self, arg: Arguments) -> str:
        return f"${{{self.parse(arg[0])}}}$"

    @override
    def super(self, arg: Arguments) -> str:
        return f"\\textsuperscript{{{self.parse(arg[0])}}}"

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
                columns: list[list[Any]] = []
                for column in row:
                    if isinstance(column, list):
                        columns.append(column)
                for column in columns[:-1]:
                    result += self.parse(column) + " & "
                result += self.parse(columns[-1])
                result += " \\\\\n\\hline\n"

        result += "\\end{tabular}\n\\end{center}\n\\end{table}\n"

        return result

    @override
    def image(self, arg: Arguments) -> str:
        result: str = (
            "\\begin{figure}[h]\\begin{center}\\includegraphics{"
            + self.parse(arg[0])
            + "}\\end{center}"
        )
        if len(arg) > 1:
            result += f"\\caption{{ {self.parse(arg[1])}}}"
        result += "\\end{figure}"
        return result

    @override
    def code(self, arg: Arguments) -> str:
        code_, _ = self._parse_code_arguments(arg)
        return f"\\begin{{verbatim}}{code_}\\end{{verbatim}}"

    def ordered(self, arg: Arguments) -> str:
        result: str = "\\begin{ordered}\n"
        for item in arg[0]:
            if isinstance(item, list):
                result += f"\\item {self.parse(item[0])}\n\n"
        result += "\\end{ordered}\n"
        return result

    def abstract(self, arg: Arguments) -> str:
        return (
            "\\begin{abstract}\n\n"
            + self.parse(arg[0], in_block=True)
            + "\\end{abstract}\n\n"
        )

    def books(self, arg: Arguments) -> str:
        result: str = "\\begin{thebibliography}{0}\n\n"
        for item in arg[0]:
            if isinstance(item, list):
                result += (
                    "\\bibitem{"
                    + self.clear(item[0])
                    + "} "
                    + self.parse(item[1])
                    + "\n\n"
                )
        result += "\\end{thebibliography}\n\n"
        return result

    @staticmethod
    def br(_: Arguments) -> str:
        return "\\\\"

    def cite(self, arg: Arguments) -> str:
        return f"\\cite{{{self.clear(arg[0])}}}"

    def ref(self, arg: Arguments) -> str:
        result: str = ""
        link = self.clear(arg[0])
        if link[0] == "#":
            link = link[1:]
        if len(arg) == 1:
            result += f"\\href {{{link}}} {{{link}}}"
        else:
            result += f"\\href {{{link}}} {{{self.parse(arg[1])}}}"
        return result

    @staticmethod
    def math(arg: Arguments) -> str:
        return f"${''.join(arg[0])}$"

    @staticmethod
    def mathblock(arg: Arguments) -> str:
        return f"\\[{''.join(arg[0])}\\]"

    def ignore(self, arg: Arguments) -> str:
        return self.clear(arg[0])

    def item(self, arg: Arguments) -> str:
        return f"\\item{{{self.parse(arg[0])}}}"

    def size(self, arg: Arguments) -> str:
        raise TagNotImplementedError("size")

    def text(self, arg: Arguments) -> str:
        return self.parse(arg[0]) + "\n\n"

    def quote(self, arg: Arguments) -> str:
        raise TagNotImplementedError("quote")


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
        logging.fatal("No output produced.")
        sys.exit(1)

    with path.with_suffix(options.output).open(
        "w+", encoding="utf-8"
    ) as output_file:
        output_file.write(output)
        logging.info("Converted to %s.", path.with_suffix(options.output))
