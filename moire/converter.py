"""
Command line Python tool for file conversion from Moire markup language to other 
formats, such as HTML, TeX, etc.
"""
import argparse
import sys

from moire.moire import Moire

__author__: str = "Sergey Vartanov"
__email__: str = "me@enzet.ru"

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-i", "--input", help="Moire input file", required=True)
    parser.add_argument("-o", "--output", help="output file", required=True)
    parser.add_argument("-f", "--format", help="output format", required=True)

    options = parser.parse_args(sys.argv[1:])

    with open(options.input, "r") as input_file:
        converter: Moire = getattr(sys.modules[__name__], options.format)
        output: str = converter.convert(input_file.read())

    if not output:
        print("Fatal: output was no produced.")
        sys.exit(1)

    with open(options.output, "w+") as output_file:
        output_file.write(output)
        print(f"Converted to {options.output}.")
