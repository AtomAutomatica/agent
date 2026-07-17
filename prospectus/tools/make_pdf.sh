#!/usr/bin/env bash
# Build the prospectus PDF from the generated HTML and render QA page images.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/output"
PDF="$OUT/Ferox-Oil-Robinson-1-Prospectus.pdf"
mkdir -p "$OUT/pages"

python3 "$ROOT/tools/build_prospectus.py"

/opt/pw-browsers/chromium \
  --headless=new --no-sandbox --disable-gpu \
  --allow-file-access-from-files \
  --no-pdf-header-footer \
  --virtual-time-budget=20000 \
  --print-to-pdf="$PDF" \
  "file://$ROOT/build/index.html" 2>/dev/null

rm -f "$OUT"/pages/*.png
pdftoppm -png -r 110 "$PDF" "$OUT/pages/page"
echo "PDF: $PDF ($(pdfinfo "$PDF" | awk '/^Pages/{print $2}') pages)"
ls "$OUT/pages" | head -30
