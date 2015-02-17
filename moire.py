# -*- coding: utf-8 -*-

"""
Moiré library.

This file is a part of Moiré project—light markup language.

Author: Sergey Vartanov (me@enzet.ru).

See http://github.com/enzet/moire
"""

import sys
import os

# Global variables

index = 0
markup_format = None
no_tags = []
id_list = ['_', '_', '_', '_', '_', '_', '_']
ruwords, enwords = [], []
status = {}

language_begin = '['
language_end = ']'

comment_begin = '/*'
comment_end = '*/'

# Constants

paragraph_delimiter = '\n\n'


class Tag:
    """
    Moiré tag definition
    """
    def __init__(self, tag_id, parameters):
        self.id = tag_id
        self.parameters = parameters

    def __str__(self):
        s = self.id + ' {' + str(self.parameters) + '}'
        return s

    def __repr__(self):
        s = self.id + ' {' + str(self.parameters) + '}'
        return s


class Lexeme:
    def __init__(self, lexeme_type, content=None):
        self.type = lexeme_type
        self.content = content

    def __repr__(self):
        s = self.type
        if self.content:
            s += ' {' + str(self.content.replace('\n', ' ')) + '}'
        return s


class Document:
    def __init__(self, id, content, title):
        self.id = id
        self.content = content
        self.title = title


class Format:
    """
    Markup format.
    """
    def __init__(self, file_name, file_format):
        self.name = file_format  # Format ID: tex, html...
        self.rules = None
        self.block_tags = None
        try:
            rules_file = open(file_name)
        except IOError:
            return
        self.rules = {}
        right = ''
        rule = None
        l = rules_file.readline()
        block = ''

        format1 = ''

        while l != '':
            if l[0] != '\t':
                if format1 == file_format:
                    add_rule(self.rules, rule, right, block)
                rule = None
                if l[0] == ':':
                    format1 = l[1:l.find(':', 2)]
                elif len(l) > 1:
                    block = l[:-2]
            else:
                if l[1] != '\t':
                    if format1 == file_format:
                        add_rule(self.rules, rule, right, block)
                    rule = [l[1:l.find(':')], '', '']
                    right = l[l.find(':') + 1:].strip()
                else:
                    right += l[2:]
            l = rules_file.readline()

        if format1 == file_format:
            add_rule(self.rules, rule, right, block)

        self.block_tags = []
        for a in self.rules['block']:
            self.block_tags.append(a[0])
        rules_file.close()


def is_space(c):
    if c == ' ' or c == '\n' or c == '\t' or c == '\r':
        return True
    else:
        return False


def trim_inside(s):
    """
    Replace all space symbol sequences with one space character.
    """
    ret = ''
    i = 0
    while i < len(s):
        if is_space(s[i]):
            ret += ' '
            while i < len(s) and is_space(s[i]):
                i += 1
            continue
        else:
            ret += s[i]
        i += 1
    return ret


def add_rule(rules, rule, right, block):
    if rule:
        rule[2] = right
        if block in rules:
            rules[block].append(rule)
        else:
            rules[block] = [rule]


def language_preprocessing(input_file, language):
    preprocessed = ''
    adding = True
    i = 0
    while i < len(input_file):
        if input_file[i] == '\\':
            if i == len(input_file) + 1:
                print 'Error: backslash at the end of the string.'
            elif input_file[i + 1] == language_begin or input_file[i + 1] == language_end:
                if adding:
                    preprocessed += input_file[i + 1]
                i += 1
            else:
                if adding:
                    preprocessed += '\\' + input_file[i + 1]
                    i += 1
        elif input_file[i] == language_begin:
            start = i
            i += 1
            while is_letter_or_digit(input_file[i]):
                i += 1
            if input_file[start + 1:i] == language:
                adding = True
            else:
                adding = False
                i += 1
        elif input_file[i] == language_end:
            adding = True
        else:
            if adding:
                preprocessed += input_file[i]
        i += 1
    return preprocessed


def comments_preprocessing(input_file):
    preprocessed = ''
    adding = True
    i = 0
    while i < len(input_file):
        if input_file[i:i + 2] == comment_begin:
            adding = False
            i += 1
        elif input_file[i:i + 2] == comment_end:
            adding = True
            i += 1
        else:
            if adding:
                preprocessed += input_file[i]
        i += 1
    return preprocessed


def is_letter_or_digit(char):
    return 'a' <= char <= 'z' or 'A' <= char <= 'Z' or \
           '0' <= char <= '9'


def lexer(text):
    """
    Parse formatted preprocessed text to a list of lexemes.
    """
    in_tag = False  # Lexer position in tag name
    in_space = True  # Lexer position in space between tag name and first '{'
    lexemes = []
    positions = []
    tag_name = ''
    word = ''

    index = 0

    while index < len(text):
        char = text[index]
        if char == '\\':
            if index == len(text) - 1:
                print 'Error: backslash at the end of string.'
            elif not is_letter_or_digit(text[index + 1]):
                if word != '':
                    lexemes.append(Lexeme('text', word))
                    positions.append(index)
                word = ''
                lexemes.append(Lexeme('symbol', text[index + 1]))
                positions.append(index + 1)
                index += 1
            else:
                if word != '':
                    lexemes.append(Lexeme('text', word))
                    positions.append(index)
                word = ''
                in_tag = True
                tag_name = ''
        elif char == '{':
            if in_tag or in_space:
                in_tag = False
                if tag_name != '':
                    lexemes.append(Lexeme('tag', tag_name))
                    positions.append(index)
            lexemes.append(Lexeme('parameter_begin'))
            positions.append(index)
            tag_name = ''
            word = ''
        elif char == '}':
            if word != '':
                lexemes.append(Lexeme('text', word))
                positions.append(index)
            word = ''
            lexemes.append(Lexeme('parameter_end'))
            positions.append(index)
        elif is_space(char):
            if in_tag:
                in_tag = False
                in_space = True
            else:
                word += char
        # elif char == '<' or char == '>' or char == '&':
        #     if word != '':
        #         lexemes.append(Lexeme('text', word))
        #         positions.append(index)
        #     word = ''
        #     # if char == '<': lexemes.append(Lexeme('symbol', '&lt;'))
        #     # if char == '>': lexemes.append(Lexeme('symbol', '&gt;'))
        #     # if char == '&': lexemes.append(Lexeme('symbol', '&amp;'))
        #     positions.append(index)
        else:
            if in_tag:
                tag_name += char
            else:
                word += char
        index += 1
    if word != '':
        lexemes.append(Lexeme('text', word))
        positions.append(index)

    return lexemes, positions


def clear(text):
    global markup_format
    if isinstance(text, list):
        s = ''
        for item in text:
            s += item
        return escape(s, markup_format.name)
    return escape(text, markup_format.name)


def escape(text, format_name):
    if format_name == 'tex':
        return text\
            .replace('_', '\\_')\
            .replace('∞', 'inf')\
            .replace('−', 'minus')\
            .replace('[', '[')\
            .replace(']', ']')\
            .replace('"', 'kav')\
            .replace('─', 'line')
    if format_name == 'html':
        return text\
            .replace('&', '&amp;')\
            .replace('~', '&nbsp;')\
            .replace('<', '&lt;')\
            .replace('>', '&gt;')
    if format_name == 'rtf':
        text = text.decode('utf-8')
        result = u''
        for c in text:
            if c == u'~':
                result += '\\~'
            elif ord(c) <= 128:
                result += c
            else:
                result += u'\\u' + unicode(ord(c)) + u'  '
        return result.encode('utf-8')


def get_intermediate(lexemes, positions, level):
    """
    Get intermediate representation.
    """
    global index
    tag = None
    result = []
    while index < len(lexemes):
        item = lexemes[index]
        if item.type == 'tag':
            if tag:
                result.append(tag)
            tag = Tag(item.content, [])
        elif item.type == 'parameter_begin':
            level += 1
            if not tag:
                index += 1
                result.append(get_intermediate(lexemes, positions, level))
            else:
                index += 1
                tag.parameters.append(get_intermediate(lexemes, positions, level))
            index += 1
            continue
        elif item.type == 'parameter_end':
            level -= 1
            if level < 0:
                position = positions[index]
                print 'Lexer error at ' + str(position) + '.'
                print input_file[position - 10:position + 10]\
                        .replace('\n', ' ').replace('\t', ' ')
                print '          ^'
                index += 1
                sys.exit(1)
            if tag:
                result.append(tag)
            return result
        elif item.type == 'text':
            if tag:
                result.append(tag)
                tag = None
            result.append(item.content)
        elif item.type == 'symbol':
            if tag:
                result.append(tag)
                tag = None
            result.append(item.content)
        index += 1
    if tag:
        result.append(tag)
    return result


def process_inner_block(inner_block):
    """
    Wrap parts of inner block element with text tag.
    """
    global status
    if len(inner_block) == 1 and inner_block[0] == '':
        return ''
    paragraphs = []
    paragraph = []
    for item in inner_block:
        if isinstance(item, str):
            previous = 0
            delimiter = item.find(paragraph_delimiter)
            while delimiter != -1:
                content = item[previous:delimiter]
                if content != '' or previous == 0:
                    paragraph.append(content)
                    paragraphs.append(paragraph)
                    paragraph = []
                previous = delimiter + len(paragraph_delimiter)
                delimiter = item.find(paragraph_delimiter, delimiter + 1)
            paragraph.append(item[previous:])
        else:
            paragraph.append(item)
    paragraphs.append(paragraph)
    s = ''
    for paragraph in paragraphs:
        if isinstance(paragraph[0], str):
            paragraph[0] = paragraph[0].lstrip()
        if isinstance(paragraph[-1], str):
            paragraph[-1] = paragraph[-1].rstrip()
        s += str(parse(Tag('text', [paragraph])))
    return s


def parse(text, inblock=False, depth=0):
    global level
    global language
    global markup_format
    global no_tags
    global status
    if not text or text == '' or text == []:
        return ''
    elif isinstance(text, str):
        return escape(trim_inside(text), markup_format.name)
    elif isinstance(text, Tag):
        for rule in markup_format.rules['block'] + markup_format.rules['inner']:
            if rule[0] == text.id:
                arg = text.parameters
                s = ''
                hide_errors = True
                if hide_errors:
                    try:
                        exec(rule[2])
                    except:
                        print 'Error for tag "' + text.id + '" in ' + \
                              str(arg)[:100] + \
                              ('...' if len(str(arg)) > 100 else '') + '.'
                else:
                    # print text.id
                    exec(rule[2])
                return s
        no_tags.append(text.id)
    else:  # if text is list of items
        s = ''
        inner_block = []
        for item in text:
            if inblock:
                if isinstance(item, Tag) and item.id in markup_format.block_tags:
                    if inner_block:
                        s += process_inner_block(inner_block)
                        inner_block = []
                    s += str(parse(item))
                else:
                    inner_block.append(item)
            else:
                s += str(parse(item))
        if inner_block:
            s += process_inner_block(inner_block)
        return s


def get_documents(level, intermediate_representation):
    if level == 0:
        documents = [Document('_', intermediate_representation)]
    else:
        documents = []
        document = Document('_', [])
        level = ['_', '_', '_', '_', '_', '_']
        for element in intermediate_representation:
            if isinstance(element, Tag) and \
                    (element.id == '1' or element.id == '2'):
                if document.content:
                    documents.append(document)
                    level[int(element.id)] = element.parameters[1][0]
                    document = Document(level[:int(element.id) + 1], [element])
            else:
                document.content.append(element)
        if document.content:
            documents.append(document)
    return documents


def convert(input, format='html', language='en', remove_comments=True, rules_file='default.ms', wrap=True):

    global index
    global id_list
    global markup_format
    global status

    status['language'] = language
    status['title'] = '_'
    status['level'] = 0
    status['root'] = '/Users/Enzet/Program/Book/_'
    status['image'] = False

    if rules_file == '' or not rules_file:
        rules_file = 'default.ms'

    result = input
    markup_format = Format(rules_file, format)

    if not markup_format:
        return None
    if language != '':
        result = language_preprocessing(result, language)
    if remove_comments:
        result = comments_preprocessing(result)

    lexemes, positions = lexer(result)
    index = 0
    intermediate_representation = get_intermediate(lexemes, positions, status['level'])
    if wrap:
        intermediate_representation = Tag('body', [intermediate_representation])    
    documents = get_documents(0, intermediate_representation)
    result = parse(documents[0].content)

    return result


def construct_book(input_file_name, kind, language, rules_file_name, book_level, output_file_name):

    global markup_format

    status['language'] = language
    status['title'] = '_'
    status['level'] = 0
    status['root'] = '/Users/Enzet/Program/Book/_'
    status['image'] = True

    result = open(input_file_name).read()

    markup_format = Format(rules_file_name, kind)

    print markup_format

    if language != '':
        result = language_preprocessing(result, language)
    result = comments_preprocessing(result)

    documents = []
    document = Document(['_'], [], 'Enzet')
    level = ['_', '_', '_', '_', '_', '_']

    lexemes, positions = lexer(result)
    index = 0
    intermediate_representation = get_intermediate(lexemes, positions, status['level'])

    for element in intermediate_representation:
        if isinstance(element, Tag) and \
                (element.id == '1' or element.id == '2'):
            if document.content != []:
                documents.append(document)
                try:
                    level[int(element.id)] = element.parameters[1][0]
                except IndexError:
                    print 'No ID for header ' + element.parameters[0][0]
                    sys.exit(0)
                document = Document(level[:int(element.id) + 1], [element], str(element.parameters[0][0]))
        else:
            document.content.append(element)
    if document.content != []:
        documents.append(document)

    for document in documents:
        name = '_/' + language
        status['id'] = document.id
        for level in document.id[1:]:
            name += '/' + level
        try:
            os.makedirs(name)
        except:
            pass
        name += '/index.html'
        output = open(name, 'w+')
        status['level'] = len(document.id)
        status['title'] = document.title
        output.write(parse(Tag('body', [document.content])))
