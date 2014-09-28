# -*- coding: utf-8 -*-

'''
File conversion from Moiré markup language to other formats.

Usage: python moire.py -i <input file> -o <output file> -t <format> 
                       -r <rules file>

This file is a part of Moiré project—light markup language.

Author: Sergey Vartanov (me@enzet.ru)

See http://github.com/enzet/moire
'''

import argparse
import os
import re
import sys

parser = argparse.ArgumentParser()

parser.add_argument('-i', dest = 'input', help = 'Moiré input file')
parser.add_argument('-o', dest = 'output', help = 'output file')
parser.add_argument('-f', dest = 'format', help = 'output format')
parser.add_argument('-r', dest = 'rules', help = 'rules file')
parser.add_argument('-b', dest = 'book_level', help = 'book level')
parser.add_argument('-l', dest = 'language', help = 'language')
parser.add_argument('-pl', dest = 'print_lexems', action = 'store_true',\
		help = 'print lexems')
parser.add_argument('-pp', dest = 'print_preprocessed', action = 'store_true',\
		help = 'print preprocessed file')

options = parser.parse_args(sys.argv[1:])

language = options.language

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

if options.book_level == 0:
	output_file = open(options.output, 'w+')

prep_file = open('preprocessed', 'w+')

def trim_inside(s):
	ret = ''
	i = 0
	while i < len(s):
		if is_space(s[i]):
			ret += ' '
			while i < len(s) and is_space(s[i]):
				s += ''
				i += 1
			continue
		else:
			ret += s[i]
		i += 1
	return ret

def is_space(c):
	if c == ' ' or c == '\n' or c == '\t' or c == '\r':
		return True
	else:
		return False

'''
Moire tag definition
'''
class Tag:
	def __init__(self, id, parameters):
		self.id = id
		self.parameters = parameters
	def __str__(self):
		s = self.id + ' {' + str(self.parameters)
		s += '}'
		return s
	def __repr__(self):
		s = self.id + ' {' + str(self.parameters)
		s += '}'
		return s

class Document:
	def __init__(self, id, content):
		self.id = id
		self.content = content

# Languages preprocessing

preprocessed = ''
adding = True
 
i = 0
while i < len(input_file):
	if input_file[i] == '[' and input_file[i - 1] != '\\':
		end = i + 3
		if input_file[i + 1:end] == options.language:
			adding = True
			i = end
		else:
			adding = False
			i += 1
	elif input_file[i] == ']' and input_file[i - 1] != '\\':
		adding = True
	else:
		if adding:
			preprocessed += input_file[i]
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

input_file = preprocessed

if options.book_level == 0:
	input_file = '\\body {' + input_file + '}'

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
			format = l[1:-1]
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

def get_intermediate(line):
	'''
	Get intermediate representation
	'''
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
				result.append(get_intermediate(line))
			else:
				index += 1
				tag.parameters.append(get_intermediate(line))
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

intermediate_representation = get_intermediate(lexems)

if options.book_level == 0:
	documents = [Document('_', intermediate_representation)]
else:
	documents = []
	document = Document('_', [])
	level = ['_', '_', '_', '_', '_', '_']
	for element in intermediate_representation:
		if isinstance(element, Tag) and \
				(element.id == '1' or element.id == '2'):
			if document.content != []:
				documents.append(document)
				level[int(element.id)] = element.parameters[1][0]
				document = Document(level[:int(element.id) + 1], [element])
		else:
			document.content.append(element)
	if document.content != []:
		documents.append(document)

no_tags = []

def process_inner_block(innerblock):
	if isinstance(innerblock[0], str):
		innerblock[0] = innerblock[0].lstrip()
	if isinstance(innerblock[-1], str):
		innerblock[-1] = innerblock[-1].rstrip()
	if len(innerblock) == 1 and innerblock[0] == '':
		return ''
	paragraphs = []
	paragraph = []
	for item in innerblock:
		if isinstance(item, str):
			previous = 0
			delimeter = item.find('\n\n')
			while delimeter != -1:
				content = item[previous:delimeter].strip()
				if content != '' or previous == 0:
					paragraph.append(content)
					paragraphs.append(paragraph)
					paragraph = []
				previous = delimeter + 1
				delimeter = item.find('\n\n', delimeter + 1)
			paragraph.append(item[previous:])
		else:
			paragraph.append(item)
	paragraphs.append(paragraph)
	s = ''
	for paragraph in paragraphs:
		s += str(parse(Tag('text', [paragraph])))
	return s

level = 0

def parse(text, inblock = False):
	global level
	global language
	global title
	if text == None or text == '' or text == []:
		return ''
	elif isinstance(text, str):
		return trim_inside(text)
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
	else: # if text is list of items
		s = ''
		innerblock = []
		for item in text:
			if inblock:
				if isinstance(item, Tag) and item.id in block_tags:
					if innerblock != []:
						s += process_inner_block(innerblock)
						innerblock = []
					s += str(parse(item))
				else:
					innerblock.append(item)
			else:
				s += str(parse(item))
		if innerblock != []:
			s += process_inner_block(innerblock)
			innerblock = []
		return s

title = '_'

if options.book_level == 0:
	p = parse(documents[0].content)
	output_file.write(p)
else:
	for document in documents:
		name = '_'
		for level in document.id[1:]:
			name += '/' + level
		try:
			os.makedirs(name)
		except:
			a += ''
		name += '/index.html'
		output = open(name, 'w+')
		level = len(document.id)
		title = name
		output.write(parse(Tag('body', [document.content])))

if len(no_tags) > 0:
	print 'Tags not found:'
	for k in set(no_tags):
		print '  ' + str(k)
