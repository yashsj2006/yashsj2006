"""Turn a photo into portrait.txt (ASCII art) for build_profile.py.

Usage:  python image_to_ascii.py my_photo.jpg
Tips:   use a head-and-shoulders photo, good lighting, plain background.
        Increase CONTRAST if the result looks washed out.
"""
import sys
from PIL import Image, ImageOps, ImageEnhance

COLS = 90          # characters per line
ROWS = 53          # lines (matches the VISUAL.MAP panel height)
CONTRAST = 1.6
INVERT = False     # True if your photo has a light subject on a dark bg
RAMP = " .:-=+*#%@"

src = sys.argv[1] if len(sys.argv) > 1 else "photo.jpg"
img = ImageOps.grayscale(Image.open(src))
img = ImageOps.autocontrast(img)
img = ImageEnhance.Contrast(img).enhance(CONTRAST)

# crop to the panel's aspect ratio (a character cell is ~1.78x taller than wide)
target = COLS / (ROWS * 1.78)
w, h = img.size
if w / h > target:
    nw = int(h * target); img = img.crop(((w - nw) // 2, 0, (w + nw) // 2, h))
else:
    nh = int(w / target); img = img.crop((0, 0, w, nh))
img = img.resize((COLS, ROWS))

lines = []
for y in range(ROWS):
    row = ""
    for x in range(COLS):
        v = img.getpixel((x, y)) / 255
        if INVERT: v = 1 - v
        row += RAMP[int(v * (len(RAMP) - 1))]
    lines.append(row.rstrip())
open("portrait.txt", "w", encoding="utf-8").write("\n".join(lines))
print("Wrote portrait.txt")
