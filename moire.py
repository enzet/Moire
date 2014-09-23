import sys
import re

input_file = open(sys.argv[1]).read()
output_file = open(sys.argv[2], 'w+')
prep_file = open('preprocessed', 'w+')

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
	if c == '[':
		end = input_file.find(' ', i)
		if input_file[i + 1:end] == 'ru':
			adding = True
			i = end
		else:
			adding = False
			i = end
	elif c == ']':
		i += 1
		adding = True
	else:
		if adding == True:
			preprocessed += c
	i += 1

input_file = preprocessed

prep_file.write(input_file)

rules = [\
	['title', 1, 's += "<title>" + parse(arg[0]) + "</title>"'],\
	['1',     1, 's += "<h1>" + parse(arg[0]) + "</h1>"'],\
	['2',     1, 's += "<h2>" + parse(arg[0]) + "</h2>"'],\
	['3',     1, 's += "<h3>" + parse(arg[0]) + "</h3>"'],\
	['4',     1, 's += "<h4>" + parse(arg[0]) + "</h4>"'],\
	['5',     1, 's += "<h5>" + parse(arg[0]) + "</h5>"'],\
	['6',     1, 's += "<h6>" + parse(arg[0]) + "</h6>"'],\
	['b',     1, 's += "<b>"  + parse(arg[0]) + "</b>"'],\
	['i',     1, 's += "<i>"  + parse(arg[0]) + "</i>"'],\
	['list',  1, 's += "<ol>" + parse(arg[0]) + "</ol>"'],\
	['item',  1, 's += "<li>" + parse(arg[0]) + "</li>"'],\
	['abbr',  1, 's += "" + parse(arg[0]) + ""'],\
	['code',  1, 's += "<tt><pre>" + arg[0][0] + "</pre></tt>"'],\
	['tt',    1, 's += "<tt>" + parse(arg[0]) + "</tt>"'],\
	['href',  2, 's += "<a href = " + str(arg[0]) + ">" + parse(arg[1]) + "</a>"'],\
	['table', 1, 's += "<table>"\nfor tr in arg[0]:\n s += "<tr>"\n for td in tr:\n  s += "<td>" + parse(td) + "</td>"\n s += "</tr>"\ns += "</table>"']\
]

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
					print 'Error for tag "' + text.id + '" in ' + str(arg) + '.'
				return s
	else:
		s = ''
		for item in text:
			kk = parse(item)
			if kk != None:
				s += kk
		return s

print parsed

output_file.write(parse(parsed))
