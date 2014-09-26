# -*- coding: utf-8 -*-

'''
File conversion from Moiré markup language to other formats.

Usage: python moire.py -i <input file> -o <output file> -t <format> 
                       -r <rules file>

Options:
    -i <file>   input file name
    -o <file>   output file name
    -f <format> resulted format
    -r <file>   rules file name

This file is a part of Moiré project—light markup language.

Author: Sergey Vartanov (me@enzet.ru)

See http://github.com/enzet/moire
'''

import argparse
import sys
import re

parser = argparse.ArgumentParser()

parser.add_argument('-i', dest = 'input', help = 'Moiré input file')
parser.add_argument('-o', dest = 'output', help = 'output file')
parser.add_argument('-f', dest = 'format', help = 'output format')
parser.add_argument('-r', dest = 'rules', help = 'rules file')
parser.add_argument('-pl', dest = 'print_lexems', action = 'store_true',\
		help = 'print lexems')
parser.add_argument('-pp', dest = 'print_preprocessed', action = 'store_true',\
		help = 'print preprocessed file')

options = parser.parse_args(sys.argv[1:])

try:
	input_file = open(options.input).read()
except:
	print 'Input file "' + options.input + '" is not found.'
	sys.exit(1)

try:
	rules_file = open(options.rules)
except:
	print 'Rules file "' + options.rules + '" is not found.'
	sys.exit(1)

output_file = open(options.output, 'w+')
prep_file = open('preprocessed', 'w+')

'''
Moire tag definition
'''
class Tag:
	def __init__(self, id, parameters):
		self.id = id
		self.parameters = parameters
	def __str__(self):
		s = ''
		s += self.id + ' {' + str(self.parameters)
		s += '}'
		return s
	def __repr__(self):
		s = '\033[31m'
		s += self.id + ' {\033[0m' + str(self.parameters)
		s += '\033[31m}\033[0m'
		return s

# Languages preprocessing

langs = ['ru']

preprocessed = ''
adding = True
 
i = 0
while i < len(input_file):
	c = input_file[i]
	if c == '[' and input_file[i - 1] != '\\':
		end = min(input_file.find(' ', i), input_file.find('\n', i))
		if input_file[i + 1:end] == 'ru':
			adding = True
			i = end
		else:
			adding = False
			i += 1
	elif c == ']' and input_file[i - 1] != '\\':
		adding = True
	else:
		if adding:
			preprocessed += c
	i += 1

# Comments preprocessing

input_file = preprocessed
preprocessed = ''
adding = True

i = 0
while i < len(input_file):
	if input_file[i:i + 2] == '/*':
		adding = False
		i += 1
	elif input_file[i:i + 2] == '*/':
		adding = True
		i += 1
	else:
		if adding:
			preprocessed += input_file[i]
	i += 1

input_file = '\\body {' + preprocessed + '}'

if options.print_preprocessed:
	print '\033[32m' + input_file + '\033[0m'

prep_file.write(input_file)

# Rules reading from file

rules = {}

def add_rule(rule, right, block):
	global rules
	if rule != None:
		rule[2] = right
		if block in rules:
			rules[block].append(rule)
		else:
			rules[block] = [rule]

right = ''
rule = None
l = rules_file.readline()
block = ''

while l != '':
	if l[0] != '\t':
		add_rule(rule, right, block)
		rule = None
		if l[0] == ':':
			language = l[1:-1]
		elif len(l) > 1:
			block = l[:-2]
	else:
		if l[1] != '\t':
			add_rule(rule, right, block)
			rule = [l[1:l.find(':')], '', '']
			right = l[l.find(':') + 1:].strip()
		else:
			right += l[2:]
	l = rules_file.readline()

add_rule(rule, right, block)

block_tags = []
for a in rules['block']:
	block_tags.append(a[0])

def is_space(c):
	if c == ' ' or c == '\n' or c == '\t' or c == '\r':
		return True
	else:
		return False

def lexer(text):
	'''
	Parse formatted preprocessed text to a list of lexems
	'''
	in_tag = False
	in_space = True
	lexems = []
	positions = []
	tag_name = ''
	word = ''

	index = 0

	for char in text:
		if char == '\\':
			if word != '':
				lexems.append(word)
				positions.append(index)
			word = ''
			in_tag = True
			tag_name = '\\'
		elif char == '{':
			if in_tag or in_space:
				in_tag = False
				if tag_name != '':
					lexems.append(tag_name)
					positions.append(index)
			lexems.append('{')
			positions.append(index)
			tag_name = ''
			word = ''
		elif char == '}':
			if word != '':
				lexems.append(word)
				positions.append(index)
			word = ''
			lexems.append('}')
			positions.append(index)
		elif is_space(char):
			if in_tag:
				in_tag = False
				in_space = True
			else:
				word += char
		else:
			if in_tag:
				tag_name += char
			else:
				word += char
		index += 1

	return lexems, positions

lexems, positions = lexer(input_file)

if options.print_lexems:
	print str(len(lexems)) + " = " + str(len(positions))
	print '\033[33m' + str(lexems) + '\033[0m'
	print '\033[34m' + str(positions) + '\033[0m'

index = 0
level = 0

def get_line(line):
	global index
	global level
	tag = None
	result = []
	while index < len(line):
		item = line[index]
		if item[0] == '\\':
			if tag != None:
				result.append(tag)
			tag = Tag(item[1:], [])
		elif item == '{':
			level += 1
			if tag == None:
				index += 1
				result.append(get_line(line))
			else:
				index += 1
				tag.parameters.append(get_line(line))
			index += 1
			continue
		elif item == '}':
			level -= 1
			if level < 0:
				position = positions[index]
				print 'Lexer error at ' + str(position) + '.'
				print input_file[position - 10:position + 10]
				print '          ^'
				index += 1
				sys.exit(1)
			if tag != None:
				result.append(tag)
			return result
		else:
			if tag != None:
				result.append(tag)
				tag = None
			result.append(item)
		index += 1
	if tag != None:
		result.append(tag)
	return result

parsed = get_line(lexems)

no_tags = []

def parse(text, inblock = False):
	if text == None or text == '' or text == []:
		return 'none'
	elif isinstance(text, str):
		return text
	elif isinstance(text, Tag):
		for rule in rules['block'] + rules['inner']:
			if rule[0] == text.id:
				arg = text.parameters
				s = ''
				try:
					exec(rule[2])
				except:
					print 'Error for tag "' + text.id + '" in ' + str(arg) + \
							'.'
				return s
		no_tags.append(text.id)
	else:
		s = ''
		innerblock = []
		for item in text:
			if inblock:
				if isinstance(item, Tag) and item.id in block_tags:
					if innerblock != []:
						s += str(parse(Tag('text', [innerblock])))
						innerblock = []
					s += str(parse(item))
				else:
					innerblock.append(item)
			else:
				s += str(parse(item))
		if innerblock != []:
			s += str(parse(Tag('text', [innerblock])))
			innerblock = []
		return s

p = parse(parsed)

# print p

output_file.write(p)

if len(no_tags) > 0:
	print 'Tags not found:'
	for k in set(no_tags):
		print '  ' + str(k)
