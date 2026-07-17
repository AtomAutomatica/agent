#!/usr/bin/env python3
"""Flatten the exhibit PNGs used by the build into high-quality JPEGs so the
final PDF stays email-sized. PNG masters in assets/extracted are kept; the
build references assets/optimized instead. The logo stays PNG (line art)."""
import os
import re

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "extracted", "robinson")
PHOTO = os.path.join(ROOT, "assets", "brand", "industrial-photo.png")
DST = os.path.join(ROOT, "assets", "optimized")
QUALITY = 90

os.makedirs(DST, exist_ok=True)

used = [f for f in sorted(os.listdir(SRC)) if re.match(r"page\d+_x\d+\.png$", f)]
total_in = total_out = 0
for fname in used + [os.path.basename(PHOTO)]:
    src = os.path.join(SRC, fname) if fname.startswith("page") else PHOTO
    out = os.path.join(DST, fname.replace(".png", ".jpg"))
    img = Image.open(src)
    if img.mode in ("RGBA", "LA", "P"):
        bg = Image.new("RGB", img.size, (255, 255, 255))
        img = img.convert("RGBA")
        bg.paste(img, mask=img.split()[-1])
        img = bg
    else:
        img = img.convert("RGB")
    img.save(out, "JPEG", quality=QUALITY, optimize=True, subsampling=1)
    total_in += os.path.getsize(src)
    total_out += os.path.getsize(out)
print(f"{len(used) + 1} images: {total_in / 1e6:.1f} MB -> {total_out / 1e6:.1f} MB")
