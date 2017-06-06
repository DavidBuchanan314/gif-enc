import struct
from sklearn.cluster import MiniBatchKMeans

def palettise(data, n_entries=256):
	height = len(data)
	width = len(data[0])
	all_colours = sum(data, [])
	print("Calculating pallete...")
	kmeans = MiniBatchKMeans(n_clusters=n_entries, random_state=0).fit(all_colours)
	pallete = [list(map(int, rgb)) for rgb in kmeans.cluster_centers_]
	
	print("Dithering...") # Floyd–Steinberg dithering
	for y in range(height):
		print("\r{:.1f}%".format((y/height)*100), end="")
		for x in range(width):
			bucket = kmeans.predict([data[y][x]])[0]
			error = [a-b for a, b in zip(data[y][x], pallete[bucket])]
			data[y][x] = bucket
			for dx, dy, coef in [(1, 0, 7/16), (-1, 1, 3/16), (0, 1, 5/16), (1, 1, 1/16)]:
				xn = x + dx
				yn = y + dy
				if ( 0 <= xn < width and 0 <= yn < height ):
					data[yn][xn] = [a+b*coef for a, b in zip(data[yn][xn], error)]
	
	print("\r100%     ")
	return data, pallete

def save(outfile, data, palette):
	assert(len(palette) == 256)
	
	height = len(data)
	width = len(data[0])
	fields = 0b11110111 # Global colour table, 8-bit colour, unsorted, 256 palette entries
	bg_index = 0
	aspect = 0
	
	buf = b"GIF89a"
	buf += struct.pack("<HHBBB", width, height, fields, bg_index, aspect)
	
	for entry in palette:
		buf += bytes(entry)
	
	desc_fields = 0b00000000 # No local table, no interlacing
	buf += struct.pack("<BHHHHB", 0x2C, 0, 0, width, height, desc_fields)
	
	data = bytes(sum(data, [])) # flatten image data
	assert(len(data) == width * height)
	
	bitstream = [0, 0, 0, 0, 0, 0, 0, 0, 1] # LZW "clear code"
	
	dictlen = 257
	
	for pixel in data:
		for _ in range(min(12, dictlen.bit_length())):
			bitstream.append(pixel & 1)
			pixel >>= 1
		dictlen += 1
	
	bitstream += [1, 0, 0, 0, 0, 0, 0, 0, 1] # LZW end fo sequence
	
	bitstream += [0] * (8 - len(bitstream) % 8) # zero padding
	assert(len(bitstream) % 8 == 0)
	
	buf += b"\x08" # initial LZ code size
	
	print("LZW encoding...") # we don't actually do any compression though
	
	streami = 0
	while streami < len(bitstream):
		size = min(0xFE, (len(bitstream)-streami)//8)
		block = [size]
		for _ in range(size):
			byte = 0
			for i in range(8):
				byte |= bitstream[streami] << i
				streami += 1
			block.append(byte)
		buf += bytes(block)
	
	buf += b"\x00\x3B" # LZ block terminator, GIF trailer block
	
	outfile.write(buf)
	outfile.close()
