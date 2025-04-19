"""Default tag definitions."""

import sys
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace
from textwrap import dedent
from typing import Any, override

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

    def title(self, arg: Arguments) -> str:
        """Document title."""
        return ""

    @abstractmethod
    def body(self, arg: Arguments) -> str:
        """Body of the document."""
        raise TagNotImplementedError("body")

    @abstractmethod
    def header(self, arg: Arguments, level: int) -> str:
        """Header.

        Arguments: <header text> <header identifier>?
        """
        raise TagNotImplementedError("header")

    @abstractmethod
    def i(self, arg: Arguments) -> str:
        """Italic text."""
        raise TagNotImplementedError("i")

    @abstractmethod
    def b(self, arg: Arguments) -> str:
        """Bold text."""
        raise TagNotImplementedError("b")

    @abstractmethod
    def u(self, arg: Arguments) -> str:
        """Underlined text."""
        raise TagNotImplementedError("u")

    @abstractmethod
    def strike(self, arg: Arguments) -> str:
        """Strikethrough text."""
        raise TagNotImplementedError("strike")

    @abstractmethod
    def m(self, arg: Arguments) -> str:
        """Monospaced text."""
        raise TagNotImplementedError("m")

    @abstractmethod
    def table(self, arg: Arguments) -> str:
        """Simple table with rows and columns.

        Format: \\table {{<cell>} {<cell>} ...} {{<cell>} {<cell>} ...} ...

        This simple table does not support header, border style, text alignment,
        or cell merging.
        """
        raise TagNotImplementedError("table")

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
    def code(self, arg: Arguments) -> str:
        """Code block.

        Arguments: <language identifier>? <code>

        Examples of language identifiers: `cpp` for C++, `python` for Python,
        `js` or `javascript` for JavaScript.
        """
        raise TagNotImplementedError("code")

    def list__(self, arg: Arguments) -> str:
        """List of items."""
        raise TagNotImplementedError("list")

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
        return arg[0][0]

    @staticmethod
    def _get_ref(link: str, text: str) -> str:
        """Get reference to a link."""
        raise NotImplementedError


class DefaultHTML(Default):
    """Default HTML format."""

    name: str = "HTML"
    id_: str = "html"
    extensions: list[str] = ["html", "htm"]
    escape_symbols: dict[str, str] = {"<": "&lt;", ">": "&gt;"}
    block_tags = BLOCK_TAGS

    def __init__(self) -> None:
        super().__init__()

    def escape(self, text: str) -> str:
        return super().escape(text.replace("&", "&amp;"))

    def block(self, arg: Arguments) -> str:
        """Block element."""
        return self.parse(arg[0], in_block=True)

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

    @override
    def code(self, arg: Arguments) -> str:
        code_, _ = self._parse_code_arguments(arg)
        return f"<pre><tt>{code_}</tt></pre>"

    @override
    def title(self, arg: Arguments) -> str:
        return f"<title>{self.parse(arg[0])}</title>"

    @override
    def header(self, arg: Arguments, level: int) -> str:
        id_: str = "" if len(arg) <= 1 else f' id="{self.clear(arg[1])}"'
        return f"<h{level}{id_}>{self.parse(arg[0])}</h{level}>"

    @override
    def list__(self, arg: Arguments) -> str:
        items: str = "".join(f"<li>{self.parse(x)}</li>" for x in arg)
        return f"<ul>{items}</ul>"

    def image(self, arg: Arguments) -> str:
        title: str = f' alt="{self.parse(arg[1])}"' if len(arg) >= 2 else ""
        return f'<img src="{self.clear(arg[0])}"{title} />'

    @override
    def table(self, arg: Arguments) -> str:
        result: str = ""

        for row in arg:
            cells: str = "".join(
                [f"<td>{self.parse(cell, in_block=True)}</td>" for cell in row]
            )
            result += f"<tr>{cells}</tr>"

        return f"<table>{result}</table>"

    # Inner tags.

    @override
    def b(self, arg: Arguments) -> str:
        return f"<b>{self.parse(arg[0])}</b>"

    @staticmethod
    def br(_: Arguments) -> str:
        """Line break."""
        return "<br />"

    @staticmethod
    def _get_ref(link: str, text: str) -> str:
        return f'<a href="{link}">{text}</a>'

    @override
    def ref(self, arg: Arguments) -> str:
        link: str = self.parse(arg[0])
        return self._get_ref(
            link, link if len(arg) == 1 else self.parse(arg[1])
        )

    @override
    def i(self, arg: Arguments) -> str:
        return f"<i>{self.parse(arg[0])}</i>"

    def size(self, arg: Arguments) -> str:
        """Font size."""
        return f'<span style="font-size: {arg[0]}">{self.parse(arg[1])}</span>'

    @override
    def strike(self, arg: Arguments) -> str:
        return f"<s>{self.parse(arg[0])}</s>"

    def sc(self, arg: Arguments) -> str:
        """Small capital letters."""
        return (
            f'<span style="font-variant: small-caps;">{self.parse(arg[0])}'
            f"</span>"
        )

    def sub(self, arg: Arguments) -> str:
        """Subscript."""
        return f"<sub>{self.parse(arg[0])}</sub>"

    def super(self, arg: Arguments) -> str:
        """Superscript."""
        return f"<sup>{self.parse(arg[0])}</sup>"

    def text(self, arg: Arguments) -> str:
        """Paragraph."""
        return f"<p>{self.parse(arg[0])}</p>"

    @override
    def m(self, arg: Arguments) -> str:
        return f"<code>{self.parse(arg[0])}</code>"

    @override
    def u(self, arg: Arguments) -> str:
        return f"<u>{self.parse(arg[0])}</u>"

    def quote(self, arg: Arguments) -> str:
        """Block quote."""
        return f"<blockquote>{self.parse(arg[0])}</blockquote>"


class DefaultText(Default):
    """Plain text."""

    name: str = "Text"
    id_: str = "text"
    extension: str = "txt"
    escape_symbols: dict[str, str] = {}

    @override
    def body(self, arg: Arguments) -> str:
        return self.parse(arg[0], in_block=True, depth=1) + "\n"

    @override
    def title(self, arg: Arguments) -> str:
        return self.parse(arg[0])

    @override
    def code(self, arg: Arguments) -> str:
        code_, _ = self._parse_code_arguments(arg)
        return code_ + "\n"

    @override
    def header(self, arg: Arguments, level: int) -> str:
        return "  " * (level - 1) + self.parse(arg[0], depth=depth + 1)

    @override
    def image(self, arg: Arguments) -> str:
        return f"[{self.parse(arg[1]) if len(arg) > 1 else ''}]"

    def list__(self, arg: Arguments) -> str:
        s = ""
        for item in arg:
            if isinstance(item, list):
                s += "  * " + self.parse(item, in_block=True, depth=depth + 1)
        return s

    @override
    def table(self, arg: Arguments) -> str:
        widths: list[int] = []
        for row in arg:
            parsed: list[str] = [self.parse(cell) for cell in row]
            for index, cell in enumerate(parsed):
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
                result += (
                    " " + parsed + " " * (widths[index] - len(parsed)) + " |"
                )
            result += "\n"
        result += ruler + "\n"

        return result

    def b(self, arg: Arguments) -> str:
        return self.parse(arg[0], depth=depth + 1)

    @staticmethod
    def _get_ref(link: str, text: str) -> str:
        return f"{text} + ({link})"

    @override
    def ref(self, arg: Arguments) -> str:
        return self._get_ref(self.clear(arg[0]), self.parse(arg[1]))

    @override
    def i(self, arg: Arguments) -> str:
        return self.parse(arg[0], depth=depth + 1)

    @override
    def size(self, arg: Arguments) -> str:
        return self.parse(arg[0], depth=depth + 1)

    @override
    def strike(self, arg: Arguments) -> str:
        return self.parse(arg[0], depth=depth + 1)

    @override
    def sc(self, arg: Arguments) -> str:
        return self.parse(arg[0], depth=depth + 1)

    @override
    def sub(self, arg: Arguments) -> str:
        return self.parse(arg[0], depth=depth + 1)

    @override
    def super(self, arg: Arguments) -> str:
        return self.parse(arg[0], depth=depth + 1)

    @override
    def text(self, arg: Arguments) -> str:
        return self.parse(arg[0], depth=depth + 1) + "\n\n"

    @override
    def m(self, arg: Arguments) -> str:
        return self.parse(arg[0], depth=depth + 1)

    @override
    def u(self, arg: Arguments) -> str:
        return self.parse(arg[0], depth=depth + 1)


class DefaultMarkdown(Default):
    """Markdown."""

    name = "Markdown"
    id_: str = "markdown"
    extensions = ["md", "markdown"]
    block_tags = BLOCK_TAGS

    def __init__(self) -> None:
        super().__init__()
        self.list_level = 0

    def block(self, arg: Arguments) -> str:
        return self.parse(arg[0], in_block=True)

    def body(self, arg: Arguments) -> str:
        return (
            self.parse(arg[0], in_block=True)
            .replace("\n\n\n", "\n\n")
            .replace("\n\n\n", "\n\n")
        )

    def header(self, arg: Arguments, number: int) -> str:
        return f"{number * '#'} {self.parse(arg[0])}"

    def list__(self, arg: Arguments) -> str:
        self.list_level += 1
        s: str = "".join(
            ("\n" + "  " * self.list_level + f"* {self.parse(item)}")
            for item in arg
        )
        self.list_level -= 1
        return s

    @override
    def table(self, arg: Arguments) -> str:
        result: str = ""
        for index, row in enumerate(arg):
            if isinstance(row, list):
                result += "|"
                for cell in row:
                    if isinstance(cell, list):
                        result += " " + self.parse(cell) + " |"
                result += "\n"
                if index == 0:
                    result += "|"
                    for cell in row:
                        if isinstance(cell, list):
                            result += "---|"
                    result += "\n"
        return result

    def b(self, arg: Arguments) -> str:
        return "**" + self.parse(arg[0]) + "**"

    def code(self, arg: Arguments) -> str:
        code_, language = self._parse_code_arguments(arg)
        return f"```{language}\n{code_}\n```"

    def _get_ref(self, link: str, text: str) -> str:
        return f"[{text}]({link})"

    def ref(self, arg: Arguments) -> str:
        return self._get_ref(self.parse(arg[0]), self.parse(arg[1]))

    def i(self, arg: Arguments) -> str:
        return "*" + self.parse(arg[0]) + "*"

    def image(self, arg: Arguments) -> str:
        if len(arg) > 1:
            return f"![{self.parse(arg[1])}]({self.parse(arg[0])})"
        else:
            return f"![{self.parse(arg[0])}]({self.parse(arg[0])})"

    def m(self, arg: Arguments) -> str:
        return f"`{self.parse(arg[0])}`"

    def u(self, arg: Arguments) -> str:
        return self.parse(arg[0])

    def strike(self, arg: Arguments) -> str:
        return f"~~{self.parse(arg[0])}~~"

    def sub(self, arg: Arguments) -> str:
        return DefaultHTML.sub(self, arg[0])

    def super(self, arg: Arguments) -> str:
        return DefaultHTML.super(self, arg[0])

    def text(self, arg: Arguments) -> str:
        return self.parse(arg[0]) + "\n\n"

    def quote(self, arg: Arguments) -> str:
        return "> " + self.parse(arg[0])


class DefaultWiki(Default):
    """Wiki syntax of Wikipedia."""

    name = "Wiki"
    id_: str = "wiki"
    extensions = ["wiki"]
    block_tags = BLOCK_TAGS

    def block(self, arg: Arguments) -> str:
        return self.parse(arg[0], in_block=True)

    def body(self, arg: Arguments) -> str:
        return (
            self.parse(arg[0], in_block=True)
            .replace("\n\n\n", "\n\n")
            .replace("\n\n\n", "\n\n")
        )

    def header(self, arg: Arguments, number: int) -> str:
        return (number * "=") + " " + self.parse(arg[0]) + " " + (number * "=")

    def list__(self, arg: Arguments) -> str:
        s = ""
        for item in arg:
            if isinstance(item, list):
                s += "* " + self.parse(item) + "\n"
        return s

    @override
    def table(self, arg: Arguments) -> str:
        result: str = (
            '{| class="wikitable" border="1" cellspacing="0" cellpadding="2"\n'
            "! Tag || Rendering\n"
        )
        for row in arg:
            result += "|-\n"
            for cell in row:
                result += "| " + self.parse(cell) + "\n"
        return result + "|}\n"

    def b(self, arg: Arguments) -> str:
        return f"'''{self.parse(arg[0])}'''"

    def code(self, arg: Arguments) -> str:
        code_, language = self._parse_code_arguments(arg)
        if language:
            return (
                f'<syntaxhighlight lang="{language}">'
                f"\n{code_}\n</syntaxhighlight>"
            )
        else:
            return f"<pre><tt>{code_}\n</tt></pre>"

    def _get_ref(self, link: str, text: str) -> str:
        return f"[[{link}|{text}]]"

    def ref(self, arg: Arguments) -> str:
        return self._get_ref(self.clear(arg[0]), self.parse(arg[1]))

    def i(self, arg: Arguments) -> str:
        return f"''{self.parse(arg[0])}''"

    def image(self, arg: Arguments) -> str:
        return (
            "[[File:"
            + self.parse(arg[0])
            + "|thumb|"
            + self.parse(arg[1])
            + "]]"
        )

    def m(self, arg: Arguments) -> str:
        return "<code>" + str(self.parse(arg[0])) + "</code>"

    def u(self, arg: Arguments) -> str:
        return f"<u>{self.parse(arg[0])}</u>"

    def text(self, arg: Arguments) -> str:
        return self.parse(arg[0]) + "\n\n"

    def quote(self, arg: Arguments) -> str:
        return ">" + self.parse(arg[0]) + ""


class DefaultTeX(Default):
    """TeX syntax."""

    name = "Tex"
    id_: str = "tex"
    extension = "tex"

    escape_symbols = {"_": "\\_"}
    block_tags = BLOCK_TAGS
    headers: list[str] = [
        "section", "subsection", "subsubsection", "paragraph", "subparagraph"
    ]  # fmt: skip

    def body(self, arg: Arguments) -> str:
        s = dedent(
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
        s += self.parse(arg[0], in_block=True)
        s += "\\end {document}"
        return s

    def title(self, arg: Arguments) -> str:
        s = f"\\title{{{self.parse(arg[0])}}}\n"
        s += "\\maketitle"
        return s

    def author(self, arg: Arguments) -> str:
        return f"\\author{{{self.parse(arg[0])}}}"

    def header(self, arg: Arguments, number: int) -> str:
        if number < 6:
            return f"\\{self.headers[number - 1]}{{{self.parse(arg[0])}}}"
        return self.parse(arg[0])

    @override
    def table(self, arg: Arguments) -> str:
        result: str = "\\begin{table}[h]\n\\begin{center}\n\\begin{tabular}"

        max_columns: int = 0
        for tr in arg:
            if isinstance(tr, list):
                columns: int = 0
                for td in tr:
                    if isinstance(td, list):
                        columns += 1
                max_columns = max(max_columns, columns)

        result += "{|" + ("l|" * max_columns) + "}\n\\hline\n"

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

    def list__(self, arg: Arguments) -> str:
        s = "\\begin{itemize}\n"
        for item in arg:
            s += f"\\item {self.parse(item)}\n\n"
        s += "\\end{itemize}\n"
        return s

    def ordered(self, arg: Arguments) -> str:
        s = "\\begin{ordered}\n"
        for item in arg[0]:
            if isinstance(item, list):
                s += f"\\item {self.parse(item[0])}\n\n"
        s += "\\end{ordered}\n"
        return s

    def abstract(self, arg: Arguments) -> str:
        return (
            "\\begin{abstract}\n\n"
            + self.parse(arg[0], in_block=True)
            + "\\end{abstract}\n\n"
        )

    def books(self, arg: Arguments) -> str:
        s = "\\begin{thebibliography}{0}\n\n"
        for item in arg[0]:
            if isinstance(item, list):
                s += (
                    "\\bibitem{"
                    + self.clear(item[0])
                    + "} "
                    + self.parse(item[1])
                    + "\n\n"
                )
        s += "\\end{thebibliography}\n\n"
        return s

    def b(self, arg: Arguments) -> str:
        return f"{{\\bf {self.parse(arg[0])}}}"

    @staticmethod
    def br(_: Arguments) -> str:
        return "\\\\"

    def cite(self, arg: Arguments) -> str:
        return "\\cite {" + self.clear(arg[0]) + "}"

    def code(self, arg: Arguments) -> str:
        code_, language = self._parse_code_arguments(arg)
        return f"\\begin{{verbatim}}{code_}\\end{{verbatim}}"

    def date(self, arg: Arguments) -> str:
        return ""

    def ref(self, arg: Arguments) -> str:
        s = ""
        link = self.clear(arg[0])
        if link[0] == "#":
            link = link[1:]
        if len(arg) == 1:
            s += f"\\href {{{link}}} {{{link}}}"
        else:
            s += f"\\href {{{link}}} {{{self.parse(arg[1])}}}"
        return s

    def i(self, arg: Arguments) -> str:
        return f"{{\\em {self.parse(arg[0])}}}"

    @staticmethod
    def math(arg: Arguments) -> str:
        return f"${''.join(arg[0])}$"

    @staticmethod
    def mathblock(arg: Arguments) -> str:
        return "\\[{0}\\]".format("".join(arg[0]))

    def ignore(self, arg: Arguments) -> str:
        return self.clear(arg[0])

    def image(self, arg: Arguments) -> str:
        s = (
            "\\begin{figure}[h]\\begin{center}\\includegraphics{"
            + self.parse(arg[0])
            + "}\\end{center}"
        )
        if len(arg) > 1:
            s += "\\caption {" + self.parse(arg[1]) + "}"
        s += "\\end{figure}"
        return s

    def item(self, arg: Arguments) -> str:
        return "\\item " + self.parse(arg[0]) + ""

    def sc(self, arg: Arguments) -> str:
        return "{\\sc " + self.parse(arg[0]) + "}"

    def size(self, arg: Arguments) -> str:
        return "" + self.parse(arg[0]) + ""

    def strike(self, arg: Arguments) -> str:
        return "" + self.parse(arg[0]) + ""

    def sub(self, arg: Arguments) -> str:
        return "$_{" + self.parse(arg[0]) + "}$"

    def super(self, arg: Arguments) -> str:
        return "\\textsuperscript{" + self.parse(arg[0]) + "}"

    def text(self, arg: Arguments) -> str:
        return self.parse(arg[0]) + "\n\n"

    def m(self, arg: Arguments) -> str:
        return "{\\tt " + self.parse(arg[0]) + "}"

    def u(self, arg: Arguments) -> str:
        return "" + self.parse(arg[0]) + ""

    def quote(self, arg: Arguments) -> str:
        return "" + self.parse(arg[0]) + ""


if __name__ == "__main__":
    parser: ArgumentParser = ArgumentParser()

    parser.add_argument("-i", "--input", help="Moire input file", required=True)
    parser.add_argument("-o", "--output", help="output file", required=True)
    parser.add_argument("-f", "--format", help="output format", required=True)

    options: Namespace = parser.parse_args(sys.argv[1:])

    with open(options.input, "r") as input_file:
        converter: Moire = getattr(sys.modules[__name__], options.format)()
        output: str = converter.convert(input_file.read())

    if not output:
        print("Fatal: output was no produced.")
        sys.exit(1)

    with open(options.output, "w+") as output_file:
        output_file.write(output)
        print(f"Converted to {options.output}.")
