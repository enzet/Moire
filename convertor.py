#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Command line Python tool for file conversion from Moire markup language to other 
formats, such as HTML, TeX, etc.

Usage: python moire.py 
       -i <input file> 
       -o <output file> 
       -f <format> 
       -r <rules file>
       -b <book level>

This file is a part of Moire project—light markup language.

Author: Sergey Vartanov (me@enzet.ru).
See http://github.com/enzet/moire
"""

import argparse
import moire
import os
import sys

parser = argparse.ArgumentParser()

parser.add_argument('-i', dest='input_file_name', help='Moire input file')
parser.add_argument('-o', dest='output_destination', help='output file')
parser.add_argument('-f', dest='format', help='output format')
parser.add_argument('-r', dest='rules', help='rules file')
parser.add_argument('-b', dest='book_level', help='book level')
parser.add_argument('-l', dest='language', help='language')
parser.add_argument('-pl', dest='print_lexemes', action='store_true', 
                    help='print lexemes')
parser.add_argument('-pp', dest='print_preprocessed', action='store_true', 
                    help='print preprocessed file')
parser.add_argument('-pi', dest='print_intermediate', action='store_true', 
                    help='print intermediate representation')
parser.add_argument('-opt', dest='opt', help='additional options')

options = parser.parse_args(sys.argv[1:])

# Arguments check

if not options.input_file_name:
    options.input_file_name = raw_input('Please, specify the input file ' + \
        'name (or use -i <file name>): ')

if not options.language:
    options.language = 'en'

while True:
    if os.path.isfile(options.input_file_name):
        break
    else:
        answer = raw_input('Input file "' + options.input_file_name + \
            '" is not found. Do you want to specity correct? [y/n] ')
        if answer.lower() in ['y', 'yes']:
            options.input_file_name = raw_input('Please, specify the input ' + \
               'file name (or use -i <file name>): ')
        else:
            sys.exit(0)

if not options.format:
    options.format = raw_input('Please, specify the output format (html, ' + \
        'tex, etc.) (or use -f <format>): ')

if not options.output_destination:
    answer = raw_input('You aren\'t specify output destination. Should I ' + \
        'create file "out.' + options.format + '"? [y/n] ')
    if answer.lower() in ['y', 'yes', 'ok']:
        options.output_destination = 'out.' + options.format
    else:
        sys.exit(0)

options.book_level = int(options.book_level) if options.book_level else 0

# Parsing

if not options.book_level or options.book_level == 0:

    output = moire.convert_file(options.input_file_name, options.format, 
            options.language, True, options.rules, True)

    if not output:
        print 'Fatal: output was no produced.'
        sys.exit(1)

    output_file = open(options.output_destination, 'w+')
    print 'Writing result to ' + options.output_destination + '...'
    output_file.write(output)
    output_file.close()
    print 'Done.'

else:

    moire.construct_book(options.input_file_name, kind=options.format, 
                         language=options.language, 
                         rules=options.rules, 
                         book_level=options.book_level, 
                         output_file_name=options.output_destination)
