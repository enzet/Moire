"""
Command line Python tool for file conversion from Moire markup language to other
formats, such as HTML, TeX, etc.
"""

import logging
import sys
from argparse import ArgumentParser, Namespace

from moire.moire import Moire
import moire.default  # noqa: F401

__author__ = "Sergey Vartanov"
__email__ = "me@enzet.ru"


def main():
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    parser: ArgumentParser = ArgumentParser()

    parser.add_argument("-i", "--input", help="Moire input file", required=True)
    parser.add_argument("-o", "--output", help="output file")
    parser.add_argument("-f", "--format", help="output format", required=True)

    options: Namespace = parser.parse_args(sys.argv[1:])

    with open(options.input, "r") as input_file:
        converter: Moire = getattr(
            sys.modules["moire.default"], options.format
        )()
        converter.file_name = options.input
        output: str = converter.convert(input_file.read())

    if not output:
        logging.fatal("Fatal: output was no produced.")
        sys.exit(1)

    if options.output:
        with open(options.output, "w+") as output_file:
            output_file.write(output)
            logging.info(f"Converted to {options.output}.")
    else:
        sys.stdout.write(output)


if __name__ == "__main__":
    main()
