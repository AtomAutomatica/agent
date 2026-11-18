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

SA="$OUT/Ferox-Oil-Robinson-1-Area-Wells-Production.pdf"
if [ -f "$ROOT/build/standalone.html" ]; then
  /opt/pw-browsers/chromium \
    --headless=new --no-sandbox --disable-gpu \
    --allow-file-access-from-files \
    --no-pdf-header-footer \
    --virtual-time-budget=20000 \
    --print-to-pdf="$SA" \
    "file://$ROOT/build/standalone.html" 2>/dev/null
  echo "Standalone: $SA ($(pdfinfo "$SA" | awk '/^Pages/{print $2}') pages)"
fi

rm -f "$OUT"/pages/*.png
pdftoppm -png -r 110 "$PDF" "$OUT/pages/page"
if [ -f "$SA" ]; then pdftoppm -png -r 110 "$SA" "$OUT/pages/sa"; fi
echo "PDF: $PDF ($(pdfinfo "$PDF" | awk '/^Pages/{print $2}') pages)"
