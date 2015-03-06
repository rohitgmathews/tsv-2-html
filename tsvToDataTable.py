#! /usr/bin/env python

import argparse

def parseArguments():
	parser = argparse.ArgumentParser()
	parser.add_argument('inputFile', help="The input tsv file")
	parser.add_argument('--hasHeaders', action='store_true', help='Does this tsv have headers')
	parser.add_argument('--headersFrom', help='Filename to read column names from')
	parser.add_argument('--colNames', nargs='+', help='Column Names')
	args = parser.parse_args()
	return args

def writeHeaders(htmlFile):
	htmlFile.write(
		'''
<html>
	<head>
		<script type='text/javascript' src='http://code.jquery.com/jquery-1.11.1.min.js'></script>
		<script type='text/javascript' src='http://cdn.datatables.net/1.10.5/js/jquery.dataTables.min.js'></script>
		<script type='text/javascript' src='http://cdn.datatables.net/plug-ins/f2c75b7247b/integration/jqueryui/dataTables.jqueryui.js'></script>
		<link rel='stylesheet' type='text/css' href='http://code.jquery.com/ui/1.11.2/themes/smoothness/jquery-ui.css'/>
		<link rel='stylesheet' type='text/css' href='http://cdn.datatables.net/plug-ins/f2c75b7247b/integration/jqueryui/dataTables.jqueryui.css'/>
		<script type='text/javascript'>
			$(document).ready(function() {
				var table = $('#myTable').DataTable( {
				    "scrollY": "300px",
				    "paging": true
				} );

				$('a.toggle-vis').on( 'click', function (e) {
				    e.preventDefault();

				    // Get the column API object
				    var column = table.column( $(this).attr('data-column') );

				    // Toggle the visibility
				    column.visible( ! column.visible() );
				} );
			} );
		</script>
	</head>
	<body>	
		'''
		)

def writeFooters(htmlFile):
	htmlFile.write(
		'''
		</table>
	</body>
</html>
		''')

def getFakeColumnNames(fromFile):
	with open(fromFile) as f:
		first_line = f.readline().strip()
		count = len("\t".split(first_line))

	return ["Column " + str(x) for x in range(1, count + 1) ]

def main():
	args = parseArguments()
	htmlFile = open(args.inputFile + '.html', 'w')
	writeHeaders(htmlFile)

	if(args.headersFrom) :
		headerFile = open(args.headersFrom, 'r')
		headers = headerFile.readline().strip().split(",")
	elif args.colNames:
		headers = args.colNames
	elif args.hasHeaders == False :
		headers = getFakeColumnNames()

	with open(args.inputFile) as f:
		if args.headersFrom == None and args.hasHeaders :
			headers = f.readline().strip().split("\t")
		htmlFile.write('<div style="text-align:center">Toggle Visibility - ')
		for idx, header in enumerate(headers):
			htmlFile.write('<a class="toggle-vis" data-column="{0}" href="#" style="padding: 4px">{1}</a>'.format(idx, header))
		htmlFile.write('<br></div>')
		htmlFile.write('''<table id='myTable' class='display' cellspacing="0" width="100%">
			<thead>''')
		htmlFile.write('<tr>')
		for header in headers:
			htmlFile.write('<th>' + header + '</th>')
		htmlFile.write('</tr>\n</thead>\n<tbody>\n')
		for line in f:
			htmlFile.write('<tr><td>' + line.strip().replace('\t', '</td><td>') + '</td></tr>\n')
		htmlFile.write('</tbody>')
		htmlFile.write('<tfoot><tr>')
		for header in headers:
			htmlFile.write('<th>' + header + '</th>')
		htmlFile.write('</tr></tfoot>')

	writeFooters(htmlFile)

	htmlFile.close()

if __name__ == '__main__':
	main()