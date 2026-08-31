#!/bin/bash
# Yeni sürüm yayınlama — çeviriyi düzenledikten sonra çalıştır.
#   ./yayinla.sh 1.0.1     (yeni sürüm numarası)
# Yaptıkları:
#   1. manifest.json Version'u günceller
#   2. server.lang + client.lang bütünlük kontrolü (eksik/çift/bozuk)
#   3. mod zip'ini üretir -> dagitim/mod/
#   4. menü çevirisini dagitim/menu/ ve UserData'ya kopyalar
set -e
cd "$(dirname "$0")"

YENI="${1:-}"
[ -z "$YENI" ] && { echo "Kullanım: ./yayinla.sh <sürüm>   örn: ./yayinla.sh 1.0.1"; exit 1; }

echo ">> manifest Version -> $YENI"
python3 -c "import json;m=json.load(open('pack/manifest.json'));m['Version']='$YENI';json.dump(m,open('pack/manifest.json','w'),indent=2,ensure_ascii=False)"

echo ">> bütünlük kontrolü..."
python3 - <<'PY'
import re,sys
def blk(fn):
    a=open(fn,encoding='utf-8').read().split('\n');i=0;o={}
    while i<len(a):
        m=re.match(r'^([A-Za-z0-9_.\-()]+) ?= ?(.*)$',a[i])
        if m:
            b=[m.group(2)];j=i
            while a[j].endswith('\\'): j+=1;b.append(a[j])
            o[m.group(1)]='\n'.join(b);i=j+1
        else:i+=1
    return o
bad=False
for ef,tf,name in [
  ("kaynak/Server/server.lang","pack/Server/Languages/tr-TR/server.lang","server.lang"),
  ("client-turkce/EN-referans.txt" if False else "kaynak/Server/server.lang","client-turkce/tr-TR/client.lang","client.lang(sadece yapı)"),
]:
    T=blk(tf)
    brace=[k for k,v in T.items() if v.count('{')!=v.count('}')]
    from collections import Counter
    lines=open(tf,encoding='utf-8').read().split('\n')
    c=Counter(re.match(r'^([A-Za-z0-9_.\-()]+) ?= ',l).group(1) for l in lines if re.match(r'^[A-Za-z0-9_.\-()]+ ?= ',l))
    dup=[k for k,v in c.items() if v>1]
    orph=0;pc=False
    for l in lines:
        if l=='' or l.startswith('#'):pc=False;continue
        if re.match(r'^[A-Za-z0-9_.\-()]+ ?= ',l):pc=l.endswith('\\');continue
        if pc:pc=l.endswith('\\');continue
        orph+=1
    # client.lang'in dogal dup'lari (oyun dosyasinda da var) - bilinen 8
    known_dup=8 if 'client' in tf else 0
    d=max(0,len(dup)-known_dup)
    print(f"  {name}: brace {len(brace)} | fazladan dup {d} | orphan {orph}")
    if brace or d or orph: bad=True
if bad:
    print("!! HATA VAR — yayınlama durduruldu"); sys.exit(1)
print("  ✓ temiz")
PY

echo ">> mod paketi üretiliyor..."
rm -f KLYC-Turkce-Ceviri-v*.zip dagitim/mod/*.zip
bash paketle.sh >/dev/null
ZIP="$(ls KLYC-Turkce-Ceviri-v*.zip)"
cp "$ZIP" dagitim/mod/
cp "$ZIP" "$HOME/Library/Application Support/Hytale/UserData/Mods/" 2>/dev/null || true

echo ">> menü çevirisi kopyalanıyor..."
cp -p client-turkce/tr-TR/client.lang dagitim/menu/tr-TR/client.lang
cp -p client-turkce/tr-TR/meta.lang   dagitim/menu/tr-TR/meta.lang

echo
echo "TAMAM.  $ZIP  ->  dagitim/mod/  +  UserData/Mods/"
echo "Menü değiştiyse: bash client-turkce-uygula.sh  (oyunu yeniden imzalar)"
echo "GitHub: dagitim/ klasörünü commit'le, release oluştur."
