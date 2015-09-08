:html

parameters:
	inherit:default
block:
	body:
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
		build_file = open('info.yml')
		buildinfo = yaml.load(build_file)
		build_file.close()
		s += '<div class = buildinfo><p><span style = "color: red;">Please <span class = abbr>DO NOT EDIT</span> this file.</span> It was built by <a href = "https://github.com/enzet/Moire">Moire</a>.</p><p>Updated ' + datetime.datetime.now().strftime('%H:%M:%S %d %B %Y') + ' (version 0.0.1.' + str(buildinfo['build']['number']) + ').</p></div>'
		build_file = open('info.yml', 'w+')
		buildinfo['build']['number'] += 1
		build_file.write(yaml.dump(buildinfo))
		build_file.close()
		s += '<span class = content>Top level subpages: '
		for index, child in enumerate(arg[1].children):
			if child.element and len(child.element) == 3 and child.element[2]:
				s += '<a href = #' + str(child.element[2][0]) + '>' + \
					parse(child.element[1]) + '</a>, '
		s = s[:-2] + '.</span>'
		s += parse(arg[0], inblock = True)
		s += '''	</body>
		</html>'''
	number:
		s += '<h' + str(number)
		header_id = None
		if len(arg) == 3:
			header_id = arg[1][0]
		if header_id:
			s += ' id="' + arg[1][0] + '"'
		s += '>' + parse(arg[0])
		if header_id:
			s += '&nbsp;<span class = normal><sup><a href = #' + arg[1][0] + \
				'>§</a>'
			if arg[2] and arg[2].parent and arg[2].parent.element and \
					arg[2].parent.element[2]:
				s += ' <a class = reference href = #' + \
					str(arg[2].parent.element[2][0]) + '>up</a>'
			s += '</sup></span>'
		s += '</h' + str(number) + '>'
		if header_id:
			if arg[2] and arg[2].children and len(arg[2].children) > 1:
				s += '<span class = content>Subpages: '
				if header_id == 'paper':
					s += '<ol>'
				for index, child in enumerate(arg[2].children):
					if header_id == 'paper':
						s += '<li>'
					if child.element and len(child.element) == 3 and \
							child.element[2]:
						s += '<a href = #' + str(child.element[2][0]) + '>' + \
							parse(child.element[1]) + '</a>'
						s += '.' if index == len(arg[2].children) - 1 else ','
						s += ' '
					if header_id == 'paper':
						s += '</li>'
				if header_id == 'paper':
					s += '</ol>'
				s += '</span>'
	image:      
		if 'inner_links' in status and not status['inner_links']:
			s += '<img src = "private.svg" />&nbsp;Image is private.'
		else:
			if not os.path.isfile(arg[0][0]):
				print 'No image: ' + arg[0][0] + '.'
			else:
				s += '<img src = "' + arg[0][0] + '" alt = "' + parse(arg[1]) + \
				 '" />'
	ordered:
		s += '<ol>'
		for item in arg[0]:
			if isinstance(item, list):
				s += '<li>' + parse(item, inblock=True) + '</li>'
		s += '</ol>'
inner:
	abbr: s += '<span class = abbr>' + parse(arg[0]) + '</span>'
	bookquote: s += '<div class = bookquote>' + parse(arg[0]) + '</div>'
	booklink: s += '<tt>' + arg[0][0] + '</tt>'
	comment: s += '<i class = comment>' + parse(arg[0]) + '</i>'
	date:
	formal: s += '<span class = formal>&lt;' + arg[0][0] + '&gt;</span>'
	hidden: s += '<a class = hidden href = "javascript:show_hide(' + 
		arg[0][0] + ')">' + parse(arg[1]) + \
		'</a><div style = "display: none" class = hidden id = ' + \
		arg[0][0] + '>' + parse(arg[2]) + '</div>'
	href: 
		link = arg[0][0]
		private = '<abbr title = "Link to private document part"><img src = "private.svg" /> <span class = no_link>' + parse(arg[1]) + '</span></abbr>'
		if link[:4] == 'http':
			s += '<a href = "' + arg[0][0] + '">' + parse(arg[1]) + '</a>'
		elif link[0] == '#':
			found = status['tree'].find(link[1:])
			if not found:
				s += private
			else:
				s += '<a href = "' + arg[0][0] + '">' + parse(arg[1]) + '</a>'
		else:
			if 'inner_links' in status and not status['inner_links']:
				s += private
			else:
				s += '<a href = "' + arg[0][0] + '">' + parse(arg[1]) + '</a>'
	key: s += '<span class = key>' + parse(arg[0]) + '</span>'
	page: s += '<span class = page>' + arg[0][0] + '</span>'
	tweet: 
		content = arg[0][0]
		s += '<div class = tweet>' + content + '</div>'
	th:
		s += '<span class = th>' + parse(arg[0]) + '</span>'

:markdown

parameters:
	inherit:default
inner:
	formal: s += '<' + arg[0][0] + '>'

:tex

parameters:
	inherit:default
inner:
	abbr: s += parse(arg[0])
	blockquote: #s += parse(arg[0])
	comment: #s += '{\\em ' + parse(arg[0]) + '}'
	date:
	formal: #s += '<' + arg[0][0] + '>'
	hidden:
	page: s += '\\textsuperscript{' + arg[0][0] + '}'

:text

parameters:
	inherit:default
inner:
	abbr: s += parse(arg[0])
	bookquote: s += parse(arg[0])
	comment: s += parse(arg[0])
	date:
	formal: s += arg[0][0]
	hidden: s += parse(arg[1]) + '\n' + parse(arg[2])
	page: s += arg[0][0]

:raw_text

parameters:
	inherit:default
inner:
	abbr: s += parse(arg[0])
	bookquote: s += parse(arg[0])
	comment: s += parse(arg[0])
	date:
	formal: s += arg[0][0]
	hidden: s += parse(arg[1]) + '\n' + parse(arg[2])
	page: s += arg[0][0]
