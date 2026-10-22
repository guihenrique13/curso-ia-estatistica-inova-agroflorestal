#!/usr/bin/env bash
# Gera apostila.docx e apostila.pdf a partir de apostila.md.
# Uso: bash apostila/build/build.sh   (de qualquer pasta)
# Requisitos: pandoc (~/.local/bin/pandoc), python3, LibreOffice snap (/snap/bin/libreoffice).
set -euo pipefail

BUILD="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APOST="$(dirname "$BUILD")"
PANDOC="${PANDOC:-$HOME/.local/bin/pandoc}"
LO="${LO:-/snap/bin/libreoffice}"
# O LibreOffice snap não enxerga /tmp: a pasta temporária fica no $HOME.
# (O caminho do log também está fixo em Module1.xba.)
TMPD="$HOME/lo_build_tmp_apostila"
PROFILE="$TMPD/profile"
PAT="UserInstallation=file://$PROFILE"   # só os processos deste build

cleanup() {
  pkill -f "soffice[.]bin.*$PAT" 2>/dev/null || true
  sleep 1
  pkill -9 -f "soffice[.]bin.*$PAT" 2>/dev/null || true
  rm -rf "$TMPD"
}
trap cleanup EXIT

rm -rf "$TMPD"; mkdir -p "$TMPD"

echo "1/4 pandoc -> docx"
"$PANDOC" "$APOST/apostila.md" -o "$APOST/apostila.docx" \
  --from markdown --reference-doc="$BUILD/reference.docx" \
  --toc --toc-depth=2 --number-sections

echo "2/4 pós-processamento (linhas de tabela sem quebra, tabelas ABNT)"
python3 "$BUILD/postprocess.py" "$APOST/apostila.docx"

echo "3/4 perfil temporário do LibreOffice"
# Um perfil novo sobrescreve as macros na primeira inicialização:
# inicia uma vez, depois grava a macro.
"$LO" --headless --norestore --terminate_after_init \
  "-env:UserInstallation=file://$PROFILE" >/dev/null 2>&1 || true
pkill -f "soffice[.]bin.*$PAT" 2>/dev/null || true
sleep 1
MACRODIR="$PROFILE/user/basic/Standard"
[ -d "$MACRODIR" ] || { echo "perfil não criado em $PROFILE" >&2; exit 1; }
cp "$BUILD/Module1.xba" "$MACRODIR/Module1.xba"

echo "4/4 LibreOffice: atualizar sumário e exportar PDF"
cp "$APOST/apostila.docx" "$TMPD/in.docx"
"$LO" --headless --norestore --invisible "-env:UserInstallation=file://$PROFILE" \
  "macro:///Standard.Module1.Export(\"$TMPD/in.docx\",\"$TMPD/out.pdf\")" >/dev/null 2>&1 &
for _ in $(seq 1 180); do
  if [ -f "$TMPD/log.txt" ] && grep -q -E '^(ok|erro)' "$TMPD/log.txt"; then break; fi
  sleep 1
done
cat "$TMPD/log.txt" 2>/dev/null || true
grep -q '^ok' "$TMPD/log.txt" 2>/dev/null || { echo "falha na exportação do PDF" >&2; exit 1; }
sleep 2
cp "$TMPD/out.pdf" "$APOST/apostila.pdf"

if command -v pdfinfo >/dev/null; then
  pdfinfo "$APOST/apostila.pdf" | grep -E '^Pages'
fi
echo "pronto: $APOST/apostila.docx e $APOST/apostila.pdf"
