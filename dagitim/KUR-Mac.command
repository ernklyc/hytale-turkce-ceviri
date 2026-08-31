#!/bin/bash
# ============================================================
#  Hytale Türkçe Çeviri Full — KLYC
#  Kurulum aracı (macOS)
#  Bu dosyaya çift tıkla. İlk seferde "Aç" demen gerekebilir
#  (sağ tık -> Aç).
# ============================================================
set -u

# --- Renkli çıktı ---
r(){ printf '\033[1;31m%s\033[0m\n' "$*"; }
g(){ printf '\033[1;32m%s\033[0m\n' "$*"; }
y(){ printf '\033[1;33m%s\033[0m\n' "$*"; }
b(){ printf '\033[1m%s\033[0m\n' "$*"; }

BURASI="$(cd "$(dirname "$0")" && pwd)"
APPSUP="$HOME/Library/Application Support/Hytale"
YEDEKKOK="$APPSUP/UserData/_KLYC_TurkceYedek"

echo
b "======================================================"
b "  Hytale Türkçe Çeviri Full  —  KLYC"
b "  Kurulum"
b "======================================================"
echo

# --- 1. Hytale kurulu mu? ---
if [ ! -d "$APPSUP" ]; then
  r "Hytale bulunamadı: $APPSUP"
  r "Önce Hytale'i kur ve bir kez çalıştır, sonra bu aracı tekrar dene."
  echo; read -r -p "Kapatmak için Enter'a bas..." _ ; exit 1
fi

# --- 2. Client.app'i bul ---
CLIENT=""
for p in \
  "$APPSUP"/install/*/package/game/latest/Client/Hytale.app \
  "$APPSUP"/install/*/*/package/game/latest/Client/Hytale.app \
  "$APPSUP"/install/release/package/game/latest/Client/Hytale.app ; do
  [ -d "$p" ] && CLIENT="$p" && break
done
if [ -z "$CLIENT" ]; then
  # geniş arama
  CLIENT="$(find "$APPSUP/install" -maxdepth 8 -name "Hytale.app" -type d 2>/dev/null | head -1)"
fi
if [ -z "$CLIENT" ] || [ ! -d "$CLIENT" ]; then
  r "Oyun dosyası (Hytale.app) bulunamadı."
  r "Hytale güncel mi ve bir kez çalıştırıldı mı? Kontrol et."
  echo; read -r -p "Kapatmak için Enter'a bas..." _ ; exit 1
fi
CLIENTDIR="$(dirname "$CLIENT")"
LANGDIR="$CLIENT/Contents/Resources/Data/Shared/Language"
g "Oyun bulundu:"
echo "   $CLIENT"

# --- 3. Sürüm tespiti ---
SURUM="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleShortVersionString' "$CLIENT/Contents/Info.plist" 2>/dev/null || echo bilinmiyor)"
BUILD="$(/usr/libexec/PlistBuddy -c 'Print :CFBundleVersion' "$CLIENT/Contents/Info.plist" 2>/dev/null || echo x)"
ETIKET="v${SURUM}-${BUILD}"
echo "   Oyun sürümü: $SURUM (build $BUILD)"
echo

# --- 4. Yedek (bu sürüm için bir kez) ---
YEDEK="$YEDEKKOK/Client_$ETIKET"
# Oyun zaten değiştirilmiş mi? (Hypixel imzası = temiz, adhoc = daha önce kurmuşuz)
TEAM="$(codesign -dv --verbose=2 "$CLIENT" 2>&1 | grep -o 'TeamIdentifier=[^ ]*' | cut -d= -f2)"
if [ -d "$YEDEK/Hytale.app" ]; then
  y "Bu sürüm için yedek zaten var, atlanıyor."
elif [ "$TEAM" != "725HRU545H" ]; then
  # Zaten değiştirilmiş, temiz yedek yok -> güncelleme olmuş olabilir.
  # Eski bir yedek var mı bak.
  ESKIYEDEK="$(ls -td "$YEDEKKOK"/Client_* 2>/dev/null | head -1)"
  if [ -n "$ESKIYEDEK" ] && [ -d "$ESKIYEDEK/Hytale.app" ]; then
    y "Oyun zaten değiştirilmiş görünüyor ve bu sürümün temiz yedeği yok."
    y "Bu genelde oyun güncellendiğinde olur (yeni imzayı bozamayız)."
    y "Önce oyunu 'Verify/Repair' ile onar, sonra bu aracı tekrar çalıştır."
    echo
    r "Güvenli devam edilemiyor — işlem durduruldu."
    echo; read -r -p "Kapatmak için Enter'a bas..." _ ; exit 1
  fi
  y "Uyarı: oyun Hypixel imzalı değil (adhoc). Yine de devam ediliyor,"
  y "yedek bu haliyle alınıyor."
  mkdir -p "$YEDEK"; cp -Rp "$CLIENTDIR"/* "$YEDEK/" 2>/dev/null || { r "Yedekleme başarısız."; rm -rf "$YEDEK"; read -r -p "Enter..." _; exit 1; }
  g "   Yedek alındı."
else
  b "1/4  Orijinal oyun yedekleniyor..."
  mkdir -p "$YEDEK"
  # sadece Client klasörünü yedekle (Assets.zip 3GB, ona dokunmuyoruz)
  if ! cp -Rp "$CLIENTDIR"/* "$YEDEK/" 2>/dev/null; then
    r "Yedekleme başarısız (disk alanı?). İşlem durduruldu."
    rm -rf "$YEDEK"
    echo; read -r -p "Kapatmak için Enter'a bas..." _ ; exit 1
  fi
  g "   Yedek alındı: $YEDEK"
fi
echo

# --- 5. Mod paketini kur (oyun içi metinler) ---
b "2/4  Oyun içi çeviri (mod paketi) kuruluyor..."
MODS="$APPSUP/UserData/Mods"
mkdir -p "$MODS"
rm -f "$MODS"/KLYC-Turkce-Ceviri-v*.zip "$MODS"/Turkce-Ceviri-v*.zip 2>/dev/null
MODZIP="$(ls "$BURASI/mod/"KLYC-Turkce-Ceviri-v*.zip 2>/dev/null | head -1)"
if [ -z "$MODZIP" ]; then
  r "mod/ klasöründe çeviri paketi bulunamadı. İndirmeyi eksiksiz aldın mı?"
  echo; read -r -p "Kapatmak için Enter'a bas..." _ ; exit 1
fi
cp "$MODZIP" "$MODS/"
g "   Kuruldu: $(basename "$MODZIP")"
echo

# --- 6. Menü çevirisini oyunun içine koy + yeniden imzala ---
b "3/4  Menü çevirisi uygulanıyor..."
if [ ! -f "$BURASI/menu/tr-TR/client.lang" ]; then
  r "menu/tr-TR/client.lang bulunamadı. İndirmeyi eksiksiz aldın mı?"
  echo; read -r -p "Kapatmak için Enter'a bas..." _ ; exit 1
fi
rm -rf "$LANGDIR/tr-TR"
mkdir -p "$LANGDIR/tr-TR"
cp "$BURASI/menu/tr-TR/client.lang" "$LANGDIR/tr-TR/client.lang"
cp "$BURASI/menu/tr-TR/meta.lang"   "$LANGDIR/tr-TR/meta.lang"
g "   tr-TR dil dosyaları eklendi."

b "4/4  Oyun yeniden imzalanıyor (birkaç saniye)..."
if ! codesign --force --deep --sign - --preserve-metadata=entitlements "$CLIENT" >/dev/null 2>&1; then
  r "İmzalama başarısız. Oyunu yedekten geri alıyorum..."
  rm -rf "$CLIENTDIR"; mkdir -p "$CLIENTDIR"; cp -Rp "$YEDEK"/* "$CLIENTDIR/"
  r "Geri alındı. KLYC'ye ekran görüntüsüyle ulaş."
  echo; read -r -p "Kapatmak için Enter'a bas..." _ ; exit 1
fi
if ! codesign --verify --deep --strict "$CLIENT" >/dev/null 2>&1; then
  r "İmza doğrulaması başarısız. Yedekten geri alıyorum..."
  rm -rf "$CLIENTDIR"; mkdir -p "$CLIENTDIR"; cp -Rp "$YEDEK"/* "$CLIENTDIR/"
  echo; read -r -p "Kapatmak için Enter'a bas..." _ ; exit 1
fi
xattr -cr "$CLIENT" 2>/dev/null || true
g "   İmza geçerli."
echo

# --- 7. Oyun dilini tr-TR yap ---
SET="$APPSUP/UserData/Settings.json"
if [ -f "$SET" ]; then
  /usr/bin/python3 - "$SET" <<'PY' 2>/dev/null || true
import json,sys
p=sys.argv[1]
try:
    s=json.load(open(p)); s["Language"]="tr-TR"
    json.dump(s,open(p,"w"),indent=2,ensure_ascii=False)
except Exception: pass
PY
fi

# kurulan sürümü not düş (bir sonraki güncellemeyi anlamak için)
echo "$ETIKET" > "$YEDEKKOK/son_kurulum.txt" 2>/dev/null || true

b "======================================================"
g "  KURULUM TAMAM!"
b "======================================================"
echo
echo "  • Oyunu tamamen kapat, sonra launcher'dan aç."
echo "  • Menü + oyun içi her şey Türkçe olmalı."
echo "  • Menü İngilizce ise: Ayarlar -> Dil -> Türkçe."
echo
y "  ÖNEMLİ: Oyun güncellenirse menü çevirisi silinir."
y "  Güncellemeden sonra bu KUR-Mac.command dosyasına tekrar çift tıkla."
echo
echo "  Geri almak için: KALDIR-Mac.command"
echo
read -r -p "Kapatmak için Enter'a bas..." _
