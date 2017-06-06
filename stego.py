import ppm
import gif

rgb_pixels_a = ppm.loadppm(open("tests/cat256.ppm", "rb"))
rgb_pixels_b = ppm.loadppm(open("tests/parrot256.ppm", "rb"))

rgbrgb_pixels = [[a+b for a, b in zip(a_row, b_row)] for a_row, b_row in zip(rgb_pixels_a ,rgb_pixels_b)]

indices, palette = gif.palettise(rgbrgb_pixels, n_entries=128)

palette_a = [rgbrgb[:3] for rgbrgb in palette]
palette_a += list(reversed([rgbrgb[3:] for rgbrgb in palette]))
palette_b = list(reversed(palette_a))

gif.save(open("tests/a.gif", "wb"), indices, palette_a)
gif.save(open("tests/b.gif", "wb"), indices, palette_b)
