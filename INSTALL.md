# WebGuvenligi - Kurulum Kılavuzu

## Sistem Gereksinimleri

- Python 3.8+
- pip (Python Package Manager)
- Git
- Internet bağlantısı

## Kurulum Adımları

### 1. Repository'yi Klonlayın

```bash
git clone https://github.com/st-webguvenligi/WebGuvenligi.git
cd WebGuvenligi
```

### 2. Virtual Environment Oluşturun (Önerilen)

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Bağımlılıkları Yükleyin

```bash
pip install -r requirements.txt
```

### 4. GUI Modunu Başlatın

```bash
python main.py
```

veya CLI Modunu Kullanın:

```bash
python cli.py --url http://target.com --scan-type all
```

## Docker ile Kurulum

```bash
docker build -t webguvenligi .
docker run -it webguvenligi python main.py
```

## Sorun Giderme

### PyQt6 Hatası
Eğer `ModuleNotFoundError: No module named 'PyQt6'` alıyorsanız:

```bash
pip install --upgrade PyQt6
```

### SSL Sertifikası Hatası
Eğer SSL sertifikası ile ilgili sorun yaşıyorsanız:

```bash
pip install --upgrade certifi
```

## Lisans

MIT License

## Destek

Herhangi bir sorun için GitHub Issues sayfasını ziyaret edin.
