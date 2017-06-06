import ppm
import gif

rgb_pixels = ppm.loadppm(open("tests/cat256.ppm", "rb"))
indices, palette = gif.palettise(rgb_pixels)

gif.save(open("tests/cat.gif", "wb"), indices, palette)
