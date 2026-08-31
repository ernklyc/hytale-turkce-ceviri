#!/bin/bash
# pack/ klasorunu yayina hazir bir .zip haline getirir.
set -euo pipefail
PROJE="$(cd "$(dirname "$0")" && pwd)"
SURUM="$(/usr/bin/python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["Version"])' "$PROJE/pack/manifest.json")"
CIKTI="$PROJE/KLYC-Turkce-Ceviri-v$SURUM.zip"

cd "$PROJE/pack"
rm -f "$CIKTI"
# .DS_Store ve gizli dosyalar haric
find . -name '.DS_Store' -delete
zip -r -X "$CIKTI" manifest.json Server Common >/dev/null
echo "Paket hazir: $CIKTI"
unzip -l "$CIKTI"
