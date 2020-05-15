"""
author: Sergey Vartanov (me@enzet.ru)
"""

from moire import parse
from moire import clear


depth = 0
status = {}


class html:
    """
    HTML.
    """
    def __init__(self):
        pass

    name = 'HTML'
    extensions = ['html', 'htm']

    escape = {
        '<': '&lt;',
        '>': '&rt;',
        '&': '&amp;',
        }

    block_tags = ['block', 'body', 'code', 'title', 'number', 'list',
        'shortlist', 'image', 'table']

    # Block tags.

    def block(self, arg): return parse(arg[0], inblock=True)

    def body(self, arg):
        status['content'] = []
        s = '''<html>
            <head>
                <meta http-equiv="Content-Type" content="text/html;
                      charset=utf-8">
                <link rel="stylesheet" href="style.css">
            </head>
            <body>'''
        s += parse(arg[0], inblock=True)
        s += '''    </body>
        </html>'''
        return s

    def code(self, arg): return f"<pre><tt>{clear(arg[0])}</tt></pre>"

    def title(self, arg): return f"<title>{parse(arg[0])}</title>"

    def header(self, arg, number):
        return f"<h{number}>{parse(arg[0], inblock=True)}</h{number}>"

    def pre_list(self, arg):
        for item in arg[0]:
            if isinstance(item, list):
                parse(item, mode='pre_')

    def list(self, arg):
        s = "<ul>"
        for item in arg[0]:
            if isinstance(item, list):
                s += f"<li>{parse(item, inblock=True)}</li>"
        s += "</ul>"
        return s

    def shortlist(self, arg):
        s = "<ul>"
        for item in arg[0]:
            if isinstance(item, list):
                s += f"<li>{parse(item)}</li>"
        s += "</ul>"
        return s

    def pre_shortlist(self, arg):
        for item in arg[0]:
            if isinstance(item, list):
                parse(item, mode='pre_')

    def image(self, arg):
        return \
            f'<img src="{arg[0][0]}"' + \
            (f' alt="{parse(arg[1])}"' if len(arg) >= 2 else "") + " />"

    def table(self, arg):
        s = '<table>'
        for tr in arg[0]:
            if isinstance(tr, list):
                s += '<tr>'
                for td in tr:
                    if isinstance(td, list):
                        s += '<td>' + parse(td, inblock=True) + '</td>'
                s += '</tr>'
        s += '</table>'
        return s

    # Inner tags.

    def b(self, arg):
        return f"<b>{parse(arg[0])}</b>"

    def br(self, arg):
        return '<br />'

    def href(self, arg):
        return '<a href="' + arg[0][0] + '">' + parse(arg[1]) + '</a>'

    def formal(self, arg):
        return '&lt;<u>' + parse(arg[0]) + '</u>&gt;'

    def i(self, arg):
        return f"<i>{parse(arg[0])}</i>"

    def size(self, arg):
        return f'<span style="font-size: {arg[0]}">{parse(arg[1])}</span>'

    def strike(self, arg):
        return f"<s>{parse(arg[0])}</s>"

    def sc(self, arg):
        return f'<span style="font-variant: small-caps;">{parse(arg[0])}</span>'

    def sub(self, arg):
        return f"<sub>{parse(arg[0])}</sub>"

    def super(self, arg):
        return f"<sup>{parse(arg[0])}</sup>"

    def text(self, arg):
        return f"<p>{parse(arg[0])}</p>"

    def tt(self, arg):
        return f"<tt>{parse(arg[0])}</tt>"

    def u(self, arg):
        return f"<u>{parse(arg[0])}</u>"

    def quote(self, arg):
        return f"<blockquote>{parse(arg[0])}</blockquote>"


class text:
    """
    Plain text.
    """
    name = 'Text'
    extension = 'txt'

    escape = {
        '<': '&lt;',
    }

    def body(self, arg):
        def justify(text, width):
            k = ''
            i = 0
            for a in text:
                k += a
                if i % width == 0:
                    k += '\n'
                i += 1
            return k
        return parse(arg[0], inblock=True, depth=1) + '\n'
    def code(self, arg): return clear(arg[0]) + '\n'
    def header(self, arg, number):
        return '  ' * (number - 1) + parse(arg[0], depth=depth + 1)
    def list(self, arg):
        s = ''
        for item in arg[0]:
            if isinstance(item, list):
                s += '  * ' + parse(item, inblock=True, depth=depth + 1)
        return s
    def table(self, arg):
        s = '+----------+----------+\n'
        for tr in arg[0]:
            s += '|'
            for td in tr:
                s += ' ' + parse(td, inblock=True, depth=depth + 1) + ' |'
            s += '\n'
            s += '+----------+----------+\n'
        return s
    def b(self, arg): return parse(arg[0], depth=depth + 1)
    def href(self, arg): return parse(arg[1], depth=depth + 1) + ' (' + arg[0][0] + ')'
    def i(self, arg): return parse(arg[0], depth=depth + 1)
    def size(self, arg): return parse(arg[0], depth=depth + 1)
    def strike(self, arg): return parse(arg[0], depth=depth + 1)
    def sc(self, arg): return parse(arg[0], depth=depth + 1)
    def sub(self, arg): return parse(arg[0], depth=depth + 1)
    def super(self, arg): return parse(arg[0], depth=depth + 1)
    def text(self, arg): return parse(arg[0], depth=depth + 1) + '\n\n'
    def tt(self, arg): return parse(arg[0], depth=depth + 1)
    def u(self, arg): return parse(arg[0], depth=depth + 1)


# Plain text without formatting.

class rawtext:

    name = 'Text'
    extension = 'txt'

    escape = {
        '<': '&lt;',
    }

    block_tags = ['block', 'body', 'code', 'title', 'number', 'list',
        'shortlist', 'image', 'table']

    def body(self, arg):
        def justify(text, width):
            k = ''
            i = 0
            for a in text:
                k += a
                if i % width == 0:
                    k += '\n'
                i += 1
            return k
        return parse(arg[0], inblock=True, depth=1) + '\n'
    def header(self, arg, number): return parse(arg[0])
    def list(self, arg):
        s = ''
        for item in arg[0]:
            if isinstance(item, list):
                s += '  * ' + parse(item, inblock=True, depth=depth + 1)
        return s
    def table(self, arg):
        s = ''
        for tr in arg[0]:
            for td in tr:
                s += ' ' + parse(td, inblock=True, depth=depth + 1) + ' |'
            s += '\n'
        return s
    def b(self, arg): return parse(arg[0])
    def href(self, arg): return parse(arg[1])
    def i(self, arg): return parse(arg[0])
    def size(self, arg): return parse(arg[0])
    def strike(self, arg): return parse(arg[0])
    def sc(self, arg): return parse(arg[0])
    def sub(self, arg): return parse(arg[0])
    def super(self, arg): return parse(arg[0])
    def text(self, arg): return parse(arg[0]) + '\n\n'
    def u(self, arg): return parse(arg[0])


# Markdown.

class markdown:
    name = 'Markdown'
    extensions = ['md', 'markdown']

    block_tags = ['block', 'body', 'code', 'title', 'number', 'list',
        'shortlist', 'image', 'table']

    level = 0

    def block(self, arg): return parse(arg[0], inblock=True)
    def body(self, arg):
        counter = []
        s = '<!-- PLEASE DO NOT EDIT THIS FILE.\n'
        s += '     IT WAS GENERATED BY MOIRE.    -->\n\n'
        s += parse(arg[0], inblock=True)
        return s
    def header(self, arg, number):
        s = ''
        if number == 1:
            parsed = parse(arg[0])
            s += parsed + '\n' + '=' * len(parsed)
        elif number == 2:
            parsed = parse(arg[0])
            s += parsed + '\n' + '-' * len(parsed)
        else:
            s += (number * '#') + ' ' + parse(arg[0]) + ' ' + (number * '#')
        return s
    def list(self, arg):
        n = 0
        s = ''
        for item in arg[0]:
            if isinstance(item, list):
                n += 1
                s += str(n) + '. ' + parse(item, inblock=True)
        return s
    def shortlist(self, arg):
        s = ''
        n = 0
        for item in arg[0]:
            if isinstance(item, list):
                n += 1
                self.level += 1
                s += '\n' + ('   ' * (self.level - 1)) +  '* ' + parse(item) + '\n'
                self.level -= 1
        return s
    def table(self, arg):
        s = ''
        for index, tr in enumerate(arg[0]):
            if isinstance(tr, list):
                s += '|'
                for td in tr:
                    if isinstance(td, list):
                        s += ' ' + parse(td) + ' |'
                s += '\n'
                if index == 0:
                    s += '|'
                    for td in tr:
                        if isinstance(td, list):
                            s += '---|'
                    s += '\n'
        return s

    def b(self, arg): return '**' + parse(arg[0]) + '**'
    def code(self, arg): return '    ' + parse(arg[0]).replace('\n', '\n    ')
    def href(self, arg): return '\[' + parse(arg[0]) + '\](' + parse(arg[0]) + ')'
    def i(self, arg): return '*' + parse(arg[0]) + '*'
    def image(self, arg): return '!\[' + parse(arg[0]) + '\](' + parse(arg[0]) + ')'
    def formal(self, arg): return '<' + parse(arg[0]) + '>'
    def tt(self, arg): return '`' + str(parse(arg[0])) + '`'
    def u(self, arg): pass
    def text(self, arg): return parse(arg[0]) + '\n\n'
    def quote(self, arg): return '>' + parse(arg[0]) + ''


# TeX.

class tex:
    name = 'Tex'
    extension = 'tex'

    escape = {
        '_': '\\_',
        }

    block_tags = ['block', 'body', 'code', 'title', 'number', 'list',
        'shortlist', 'image', 'table']

    def body(self, arg):
        s = '''\\documentclass[twoside,psfig]{article}:
        \\usepackage[utf8]{inputenc}
        \\usepackage[russian]{babel}
        \\usepackage{enumitem}
        \\usepackage{float}
        \\usepackage[margin=3cm,hmarginratio=1:1,top=32mm,columnsep=20pt]{geometry}
        \\usepackage{graphicx}
        \\usepackage{hyperref}
        \\usepackage{multicol}
        \\begin{document}'''
        s += parse(arg[0], inblock=True)
        s += '\\end {document}'
        return s

    def title(self, arg):
        s = '\\title{' + parse(arg[0]) + '}'
        s += '\\vspace{12em}\\begin{center}{\\huge ' + parse(arg[0]) + '}\\end{center}\\vspace{2em}'
        return s

    def header(self, arg, number):
        if number == 1:
            return '\\section{' + parse(arg[0]) + '}'
        if number == 2:
            return '\\subsection{' + parse(arg[0]) + '}'
        if number == 3:
            return '\\subsubsection{' + parse(arg[0]) + '}'
        if number == 4:
            return '\\paragraph{' + parse(arg[0]) + '}'
        if number == 5:
            return '\\subparagraph{' + parse(arg[0]) + '}'
        if number == 6:
            return '' + parse(arg[0]) + ''

    def table(self, arg):
        s = '\\begin{table}[h]\n\\begin{center}\n\\begin{tabular}{|'
        max_tds = 0
        for tr in arg[0]:
            if isinstance(tr, list):
                tds = 0
                for td in tr:
                    if isinstance(td, list):
                        tds += 1
                if tds > max_tds:
                    max_tds = tds
        for k in range(max_tds):
            s += 'p{2cm}|'
        s += '}\n\\hline\n'
        for tr in arg[0]:
            if isinstance(tr, list):
                tds = []
                for td in tr:
                    if isinstance(td, list):
                        tds.append(td)
                for td in tds[:-1]:
                    s += parse(td) + ' & '
                s += parse(tds[-1])
                s += ' \\\\\n\\hline\n'
        s += '\\end{tabular}\n\\end{center}\n\\end{table}\n'
        return s

    def list(self, arg):
        s = '\\begin{itemize}\n'
        for item in arg[0]:
            if isinstance(item, list):
                s += '\\item ' + parse(item) + '\n\n'
        s += '\\end{itemize}\n'
        return s

    def shortlist(self, arg):
        s = '\\begin{itemize}[itemsep=-0.5ex]\n'
        for item in arg[0]:
            if isinstance(item, list):
                s += '\\item ' + parse(item) + '\n\n'
        s += '\\end{itemize}\n\n'
        return s

    def ordered(self, arg):
        s = '\\begin{ordered}\n'
        for item in arg[0]:
            if isinstance(item, list):
                s += '\\item ' + parse(item[0]) + '\n\n'
        s += '\\end{ordered}\n'
        return s

    def annotation(self, arg): return '\\begin {abstract}\n\n' + parse(arg[0], inblock=True) + '\\end {abstract}\n\n'

    def books(self, arg):
        s = '\\begin{thebibliography}{0}\n\n'
        for item in arg[0]:
            if isinstance(item, list):
                s += '\\bibitem{' + item[0][0] + '} ' + parse(item[1]) + '\n\n'
        s += '\\end{thebibliography}\n\n'
        return s
        
    def b(self, arg): return '{\\bf ' + parse(arg[0]) + '}'
    def br(self, arg): return '\\\\'
    def cite(self, arg): return '\\cite {' + arg[0][0] + '}'
    def code(self, arg): return '\\begin{verbatim}' + arg[0][0] + '\\end{verbatim}'
    def date(self, arg): pass
    def href(self, arg):
        s = ''
        link = arg[0][0]
        if link[0] == '#':
            link = link[1:]
        if len(arg) == 1:
            s += '\\href {' + link + '} {' + link + '}'
        else:
            s += '\\href {' + link + '} {' + parse(arg[1]) + '}'
        return s
    def i(self, arg): return '{\\em ' + parse(arg[0]) + '}'
    def math(self, arg): return '$' + ''.join(arg[0]) + '$'
    def mathblock(self, arg): return '\\[' + ''.join(arg[0]) + '\\]'
    def ignore(self, arg): return '' + arg[0][0] + ''
    def image(self, arg):
        s = '\\begin{figure}[h]\\begin{center}\\includegraphics{' + parse(arg[0]) + '}\\end{center}'
        if len(arg) > 1:
            s += '\\caption {' + parse(arg[1]) + '}'
        s += '\\end{figure}'
        return s
    def item(self, arg): return '\\item ' + parse(arg[0]) + ''
    def page(self, arg): return '\\textsuperscript{' + parse(arg[0]) + '}'
    def sc(self, arg): return '{\\sc ' + parse(arg[0]) + '}'
    def size(self, arg): return '' + parse(arg[0]) + ''
    def strike(self, arg): return '' + parse(arg[0]) + ''
    def sub(self, arg): return '$_{' + parse(arg[0]) + '}$'
    def super(self, arg): return '\\textsuperscript{' + parse(arg[0]) + '}'
    def text(self, arg): return parse(arg[0]) + '\n\n'
    def tr(self, arg): return '' + parse(arg[0]) + '|'
    def td(self, arg): return '| ' + parse(arg[0]) + ''
    def tt(self, arg): return '{\\tt ' + parse(arg[0]) + '}'
    def u(self, arg): return '' + parse(arg[0]) + ''
    def quote(self, arg): return '' + parse(arg[0]) + ''
    def cite(self, arg): return '\\cite{' + arg[0][0] + '}'


# RTF.

class rtf:
    name = 'RTF'

    def block(self, arg): return parse(arg[0], inblock=True)
    def body(self, arg):
        status['levels'] = [0, 0, 0, 0, 0, 0, 0]
        status['bookindex'] = 0
        status['books'] = {}
        s = '''{\\rtf0\\ansi\\deff0\n{\\*\\listtable{\\list\\listtemplateid1
        {\\listlevel\\levelnfc23{\\leveltext \\'01\\u8226 ?;}\\li720}
        {\\listlevel\\levelnfc23{\\leveltext \\'01\\u9702 ?;}\\li1080}
        {\\listlevel\\levelnfc23{\\leveltext \\'01\\u9642 ?;}\\li1440}
        {\\listlevel\\levelnfc23{\\leveltext \\'01\\u8226 ?;}\\li1800}
        {\\listlevel\\levelnfc23{\\leveltext \\'01\\u9702 ?;}\\li2160}
        {\\listlevel\\levelnfc23{\\leveltext \\'01\\u9642 ?;}\\li2520}
        {\\listlevel\\levelnfc23{\\leveltext \\'01\\u8226 ?;}\\li2880}
        {\\listlevel\\levelnfc23{\\leveltext \\'01\\u9702 ?;}\\li3240}
        {\\listlevel\\levelnfc23{\\leveltext \\'01\\u9642 ?;}\\li3600}\\listid1}}
        {\\listoverridetable{\\listoverride\\listid1\\ls1}}
        {\\fonttbl{\\f1 Courier 10 Pitch;}{\\f2 Arial;}{\\f3 Times New Roman;}}\\fs20'''
        s += '{\\f3 ' + parse(arg[0], inblock=True) + '}'
        s += '\n}'
        return s
    def title(self, arg): return '\\par\\pard \\qc\\b\\sb346\\sa173{\\f2{\\fs32 ' + parse(arg[0]) + '  \\fs20}}\\b0\n'
    def table(self, arg): return parse(arg[0])
    def list(self, arg):
        s = ''
        for item in arg[0]:
            if isinstance(item, list):
                lc = 0  # FIXME
                lc += 1
                s += parse(item) + ' '
                lc -= 1
                if lc == 0:
                    s += '\\par\\pard'
        return s
    def header(self, arg, number):
        if number == 1:
            status['levels'][1] += 1
            status['levels'][2] = 0
            status['levels'][3] = 0
            level = status['levels'][1]
            return '\\i\\b\\sb346\\sa173{\\f2\\fs22 ' + str(level) + '. ' + parse(arg[0]) + '\\fs20}\\b0\\i0\n'
        elif number == 2:
            status['levels'][2] += 1
            status['levels'][3] = 0
            level = str(status['levels'][1]) + '.' + str(status['levels'][2]) + ' '
            return '\\b\\par\\pard\\sb346\\sa173{\\fs22 ' + level + parse(arg[0]) + '\\fs20}\\b0\n'
        elif number == 3:
            status['levels'][3] += 1
            level = str(status['levels'][1]) + '.' + str(status['levels'][2]) + '.' + str(status['levels'][3]) + ' '
            return '\\parb\\par\\pard\\sb346\\sa173{\\fs20 ' + level + parse(arg[0]) + '\\fs20}\\b0\\i0\n'
        elif number == 4:
            return '\\parpar\\pard\\sb346\\sa173{\\fs20 ' + parse(arg[0]) + '\\fs20}\\b0\n'
        elif number == 5:
            return '\\b\\sb346\\sa173{\\fs20 ' + parse(arg[0]) + '\\fs20}\\b0\n'
        elif number == 6:
            return '\\b\\sb346\\sa173{\\fs20 ' + parse(arg[0]) + '\\fs20}\\b0\n'
    def center(self, arg): return '\\qc' + parse(arg[0])
    def left(self, arg): return '\\ql' + parse(arg[0])
    def right(self, arg): return '\\qr' + parse(arg[0])
    def b(self, arg): return '\n\\b ' + parse(arg[0]) + '\\b0\n'
    def code(self, arg): return parse(arg[0])
    def font(self, arg): return ''
    def href(self, arg): return '{\\field{\\*\\fldinst{HYPERLINK  "' + parse(arg[0]) + '"}}{\\fldrslt{\\u1  ' + parse(arg[-1]) +'\n}}}'
    def i(self, arg): return '\\i ' + parse(arg[0]) + '\\i0\n'
    def math(self, arg): return parse(arg[0])
    def ignore(self, arg): return parse(arg[0])
    def image(self, arg): return parse(arg[0])
    def shortlist(self, arg): return parse(arg[0])
    def ordered(self, arg): return '\\levelnfc0\\list ' + parse(arg[0]) + ' \\list0'
    def s(self, arg): return '\\strike ' + parse(arg[0]) + '\\strike0'
    def sc(self, arg): return '\\scaps ' + parse(arg[0]) + '\\scaps0\n'
    def size(self, arg): return '\\fs' + str(int(parse(arg[0])) * 2) + parse(arg[1])
    def strike(self, arg): return parse(arg[0])
    def sub(self, arg): return '\\sub ' + parse(arg[0]) + '\\nosupersub\n'
    def super(self, arg): return '\\super ' + parse(arg[0]) + '\\nosupersub\n'
    def tr(self, arg): return parse(arg[0]) + '|'
    def td(self, arg): return '| ' + parse(arg[0])
    def tt(self, arg): return '{\\f1 ' + parse(arg[0]) + '}'
    def u(self, arg): return '\\ul ' + parse(arg[0]) + '\\ul0\n'
    def quote(self, arg): return parse(arg[0])
    def book(self, arg): return parse(arg[0])
    def books(self, arg):
        s = ''
        # for item in arg[0]:
        #   if isinstance(item, list):
        #       s += '\\par\\pard [' + status[] + '] ' + parse(item[1]) + '\n\n'
        for index in range(status['bookindex']):
            s += '\\par\\pard\\li720\\fi-360[' + str(index + 1) + ']\\tab '
            for item in arg[0]:
                if isinstance(item, list):
                    if status['books'][item[0][0]] == index + 1:
                        s += parse(item[1])
        s += '\\par\\pard'
        return s
    def cite(self, arg):
        s = ''
        cites = arg[0][0].split(', ')
        for cite in cites:
            print(cite, status['books'])
            if not (cite in status['books']):
                status['bookindex'] += 1
                status['books'][cite] = status['bookindex']
        s += '['
        s += str(status['books'][cites[0]])
        for cite in cites[1:]:
            s += ', ' + str(status['books'][cite])
        s += ']'
        return s
    def text(self, arg): return '\\par\\pard\\qj' + parse(arg[0]) + '\n'
    def br(self, arg): return '\\par\\pard'
