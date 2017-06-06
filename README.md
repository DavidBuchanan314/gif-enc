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

I plan to use this code to play with some GIF steganography techniques I've come up with.
