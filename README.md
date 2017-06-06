# gif-enc
A rather inefficient GIF encoder, in ~64 lines of python.

The goal of this project was to understand how the GIF format works, along with quantisation and dithering techniques.

Colour quantisation is achieved using `MiniBatchKMeans` from scikit. Dithering is implemented using the Floyd–Steinberg algorithm.

GIF image data is stored using LZW compression. My implementation doesn't actually do any compression, although it still has to use the LZW format.

## Example:

```python
import ppm
import gif

rgb_pixels = ppm.loadppm(open("tests/cat256.ppm", "rb"))
indices, palette = gif.palettise(rgb_pixels)

gif.save(open("tests/cat.gif", "wb"), indices, palette)
```

Input (converted from PPM to PNG so your browser can view it):

![Example input](https://github.com/DavidBuchanan314/gif-enc/blob/master/tests/cat256.png)

Output:

![Example output](https://github.com/DavidBuchanan314/gif-enc/blob/master/tests/cat.gif)

## Steganography

Using the relatively simple method of merging two images together as a "6 dimensional" image, treating
it as if it were a single image with 6 colour channels, I was able to reuse the same clustering algorithm
to create an image which contains two seperate images in one. Only one image is visible at a time, and
reversing the order of the entries in the colour pallete reveals the second image.

```python
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
```

This image could be considered the "cover" image:

![Example input](https://github.com/DavidBuchanan314/gif-enc/blob/master/tests/a.gif)

To reveal the second image, the recipient just needs to reverse the order of the pallete entries:

![Example input](https://github.com/DavidBuchanan314/gif-enc/blob/master/tests/b.gif)

If you examine these two files in a hex editor, you can verify that the only difference is in the colour
pallete, a 768 byte region located at a 13 byte offset in the file. The rest of the two files are completely
identical.
