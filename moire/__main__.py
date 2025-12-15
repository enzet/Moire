#!/usr/bin/env python3

"""Moire entry point.

Converts code in Moire markup to other formats, such as HTML, TeX, etc.
"""

import logging
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

from moire.default import Default
from moire.moire import Moire

__author__ = "Sergey Vartanov"
__email__ = "me@enzet.ru"

logger: logging.Logger = logging.getLogger(__name__)


def main(
    arguments: list[str] | None = None, top_class: type[Moire] | None = None
) -> None:
    """Convert Moire markup to other formats."""

    if not arguments:
        arguments = sys.argv[1:]
    if not top_class:
        top_class = Default

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    parser: ArgumentParser = ArgumentParser()

    parser.add_argument("-i", "--input", help="Moire input file", required=True)
    parser.add_argument("-o", "--output", help="output file")
    parser.add_argument("-f", "--format", help="output format", required=True)
    parser.add_argument("--wrap", action="store_true", default=True)

    options: Namespace = parser.parse_args(arguments)

    converter: Moire | None = None
    for class_ in top_class.__subclasses__():
        if class_.id_ == options.format:
            converter = class_()

    if not converter:
        logger.fatal(
            "No converter class found for format `%s`.", options.format
        )
        sys.exit(1)

    with Path(options.input).open(encoding="utf-8") as input_file:
        if converter is not None:  # TODO(enzet): remove when ty is fixed.
            converter.file_name = options.input
            output: str = converter.convert(
                input_file.read(), wrap=options.wrap
            )

    if not output:
        logger.fatal("No output was produced.")
        sys.exit(1)

    if options.output:
        with Path(options.output).open("w", encoding="utf-8") as output_file:
            output_file.write(output)
            logger.info("Converted to %s.", options.output)
    else:
        sys.stdout.write(output)


if __name__ == "__main__":
    main(sys.argv[1:], Default)
