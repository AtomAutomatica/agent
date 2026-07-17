#!/usr/bin/env python3
"""Restore the as-delivered appearance of four exhibits whose raw embedded
bitmaps differ from what the original book visibly showed:

- page03: the delivered book whited out a superseded company line in the
  road-map letterhead; the raw bitmap still contains it. Re-cover it.
- page09 / page20: bitmaps are stored rotated 90deg CCW (the original PDF
  rotated them at placement). Rotate 90deg CW back to display orientation.
  page20 also carries a screenshot-annotation banner added onto the sideways
  bitmap that the original book never displayed — crop it off first.
- page23: the raw bitmap is a full recycled template page from a different
  book ("Paducah Lease Development") with the Geology of Texas map in the
  middle; the original book displayed only the map. Crop to the map.

Patched copies go to assets/patched/robinson/; extracted masters are kept."""
import os

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "assets", "extracted", "robinson")
DST = os.path.join(ROOT, "assets", "patched", "robinson")
os.makedirs(DST, exist_ok=True)


def load(name):
    return Image.open(os.path.join(SRC, name)).convert("RGB")


def save(img, name):
    img.save(os.path.join(DST, name))
    print(f"patched {name}: {img.size}")


# page03 — re-cover the whited-out letterhead line (box found by inspection)
img = load("page03_x10.png")
paper = img.crop((620, 150, 780, 200)).resize((1, 1)).getpixel((0, 0))
img.paste(Image.new("RGB", (600 - 240, 191 - 164), paper), (240, 164))
save(img, "page03_x10.png")

# page09 — rotate back to display orientation
save(load("page09_x40.png").transpose(Image.ROTATE_270), "page09_x40.png")

# page20 — drop the sideways annotation banner, then rotate back
img = load("page20_x101.png")
img = img.crop((0, 78, img.width, img.height)).transpose(Image.ROTATE_270)
save(img, "page20_x101.png")

# page23 — keep only the Geology of Texas map from the recycled template page
save(load("page23_x114.png").crop((108, 178, 1016, 1178)), "page23_x114.png")
