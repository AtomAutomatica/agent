#!/usr/bin/env python3
"""Extract embedded images (with placement geometry) and page renders from the
source PDFs so the prospectus can be rebuilt around the original exhibits."""
import json
import os
import sys

import fitz  # PyMuPDF

UPLOADS = "/root/.claude/uploads/c9d786d4-fdaa-571d-991a-243da74becde"
SOURCES = {
    "robinson": os.path.join(UPLOADS, "df2a3b24-ccRobinson_1_.pdf.pdf"),
    "lilly_email": os.path.join(UPLOADS, "8ed33dcf-Lilly_1H__Email_1.pdf"),
    "lilly_agreement": os.path.join(UPLOADS, "63a8d403-Lilly_1H__Agreement_2.pdf"),
}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACT_DIR = os.path.join(ROOT, "assets", "extracted")
ORIG_DIR = os.path.join(ROOT, "assets", "originals")


def pixmap_for_xref(doc, xref, smask):
    pix = fitz.Pixmap(doc, xref)
    if smask:
        mask = fitz.Pixmap(doc, smask)
        try:
            pix = fitz.Pixmap(pix, mask)
        except Exception:
            pass
    if pix.colorspace and pix.colorspace.n >= 4:
        pix = fitz.Pixmap(fitz.csRGB, pix)
    return pix


def extract(name, path, render_dpi=150):
    doc = fitz.open(path)
    out_dir = os.path.join(EXTRACT_DIR, name)
    orig_dir = os.path.join(ORIG_DIR, name)
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(orig_dir, exist_ok=True)
    manifest = []
    for pno in range(doc.page_count):
        page = doc[pno]
        pw, ph = page.rect.width, page.rect.height
        # reference render of the original page
        page.get_pixmap(dpi=render_dpi).save(
            os.path.join(orig_dir, f"page{pno + 1:02d}.png"))
        seen = {}
        for item in page.get_images(full=True):
            xref, smask = item[0], item[1]
            if xref in seen:
                rects = seen[xref]
            else:
                rects = [list(r) for r in page.get_image_rects(xref)]
                seen[xref] = rects
                pix = pixmap_for_xref(doc, xref, smask)
                fname = f"page{pno + 1:02d}_x{xref}.png"
                pix.save(os.path.join(out_dir, fname))
                manifest.append({
                    "page": pno + 1,
                    "xref": xref,
                    "file": fname,
                    "px_w": pix.width,
                    "px_h": pix.height,
                    "has_alpha": bool(pix.alpha),
                    "rects_pt": rects,
                    "page_size_pt": [pw, ph],
                })
        # capture template text spans so nothing sneaks through unnoticed
        text = page.get_text("text").strip()
        manifest.append({"page": pno + 1, "text": text})
    with open(os.path.join(out_dir, "manifest.json"), "w") as fh:
        json.dump(manifest, fh, indent=1)
    print(f"{name}: {doc.page_count} pages -> {out_dir}")


if __name__ == "__main__":
    for name, path in SOURCES.items():
        extract(name, path)
    print("done")
