# -*- coding: utf-8 -*-

"""
Moire library.

This file is a part of Moire project—light markup language.

Author: Sergey Vartanov (me@enzet.ru).

See http://github.com/enzet/Moire
"""

import sys
import os
import re

# Global variables

index = 0
markup_format = None
no_tags = []
id_list = ['_', '_', '_', '_', '_', '_', '_']
status = {}

# Constants

comment_begin = '/*'
comment_end = '*/'

paragraph_delimiter = '\n\n'


def error(message):
    print ' [ERROR] ' + str(message) + '.'


class Tag:
    """
    Moire tag definition. Tag has name and parameters:
    \<tag name> {<parameter 1>} ... {<parameter N>}.
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


class Tree:
    def __init__(self, parent, children, element):
        self.element = element
        self.parent = parent
        self.children = children
        self.number = 0

    def pr(self):
        print self.element
        for child in self.children:
            child.pr()

    def find(self, text):
        if len(self.element.parameters) > 1 and \
                self.element.parameters[1][0] == text:
            return self
        for child in self.children:
            a = child.find(text)
            if a:
                return a
        return None


def is_space(c):
    return c in ' \n\t\r'


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


def comments_preprocessing(text):
    """
    Text to text processing: comments removing.
    """
    preprocessed = ''
    adding = True
    i = 0
    while i < len(text):
        if text[i:i + 2] == comment_begin:
            adding = False
            i += 1
        elif text[i:i + 2] == comment_end:
            adding = True
            i += 1
        else:
            if adding:
                preprocessed += text[i]
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
            if isinstance(item, str):
                s += item
        return escape(s, markup_format.name, True)
    return escape(text, markup_format.name, True)


def escape(text, format_name, from_clear=False):
    if format_name == 'Tex':
        if from_clear:
            return text\
                .replace('%', '\\%')\
                .replace('$', '\\$')\
                .replace('|', 'VERTICAL')\
                .replace('∞', 'inf')\
                .replace('−', 'minus')\
                .replace('[', '[')\
                .replace(']', ']')\
                .replace('"', 'kav')\
                .replace('─', 'line')\
                .replace('#', 'sharp')
        else:
            return text\
                .replace('%', '\\%')\
                .replace('$', '\\$')\
                .replace('|', 'VERTICAL')\
                .replace('_', '\\_')\
                .replace('∞', 'inf')\
                .replace('−', 'minus')\
                .replace('[', '[')\
                .replace(']', ']')\
                .replace('"', 'kav')\
                .replace('─', 'line')\
                .replace('#', 'sharp')
    elif format_name == 'HTML':
        return text\
            .replace('&', '&amp;')\
            .replace('~', '&nbsp;')\
            .replace('<', '&lt;')\
            .replace('>', '&gt;')
    elif format_name == 'RTF':
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
    else:
        return text


def get_intermediate(lexemes, positions, level, index=0):
    """
    Get intermediate representation.
    """
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
                index, res = get_intermediate(lexemes, positions, level, index)
                result.append(res)
            else:
                index += 1
                index, res = get_intermediate(lexemes, positions, level, index)
                tag.parameters.append(res)
            index += 1
            continue
        elif item.type == 'parameter_end':
            level -= 1
            if level < 0:
                position = positions[index]
                print 'Lexer error at ' + str(position) + '.'
                #print input_file[position - 10:position + 10]\
                #        .replace('\n', ' ').replace('\t', ' ')
                #print '          ^'
                index += 1
                sys.exit(1)
            if tag:
                result.append(tag)
            return index, result
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
    return index, result


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


def parse(text, inblock=False, depth=0, mode=''):
    """
    Element parsing into formatted text. Element may be plain text, tag, or
    list of elements.
    """
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
        key = 'header' if (text.id in '123456') else text.id
        method = None
        try:
            method = getattr(markup_format, mode + key)
        except Exception as e:
            pass
        if method:
            s = ''
            if key == 'header':
                s += str(method(text.parameters, int(text.id)))
            else:
                s += str(method(text.parameters))
            return s
        no_tags.append(mode + key)
        try:
            method = getattr(markup_format, mode + 'notag')
        except Exception as e:
            pass
        if method:
            return str(method([key] + text.parameters))
        if not mode:
            error('No such tag: ' + mode + key)
    else:  # if text is list of items
        s = ''
        inner_block = []
        for item in text:
            if inblock:
                if isinstance(item, Tag) and item.id in markup_format.block_tags:
                    if inner_block:
                        s += process_inner_block(inner_block)
                        inner_block = []
                    s += str(parse(item, inblock=inblock, depth=depth + 1, \
                        mode=mode))
                else:
                    inner_block.append(item)
            else:
                s += str(parse(item, inblock=inblock, depth=depth + 1, \
                    mode=mode))
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


def convert(input, format='HTML', language='en', remove_comments=True,
        rules='default', wrap=True, opt=None):
    """
    Convert Moire text without includes but with comments artefacts to selected
    format.
    """

    global index
    global id_list
    global markup_format
    global status

    status['language'] = language
    status['title'] = '_'
    status['level'] = 0
    status['root'] = '/Users/Enzet/Program/Book/_'
    status['image'] = False

    if opt:
        for key in opt:
            status[key] = opt[key]

    # Initialization

    result = input
    __import__(rules)
    module = sys.modules[rules]
    markup_format = module.__dict__[format]()
    if not markup_format:
        return None

    # Comments preprocessing

    if remove_comments:
        result = comments_preprocessing(result)

    lexemes, positions = lexer(result)
    index = 0
    intermediate_representation = \
        get_intermediate(lexemes, positions, status['level'])

    # Construct content table

    tree = Tree(None, [], Tag('0', ['_', '_']))
    content_root = tree
    for k in intermediate_representation:
        if isinstance(k, Tag) and k.id in '123456':
            element = Tree(tree, [], k)
            if int(k.id) > int(tree.element.id):
                tree.children.append(element)
                element.number = len(tree.children) - 1
                tree = tree.children[-1]
            else:
                while int(k.id) <= int(tree.element.id):
                    tree = tree.parent
                tree.children.append(element)
                element.number = len(tree.children) - 1
                element.parent = tree
                tree = tree.children[-1]
    status['tree'] = content_root
    markup_format.tree = content_root

    # Wrap whole text with "body" tag

    if wrap:
        intermediate_representation = \
            Tag('body', [intermediate_representation, content_root])

    parse(intermediate_representation, False, 0, 'pre_')
    result = parse(intermediate_representation)

    return result


def include(input_file, directory, path=None, offset=0, prefix=''):
    input = ''
    if path == None:
        path = []
    l = None
    while l != '':
        l = input_file.readline()
        if '\\include {' in l:
            file_name = re.match('\\\\include \{(?P<name>[\w\._/-]*)\}' +
                '( \{(?P<prefix>[\w_])\} \{(?P<offset>[\d-])\})?\n', l)\
                .group('name')
            found = False
            if os.path.isfile(file_name):
                l = include(open(file_name), directory, path) + '\n'
                found = True
            else:
                for direct in [directory] + path:
                    if os.path.isfile(direct + '/' + file_name):
                        l = include(open(direct + '/' + file_name), \
                            directory, path) + '\n'
                        found = True
                        break
            if not found:
                error('no such file to include: ' + file_name)
                l = '\n'
        input += l
    return input


def full_parse(input_file, directory, path=None, offset=0, prefix=''):
    if path == None:
        path = []

    text = input_file.read()
    text = comments_preprocessing(text)
    lexemes, positions = lexer(text)
    index, raw_IR = get_intermediate(lexemes, positions, 0, 0)

    resulted_IR = []

    for item in raw_IR:
        if isinstance(item, Tag):
            if item.id == 'include':
                file_name = item.parameters[0][0]
                offset1, prefix1 = 0, ''
                if len(item.parameters) > 1:
                    prefix1 = item.parameters[1][0]
                if len(item.parameters) > 2:
                    offset1 = int(item.parameters[2][0])
                found = False
                if os.path.isfile(file_name):
                    resulted_IR += full_parse(open(file_name), directory, path, offset1, prefix1)
                    found = True
                else:
                    for direct in [directory] + path:
                        if os.path.isfile(direct + '/' + file_name):
                            resulted_IR += full_parse(\
                                open(direct + '/' + file_name), \
                                directory, path, offset1, prefix1)
                            found = True
                            break
                if not found:
                    error('no such file to include: ' + file_name)
            elif item.id in '123456' and (offset or prefix):
                new_item = Tag(str(int(item.id) + offset), item.parameters)
                resulted_IR.append(new_item)
            else:
                resulted_IR.append(item)
        else:
            resulted_IR.append(item)

    return resulted_IR


def convert_file(input_file_name, format='html', language='en', 
        remove_comments=True, rules_file='default', wrap=True, opt=None,
        path=None):

    input_file = open(input_file_name)
    directory = ''
    if '/' in input_file_name:
        directory = input_file_name[:input_file_name.rfind('/') + 1]

    input = include(input_file, directory, path)

    return convert(input, format, language, remove_comments, rules_file, wrap, 
        opt=opt)


def construct_book(input_file_name, output_directory, kind='html',
        language='en', rules='default', book_level=2, remove_comments=True,
        path=None):

    global markup_format

    status['language'] = language
    status['title'] = '_'
    status['level'] = 0
    status['root'] = '/Users/Enzet/Program/Book/_'
    status['image'] = True

    # Initialization

    result = open(input_file_name).read()
    __import__(rules)
    module = sys.modules[rules]
    markup_format = module.__dict__[kind]()
    if not markup_format:
        return None

    # Comments preprocessing

    input_file = open(input_file_name, 'r')
    directory = ''
    if '/' in input_file_name:
        directory = input_file_name[:input_file_name.rfind('/') + 1]

    intermediate_representation = full_parse(input_file, directory, path)

    '''
    result = include(input_file, directory, path)
    if remove_comments:
        result = comments_preprocessing(result)

    lexemes, positions = lexer(result)
    index = 0
    intermediate_representation = \
        get_intermediate(lexemes, positions, status['level'])
    '''

    documents = []
    document = Document(['_'], [], 'Enzet')
    level = ['_', '_', '_', '_', '_', '_']

    # Construct content table

    tree = Tree(None, [], Tag('0', ['_', '_']))
    content_root = tree

    for k in intermediate_representation:
        if isinstance(k, Tag) and k.id in '123456':
            element = Tree(tree, [], k)
            if int(k.id) > int(tree.element.id):
                tree.children.append(element)
                element.number = len(tree.children) - 1
                tree = tree.children[-1]
            else:
                while int(k.id) <= int(tree.element.id):
                    tree = tree.parent
                tree.children.append(element)
                element.number = len(tree.children) - 1
                element.parent = tree
                tree = tree.children[-1]

    status['tree'] = content_root
    markup_format.tree = content_root

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
                document = Document(level[:int(element.id) + 1], [element], \
                    str(element.parameters[0][0]))
        else:
            document.content.append(element)

    if document.content != []:
        documents.append(document)

    for document in documents:
        name = output_directory
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

        parse(Tag('body', [document.content]), False, 0, 'pre_')
        output.write(parse(Tag('body', [document.content])))
