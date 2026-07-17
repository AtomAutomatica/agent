#!/usr/bin/env python3
"""Compose the Robinson #1 area-wells exhibit from RRC Public GIS Viewer data.

Inputs (data/rrc/): basemap.png — styled map export from the RRC MapServer
(bbox -95.906,32.596 / -95.816,32.686, EPSG:3857, layers: wells, horiz/dir,
subdivisions, surveys, counties); wells.json — layer-1 feature query for the
same area; legend.json — service legend with official symbol swatches.

Output: assets/generated/robinson-area-wells.png — base map + Ferox-red
highlight on the Robinson #1 permitted location, soft emphasis rings on active
oil wells, RRC-swatch legend, scale bar, north arrow, and source credit."""
import base64
import io
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data", "rrc")
OUT = os.path.join(ROOT, "assets", "generated", "robinson-area-wells.png")

BBOX = (-95.906, 32.596, -95.816, 32.686)  # lonmin, latmin, lonmax, latmax
RED = (191, 0, 0)
INK = (22, 24, 29)
GRAY = (90, 95, 102)
OIL_GREEN = (0, 140, 60)

FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def merc_y(lat):
    return math.log(math.tan(math.pi / 4 + math.radians(lat) / 2))


def to_px(lon, lat, w, h):
    x = (lon - BBOX[0]) / (BBOX[2] - BBOX[0]) * w
    y0, y1 = merc_y(BBOX[3]), merc_y(BBOX[1])
    y = (y0 - merc_y(lat)) / (y0 - y1) * h
    return x, y


def main():
    base = Image.open(os.path.join(DATA, "basemap.png")).convert("RGBA")
    w, h = base.size
    flat = Image.new("RGBA", (w, h), (255, 255, 255, 255))
    flat.alpha_composite(base)

    wells = json.load(open(os.path.join(DATA, "wells.json")))["features"]
    draw = ImageDraw.Draw(flat)

    # soft emphasis rings on active oil wells
    for f in wells:
        a = f["attributes"]
        if a["GIS_SYMBOL_DESCRIPTION"] == "Oil Well":
            x, y = to_px(f["geometry"]["x"], f["geometry"]["y"], w, h)
            for r, wd in ((26, 4),):
                draw.ellipse([x - r, y - r, x + r, y + r], outline=OIL_GREEN + (110,), width=wd)

    # Robinson #1 highlight
    rob = next(f for f in wells if f["attributes"]["API"] == "46731190")
    rx, ry = to_px(rob["geometry"]["x"], rob["geometry"]["y"], w, h)
    for r, wd, alpha in ((52, 7, 255), (68, 3, 160)):
        draw.ellipse([rx - r, ry - r, rx + r, ry + r], outline=RED + (alpha,), width=wd)

    # callout box with leader line
    f_call = ImageFont.truetype(FB, 40)
    f_call2 = ImageFont.truetype(FR, 30)
    line1, line2 = "ROBINSON #1", "PERMITTED LOCATION · API 42-467-31190"
    pad = 22
    w1 = draw.textlength(line1, font=f_call)
    w2 = draw.textlength(line2, font=f_call2)
    bw, bh = max(w1, w2) + pad * 2, 40 + 30 + pad * 2 + 10
    bx, by = rx - bw - 150, ry - bh - 210
    draw.line([rx - 34, ry - 34, bx + bw - 40, by + bh], fill=RED + (255,), width=5)
    draw.rectangle([bx, by, bx + bw, by + bh], fill=(255, 255, 255, 242), outline=RED + (255,), width=6)
    draw.text((bx + pad, by + pad - 4), line1, font=f_call, fill=RED)
    draw.text((bx + pad, by + pad + 46), line2, font=f_call2, fill=INK)

    # scale bar (1 mile) and north arrow
    lat_c = (BBOX[1] + BBOX[3]) / 2
    deg_per_mile = 1 / (69.172 * math.cos(math.radians(lat_c)))
    mile_px = deg_per_mile / (BBOX[2] - BBOX[0]) * w
    sx, sy = 70, h - 90
    f_sm = ImageFont.truetype(FR, 30)
    draw.rectangle([sx, sy, sx + mile_px, sy + 12], outline=INK, width=3)
    draw.rectangle([sx, sy, sx + mile_px / 2, sy + 12], fill=INK)
    draw.text((sx, sy - 42), "0", font=f_sm, fill=INK)
    draw.text((sx + mile_px / 2 - 15, sy - 42), "0.5", font=f_sm, fill=INK)
    draw.text((sx + mile_px - 30, sy - 42), "1 mi", font=f_sm, fill=INK)
    ax, ay = w - 100, h - 180
    draw.polygon([(ax, ay - 55), (ax - 26, ay + 25), (ax, ay + 8)], fill=INK)
    draw.polygon([(ax, ay - 55), (ax + 26, ay + 25), (ax, ay + 8)], outline=INK, width=3)
    draw.text((ax - 14, ay + 32), "N", font=ImageFont.truetype(FB, 38), fill=INK)

    # legend band from official RRC swatches
    legend = json.load(open(os.path.join(DATA, "legend.json")))
    lay1 = next(l for l in legend["layers"] if l["layerId"] == 1)
    swatches = {it["label"]: it["imageData"] for it in lay1["legend"]}
    present = [
        ("Oil", "Oil Well (active)"),
        ("Gas", "Gas Well"),
        ("Permitted Location", "Permitted Location"),
        ("Dry Hole", "Dry Hole"),
        ("Plugged Oil", "Plugged Oil"),
        ("Plugged Gas", "Plugged Gas"),
        ("Injection / Disposal from Oil", "Injection / Disposal"),
        ("Water Supply", "Water Supply"),
    ]
    band_h = 300
    canvas = Image.new("RGBA", (w, h + band_h), (255, 255, 255, 255))
    canvas.alpha_composite(flat, (0, 0))
    d2 = ImageDraw.Draw(canvas)
    d2.line([40, h + 14, w - 40, h + 14], fill=RED + (255,), width=4)
    f_leg = ImageFont.truetype(FR, 30)
    f_legb = ImageFont.truetype(FB, 30)
    cols, col_w = 4, (w - 120) // 4
    for i, (key, label) in enumerate(present):
        cx = 60 + (i % cols) * col_w
        cy = h + 44 + (i // cols) * 62
        sw = Image.open(io.BytesIO(base64.b64decode(swatches[key]))).convert("RGBA")
        sw = sw.resize((44, 44))
        canvas.alpha_composite(sw, (cx, cy))
        d2.text((cx + 58, cy + 6), label, font=f_leg, fill=INK)
    # Robinson marker and oil-emphasis ring samples in legend
    cx, cy = 60, h + 44 + 2 * 62
    d2.ellipse([cx + 8, cy + 8, cx + 40, cy + 40], outline=RED + (255,), width=6)
    d2.text((cx + 58, cy + 6), "Robinson #1 — permitted location", font=f_legb, fill=RED)
    cx = 60 + 2 * col_w
    d2.ellipse([cx + 8, cy + 8, cx + 40, cy + 40], outline=OIL_GREEN + (150,), width=4)
    d2.text((cx + 58, cy + 6), "Emphasis ring — active oil well", font=f_leg, fill=INK)
    d2.text(
        (60, h + band_h - 46),
        "Source: Railroad Commission of Texas — Public GIS Viewer (gis.rrc.texas.gov), "
        "well locations layer, July 2026. Van Zandt County, Texas.",
        font=ImageFont.truetype(FR, 26), fill=GRAY,
    )

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    canvas.convert("RGB").save(OUT)
    print("wrote", OUT, canvas.size)


if __name__ == "__main__":
    main()
