"""Extended Moire tag set.

This set has a number of useful tags for enriching the text.
"""


from moire.default import Arguments, Default


class Extended(Default):
    """Extended Moire tag set."""

    name: str = "Extended"
    id_: str = "extended"

    def formal(self, arg: Arguments) -> str:
        """Formal argument inside code.

        E.g. in text "Run command `ssh <username>@<host>`", the `<username>`
        and `<host>` are formal arguments.

        By default, the formal argument is wrapped in with `<` and `>`.
        """
        return f"<{self.parse(arg[0])}>"
