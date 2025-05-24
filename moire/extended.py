"""Extended Moire tag set.

This set has a number of useful tags for enriching the text.
"""

from dataclasses import dataclass
from typing import ClassVar

from moire.default import Arguments, Default


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
