# -*- coding: utf-8 -*-
#!/usr/bin/python

"""
Command line Python tool for file conversion from Moiré markup language to other formats, such as HTML, TeX, etc.

Usage: python moire.py -i <input file> -o <output file> -t <format> -r <rules file>

This file is a part of Moiré project—light markup language.

Author: Sergey Vartanov (me@enzet.ru).

See http://github.com/enzet/moire
"""

import moire
import argparse
import sys

parser = argparse.ArgumentParser()

parser.add_argument('-i', dest='input', help='Moiré input file')
parser.add_argument('-o', dest='output', help='output file')
parser.add_argument('-f', dest='format', help='output format')
parser.add_argument('-r', dest='rules', help='rules file')
parser.add_argument('-b', dest='book_level', help='book level')
parser.add_argument('-l', dest='language', help='language')
parser.add_argument('-pl', dest='print_lexemes', action='store_true', help='print lexemes')
parser.add_argument('-pp', dest='print_preprocessed', action='store_true', help='print preprocessed file')
parser.add_argument('-pi', dest='print_intermediate', action='store_true', help='print intermediate representation')
parser.add_argument('-opt', dest='opt', help='additional options')

options = parser.parse_args(sys.argv[1:])

try:
    input_file = open(options.input).read()
except:
    print 'Error: input file "' + options.input + '" is not found.'
    sys.exit(1)

book_level = int(options.book_level)

if book_level == 0:

	output = moire.convert(input_file, options.format, options.language, True, options.rules, True)

	if not output:
	    print 'Error: cannot convert.'
	    sys.exit(1)

	output_file = open(options.output, 'w+')
	output_file.write(output)

else:

	moire.construct_book(options.input, kind=options.format, 
		                 language=options.language, 
		                 rules_file_name=options.rules, book_level=book_level, 
		                 output_file_name=options.output)
