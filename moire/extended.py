"""Extended Moire tag set.

This set has a number of useful tags for enriching the text.
"""

from dataclasses import dataclass
from typing import ClassVar, override

from moire.default import Arguments, Default, DefaultHTML, DefaultMarkdown


@dataclass
class Extended(Default):
    """Extended Moire tag set."""

    name: ClassVar[str] = "Extended"
    id_: ClassVar[str] = "extended"

    def formal(self, arg: Arguments) -> str:
        """Formal argument inside code.

        E.g. in text "Run command `ssh <username>@<host>`", the `<username>`
        and `<host>` are formal arguments.

        By default, the formal argument is wrapped in with `<` and `>`.
        """
        return f"<{self.parse(arg[0])}>"

    def abbr(self, arg: Arguments) -> str:
        """Abbreviation."""
        return self.parse(arg[0])

    def skw(self, arg: Arguments) -> str:
        """Syntax keyword."""
        return self.parse(arg[0])


@dataclass
class ExtendedHTML(Extended, DefaultHTML):
    """Extended HTML format."""

    name: ClassVar[str] = "Extended HTML"
    id_: ClassVar[str] = "extended_html"

    @override
    def formal(self, arg: Arguments) -> str:
        return f'<span class="formal">{self.parse(arg[0])}</span>'

    @override
    def abbr(self, arg: Arguments) -> str:
        return f'<span class="abbr">{self.parse(arg[0])}</span>'

    @override
    def skw(self, arg: Arguments) -> str:
        return f'<span class="skw">{self.parse(arg[0])}</span>'


@dataclass
class ExtendedMarkdown(Extended, DefaultMarkdown):
    """Extended HTML format."""

    name: ClassVar[str] = "Extended Markdown"
    id_: ClassVar[str] = "extended_markdown"
    list_level: int = 0
