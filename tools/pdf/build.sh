#!/bin/bash
# Build a reading PDF in the project's 13-part format: tools/pdf/build.sh SOURCE.md OUTPUT.pdf
set -e
SRC="$1"; OUT="$2"; HERE="$(cd "$(dirname "$0")" && pwd)"; TMP="$(mktemp -d)"
pandoc "$SRC" -f markdown -t html5 -s --toc --toc-depth=1 --metadata toc-title="Contents" -c "$HERE/style.css" -o "$TMP/r.html"
wkhtmltopdf -q --enable-local-file-access -s A4 -T 18mm -B 18mm -L 18mm -R 18mm \
  --footer-center "[page]" --footer-font-name "DejaVu Sans" --footer-font-size 8 "$TMP/r.html" "$OUT" 2>/dev/null || true
test -s "$OUT" && echo "built $OUT"
