# -*- coding: utf-8 -*-

'''
File conversion from Moire markup language to other formats.

Usage: python moire.py -i <input file> -o <output file> -t <format> 
                       -r <rules file>

Options:
    -i <file>   input file name
    -o <file>   output file name
    -f <format> resulted format
    -r <file>   rules file name

This file is a part of Moire project—light markup language.

Author: Sergey Vartanov (me@enzet.ru)

See http://github.com/enzet/moire
'''

import argparse
import sys
import re

parser = argparse.ArgumentParser()

parser.add_argument('-i', dest = 'input')
parser.add_argument('-o', dest = 'output')
parser.add_argument('-f', dest = 'format')
parser.add_argument('-r', dest = 'rules')

options = parser.parse_args(sys.argv[1:])

input_file = open(options.input).read()
output_file = open(options.output, 'w+')
prep_file = open('preprocessed', 'w+')
rules_file = open(options.rules)

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

langs = ['ru']

preprocessed = ''
adding = True
 
i = 0
while i < len(input_file):
	c = input_file[i]
	if c == '[' and input_file[i - 1] != '\\':
		end = input_file.find(' ', i)
		if input_file[i + 1:end] == 'ru':
			adding = True
			i = end
		else:
			adding = False
			i = end
	elif c == ']' and input_file[i - 1] != '\\':
		i += 1
		adding = True
	else:
		if adding:
			preprocessed += c
	i += 1

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

input_file = '\\begin {} ' + preprocessed + '\\end {} '

prep_file.write(input_file)

rules = []
right = ''
rule = None

l = rules_file.readline()
while l != '':
	if l[1] != '\t':
		if rule != None:
			rule[2] = right
			rules.append(rule)
		rule = [l[1:l.find(':')], '', '']
		right = l[l.find(':') + 1:].strip()
	else:
		right += l[2:]
	l = rules_file.readline()

if rule != None:
	rule[2] = right
	rules.append(rule)

def is_space(c):
	if c == ' ' or c == '\n' or c == '\t' or c == '\r':
		return True
	else:
		return False

def lexer(tx):
	in_tag = False
	in_space = True
	lexems = []
	tag_name = ''
	word = ''

	for char in tx:
		if char == '\\':
			if word != '':
				lexems.append(word)
			in_tag = True
			tag_name = '\\'
		elif char == '{':
			if in_tag or in_space:
				in_tag = False
				if tag_name != '':
					lexems.append(tag_name)
			lexems.append('{')
			tag_name = ''
			word = ''
		elif char == '}':
			if word != '':
				lexems.append(word)
			word = ''
			lexems.append('}')
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

	return lexems

lexems = lexer(input_file)

index = 0

def get_line(line):
	global index
	tag = None
	result = []
	level = 0
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
			continue
		elif item == '}':
			if level == 0:
				if tag != None:
					result.append(tag)
				return result
			level -= 1
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

def parse(text):
	if text == None or text == '' or text == []:
		return 'none'
	elif isinstance(text, str):
		return text
	elif isinstance(text, Tag):
		for rule in rules:
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
		for item in text:
			kk = parse(item)
			if kk != None:
				s += kk
		return s

output_file.write(parse(parsed))

print 'No tags: ' + str(set(no_tags))
