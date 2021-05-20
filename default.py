import argparse
import sys
from typing import Any, List, Set

from moire import Moire

__author__ = "Sergey Vartanov"
__email__ = "me@enzet.ru"

depth = 0
status = {}
BLOCK_TAGS: Set[str] = {
    "block", "body", "code", "title", "number", "list", "shortlist", "image",
    "table"
}


class DefaultHTML(Moire):
    """
    Default HTML format.
    """

    name = "HTML"
    extensions = ["html", "htm"]
    escape_symbols = {"<": "&lt;", ">": "&gt;"}
    block_tags = BLOCK_TAGS

    # Block tags.

    def escape(self, text: str) -> str:
        return super().escape(text.replace("&", "&amp;"))

    def block(self, arg: List[Any]) -> str:
        return self.parse(arg[0], inblock=True)

    def body(self, arg: List[Any]) -> str:
        status["content"] = []
        s = """<html>
            <head>
                <meta http-equiv="Content-Type" content="text/html;
                      charset=utf-8">
                <link rel="stylesheet" href="style.css">
            </head>
            <body>"""
        s += self.parse(arg[0], inblock=True)
        s += """    </body>
        </html>"""
        return s

    def code(self, arg: List[Any]) -> str:
        return f"<pre><tt>{self.clear(arg[0])}</tt></pre>"

    def title(self, arg: List[Any]) -> str:
        return f"<title>{self.parse(arg[0])}</title>"

    def header(self, arg, number):
        id_: str = ""
        if len(arg) > 1:
            id_ = f' id="{self.clear(arg[1])}"'
        return f"<h{number}{id_}>{self.parse(arg[0])}</h{number}>"

    def list(self, arg: List[Any]) -> str:
        items: List[str] = [f"<li>{self.parse(x)}</li>" for x in arg]
        return "<ul>" + "".join(items) + "</ul>"

    def image(self, arg: List[Any]) -> str:
        title: str = (f' alt="{self.parse(arg[1])}"' if len(arg) >= 2 else "")
        return f'<img src="{self.clear(arg[0])}"{title} />'

    def table(self, arg: List[Any]) -> str:
        content: str = ""
        for tr in arg:
            cell: str = "".join(
                ["<td>" + self.parse(td, inblock=True) + "</td>" for td in tr]
            )
            content += f"<tr>{cell}</tr>"
        return f"<table>{content}</table>"

    # Inner tags.

    def b(self, arg: List[Any]) -> str:
        return f"<b>{self.parse(arg[0])}</b>"

    @staticmethod
    def br(arg: List[Any]) -> str:
        return "<br />"

    @staticmethod
    def _get_href(link: str, text: str) -> str:
        return f'<a href="{link}">{text}</a>'

    def href(self, arg: List[Any]) -> str:
        return self._get_href(self.clear(arg[0]), self.parse(arg[1]))

    def i(self, arg: List[Any]) -> str:
        return f"<i>{self.parse(arg[0])}</i>"

    def size(self, arg: List[Any]) -> str:
        return f'<span style="font-size: {arg[0]}">{self.parse(arg[1])}</span>'

    def strike(self, arg: List[Any]) -> str:
        return f"<s>{self.parse(arg[0])}</s>"

    def sc(self, arg: List[Any]) -> str:
        return f'<span style="font-variant: small-caps;">{self.parse(arg[0])}</span>'

    def sub(self, arg: List[Any]) -> str:
        return f"<sub>{self.parse(arg[0])}</sub>"

    def super(self, arg: List[Any]) -> str:
        return f"<sup>{self.parse(arg[0])}</sup>"

    def text(self, arg: List[Any]) -> str:
        return f"<p>{self.parse(arg[0])}</p>"

    def tt(self, arg: List[Any]) -> str:
        return f"<tt>{self.parse(arg[0])}</tt>"

    def u(self, arg: List[Any]) -> str:
        return f"<u>{self.parse(arg[0])}</u>"

    def quote(self, arg: List[Any]) -> str:
        return f"<blockquote>{self.parse(arg[0])}</blockquote>"


class DefaultText(Moire):
    """
    Plain text.
    """

    name = "Text"
    extension = "txt"
    escape_symbols = {}

    def body(self, arg: List[Any]) -> str:
        def justify(text, width):
            k = ""
            i = 0
            for a in text:
                k += a
                if i % width == 0:
                    k += "\n"
                i += 1
            return k

        return self.parse(arg[0], inblock=True, depth=1) + "\n"

    def code(self, arg: List[Any]) -> str:
        return self.clear(arg[0]) + "\n"

    def header(self, arg, number):
        return "  " * (number - 1) + self.parse(arg[0], depth=depth + 1)

    def image(self, arg) -> str:
        return f"[{self.parse(arg[1]) if len(arg) > 1 else ''}]"

    def list(self, arg: List[Any]) -> str:
        s = ""
        for item in arg:
            if isinstance(item, list):
                s += "  * " + self.parse(item, inblock=True, depth=depth + 1)
        return s

    def table(self, arg: List[Any]) -> str:
        widths: List[int] = []
        for tr in arg:
            parsed = [self.parse(td) for td in tr]
            for index, cell in enumerate(parsed):
                if len(widths) - 1 < index:
                    widths.append(len(cell))
                else:
                    widths[index] = max(widths[index], len(cell))

        ruler = "+" + "+".join(["-" * (x + 2) for x in widths]) + "+"

        s = ruler + "\n"
        for tr in arg:
            s += "|"
            for index, td in enumerate(tr):
                parsed = self.parse(td)
                s += " " + parsed + " " * (widths[index] - len(parsed)) + " |"
            s += "\n"
        s += ruler + "\n"

        return s

    def b(self, arg: List[Any]) -> str:
        return self.parse(arg[0], depth=depth + 1)

    def _get_href(self, link, text):
        return f"{text} + ({link})"

    def href(self, arg: List[Any]) -> str:
        return self._get_href(self.clear(arg[0]), self.parse(arg[1]))

    def i(self, arg: List[Any]) -> str:
        return self.parse(arg[0], depth=depth + 1)

    def size(self, arg: List[Any]) -> str:
        return self.parse(arg[0], depth=depth + 1)

    def strike(self, arg: List[Any]) -> str:
        return self.parse(arg[0], depth=depth + 1)

    def sc(self, arg: List[Any]) -> str:
        return self.parse(arg[0], depth=depth + 1)

    def sub(self, arg: List[Any]) -> str:
        return self.parse(arg[0], depth=depth + 1)

    def super(self, arg: List[Any]) -> str:
        return self.parse(arg[0], depth=depth + 1)

    def text(self, arg: List[Any]) -> str:
        return self.parse(arg[0], depth=depth + 1) + "\n\n"

    def tt(self, arg: List[Any]) -> str:
        return self.parse(arg[0], depth=depth + 1)

    def u(self, arg: List[Any]) -> str:
        return self.parse(arg[0], depth=depth + 1)


# Plain text without formatting.


class DefaultRawText(Moire):
    name = "Text"
    extension = "txt"

    escape_symbols = {
        "<": "&lt;",
    }
    block_tags = BLOCK_TAGS

    def body(self, arg: List[Any]) -> str:
        def justify(text, width):
            k = ""
            i = 0
            for a in text:
                k += a
                if i % width == 0:
                    k += "\n"
                i += 1
            return k

        return self.parse(arg[0], inblock=True, depth=1) + "\n"

    def header(self, arg, number):
        return self.parse(arg[0])

    def list(self, arg: List[Any]) -> str:
        s = ""
        for item in arg[0]:
            if isinstance(item, list):
                s += "  * " + self.parse(item, inblock=True, depth=depth + 1)
        return s

    def table(self, arg: List[Any]) -> str:
        s = ""
        for tr in arg[0]:
            for td in tr:
                s += " " + self.parse(td, inblock=True, depth=depth + 1) + " |"
            s += "\n"
        return s

    def b(self, arg: List[Any]) -> str:
        return self.parse(arg[0])

    def href(self, arg: List[Any]) -> str:
        return self.parse(arg[1])

    def i(self, arg: List[Any]) -> str:
        return self.parse(arg[0])

    def size(self, arg: List[Any]) -> str:
        return self.parse(arg[0])

    def strike(self, arg: List[Any]) -> str:
        return self.parse(arg[0])

    def sc(self, arg: List[Any]) -> str:
        return self.parse(arg[0])

    def sub(self, arg: List[Any]) -> str:
        return self.parse(arg[0])

    def super(self, arg: List[Any]) -> str:
        return self.parse(arg[0])

    def text(self, arg: List[Any]) -> str:
        return self.parse(arg[0]) + "\n\n"

    def u(self, arg: List[Any]) -> str:
        return self.parse(arg[0])


# Markdown.


class DefaultMarkdown(Moire):
    name = "Markdown"
    extensions = ["md", "markdown"]
    block_tags = BLOCK_TAGS

    level = 0

    def block(self, arg: List[Any]) -> str:
        return self.parse(arg[0], inblock=True)

    def body(self, arg: List[Any]) -> str:
        counter = []
        return (
            self.parse(arg[0], inblock=True)
            .replace("\n\n\n", "\n\n")
            .replace("\n\n\n", "\n\n")
        )

    def header(self, arg, number):
        s = ""
        if number == 1:
            parsed = self.parse(arg[0])
            s += parsed + "\n" + "=" * len(parsed)
        elif number == 2:
            parsed = self.parse(arg[0])
            s += parsed + "\n" + "-" * len(parsed)
        else:
            s += (
                (number * "#") + " " + self.parse(arg[0]) + " " + (number * "#")
            )
        return s

    def list(self, arg: List[Any]) -> str:
        s = ""
        for item in arg:
            if isinstance(item, list):
                s += "  * " + self.parse(item) + "\n"
        return s

    def shortlist(self, arg: List[Any]) -> str:
        s = ""
        n = 0
        for item in arg:
            if isinstance(item, list):
                n += 1
                self.level += 1
                s += (
                    "\n"
                    + ("   " * (self.level - 1))
                    + "* "
                    + self.parse(item)
                    + "\n"
                )
                self.level -= 1
        return s

    def table(self, arg: List[Any]) -> str:
        s = ""
        for index, tr in enumerate(arg):
            if isinstance(tr, list):
                s += "|"
                for td in tr:
                    if isinstance(td, list):
                        s += " " + self.parse(td) + " |"
                s += "\n"
                if index == 0:
                    s += "|"
                    for td in tr:
                        if isinstance(td, list):
                            s += "---|"
                    s += "\n"
        return s

    def b(self, arg: List[Any]) -> str:
        return "**" + self.parse(arg[0]) + "**"

    def code(self, arg: List[Any]) -> str:
        s: str = "```"
        if len(arg) > 1:
            s += self.clear(arg[1])
        s += f"\n{self.clear(arg[0])}\n```"
        return s

    def _get_href(self, link: str, text: str) -> str:
        return f"[{text}]({link})"

    def href(self, arg: List[Any]) -> str:
        return self._get_href(self.parse(arg[0]), self.parse(arg[1]))

    def i(self, arg: List[Any]) -> str:
        return "*" + self.parse(arg[0]) + "*"

    def image(self, arg: List[Any]) -> str:
        return "![" + self.parse(arg[1]) + "](" + self.parse(arg[0]) + ")"

    def formal(self, arg: List[Any]) -> str:
        return "<" + self.parse(arg[0]) + ">"

    def tt(self, arg: List[Any]) -> str:
        return "`" + str(self.parse(arg[0])) + "`"

    def u(self, arg: List[Any]) -> str:
        pass

    def text(self, arg: List[Any]) -> str:
        return self.parse(arg[0]) + "\n\n"

    def quote(self, arg: List[Any]) -> str:
        return ">" + self.parse(arg[0]) + ""


class DefaultWiki(Moire):
    """
    Wiki syntax of Wikipedia.
    """

    name = "Wiki"
    extensions = ["wiki"]
    block_tags = BLOCK_TAGS

    level = 0

    def block(self, arg: List[Any]) -> str:
        return self.parse(arg[0], inblock=True)

    def body(self, arg: List[Any]) -> str:
        counter = []
        return (
            self.parse(arg[0], inblock=True)
            .replace("\n\n\n", "\n\n")
            .replace("\n\n\n", "\n\n")
        )

    def header(self, arg, number):
        return (number * "=") + " " + self.parse(arg[0]) + " " + (number * "=")

    def list(self, arg: List[Any]) -> str:
        s = ""
        for item in arg:
            if isinstance(item, list):
                s += "* " + self.parse(item) + "\n"
        return s

    def shortlist(self, arg: List[Any]) -> str:
        s = ""
        n = 0
        for item in arg:
            if isinstance(item, list):
                n += 1
                self.level += 1
                s += (
                    "\n"
                    + ("   " * (self.level - 1))
                    + "* "
                    + self.parse(item)
                    + "\n"
                )
                self.level -= 1
        return s

    def table(self, arg: List[Any]) -> str:
        s = ""
        for index, tr in enumerate(arg[0]):
            if isinstance(tr, list):
                s += "|"
                for td in tr:
                    if isinstance(td, list):
                        s += " " + self.parse(td) + " |"
                s += "\n"
                if index == 0:
                    s += "|"
                    for td in tr:
                        if isinstance(td, list):
                            s += "---|"
                    s += "\n"
        return s

    def b(self, arg: List[Any]) -> str:
        return f"'''{self.parse(arg[0])}'''"

    def code(self, arg: List[Any]) -> str:
        if len(arg) > 1:
            return (
                f'<syntaxhighlight lang="{self.clear(arg[1])}">'
                f"\n{self.clear(arg[0])}\n</syntaxhighlight>"
            )
        else:
            return f"<pre><tt>{self.clear(arg[0])}\n</tt></pre>"

    def href(self, arg: List[Any]) -> str:
        OSM_WIKI_PREFIX: str = "https://wiki.openstreetmap.org/wiki/"
        link: str = self.parse(arg[0])
        if link.startswith(OSM_WIKI_PREFIX):
            return f"[[{link[len(OSM_WIKI_PREFIX):]}|{self.parse(arg[1])}]]"
        return "[" + link + " " + self.parse(arg[1]) + "]"

    def i(self, arg: List[Any]) -> str:
        return f"''{self.parse(arg[0])}''"

    def image(self, arg: List[Any]) -> str:
        return (
            "[[File:"
            + self.parse(arg[0])
            + "|thumb|"
            + self.parse(arg[1])
            + "]]"
        )

    def formal(self, arg: List[Any]) -> str:
        return "<" + self.parse(arg[0]) + ">"

    def tt(self, arg: List[Any]) -> str:
        return "<code>" + str(self.parse(arg[0])) + "</code>"

    def u(self, arg: List[Any]) -> str:
        return f"<u>{self.parse(arg[0])}</u>"

    def text(self, arg: List[Any]) -> str:
        return self.parse(arg[0]) + "\n\n"

    def quote(self, arg: List[Any]) -> str:
        return ">" + self.parse(arg[0]) + ""


# TeX.


class DefaultTeX(Moire):
    name = "Tex"
    extension = "tex"

    escape_symbols = {
        "_": "\\_",
    }
    block_tags = BLOCK_TAGS

    def body(self, arg: List[Any]) -> str:
        s = """\\documentclass[twoside,psfig]{article}:
        \\usepackage[utf8]{inputenc}
        \\usepackage[russian]{babel}
        \\usepackage{enumitem}
        \\usepackage{float}
        \\usepackage[margin=3cm,hmarginratio=1:1,top=32mm,columnsep=20pt]{geometry}
        \\usepackage{graphicx}
        \\usepackage{hyperref}
        \\usepackage{multicol}
        \\begin{document}"""
        s += self.parse(arg[0], inblock=True)
        s += "\\end {document}"
        return s

    def title(self, arg: List[Any]) -> str:
        s = "\\title{" + self.parse(arg[0]) + "}"
        s += (
            "\\vspace{12em}\\begin{center}{\\huge "
            + self.parse(arg[0])
            + "}\\end{center}\\vspace{2em}"
        )
        return s

    def header(self, arg, number):
        if number == 1:
            return "\\section{" + self.parse(arg[0]) + "}"
        if number == 2:
            return "\\subsection{" + self.parse(arg[0]) + "}"
        if number == 3:
            return "\\subsubsection{" + self.parse(arg[0]) + "}"
        if number == 4:
            return "\\paragraph{" + self.parse(arg[0]) + "}"
        if number == 5:
            return "\\subparagraph{" + self.parse(arg[0]) + "}"
        if number == 6:
            return "" + self.parse(arg[0]) + ""

    def table(self, arg: List[Any]) -> str:
        s = "\\begin{table}[h]\n\\begin{center}\n\\begin{tabular}{|"
        max_tds = 0
        for tr in arg:
            if isinstance(tr, list):
                tds = 0
                for td in tr:
                    if isinstance(td, list):
                        tds += 1
                if tds > max_tds:
                    max_tds = tds
        for k in range(max_tds):
            s += "p{2cm}|"
        s += "}\n\\hline\n"
        for tr in arg:
            if isinstance(tr, list):
                tds = []
                for td in tr:
                    if isinstance(td, list):
                        tds.append(td)
                for td in tds[:-1]:
                    s += self.parse(td) + " & "
                s += self.parse(tds[-1])
                s += " \\\\\n\\hline\n"
        s += "\\end{tabular}\n\\end{center}\n\\end{table}\n"
        return s

    def list(self, arg: List[Any]) -> str:
        s = "\\begin{itemize}\n"
        for item in arg[0]:
            if isinstance(item, list):
                s += "\\item " + self.parse(item) + "\n\n"
        s += "\\end{itemize}\n"
        return s

    def shortlist(self, arg: List[Any]) -> str:
        s = "\\begin{itemize}[itemsep=-0.5ex]\n"
        for item in arg[0]:
            if isinstance(item, list):
                s += "\\item " + self.parse(item) + "\n\n"
        s += "\\end{itemize}\n\n"
        return s

    def ordered(self, arg: List[Any]) -> str:
        s = "\\begin{ordered}\n"
        for item in arg[0]:
            if isinstance(item, list):
                s += "\\item " + self.parse(item[0]) + "\n\n"
        s += "\\end{ordered}\n"
        return s

    def annotation(self, arg: List[Any]) -> str:
        return (
            "\\begin {abstract}\n\n"
            + self.parse(arg[0], inblock=True)
            + "\\end {abstract}\n\n"
        )

    def books(self, arg: List[Any]) -> str:
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

    def b(self, arg: List[Any]) -> str:
        return "{\\bf " + self.parse(arg[0]) + "}"

    def br(self, arg: List[Any]) -> str:
        return "\\\\"

    def cite(self, arg: List[Any]) -> str:
        return "\\cite {" + self.clear(arg[0]) + "}"

    def code(self, arg: List[Any]) -> str:
        return "\\begin{verbatim}" + self.clear(arg[0]) + "\\end{verbatim}"

    def date(self, arg: List[Any]) -> str:
        pass

    def href(self, arg: List[Any]) -> str:
        s = ""
        link = self.clear(arg[0])
        if link[0] == "#":
            link = link[1:]
        if len(arg) == 1:
            s += "\\href {" + link + "} {" + link + "}"
        else:
            s += "\\href {" + link + "} {" + self.parse(arg[1]) + "}"
        return s

    def i(self, arg: List[Any]) -> str:
        return "{\\em " + self.parse(arg[0]) + "}"

    def math(self, arg: List[Any]) -> str:
        return f"${''.join(arg[0])}$"

    def mathblock(self, arg: List[Any]) -> str:
        return "\\[{0}\\]".format("".join(arg[0]))

    def ignore(self, arg: List[Any]) -> str:
        return self.clear(arg[0])

    def image(self, arg: List[Any]) -> str:
        s = (
            "\\begin{figure}[h]\\begin{center}\\includegraphics{"
            + self.parse(arg[0])
            + "}\\end{center}"
        )
        if len(arg) > 1:
            s += "\\caption {" + self.parse(arg[1]) + "}"
        s += "\\end{figure}"
        return s

    def item(self, arg: List[Any]) -> str:
        return "\\item " + self.parse(arg[0]) + ""

    def page(self, arg: List[Any]) -> str:
        return "\\textsuperscript{" + self.parse(arg[0]) + "}"

    def sc(self, arg: List[Any]) -> str:
        return "{\\sc " + self.parse(arg[0]) + "}"

    def size(self, arg: List[Any]) -> str:
        return "" + self.parse(arg[0]) + ""

    def strike(self, arg: List[Any]) -> str:
        return "" + self.parse(arg[0]) + ""

    def sub(self, arg: List[Any]) -> str:
        return "$_{" + self.parse(arg[0]) + "}$"

    def super(self, arg: List[Any]) -> str:
        return "\\textsuperscript{" + self.parse(arg[0]) + "}"

    def text(self, arg: List[Any]) -> str:
        return self.parse(arg[0]) + "\n\n"

    def tr(self, arg: List[Any]) -> str:
        return "" + self.parse(arg[0]) + "|"

    def td(self, arg: List[Any]) -> str:
        return "| " + self.parse(arg[0]) + ""

    def tt(self, arg: List[Any]) -> str:
        return "{\\tt " + self.parse(arg[0]) + "}"

    def u(self, arg: List[Any]) -> str:
        return "" + self.parse(arg[0]) + ""

    def quote(self, arg: List[Any]) -> str:
        return "" + self.parse(arg[0]) + ""


# RTF.


class DefaultRTF(Moire):
    name = "RTF"

    def escape(self, text: str) -> str:
        result = ""
        for c in text:
            if c == "~":
                result += "\\~"
            elif ord(c) <= 128:
                result += c
            else:
                result += "\\u" + unicode(ord(c)) + "  "
        return result

    def block(self, arg: List[Any]) -> str:
        return self.parse(arg[0], inblock=True)

    def body(self, arg: List[Any]) -> str:
        status["levels"] = [0, 0, 0, 0, 0, 0, 0]
        status["bookindex"] = 0
        status["books"] = {}
        s = """{\\rtf0\\ansi\\deff0\n{\\*\\listtable{\\list\\listtemplateid1
        {\\listlevel\\levelnfc23{\\leveltext \\'01\\u8226 ?;}\\li720}
        {\\listlevel\\levelnfc23{\\leveltext \\'01\\u9702 ?;}\\li1080}
        {\\listlevel\\levelnfc23{\\leveltext \\'01\\u9642 ?;}\\li1440}
        {\\listlevel\\levelnfc23{\\leveltext \\'01\\u8226 ?;}\\li1800}
        {\\listlevel\\levelnfc23{\\leveltext \\'01\\u9702 ?;}\\li2160}
        {\\listlevel\\levelnfc23{\\leveltext \\'01\\u9642 ?;}\\li2520}
        {\\listlevel\\levelnfc23{\\leveltext \\'01\\u8226 ?;}\\li2880}
        {\\listlevel\\levelnfc23{\\leveltext \\'01\\u9702 ?;}\\li3240}
        {\\listlevel\\levelnfc23{\\leveltext \\'01\\u9642 ?;}\\li3600}\\listid1}}
        {\\listoverridetable{\\listoverride\\listid1\\ls1}}
        {\\fonttbl{\\f1 Courier 10 Pitch;}{\\f2 Arial;}{\\f3 Times New Roman;}}\\fs20"""
        s += "{\\f3 " + self.parse(arg[0], inblock=True) + "}"
        s += "\n}"
        return s

    def title(self, arg: List[Any]) -> str:
        return (
            "\\par\\pard \\qc\\b\\sb346\\sa173{\\f2{\\fs32 "
            + self.parse(arg[0])
            + "  \\fs20}}\\b0\n"
        )

    def table(self, arg: List[Any]) -> str:
        return self.parse(arg[0])

    def list(self, arg: List[Any]) -> str:
        s = ""
        for item in arg[0]:
            if isinstance(item, list):
                lc = 0  # FIXME
                lc += 1
                s += self.parse(item) + " "
                lc -= 1
                if lc == 0:
                    s += "\\par\\pard"
        return s

    def header(self, arg, number):
        if number == 1:
            status["levels"][1] += 1
            status["levels"][2] = 0
            status["levels"][3] = 0
            level = status["levels"][1]
            return (
                "\\i\\b\\sb346\\sa173{\\f2\\fs22 "
                + str(level)
                + ". "
                + self.parse(arg[0])
                + "\\fs20}\\b0\\i0\n"
            )
        elif number == 2:
            status["levels"][2] += 1
            status["levels"][3] = 0
            level = (
                str(status["levels"][1]) + "." + str(status["levels"][2]) + " "
            )
            return (
                "\\b\\par\\pard\\sb346\\sa173{\\fs22 "
                + level
                + self.parse(arg[0])
                + "\\fs20}\\b0\n"
            )
        elif number == 3:
            status["levels"][3] += 1
            level = (
                str(status["levels"][1])
                + "."
                + str(status["levels"][2])
                + "."
                + str(status["levels"][3])
                + " "
            )
            return (
                "\\parb\\par\\pard\\sb346\\sa173{\\fs20 "
                + level
                + self.parse(arg[0])
                + "\\fs20}\\b0\\i0\n"
            )
        elif number == 4:
            return (
                "\\parpar\\pard\\sb346\\sa173{\\fs20 "
                + self.parse(arg[0])
                + "\\fs20}\\b0\n"
            )
        elif number == 5:
            return (
                "\\b\\sb346\\sa173{\\fs20 "
                + self.parse(arg[0])
                + "\\fs20}\\b0\n"
            )
        elif number == 6:
            return (
                "\\b\\sb346\\sa173{\\fs20 "
                + self.parse(arg[0])
                + "\\fs20}\\b0\n"
            )

    def center(self, arg: List[Any]) -> str:
        return "\\qc" + self.parse(arg[0])

    def left(self, arg: List[Any]) -> str:
        return "\\ql" + self.parse(arg[0])

    def right(self, arg: List[Any]) -> str:
        return "\\qr" + self.parse(arg[0])

    def b(self, arg: List[Any]) -> str:
        return "\n\\b " + self.parse(arg[0]) + "\\b0\n"

    def code(self, arg: List[Any]) -> str:
        return self.parse(arg[0])

    def font(self, arg: List[Any]) -> str:
        return ""

    def href(self, arg: List[Any]) -> str:
        return (
            '{\\field{\\*\\fldinst{HYPERLINK  "'
            + self.parse(arg[0])
            + '"}}{\\fldrslt{\\u1  '
            + self.parse(arg[-1])
            + "\n}}}"
        )

    def i(self, arg: List[Any]) -> str:
        return "\\i " + self.parse(arg[0]) + "\\i0\n"

    def math(self, arg: List[Any]) -> str:
        return self.parse(arg[0])

    def ignore(self, arg: List[Any]) -> str:
        return self.parse(arg[0])

    def image(self, arg: List[Any]) -> str:
        return self.parse(arg[0])

    def shortlist(self, arg: List[Any]) -> str:
        return self.parse(arg[0])

    def ordered(self, arg: List[Any]) -> str:
        return "\\levelnfc0\\list " + self.parse(arg[0]) + " \\list0"

    def s(self, arg: List[Any]) -> str:
        return "\\strike " + self.parse(arg[0]) + "\\strike0"

    def sc(self, arg: List[Any]) -> str:
        return "\\scaps " + self.parse(arg[0]) + "\\scaps0\n"

    def size(self, arg: List[Any]) -> str:
        return "\\fs" + str(int(self.parse(arg[0])) * 2) + self.parse(arg[1])

    def strike(self, arg: List[Any]) -> str:
        return self.parse(arg[0])

    def sub(self, arg: List[Any]) -> str:
        return "\\sub " + self.parse(arg[0]) + "\\nosupersub\n"

    def super(self, arg: List[Any]) -> str:
        return "\\super " + self.parse(arg[0]) + "\\nosupersub\n"

    def tr(self, arg: List[Any]) -> str:
        return self.parse(arg[0]) + "|"

    def td(self, arg: List[Any]) -> str:
        return "| " + self.parse(arg[0])

    def tt(self, arg: List[Any]) -> str:
        return "{\\f1 " + self.parse(arg[0]) + "}"

    def u(self, arg: List[Any]) -> str:
        return "\\ul " + self.parse(arg[0]) + "\\ul0\n"

    def quote(self, arg: List[Any]) -> str:
        return self.parse(arg[0])

    def book(self, arg: List[Any]) -> str:
        return self.parse(arg[0])

    def books(self, arg: List[Any]) -> str:
        s = ""
        # for item in arg[0]:
        #   if isinstance(item, list):
        #       s += "\\par\\pard [" + status[] + "] " + self.parse(item[1]) + "\n\n"
        for index in range(status["bookindex"]):
            s += "\\par\\pard\\li720\\fi-360[" + str(index + 1) + "]\\tab "
            for item in arg[0]:
                if isinstance(item, list):
                    if status["books"][self.clear(item[0])] == index + 1:
                        s += self.parse(item[1])
        s += "\\par\\pard"
        return s

    def cite(self, arg: List[Any]) -> str:
        s = ""
        cites = self.clear(arg[0]).split(", ")
        for cite in cites:
            print(cite, status["books"])
            if not (cite in status["books"]):
                status["bookindex"] += 1
                status["books"][cite] = status["bookindex"]
        s += "["
        s += str(status["books"][cites[0]])
        for cite in cites[1:]:
            s += ", " + str(status["books"][cite])
        s += "]"
        return s

    def text(self, arg: List[Any]) -> str:
        return "\\par\\pard\\qj" + self.parse(arg[0]) + "\n"

    def br(self, arg: List[Any]) -> str:
        return "\\par\\pard"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", help="Moire input file", required=True)
    parser.add_argument("-o", "--output", help="output file", required=True)
    parser.add_argument("-f", "--format", help="output format", required=True)

    options = parser.parse_args(sys.argv[1:])

    with open(options.input, "r") as input_file:
        converter: Moire = getattr(sys.modules[__name__], options.format)()
        output: str = converter.convert(input_file.read())

    if not output:
        print("Fatal: output was no produced.")
        sys.exit(1)

    with open(options.output, "w+") as output_file:
        output_file.write(output)
        print(f"Converted to {options.output}.")
