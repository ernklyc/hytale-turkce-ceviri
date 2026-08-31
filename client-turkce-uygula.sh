#!/bin/bash
# Menü çevirisini oyuna (yeniden) uygular + ad-hoc imzalar.
# Oyun güncellemesinden SONRA tekrar çalıştır (güncelleme tr-TR/ klasörünü siler).
set -e
APP="/Users/eren/Library/Application Support/Hytale/install/release/package/game/latest/Client/Hytale.app"
SRC="/Users/eren/hytale-turkce-mod/client-turkce/tr-TR"
LANGDIR="$APP/Contents/Resources/Data/Shared/Language"
[ -d "$SRC" ] || { echo "Kaynak yok: $SRC"; exit 1; }
[ -d "$APP" ] || { echo "Oyun bulunamadi: $APP"; exit 1; }
# yedek yoksa al
YEDEK="/Users/eren/hytale-turkce-mod/_client_yedek/Client_v0.6.2_build25"
if [ ! -d "$YEDEK" ]; then
  echo "UYARI: orijinal yedek yok. Once dokunmadan yedek al:"
  echo "  mkdir -p \"\$(dirname \"$YEDEK\")\" && cp -Rp \"\$(dirname \"$APP\")\" \"$YEDEK\""
fi
rm -rf "$LANGDIR/tr-TR"
cp -Rp "$SRC" "$LANGDIR/tr-TR"
codesign --force --deep --sign - --preserve-metadata=entitlements "$APP"
codesign --verify --deep --strict "$APP" && echo "imza: GECERLI"
xattr -cr "$APP"
# dil ayarini tr-TR yap
python3 - <<'PY'
import json
p="/Users/eren/Library/Application Support/Hytale/UserData/Settings.json"
s=json.load(open(p)); s["Language"]="tr-TR"
json.dump(s,open(p,"w"),indent=2,ensure_ascii=False)
PY
echo "TAMAM - oyunu baslat, menuler Turkce olmali."
