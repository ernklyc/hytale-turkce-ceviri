# Hytale Türkçe Çeviri Full — Detaylı Kurulum ve Teknik Rehber

**Yapım:** Eren KALAYCI (KLYC) · ernklyc@gmail.com · https://ernklyc.dev
**Kapsam:** Oyunun **tamamı** — ana menü, ayarlar, dünyalar, sunucular, avatar,
envanter, tooltip'ler, inşaatçı araçları + oyun içi tüm metinler (eşya, blok,
komut, NPC, dünya, geçitler...).

---

## 1. Çeviri iki parçadan oluşur

| Parça | Ne kapsar | Nasıl kurulur | Güncellemede |
|---|---|---|---|
| **Mod paketi** (`KLYC-Turkce-Ceviri-vX.Y.Z.zip`) | Oyun içinde, bir dünyaya girince görünen her şey: eşya/blok adları, açıklamalar, komutlar, NPC, dünya metinleri | `UserData/Mods/` klasörüne kopyalanır. Hytale'in **resmi mod sistemi** | ✅ Kalıcı |
| **Menü çevirisi** (`tr-TR/client.lang`) | Ana menü, ayarlar, butonlar, sekmeler, tooltip'ler, yükleme ekranı | Oyunun dil klasörüne eklenir + (macOS'ta) yeniden imzalanır | ⚠️ Güncelleme silebilir → `KUR-Mac.command`'ı tekrar çalıştır |

---

## 2. macOS kurulumu

### Otomatik (önerilen)
1. `KUR-Mac.command` → çift tıkla (ilk sefer: sağ tık → Aç).
2. Terminal penceresi açılır, işlem biter.
3. Hytale'i tam kapat–aç.

### Elle (ileri düzey)
```bash
APP="$HOME/Library/Application Support/Hytale/install/release/package/game/latest/Client/Hytale.app"
LANG="$APP/Contents/Resources/Data/Shared/Language"

# 1. Yedek
mkdir -p ~/hytale-yedek && cp -Rp "$(dirname "$APP")" ~/hytale-yedek/

# 2. Mod paketi
cp mod/KLYC-Turkce-Ceviri-v*.zip "$HOME/Library/Application Support/Hytale/UserData/Mods/"

# 3. Menü çevirisi
cp -R menu/tr-TR "$LANG/"

# 4. Yeniden imzala (ad-hoc)
codesign --force --deep --sign - --preserve-metadata=entitlements "$APP"
codesign --verify --deep --strict "$APP"      # "valid on disk" demeli
xattr -cr "$APP"

# 5. Dil ayarı
# UserData/Settings.json içinde "Language": "tr-TR" yap
```

---

## 3. Windows kurulumu

Windows'ta menü çevirisi **çok daha kolay** — kod imzası duvarı yok, yeniden
imzalamaya gerek yok.

1. **Mod paketi:**
   `KLYC-Turkce-Ceviri-vX.Y.Z.zip` dosyasını şuraya kopyala:
   `%AppData%\Hytale\UserData\Mods\`

2. **Menü çevirisi:**
   `menu\tr-TR\` klasörünü (içinde `client.lang` + `meta.lang`) şuraya kopyala:
   `%AppData%\Hytale\install\release\package\game\latest\Client\Hytale\Data\Shared\Language\`
   (klasör yolu sürümle biraz değişebilir; `Language` klasörünü `en-US`'in
   yanında ara)

3. Oyun içi: **Ayarlar → Dil → Türkçe**.

> Windows'ta güncelleme de `tr-TR` klasörünü silebilir; silinirse 2. adımı
> tekrarla.

---

## 4. Sık sorulanlar

**"Some Hytale files are missing or corrupted" diyor.**
Genelde bir oyun güncellemesi menü dosyalarını değiştirdi ve ad-hoc imza
uyuşmadı. Launcher'da **Verify / Repair** yap → sonra `KUR-Mac.command`.

**Menü İngilizce ama eşya adları Türkçe.**
Menü çevirisi kurulmamış ya da güncelleme silmiş. `KUR-Mac.command` çalıştır.
Ayrıca **Ayarlar → Dil → Türkçe** seçili mi bak.

**Eşya adları İngilizce ama menü Türkçe.**
Mod paketi `UserData/Mods/` içinde değil, ya da dünyada mod devre dışı.
Dünya Ayarları → Modlar → "Türkçe Çeviri Full" **etkin** olmalı.

**Karakter panelinde garip bir yazı var ("MACKALIFIRLAMA" gibi).**
O senin avatar adın, çeviri değil.

**Bazı büyük harfli yazılarda "İ" yerine "I" var.**
Oyunun büyük-harf sistemi Türkçe'yi tam desteklemiyor. En görünür yerler
(butonlar, sekmeler) düzeltildi; kalan yerleri bildirirsen eklerim.

**Bazı yazılar taşıyor / üst üste biniyor.**
Türkçe İngilizce'den uzun. O metni bildirirsen kısaltırım.

**Oyun güncellemesi geldi.**
Mod paketi kalır. Menü için `KUR-Mac.command`'ı tekrar çalıştır (10 sn).

---

## 5. Ne değiştiriliyor, ne değiştirilmiyor

**Değişen:** Yalnızca metin dosyaları (`.lang`) ve oyunun yerel imzası.
**Değişmeyen:** Oyun kodu, mantık, ağ, kayıtlar, `Assets.zip` (3 GB — ona
dokunulmuyor).

Bu araç:
- İnternete bağlanmaz, veri göndermez.
- Kurulumdan önce oyunu yedekler (`UserData/_KLYC_TurkceYedek/`).
- Her adımda hata kontrolü yapar; imza tutmazsa otomatik geri alır.

---

## 6. Kaldırma

`KALDIR-Mac.command` → oyun orijinal (Hypixel imzalı) haline döner, mod silinir,
dil ayarı sıfırlanır. Yedek klasörü kalır (elle silebilirsin).

---

## 7. Lisans

Bu paket oyunun **hiçbir orijinal dosyasını içermez** — yalnızca KLYC'nin
özgün Türkçe çeviri metinleri. Hytale EULA çeviri ve modlamaya izin verir.
Serbestçe paylaşabilirsin; kaynak göstermen yeterli.
