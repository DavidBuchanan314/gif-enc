def nextline(infile):
	comment = b"#"[0]
	line = b"#"
	while line[0] == comment:
		line = infile.readline().strip()
	return line

def loadppm(infile):
	nextline(infile)
	width, height = map(int, nextline(infile).split())
	nextline(infile)
	data = []
	for y in range(height):
		row = []
		for x in range(width):
			row.append(list(infile.read(3)))
		data.append(row)
	return data
