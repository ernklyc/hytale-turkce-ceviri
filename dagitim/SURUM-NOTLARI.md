# Sürüm Notları — Hytale Türkçe Çeviri Full (KLYC)

## v1.0.0 — İlk yayın (2026-08-31)

Oyunun **tamamı Türkçe**: hem oyun içi metinler hem menüler.

### Oyun içi (mod paketi)
- `server.lang`: 11009 anahtarın hepsi işlendi, ~%99 çeviri
  (kalan = fantezi özel adlar, kod şablonları)
- Eşya/blok adları, tüm açıklamalar, ~2800 komut mesajı, NPC'ler,
  dünya metinleri, hatıralar, geçitler, inşaatçı/editör araçları
- `Common/` avatar özelleştirme: 22 dosya, ~%98

### Menü (ayrı kurulum betiği)
- `client.lang`: ~3480 anahtar, %100 çevrilebilir içerik
  (kalan = klavye tuş adları, `x10`/`ms` gibi evrensel gösterimler,
  marka terimleri)
- Ana menü, ayarlar, dünyalar, sunucular, avatar, envanter,
  tooltip'ler, inşaatçı araçları eğitim metinleri

### Teknik
- Windows + macOS kurulum/kaldırma betikleri
- macOS'ta oyun ad-hoc yeniden imzalanır; kurulum öncesi tam yedek
- Tüm katmanlarda: 0 eksik anahtar, 0 çift kayıt, 0 bozuk satır,
  0 placeholder/etiket hatası

### Bilinen sınırlar
- Oyunun büyük-harf sistemi Türkçe `i/İ/ı/I` kurallarını tam bilmez;
  en görünür yerler (butonlar/sekmeler) elle düzeltildi
- Türkçe İngilizce'den uzun olduğu için bazı dar kutularda taşma olabilir
- Menü çevirisi oyun güncellemesinde silinir → `KUR` betiği tekrar çalıştırılır

---

## Güncelleme politikası

- **Kimlik asla değişmez:** `KLYC : Türkçe Çeviri Full`. Değişirse eski
  dünyalar "MISSING MOD" verir. Yalnızca `Version` artar.
- `ServerVersion: "*"` → mod her oyun sürümüyle uyumlu sayılır,
  "güncel değil" uyarısı vermez.
- Oyun yeni metin eklerse: çevrilmemiş anahtarlar otomatik İngilizce
  görünür (bozulma olmaz). Yeni sürümde eklenir.
- Sürüm numarası: `BÜYÜK.KÜÇÜK.YAMA`
  - YAMA: çeviri düzeltmeleri (1.0.1, 1.0.2...)
  - KÜÇÜK: yeni oyun sürümü kapsaması, yeni bölüm çevirileri
  - BÜYÜK: yapı değişikliği (nadir)

---
Yapım: **Eren KALAYCI (KLYC)** · ernklyc@gmail.com · https://ernklyc.dev
github.com/ernklyc/hytale-turkce-ceviri
