#!/usr/bin/env bash
# Regenera a versão HTML dos slides (docs/slides/) a partir do PDF exportado.
# Uso: bash slides/gerar_html.sh   (a partir da raiz do repositório)
set -euo pipefail
cd "$(dirname "$0")/.."
PDF=slides/curso-ia-estatistica.pdf
OUT=docs/slides
rm -f "$OUT"/img/s-*.jpg
mkdir -p "$OUT/img"
pdftoppm -r 110 -jpeg -jpegopt quality=85 "$PDF" "$OUT/img/s" 2>/dev/null
N=$(ls "$OUT"/img/s-*.jpg | wc -l)
python3 - "$PDF" "$N" "$OUT/textos.json" <<'PY'
import json, re, subprocess, sys
pdf, n, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
textos = []
for i in range(1, n + 1):
    t = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), pdf, "-"],
                       capture_output=True, text=True).stdout
    textos.append(re.sub(r"\s+", " ", t).strip()[:600])
json.dump(textos, open(out, "w", encoding="utf-8"), ensure_ascii=False)
PY
sed -i "s/const TOTAL = [0-9]*;/const TOTAL = $N;/" "$OUT/index.html"
echo "$N slides gerados em $OUT"
