import ppm
import gif

rgb_pixels_a = ppm.loadppm(open("tests/cat256.ppm", "rb"))
rgb_pixels_b = ppm.loadppm(open("tests/parrot256.ppm", "rb"))

# merge the two 3-channel images into a single 6-channel image
rgbrgb_pixels = [[a+b for a, b in zip(a_row, b_row)] for a_row, b_row in zip(rgb_pixels_a ,rgb_pixels_b)]

indices, palette = gif.palettise(rgbrgb_pixels, n_entries=128)

# un-merge the 6-channel pallete into a 3-channel palette
palette_a = [rgbrgb[:3] for rgbrgb in palette]
palette_a += list(reversed([rgbrgb[3:] for rgbrgb in palette]))

gif.save(open("tests/a.gif", "wb"), indices, palette_a)
gif.save(open("tests/b.gif", "wb"), indices, list(reversed(palette_a))) # exactly the same image data, only reversed palette order
