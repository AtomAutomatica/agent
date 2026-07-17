# Ferox Oil — Robinson #1 Prospectus

Rebuild of the Robinson #1 (Van Zandt County, TX) well prospectus under the
Ferox Oil brand: red/black/white theme, Ferox Oil logo, accurate table of
contents, cleaned-up template typos, and a new cover and contact page.

## Layout

- `assets/brand/` — Ferox Oil logo (extracted from the Lilly #1-H subscription
  agreement) and the cover photo (extracted from the original book).
- `assets/extracted/robinson/` — every exhibit scan pulled untouched from the
  original ccRobinson PDF, plus `manifest.json` with placement geometry.
- `assets/optimized/` — JPEG versions of the exhibits used by the build to keep
  the final PDF email-sized (PNG masters remain in `assets/extracted/`).
- `assets/fonts/` — locally hosted Barlow Condensed + Archivo woff2 files.
- `build/` — generated `index.html` plus the hand-written `style.css` design
  system (brand tokens: red `#BF0000`, orange `#FFA300`).
- `tools/` — pipeline scripts (see below).
- `output/Ferox-Oil-Robinson-1-Prospectus.pdf` — the deliverable.

## Build

```sh
python3 tools/extract_assets.py    # one-time: pull exhibits from source PDFs
python3 tools/optimize_images.py   # one-time: JPEG-flatten exhibits
bash tools/make_pdf.sh             # generate HTML, print to PDF via Chromium,
                                   # render per-page QA PNGs
```

## Content decisions

- Every exhibit page of the original book is preserved 1:1 and in order; only
  the surrounding template chrome (headers, footers, titles, TOC) was rebuilt.
- Official/third-party documents inside the scans — the RRC Form W-1 permit,
  permit plat, RRC online-system records, surveyor and geologist documents —
  are reproduced exactly as filed and intentionally left unmodified.
- The one typed template page ("Multiple Stacked Proven Production") was
  retyped with obvious typos fixed ("Smackdown" → "Smackover", "act of well
  control" → "lack of well control", etc.) without changing its meaning.
- A leftover Canva header ("SOCIAL MEDIA REPORT // JUNE 2020") and title typos
  ("PALUXY 7.700'", "SMACKOVER 15,000\"", "RCC MAP WITH FRE SITE") were fixed.
- Contact details come from Ferox Oil's own Lilly #1-H investor kit.
