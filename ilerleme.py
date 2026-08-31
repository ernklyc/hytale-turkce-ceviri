#!/usr/bin/env python3
# Ceviri ilerlemesini gosterir: her bolumde kac satir cevrildi.
# Kullanim: python3 ilerleme.py
import re, sys, pathlib

PROJE = pathlib.Path(__file__).parent
KAYNAK = PROJE / "kaynak" / "Server" / "server.lang"
CEVIRI = PROJE / "pack" / "Server" / "Languages" / "tr-TR" / "server.lang"

def yukle(p):
    d, sec, devam = {}, "(bas)", False
    if not p.exists():
        return d
    for raw in p.read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        onceki = devam
        devam = raw.endswith("\\")
        if onceki:
            continue
        m = re.match(r"#\s*===\s*(.+?)\s*===", s)
        if m:
            sec = m.group(1); continue
        if not s or s.startswith("#") or "=" not in s:
            continue
        k = s.split("=", 1)[0].strip()
        if re.fullmatch(r"[A-Za-z0-9_.]+", k):
            d[k] = sec
    return d

kaynak = yukle(KAYNAK)
ceviri = set(yukle(CEVIRI))

# bolum -> [toplam, cevrilen]
sec = {}
for k, s in kaynak.items():
    sec.setdefault(s, [0, 0])
    sec[s][0] += 1
    if k in ceviri:
        sec[s][1] += 1

top_t = top_c = 0
print(f"{'BOLUM':<22} {'CEVRILEN':>10} {'TOPLAM':>8}  %")
print("-" * 50)
for s, (t, c) in sorted(sec.items(), key=lambda x: -x[1][0]):
    top_t += t; top_c += c
    bar = f"{100*c//t if t else 0:3d}%"
    print(f"{s:<22} {c:>10} {t:>8}  {bar}")
print("-" * 50)
print(f"{'TOPLAM':<22} {top_c:>10} {top_t:>8}  {100*top_c//top_t if top_t else 0}%")
