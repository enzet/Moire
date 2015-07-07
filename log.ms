
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
inner:
	i: s += ''
	temp: pass
