#!/bin/bash
# ============================================================
#  Hytale Türkçe Çeviri Full — KLYC
#  Kaldırma aracı (macOS)
#  Menü çevirisini geri alır, mod paketini siler.
# ============================================================
set -u
r(){ printf '\033[1;31m%s\033[0m\n' "$*"; }
g(){ printf '\033[1;32m%s\033[0m\n' "$*"; }
y(){ printf '\033[1;33m%s\033[0m\n' "$*"; }
b(){ printf '\033[1m%s\033[0m\n' "$*"; }

APPSUP="$HOME/Library/Application Support/Hytale"
YEDEKKOK="$APPSUP/UserData/_KLYC_TurkceYedek"

echo; b "======================================================"
b "  Hytale Türkçe Çeviri Full — Kaldırma"
b "======================================================"; echo

if [ ! -d "$APPSUP" ]; then r "Hytale bulunamadı."; read -r -p "Enter..." _; exit 1; fi

CLIENT="$(find "$APPSUP/install" -maxdepth 8 -name "Hytale.app" -type d 2>/dev/null | head -1)"
[ -z "$CLIENT" ] && { r "Oyun bulunamadı."; read -r -p "Enter..." _; exit 1; }
CLIENTDIR="$(dirname "$CLIENT")"
LANGDIR="$CLIENT/Contents/Resources/Data/Shared/Language"

# 1. Menü: en güncel yedekten Client'i geri koy (varsa)
YEDEK="$(ls -td "$YEDEKKOK"/Client_* 2>/dev/null | head -1)"
b "1/3  Menü çevirisi geri alınıyor..."
if [ -n "$YEDEK" ] && [ -d "$YEDEK/Hytale.app" ] && codesign --verify --strict "$YEDEK/Hytale.app" >/dev/null 2>&1; then
  # güvenli takas: önce yanına kopyala, sonra yer değiştir
  TMP="${CLIENTDIR}.__yeni__"
  rm -rf "$TMP"; mkdir -p "$TMP"
  if cp -Rp "$YEDEK"/* "$TMP/" 2>/dev/null && [ -d "$TMP/Hytale.app" ]; then
    ESKI="${CLIENTDIR}.__eski__"
    rm -rf "$ESKI"
    mv "$CLIENTDIR" "$ESKI" && mv "$TMP" "$CLIENTDIR" && rm -rf "$ESKI"
    g "   Oyun orijinal (Hypixel imzalı) haline döndürüldü."
  else
    rm -rf "$TMP"
    r "   Geri yükleme kopyası başarısız — hiçbir şey değiştirilmedi."
  fi
else
  # yedek yoksa: sadece tr-TR klasörünü sil + yeniden imzala
  rm -rf "$LANGDIR/tr-TR"
  codesign --force --deep --sign - --preserve-metadata=entitlements "$CLIENT" >/dev/null 2>&1
  xattr -cr "$CLIENT" 2>/dev/null || true
  y "   Yedek bulunamadı; tr-TR dil dosyası kaldırıldı ve yeniden imzalandı."
fi
echo

# 2. Mod paketini sil
b "2/3  Mod paketi siliniyor..."
rm -f "$APPSUP/UserData/Mods/"KLYC-Turkce-Ceviri-v*.zip "$APPSUP/UserData/Mods/"Turkce-Ceviri-v*.zip 2>/dev/null
g "   Silindi."
echo

# 3. Dili sıfırla
b "3/3  Dil ayarı sıfırlanıyor..."
SET="$APPSUP/UserData/Settings.json"
if [ -f "$SET" ]; then
  /usr/bin/python3 - "$SET" <<'PY' 2>/dev/null || true
import json,sys
p=sys.argv[1]
try:
    s=json.load(open(p))
    if s.get("Language")=="tr-TR": s["Language"]=None
    json.dump(s,open(p,"w"),indent=2,ensure_ascii=False)
except Exception: pass
PY
fi
g "   Tamam."
echo

y "Not: Yedekler '$YEDEKKOK' klasöründe duruyor."
y "Yer açmak istersen o klasörü elle silebilirsin."
echo
b "KALDIRMA TAMAM. Oyunu kapat–aç."
echo
read -r -p "Kapatmak için Enter'a bas..." _
