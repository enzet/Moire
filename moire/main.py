"""
Command line Python tool for file conversion from Moire markup language to other
formats, such as HTML, TeX, etc.
"""

import logging
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import List, Optional

from moire.default import Default
from moire.moire import Moire

__author__ = "Sergey Vartanov"
__email__ = "me@enzet.ru"


def main(arguments: List[str] = None, top_class=None):
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

    converter: Optional[Moire] = None
    for class_ in top_class.__subclasses__():
        if class_.id_ == options.format:
            converter = class_()

    if not converter:
        logging.fatal(
            f"No converter class found for format `{options.format}`."
        )
        exit(1)

    with Path(options.input).open() as input_file:
        converter.file_name = options.input
        output: str = converter.convert(input_file.read(), wrap=options.wrap)

    if not output:
        logging.fatal("No output was produced.")
        sys.exit(1)

    if options.output:
        with open(options.output, "w") as output_file:
            output_file.write(output)
            logging.info(f"Converted to {options.output}.")
    else:
        sys.stdout.write(output)


if __name__ == "__main__":
    main(sys.argv[1:], Default)
