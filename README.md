# WebGuvenligi - Advanced Web Security Scanner

**Tarafından Oluşturuldu: ST \\ For WebGuvenligi**

## Özellikler

- 🔍 **SQL Injection (SQLi)** - 500+ test payload
- ⚡ **Cross-Site Scripting (XSS)** - DOM, Reflected, Stored
- 🌐 **Server-Side Request Forgery (SSRF)** - 200+ payload
- 🛡️ **Cross-Site Request Forgery (CSRF)** - Token analizi
- 🖱️ **Clickjacking** - X-Frame-Options kontrol

## Tarama Metodları

✅ Otomatik Tarama
✅ Batch İşleme (URL listesi)
✅ HTTP Metodları: GET, POST, PUT, PATCH, DELETE
✅ Multi-threading Desteği
✅ Proxy Desteği (Burp Suite, OWASP ZAP)
✅ WAF Bypass Teknikleri
✅ Rate Limiting Yönetimi

## GUI

- PyQt6 Tabanlı Modern Arayüz
- Real-time Tarama Sonuçları
- Detaylı Rapor Oluşturma (HTML)
- Payload Editleme ve Customizasyon
- Geçmiş Taramaları Yönetme

## Kurulum

```bash
git clone https://github.com/st-webguvenligi/WebGuvenligi.git
cd WebGuvenligi
pip install -r requirements.txt
python main.py
```

## Kullanım

### CLI Modu
```bash
python cli.py --url http://target.com --scan-type all --output report.html
```

### GUI Modu
```bash
python main.py
```

## Lisans

MIT Lisansı - Ayrıntılar için LICENSE dosyasına bakınız.

---
**⚠️ DİKKAT**: Bu araç yalnızca yetkili testler için kullanılmalıdır. Yetkisiz erişim yasalara aykırıdır.