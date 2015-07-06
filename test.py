# -*- coding: utf-8 -*-

"""
Tests for Moiré project.

This file is a part of Moiré project—light markup language.

Author: Sergey Vartanov (me@enzet.ru).

See http://github.com/enzet/moire
"""

import moire

red_color = '\033[31m'
green_color = '\033[32m'
clear_color = '\033[0m'

# Positive tests list: Moiré code, HTML equivalent, description.

tests = \
    {
        'html':
        [
            [
                'plain text',
                'plain text',
                'Plain text'
            ],
            [
                'plain  text',
                'plain text',
                'Double space in plain text'
            ],
            [
                '  plain  text  ',
                ' plain text ',
                'Spaces around plain text'
            ],
            [
                '\\b{bold}',
                '<b>bold</b>',
                'Simple tag'
            ],
            [
                '\\b {bold}',
                '<b>bold</b>',
                'Simple tag with space'
            ],
            [
                '\\code{code}',
                '<pre><tt>code</tt></pre>',
                'Verbatim'
            ],
            [
                '\\\\\\{\\}',
                '\\{}',
                'Escaped tags'
            ],
            [
                '\\b{\\}}',
                '<b>}</b>',
                'Escaped tags in tag'
            ],
            [
                '<&>',
                '&lt;&amp;&gt;',
                'Escaped symbols'
            ],
            [
                '&nbsp;',
                '&amp;nbsp;',
                'Escaped'
            ],
            [
                '\\code{<&>&nbsp;}',
                '<pre><tt>&lt;&amp;&gt;&amp;nbsp;</tt></pre>',
                'Escaped in code'
            ],
            [
                '\\b{  bold  }',
                '<b> bold </b>',
                'Simple tag with spaces'
            ],
            [
                '\\b{bold}text',
                '<b>bold</b>text',
                'Simple tag and plain text'
            ],
            [
                '\\b{bold} text',
                '<b>bold</b> text',
                'Simple tag and plain text with space'
            ],
            [
                'text\\b{bold}text',
                'text<b>bold</b>text',
                'Text around tag'
            ],
            [
                'text \\b{bold} text',
                'text <b>bold</b> text',
                'Text around tag with spaces'
            ],
            [
                '\\block {a\n\nt \\tt {tt} t\n\na}',
                '<p>a</p><p>t <tt>tt</tt> t</p><p>a</p>',
                'Text around two tags with spaces'
            ],
            [
                '\\block {a\n\n t \\tt {tt} t \n\na}',
                '<p>a</p><p>t <tt>tt</tt> t</p><p>a</p>',
                'Text around two tags with spaces'
            ],
            [
                '\\block {a\n\n t  \\tt {tt}  t \n\na}',
                '<p>a</p><p>t <tt>tt</tt> t</p><p>a</p>',
                'Text around two tags with spaces'
            ],
            [
                '\\b{bold}\\i{italic}',
                '<b>bold</b><i>italic</i>',
                'Two tags'
            ],
            [
                '\\b{bold} \\i{italic}',
                '<b>bold</b> <i>italic</i>',
                'Two tags with space'
            ],
            [
                '\\b{\\i{bold italic}}',
                '<b><i>bold italic</i></b>',
                'Tag inside tag'
            ],
            [
                '\\href{link}{text}',
                '<a href = "link">text</a>',
                'Tag with multiple parameters'
            ],
            [
                'text \\href{link}{text} text',
                'text <a href = "link">text</a> text',
                'Text around tag with multiple parameters'
            ],
            [
                'text \\href {link} {text} text',
                'text <a href = "link">text</a> text',
                'Text around tag with multiple parameters'
            ],
            [
                '\\href {  link  } {  text  }',
                '<a href = "  link  "> text </a>',
                'Tag with multiple parameters with spaces'
            ],
            [
                '\\table{{{td}}}',
                '<table><tr><td><p>td</p></td></tr></table>',
                'Tag with nested parameters'
            ],
            [
                '\\table{{{\\i {td}}}}',
                '<table><tr><td><p><i>td</i></p></td></tr></table>',
                'Tag in tag with nested parameters'
            ],
            [
                '\\table{{{td}{td}}}',
                '<table><tr><td><p>td</p></td><td><p>td</p></td></tr></table>',
                'Tag with more nested parameters'
            ],
            [
                '[lang language][nolang nolanguage]',
                'language',
                'Language'
            ],
            [
                '\\[lang lang\\]',
                '[lang lang]',
                'Escaped language'
            ],
            [
                '\\\\[lang lang\\\\]',
                '\\lang\\',
                'Not escaped language'
            ],
            [
                'before[lang ]after',
                'beforeafter',
                'Empty language'
            ],
            [
                'before[nolang ]after',
                'beforeafter',
                'Empty nolanguage'
            ],
        ],
        'rtf':
        [
            [
                'АБВ',
                '\\u1040  \\u1041  \\u1042  ',
                'Unicode in RTF'
            ],
        ],
        'tex':
        [
            [
                '_',
                '\\_',
                'Escape sequences in TeX'
            ],
        ],
    }

for f in tests:
    for test in tests[f]:
        converted = moire.convert(test[0], language='lang', wrap=False, format=f)
        if converted == test[1]:
            print ' ' + green_color + ' OK ' + clear_color + '  ' + test[2]
        else:
            print ' ' + red_color + 'FAIL' + clear_color + '  ' + test[2]
            print '       Rule: ' + repr(test[0])
            print '             ' + red_color + repr(converted) + clear_color
            print '             ' + green_color + repr(test[1]) + clear_color
