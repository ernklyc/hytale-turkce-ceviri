#!/bin/bash
# Paketi yerelde test etmek icin UserData/Mods icine kurar.
set -euo pipefail
PROJE="$(cd "$(dirname "$0")" && pwd)"
MODS="/Users/eren/Library/Application Support/Hytale/UserData/Mods"

bash "$PROJE/paketle.sh"
ZIP="$(ls -t "$PROJE"/KLYC-Turkce-Ceviri-v*.zip | head -1)"

mkdir -p "$MODS"
# eski test kopyalarini temizle
rm -f "$MODS"/KLYC-Turkce-Ceviri-v*.zip "$MODS"/Turkce-Ceviri-v*.zip
cp "$ZIP" "$MODS/"
echo
echo "Kuruldu: $MODS/$(basename "$ZIP")"
echo "Simdi: oyunu ac -> bir dunya olustur/ac -> Dunya Ayarlari > Modlar -> 'Turkce Ceviri' etkin olsun"
echo "Sonra dunyaya gir, esya/blok isimlerine bak."
echo
echo "Kontrol: en yeni server log'da 'entries for tr-TR' satiri var mi?"
echo "  ls -t '/Users/eren/Library/Application Support/Hytale/UserData/Saves'/*/logs/*.log | head -1"
