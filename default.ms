author:'Sergey Vartanov (me@enzet.ru)'

:__main

block:
	body {text}:'main top-level tag'
	code {text}:'verbatim text'
	title {text}:'document title'
	1 {text}:'first-level header'
	2 {text}:'second-level header'
	3 {text}:'third-level header'
	4 {text}:'fourth-level header'
	5 {text}:'fifth-level header'
	6 {text}:'sixth-level header'
	list {items}:'list of items'
	image {path} {description}:'picture'
	table {table data}:'table'
	b {text}:'bold'
	href {text}:'hyper reference'
	i {text}:'italic'



:html

name:'HTML'
extension:'html'

escape:
'<':'&lt;'
'>':'&rt;'
'&':'&amp;'

block:
	block: s += parse(arg[0], inblock = True)
	body:
		status['content'] = []
		s += '''<!------------------------------------------------------------------------------ 
		-----                                                                      -----
		-----       PLEASE, DON'T EDIT THIS FILE! IT IS GENERATED FROM MOIRE.      -----
		-----                                                                      -----
		------------------------------------------------------------------------------->
		<html>
			<head>
				<meta http-equiv = "Content-Type" content = "text/html; charset = utf-8">
				<!--<meta http-equiv="refresh" content="10" >-->
				<link rel = "stylesheet" href = "style.css">
			</head>
			<script>
			function show_hide(div_id) {
				div = div_id
			    if (div.style.display == "none")
			    {
			        div.style.display = "block";
			    }
			    else
			    {
			        div.style.display = "none";
			    }
			}
			</script>
			<body>'''
		s += '<div class = top><a href = #>↟</a></div>'
		s += '<span class = content>Top level subpages: '
		for child in arg[1].children:
			if child.element and len(child.element) == 3 and child.element[2]:
				s += '<a href = #' + str(child.element[2][0]) + '>' + parse(child.element[1]) + '</a>, '
		s = s[:-2] + '.</span>'
		s += parse(arg[0], inblock = True)
		s += '''	</body>
		</html>'''
	code: s += '<pre><tt>' + clear(arg[0]) + '</tt></pre>'
	title: s += '<title>' + parse(arg[0]) + '</title>'
	number:
		s += '<h' + str(number)
		if len(arg) == 3:
			s += ' id="' + arg[1][0] + '"'
			status['content'].append([parse(arg[0]), arg[1][0], 2])
		s += '>' + parse(arg[0])
		if len(arg) == 3:
			s += '&nbsp;<span class = normal><sup><a href = #' + arg[1][0] + '>§</a>'
			if arg[2] and arg[2].parent and arg[2].parent.element and arg[2].parent.element[2]:
				s += ' <a href = #' + str(arg[2].parent.element[2][0]) + '>up</a>'
			s += '</sup></span>'
		s += '</h' + str(number) + '>'
		if len(arg) == 3:
			if arg[2] and arg[2].children and len(arg[2].children) > 1:
				s += '<span class = content>Subpages: '
				for child in arg[2].children:
					if child.element and len(child.element) == 3 and child.element[2]:
						s += '<a href = #' + str(child.element[2][0]) + '>' + parse(child.element[1]) + '</a>, '
				s = s[:-2] + '.</span>'
	list:
		s += '<ul>'
		for item in arg[0]:
			if isinstance(item, list):
				s += '<li>' + parse(item, inblock = True) + '</li>'
		s += '</ul>'
	shortlist:
		s += '<ul>'
		for item in arg[0]:
			if isinstance(item, list):
				s += '<li>' + parse(item) + '</li>'
		s += '</ul>'
	image:      
		s += '<img src = "' + arg[0][0] + '" alt = "' + parse(arg[1]) + '" />'
	table:
		s += '<table>'
		for tr in arg[0]:
			if isinstance(tr, list):
				s += '<tr>'
				for td in tr:
					if isinstance(td, list):
						s += '<td>' + parse(td, inblock = True) + '</td>'
				s += '</tr>'
		s += '</table>'
inner:
	b: s += '<b>'  + parse(arg[0]) + '</b>'
	bookquote: s += '<div class = bookquote>' + parse(arg[0]) + '</div>'
	br: s += '<br />'
	comment: s += '<i class = comment>' + parse(arg[0]) + '</i>'
	href: s += '<a href = "' + arg[0][0] + '">' + parse(arg[1]) + '</a>'
	href_no_parse: s += parse(arg[1])
	i: s += '<i>'  + parse(arg[0]) + '</i>'
	size:
		s += '<span style = "font-size: ' + str(arg[0]) + '">' + \
			parse(arg[1]) + '</span>'
	strike: s += '<s>' + parse(arg[0]) + '</s>'
	sc: s += '<span style = "font-variant: small-caps;">' + parse(arg[0]) + '</span>'
	sub: s += '<sub>' + parse(arg[0]) + '</sub>'
	super: s += '<sup>' + parse(arg[0]) + '</sup>'
	text: s += '<p>' + parse(arg[0]) + '</p>'
	tt: s += '<tt>' + parse(arg[0]) + '</tt>'
	u: s += '<u>' + parse(arg[0]) + '</u>'
	quote: s += '<blockquote>' + parse(arg[0]) + '</blockquote>'
	date:
	page: s += '<span class = page>' + arg[0][0] + '</span>'
	formal: s += '&lt;' + arg[0][0] + '&gt;'
	red: s += '<span style = "color: red;">' + parse(arg[0]) + '</span>'
	hidden: s += '<a class = hidden href = "javascript:show_hide(' + arg[0][0] + ')">' + parse(arg[1]) + '</a><div style = "display: none" class = hidden id = ' + arg[0][0] + '>' + parse(arg[2]) + '</div>'

:text

name:'Text'
extension:'txt'

escape:
<:&lt;

block:
	body:
		def justify(text, width):
			k = ''
			i = 0
			for a in text:
				k += a
				if i % width == 0:
					k += '\n'
				i += 1
			return k
		s += parse(arg[0], inblock = True, depth = 1) + '\n'
	code: s += clear(arg[0]) + '\n'
	title:
	1: s += parse(arg[0], depth = depth + 1)
	2: s += '  ' + parse(arg[0], depth = depth + 1)
	3: s += '    ' + parse(arg[0], depth = depth + 1)
	4: s += '      ' + parse(arg[0], depth = depth + 1)
	5: s += '        ' + parse(arg[0], depth = depth + 1)
	6: s += '          ' + parse(arg[0], depth = depth + 1)
	list:
		for item in arg[0]:
			if isinstance(item, list):
				s += '  * ' + parse(item, inblock = True, depth = depth + 1)
	image:
	table:
		s += '+----------+----------+\n'
		for tr in arg[0]:
			s += '|'
			for td in tr:
				s += ' ' + parse(td, inblock = True, depth = depth + 1) + ' |'
			s += '\n'
			s += '+----------+----------+\n'
inner:
	b: s += parse(arg[0], depth = depth + 1)
	href: s += parse(arg[1], depth = depth + 1) + ' (' + arg[0][0] + ')'
	i: s += parse(arg[0], depth = depth + 1)
	size: s += parse(arg[0], depth = depth + 1)
	strike: s += parse(arg[0], depth = depth + 1)
	sc: s += parse(arg[0], depth = depth + 1)
	sub: s += parse(arg[0], depth = depth + 1)
	super: s += parse(arg[0], depth = depth + 1)
	text: s += parse(arg[0], depth = depth + 1) + '\n\n'
	tt: s += parse(arg[0], depth = depth + 1)
	u: s += parse(arg[0], depth = depth + 1)



:markdown

name:'Markdown'
extension:'md'

block:
	block: s += parse(arg[0], inblock = True)
	body: 
		counter = []
		s += parse(arg[0], inblock = True)
	title:
	1:
		parsed = parse(arg[0])
		s += parsed + '\n' + '=' * len(parsed)
	2:
		parsed = parse(arg[0])
		s += parsed + '\n' + '-' * len(parsed)
	3: s += '### ' + parse(arg[0]) + ' ###'
	4: s += '#### ' + parse(arg[0]) + ' ####'
	5: s += '##### ' + parse(arg[0]) + ' #####'
	6: s += '###### ' + parse(arg[0]) + ' ######'
inner:
	b: s += '**' + parse(arg[0]) + '**'
	code: s += '    ' + parse(arg[0]).replace('\n', '\n    ')
	href: s += '\[' + parse(arg[0]) + '\](' + parse(arg[0]) + ')'
	href: s += '\[' + parse(arg[1]) + '\](' + parse(arg[0]) + ')'
	i: s += '*' + parse(arg[0]) + '*'
	image: s += '!\[' + parse(arg[0]) + '\](' + parse(arg[0]) + ')'
	image: s += '!\[' + parse(arg[1]) + '\](' + parse(arg[0]) + ')'
	item: s += '\n[return multiline(counter.size() - 1, "    ");][return isOrdered ? counter.get(counter.size() - 1) + ".  " : "*   ";]' + parse(arg[0]) + '{counter.set(counter.size() - 1, 1);}'
	list: s += '{isOrdered = false; counter.add(1);}' + parse(arg[0]) + '{counter.remove(counter.size() - 1);}'
	ordered: s += '{isOrdered = true; counter.add(1);}' + parse(arg[0]) + '{counter.remove(counter.size() - 1);}'
	size:
	strike:
	sub:
	super:
	table:
	tt: s += '``' + str(clear(arg[0])) + '``'
	u: s += skip()
	quote: s += '>' + parse(arg[0]) + ''
	text: s += parse(arg[0]) + '\n\n'



:tex::__main

name:'Tex'
extension:'tex'

escape:
	'_':'\\_'

block:
	body:
		s += '''\\documentclass[twoside,psfig]{article}
		\\usepackage[utf8]{inputenc}
		\\usepackage[russian]{babel}
		\\usepackage{enumitem}
		\\usepackage{float}
		\\usepackage[margin=3cm,hmarginratio=1:1,top=32mm,columnsep=20pt]{geometry}
		\\usepackage{graphicx}
		\\usepackage{hyperref}
		\\usepackage{multicol}
		\\begin{document}'''
		s += parse(arg[0], inblock = True)
		s += '\\end {document}'
	title:
		s += '\\title{' + parse(arg[0]) + '}'
		s += '\\vspace{12em}\\begin{center}{\\huge ' + parse(arg[0]) + '}\\end{center}\\vspace{2em}'
	1: s += '\\section{' + parse(arg[0]) + '}'
	2: s += '\\subsection{' + parse(arg[0]) + '}'
	3: s += '\\subsubsection{' + parse(arg[0]) + '}'
	4: s += '\\paragraph{' + parse(arg[0]) + '}'
	5: s += '\\subparagraph{' + parse(arg[0]) + '}'
	6: s += '' + parse(arg[0]) + ''
	table:
		s += '\\begin{table}[h]\n\\begin{center}\n\\begin{tabular}{|'
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
	list:
		s += '\\begin{itemize}\n'
		for item in arg[0]:
			if isinstance(item, list):
				s += '\\item ' + parse(item) + '\n\n'
		s += '\\end{itemize}\n'
	shortlist:
		s += '\\begin{itemize}[itemsep=-0.5ex]\n'
		for item in arg[0]:
			if isinstance(item, list):
				s += '\\item ' + parse(item) + '\n\n'
		s += '\\end{itemize}\n\n'
	ordered:
		s += '\\begin{ordered}\n'
		for item in arg[0]:
			if isinstance(item, list):
				s += '\\item ' + parse(item[0]) + '\n\n'
		s += '\\end{ordered}\n'
	annotation: s += '\\begin {abstract}\n\n' + parse(arg[0], inblock = True) + '\\end {abstract}\n\n'
	books:
		s += '\\begin{thebibliography}{0}\n\n'
		for item in arg[0]:
			if isinstance(item, list):
				s += '\\bibitem{' + item[0][0] + '} ' + parse(item[1]) + '\n\n'
		s += '\\end{thebibliography}\n\n'
inner:
	b:          s += '{\\bf ' + parse(arg[0]) + '}'
	br:         s += '\\\\'
	cite:       s += '\\cite {' + arg[0][0] + '}'
	code:       s += '\\begin{verbatim}' + arg[0][0] + '\\end{verbatim}'
	date:       pass
	href:
		link = arg[0][0]
		if link[0] == '#':
			link = link[1:]
		if len(arg) == 1:
			s += '\\href {' + link + '} {' + link + '}'
		else:
			s += '\\href {' + link + '} {' + parse(arg[1]) + '}'
	i: s += '{\\em ' + parse(arg[0]) + '}'
	math: s += '$' + ''.join(arg[0]) + '$'
	mathblock: s += '\\[' + ''.join(arg[0]) + '\\]'
	ignore: s += '' + arg[0][0] + ''
	image: 
		s += '\\begin{figure}[h]\\begin{center}\\includegraphics{' + parse(arg[0]) + '}\\end{center}'
		if len(arg) > 1:
			s += '\\caption {' + parse(arg[1]) + '}'
		s += '\\end{figure}'
	item: s += '\\item ' + parse(arg[0]) + ''
	page: s += '\\textsuperscript{' + parse(arg[0]) + '}'
	sc: s += '{\\sc ' + parse(arg[0]) + '}'
	size: s += '' + parse(arg[0]) + ''
	strike: s += '' + parse(arg[0]) + ''
	sub: s += '$_{' + parse(arg[0]) + '}$'
	super: s += '\\textsuperscript{' + parse(arg[0]) + '}'
	text: s += parse(arg[0]) + '\n\n'
	tr: s += '' + parse(arg[0]) + '|'
	td: s += '| ' + parse(arg[0]) + ''
	tt: s += '{\\tt ' + parse(arg[0]) + '}'
	u: s += '' + parse(arg[0]) + ''
	quote: s += '' + parse(arg[0]) + ''
	cite: s += '\\cite{' + arg[0][0] + '}'



:rtf

# ::: header

# import java.util.ArrayList;
# import java.util.List;

# ::: init

# static boolean isOrdered;
# static List<Integer> counter;
# static int lc = 0; /* List counter */

# ::: tags

block:
	block: s += parse(arg[0], inblock = True)
	body:
		status['levels'] = [0, 0, 0, 0, 0, 0, 0]
		status['bookindex'] = 0
		status['books'] = {}
		s += '''{\\rtf0\\ansi\\deff0\n{\\*\\listtable{\\list\\listtemplateid1
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
		s += '{\\f3 ' + parse(arg[0], inblock = True) + '}'
		s += '\n}'
	title: s += '\\par\\pard \\qc\\b\\sb346\\sa173{\\f2{\\fs32 ' + parse(arg[0]) + '  \\fs20}}\\b0\n'
	table: s += parse(arg[0])
	list:
		for item in arg[0]:
			if isinstance(item, list):
				lc = 0 # FIXME
				lc += 1
				s += parse(item) + ' '
				lc -= 1
				if lc == 0:
					s += '\\par\\pard'
	1: 
		status['levels'][1] += 1
		status['levels'][2] = 0
		status['levels'][3] = 0
		level = status['levels'][1]
		s += '\\i\\b\\sb346\\sa173{\\f2\\fs22 ' + str(level) + '. ' + parse(arg[0]) + '\\fs20}\\b0\\i0\n'
	2: 
		status['levels'][2] += 1
		status['levels'][3] = 0
		level = str(status['levels'][1]) + '.' + str(status['levels'][2]) + ' '
		s += '\\b\\par\\pard\\sb346\\sa173{\\fs22 ' + level + parse(arg[0]) + '\\fs20}\\b0\n'
	3: 
		status['levels'][3] += 1
		level = str(status['levels'][1]) + '.' + str(status['levels'][2]) + '.' + str(status['levels'][3]) + ' '
		s += '\\parb\\par\\pard\\sb346\\sa173{\\fs20 ' + level + parse(arg[0]) + '\\fs20}\\b0\\i0\n'
	4: 
		s += '\\parpar\\pard\\sb346\\sa173{\\fs20 ' + parse(arg[0]) + '\\fs20}\\b0\n'
		print 'Warning: Наличие в статье заголовков пятого и больших уровней не приветствуется. Если они необходимы, решение об оформлении принимает автор.'
	5: 
		s += '\\b\\sb346\\sa173{\\fs20 ' + parse(arg[0]) + '\\fs20}\\b0\n'
		print 'Warning: Наличие в статье заголовков пятого и больших уровней не приветствуется. Если они необходимы, решение об оформлении принимает автор.'
	6: 
		s += '\\b\\sb346\\sa173{\\fs20 ' + parse(arg[0]) + '\\fs20}\\b0\n'
		print 'Warning: Наличие в статье заголовков пятого и больших уровней не приветствуется. Если они необходимы, решение об оформлении принимает автор.'
	center: s += '\\qc' + parse(arg[0])
	left: s += '\\ql' + parse(arg[0])
	right: s += '\\qr' + parse(arg[0])
inner:
	b: s += '\n\\b ' + parse(arg[0]) + '\\b0\n'
	code: s += parse(arg[0])
	font: s += ''
	href: s += '{\\field{\\*\\fldinst{HYPERLINK  "' + parse(arg[0]) + '"}}{\\fldrslt{\\u1  ' + parse(arg[-1]) +'\n}}}'
	i: s += '\\i ' + parse(arg[0]) + '\\i0\n'
	math: s += parse(arg[0])
	ignore: s += parse(arg[0])
	image: s += parse(arg[0])
	shortlist: s += parse(arg[0])
	ordered: s += '\\levelnfc0\\list ' + parse(arg[0]) + ' \\list0'
	s: s += '\\strike ' + parse(arg[0]) + '\\strike0'
	sc: s += '\\scaps ' + parse(arg[0]) + '\\scaps0\n'
	size: s += '\\fs' + str(int(parse(arg[0])) * 2) + parse(arg[1])
	strike: s += parse(arg[0])
	sub: s += '\\sub ' + parse(arg[0]) + '\\nosupersub\n'
	super: s += '\\super ' + parse(arg[0]) + '\\nosupersub\n'
	tr: s += parse(arg[0]) + '|'
	td: s += '| ' + parse(arg[0])
	tt: s += '{\\f1 ' + parse(arg[0]) + '}'
	u: s += '\\ul ' + parse(arg[0]) + '\\ul0\n'
	quote: s += parse(arg[0])
	book: s += parse(arg[0])
	books:
		# for item in arg[0]:
		# 	if isinstance(item, list):
		# 		s += '\\par\\pard [' + status[] + '] ' + parse(item[1]) + '\n\n'
		for index in range(status['bookindex']):
			s += '\\par\\pard\\li720\\fi-360[' + str(index + 1) + ']\\tab '
			for item in arg[0]:
				if isinstance(item, list):
					if status['books'][item[0][0]] == index + 1:
						s += parse(item[1])
		s += '\\par\\pard'
	cite: 
		cites = arg[0][0].split(', ')
		for cite in cites:
			print cite, status['books']
			if not (cite in status['books']):
				status['bookindex'] += 1
				status['books'][cite] = status['bookindex']
		s += '['
		s += str(status['books'][cites[0]])
		for cite in cites[1:]:
			s += ', ' + str(status['books'][cite])
		s += ']'
	text: s += '\\par\\pard\\qj' + parse(arg[0]) + '\n'
	br: s += '\\par\\pard'

::: symbols

\n\n:\\par\\pard
~:\\u0160
---:\\u8212
--:\\u8211

::: screen
