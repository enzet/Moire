:html

parameters:
	inherit:default
block:
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
inner:
	bookquote: s += '<div class = bookquote>' + parse(arg[0]) + '</div>'
	comment: s += '<i class = comment>' + parse(arg[0]) + '</i>'
	date:
	formal: s += '&lt;' + arg[0][0] + '&gt;'
	hidden: s += '<a class = hidden href = "javascript:show_hide(' + arg[0][0] + ')">' + parse(arg[1]) + '</a><div style = "display: none" class = hidden id = ' + arg[0][0] + '>' + parse(arg[2]) + '</div>'
	page: s += '<span class = page>' + arg[0][0] + '</span>'
	red: s += '<span style = "color: red;">' + parse(arg[0]) + '</span>'
