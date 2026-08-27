# WebGuvenligi - Kullanım Kılavuzu

## GUI Kullanımı

### 1. Uygulamayı Başlatın

```bash
python main.py
```

### 2. Tarama Konfigürasyonu

- **Target URL**: Taranacak web sitesinin URL'sini girin
- **HTTP Method**: GET, POST, PUT, PATCH veya DELETE seçin
- **Threads**: Eşzamanlı istek sayısını ayarlayın (1-20)
- **Timeout**: Bağlantı zaman aşımını ayarlayın (saniye)

### 3. Tarama Türlerini Seçin

- ✅ **SQL Injection**: SQL enjeksiyonu açıkları tarama
- ✅ **Cross-Site Scripting**: XSS açıkları tarama
- ✅ **SSRF**: Sunucu tarafı istek sahteciliği tarama
- ✅ **CSRF**: CSRF koruma kontrolleri
- ✅ **Clickjacking**: Clickjacking açıkları tarama

### 4. Taramayı Başlatın

"▶ Start Scan" butonuna tıklayın

### 5. Sonuçları İnceleyim

"Results" sekmesinde bulguları göreceğiniz detaylı tablo vardır:
- Açık Türü
- Hedef URL
- Payload
- Öncelik Seviyesi
- Parametre
- Zaman Damgası

### 6. Rapor Oluşturun

"Reports" sekmesinde:
- "📄 Generate Report" ile HTML rapor oluşturun
- "💾 Export Results" ile JSON formatında kaydedin

## CLI Kullanımı

### Temel Kullanım

```bash
# Tek URL tarama
python cli.py --url http://target.com --scan-type all

# Belirli tarama türleri
python cli.py --url http://target.com --scan-type sqli,xss

# Batch tarama
python cli.py --batch urls.txt --output report.html
```

### İleri Seçenekler

```bash
# Proxy ile tarama
python cli.py --url http://target.com --proxy http://127.0.0.1:8080

# POST metoduyla tarama
python cli.py --url http://target.com --method POST --scan-type all

# Verbose çıktı ile tarama
python cli.py --url http://target.com -v --output report.html

# JSON formatında rapor
python cli.py --url http://target.com --format json --output report.json
```

### Batch Dosyası Formatı

`urls.txt` dosyasında her URL ayrı satırda:

```
http://target1.com
http://target2.com:8080
http://api.target3.com/login
```

## Payload Yönetimi

### Önceden Yüklenmiş Payloads

- **SQL Injection**: 500+ payload
- **XSS**: 300+ payload
- **SSRF**: 200+ payload
- **CSRF**: 50+ indicator
- **Clickjacking**: 20+ check

### Custom Payload Ekleme

GUI'de "Payloads" sekmesinde:

1. Payload türünü seçin
2. "Add Custom Payload" bölümüne payload yazın
3. "➕ Add Payload" butonuna tıklayın

## Proxy Yapılandırması

### Burp Suite ile Kullanım

```bash
python cli.py --url http://target.com --proxy http://127.0.0.1:8080
```

### OWASP ZAP ile Kullanım

```bash
python cli.py --url http://target.com --proxy http://127.0.0.1:8090
```

## Rapor Formatları

### HTML Rapor

Detaylı, profesyonel HTML rapor:
- Özet İstatistikler
- Açıkların Dağılımı
- Detaylı Bulgular Tablosu
- Öneriler

### JSON Rapor

Program tarafından işlenebilir JSON format:
```json
{
  "url": "http://target.com",
  "timestamp": "2024-01-01T12:00:00",
  "vulnerabilities": [...]
}
```

## Best Practices

1. **Yetki Alın**: Her zaman tarama öncesi yazılı izin alın
2. **Saatler**: Yoğun saatlarda tarama yapmayın
3. **Rate Limiting**: Sunucu tarafından yasaklanmamak için thread sayısını ayarlayın
4. **VPN Kullanın**: Anonim kalın
5. **Sonuçları Saklayın**: Gizlilik için rapor dosyalarını güvenli bir yerde saklayın

## Yasal Uyarı

⚠️ Bu araç **yalnızca** yasal amaçlar için ve **yazılı izin** ile kullanılmalıdır.
Yetkisiz erişim ve saldırı yasalara aykırıdır.
