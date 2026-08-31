#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# items.*.description icin kalip tabanli ceviri. Karmasik lore metinleri INGILIZCE birakir.
import re, sys, pathlib
P = pathlib.Path(__file__).parent
KAYNAK = P/"kaynak"/"Server"/"server.lang"
HEDEF  = P/"pack"/"Server"/"Languages"/"tr-TR"/"server.lang"

def oku(p):
    d={}
    if not p.exists(): return d
    devam=False
    for raw in p.read_text(encoding="utf-8").splitlines():
        s=raw.strip(); o=devam; devam=raw.endswith("\\")
        if o: continue
        if not s or s.startswith("#") or "=" not in s: continue
        k,v=s.split("=",1)
        if re.fullmatch(r"[A-Za-z0-9_.]+",k.strip()): d[k.strip()]=v.strip()
    return d

mevcut=set(oku(HEDEF))
kaynak=oku(KAYNAK)

# --- basit sozluk (agac/urun adlari) ---
W={"Tree":"Ağacı","Wood":"Ahşap","Hardwood":"Sert Ahşap","Softwood":"Yumuşak Ahşap",
 "Lightwood":"Açık Ahşap","Darkwood":"Koyu Ahşap","Redwood":"Kızıl Ahşap","Blackwood":"Kara Ahşap",
 "Deadwood":"Ölü Ağaç","Drywood":"Kuru Ağaç","Goldenwood":"Altın Ahşap","Greenwood":"Yeşil Ahşap",
 "Frostwood":"Ayaz Ağacı","Tropical Wood":"Tropik Ahşap","Azure Wood":"Gök Mavisi Ahşap",
 "Apple":"Elma","Carrot":"Havuç","Corn":"Mısır","Cotton":"Pamuk","Onion":"Soğan","Potato":"Patates",
 "Pumpkin":"Balkabağı","Rice":"Pirinç","Tomato":"Domates","Turnip":"Şalgam","Wheat":"Buğday",
 "Lettuce":"Marul","Chilli":"Acı Biber","Cauliflower":"Karnabahar","Aubergine":"Patlıcan",
 "Wild Grass":"Yabani Ot","Wild Berries":"Yabani Meyve","Apples":"Elma","Stages":"Aşama","Stage":"Aşama",
 "Days":"Gün","Day":"Gün","Hours":"Saat","Regrows":"Yeniden büyür","Yields":"Verir","Water":"Su",
 "Oak":"Meşe","Ash":"Dişbudak","Birch":"Huş","Cedar":"Sedir","Maple":"Akçaağaç","Spruce":"Ladin",
 "Pine":"Çam","Palm":"Palmiye","Bamboo":"Bambu","Willow":"Söğüt","Aspen":"Titrek Kavak","Beech":"Kayın"}

def kel(m):
    return W.get(m.group(0), m.group(0))

def cevir(v):
    o=v
    # kalip 1: eritme
    m=re.match(r'Can be smelted into an? (<item[^/]*/>) at a (<item[^/]*/>)\.?$', v)
    if m: return f'{m.group(2)} içinde {m.group(1)} haline eritilebilir.'
    # kalip 2: isleme
    m=re.match(r'Can be processed into (<item[^/]*/>) at a (<item[^/]*/>)\.?$', v)
    if m: return f'{m.group(2)} tezgahında {m.group(1)} haline işlenebilir.'
    # kalip 3: Grows X
    m=re.match(r'Grows (.+)$', v)
    if m:
        x=W.get(m.group(1), m.group(1)); return f'{x} yetiştirir'
    # kalip 4: Must be planted on X
    m=re.match(r'(\[TMP\] )?Must be planted on (<item[^/]*/>)\.?$', v)
    if m: return f'{m.group(2)} üzerine ekilmelidir.'
    m=re.match(r'(\[TMP\] )?Must be planted on (<item[^/]*/>) (near Water|near gold blocks|against a 2 block high wall)\.?$', v)
    if m:
        ek={'near Water':'suyun yakınına','near gold blocks':'altın blokların yakınına','against a 2 block high wall':'2 blok yüksekliğinde bir duvara dayalı'}[m.group(3)]
        return f'{m.group(2)} üzerine, {ek} ekilmelidir.'
    # kalip 5: Can be obtained by destroying X
    m=re.match(r'(\[TMP\] )?Can be obtained by destroying (.+?)\.?$', v)
    if m: return f'{m.group(2)} yok edilerek elde edilebilir.'
    # kalip 6: Grows into a <color>X Tree</color>. \n• Yields ...
    if re.match(r'(\[TMP\] )?Grows into an? <color', v):
        t=v.replace('[TMP] ','')
        t=t.replace('Grows into a ','').replace('Grows into an ','')
        t=re.sub(r'</color>\.',  '</color>na dönüşür.', t, count=1)
        t=t.replace('Yields','Şunu verir:').replace('Growth Time:','Büyüme Süresi:')
        t=t.replace(' Grows ',' Büyür: ').replace('regrow every','şu sürede yeniden büyür:').replace('Apples','Elma')
        t=re.sub(r'\b(Stages?|Days?|Hours?|Hour)\b', kel, t)
        return t
    # kalip 7: kisa kullanim aciklamalari
    kısa={
      'Invisible Block use to block off areas.':'Alanları kapatmak için kullanılan görünmez blok.',
      'Use to leave the instance.':'Bu alandan çıkmak için kullan.',
      'Use to enter the Forgotten Temple.':'Unutulmuş Tapınak\'a girmek için kullan.',
      'Cures poison and grants temporary immunity.':'Zehri iyileştirir ve geçici bağışıklık sağlar.',
      'Work in Progress':'Yapım Aşamasında',
      'When placed, allows an Avatar to set their respawn point to this location.':'Yerleştirildiğinde, bir Avatar\'ın yeniden doğuş noktasını buraya ayarlamasına izin verir.',
      'Used to craft basic armor.':'Temel zırh üretmek için kullanılır.',
      'Used to craft basic weaponry.':'Temel silah üretmek için kullanılır.',
      'Used to fashion basic weaponry.':'Temel silah üretmek için kullanılır.',
      'Used to create structural building blocks.':'Yapısal inşaat blokları oluşturmak için kullanılır.',
      'Used to create potions and elixirs.':'İksir ve iksirler oluşturmak için kullanılır.',
      'The heart of any workshop. Used to forge advanced armor and weapons.':'Her atölyenin kalbi. Gelişmiş zırh ve silah dövmek için kullanılır.',
    }
    if v in kısa: return kısa[v]
    return None  # cevrilemedi

taslak=["", "# === items descriptions (KALIP TASLAK) ==="]
n=t=0
for k,v in kaynak.items():
    if k.startswith("items.") and k.endswith(".description") and k not in mevcut:
        t+=1
        c=cevir(v)
        if c: taslak.append(f"{k} = {c}"); n+=1
print("\n".join(taslak))
print(f"\n# {n}/{t} kalıpla çevrildi", file=sys.stderr)
