# FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi

![Version](https://img.shields.io/badge/version-0.5.0-blue.svg)
![Status](https://img.shields.io/badge/status-development-orange)

FACE1, Raspberry Pi 5 tabanlı robotlar için duygu ifadeleri gösterebilen bir yüz eklentisidir. Bu sistem, 3 adet OLED SSD1306 ekran (sol göz, sağ göz ve ağız) kullanarak robotun duygu ifadelerini sergiler ve WS2812 LED şeritler ile senkronize ışık efektleri üretir.

## Özellikler

- 7 temel duygu ve çeşitli alt tipleri
- Duygu yoğunluğuna göre otomatik ifade ayarlaması
- Mikro-ifadeler sistemi ve göz takibi
- Temaya dayalı görsel ifadeler ve renkler
- Web tabanlı kontrol paneli ve API
- WebSocket ve REST API ile uzaktan kontrol
- Gerçek zamanlı animasyonlar ve geçişler
- Simülasyon modu ve fiziksel donanım desteği
- **Ses tepkimeli ifade sistemi (v0.5.0 ile eklendi)**
  - Ses seviyesi algılama ve görselleştirme
  - Konuşma durumu tespit etme ve ağız animasyonları
  - Ses karakteristiğine göre duygu önerileri
  - Gerçek zamanlı dashboard izleme

## Kurulum

### Gereksinimler

- Raspberry Pi 5 (veya uyumlu bir bilgisayar)
- 3 adet SSD1306 OLED ekran (128x64, monokrom)
- WS2812B LED şeritleri
- TCA9548A I2C çoğaltıcı (çoklu ekran yönetimi için)
- USB mikrofon veya 3.5mm jak mikrofon (ses tepkimeli sistem için)
- Python 3.9+
- Git

### Bağımlılıklar

- Pillow
- Adafruit SSD1306
- Adafruit GPIO
- FastAPI
- websockets
- paho-mqtt (opsiyonel)
- RPi.GPIO (sadece Raspberry Pi üzerinde)
- PyAudio (ses tepkimeli sistem için)
- NumPy (ses analizi için)

### Kurulum Adımları

1. Projeyi klonlayın:
   ```bash
   git clone https://github.com/kullaniciadi/face1.git
   cd face1
   ```

2. Sanal ortamı oluşturun ve bağımlılıkları yükleyin:
   ```bash
   python create_venv.py
   source venv/bin/activate
   ```

3. PyAudio kurulumu (ses tepkimeli sistem için):
   ```bash
   # Debian/Ubuntu/Raspberry Pi OS
   sudo apt-get install python3-pyaudio
   
   # Sanal ortama pip ile kurulum
   pip install pyaudio
   ```

4. Yapılandırmayı özelleştirin:
   ```bash
   cp config/default_config.json config/user_config.json
   # user_config.json dosyasını ihtiyaçlarınıza göre düzenleyin
   ```

5. Çalıştırın:
   ```bash
   ./run_face.sh
   ```
   veya
   ```bash
   python src/face_plugin.py
   ```

## Kullanım

### Temel Kullanım

Sistemin çalışmasını başlatmak için terminalde aşağıdaki komutu çalıştırın:

```bash
./run_face.sh
```

Bu komut, tüm modülleri başlatır, WebSocket sunucusunu ve Dashboard sunucusunu aktifleştirir.

### Dashboard Arayüzü

Web tarayıcınızda `http://localhost:8000` adresini açarak kontrol paneline erişebilirsiniz. Bu panel şu özellikleri sağlar:

- Duygu durumunu değiştirme
- Duygu yoğunluğunu ayarlama
- Tema seçimi ve özelleştirme
- Sistem durumu izleme
- Simülasyon görüntüleme
- Ses seviyesi ve konuşma durumu izleme (v0.5.0+)

### Simülasyon Modu

Fiziksel donanım olmadan geliştirme yaparken simülasyon modunu etkinleştirebilirsiniz:

1. `config.json` içinde `"simulation_mode": true` ayarını yapın
2. Uygulamayı başlatın
3. Simülasyon çıktıları `/simulation/` klasöründe PNG dosyaları olarak görüntülenecektir
4. Dashboard'da simülasyon görüntülerini canlı olarak izleyebilirsiniz

### API Kullanımı

REST API üzerinden kontrol:

```bash
# Duygu durumunu ayarlamak için
curl -X POST http://localhost:8000/api/emotion -H "Content-Type: application/json" -d '{"emotion": "happy", "intensity": 80}'

# Tema değiştirmek için
curl -X POST http://localhost:8000/api/theme -H "Content-Type: application/json" -d '{"theme_name": "pixel"}'

# Ses işleme durumu almak için (v0.5.0+)
curl -X GET http://localhost:8000/api/sound/status
```

WebSocket üzerinden kontrol:

```javascript
const ws = new WebSocket('ws://localhost:8765');

// Duygu durumunu ayarlamak için
ws.send(JSON.stringify({
  type: 'command',
  command: 'setEmotion',
  data: {
    emotion: 'happy',
    intensity: 80
  }
}));

// Tema değiştirmek için
ws.send(JSON.stringify({
  type: 'command',
  command: 'setTheme',
  data: {
    theme_name: 'pixel'
  }
}));

// Ses tepkimeli ifade sistemini etkinleştirmek/devre dışı bırakmak için (v0.5.0+)
ws.send(JSON.stringify({
  type: 'command',
  command: 'setSoundProcessing',
  data: {
    enabled: true
  }
}));

// WebSocket'ten ses verilerini almak için dinleyici (v0.5.0+)
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'volume_update') {
    console.log(`Ses Seviyesi: ${data.volume_level}`);
    console.log(`Konuşma Durumu: ${data.is_speaking ? 'Konuşuyor' : 'Sessiz'}`);
  }
};
```

## Modüller

FACE1 projesi aşağıdaki ana modüllerden oluşur:

| Modül | Dosya | Açıklama |
|-------|-------|----------|
| Ana Kontrolcü | `face_plugin.py` | Tüm modülleri yönetir ve entegre eder |
| OLED Kontrolcü | `modules/oled_controller.py` | Göz ve ağız ekranlarını kontrol eder |
| Duygu Motoru | `modules/emotion_engine.py` | Duygu algoritmaları ve geçişleri yönetir |
| LED Kontrolcü | `modules/led_controller.py` | LED şeritlerini ve renk animasyonlarını kontrol eder |
| Tema Yöneticisi | `modules/theme_manager.py` | Görsel temaları yönetir |
| I/O Yöneticisi | `modules/io_manager.py` | Harici iletişim protokollerini yönetir |
| Dashboard Server | `modules/dashboard_server.py` | Web tabanlı arayüz sunar |
| Ses İşleme | `modules/sound_processor.py` | Ses seviyesi analizi ve konuşma tespiti yapar (v0.5.0+) |
| Animasyon Motoru | `modules/animation_engine.py` | Animasyon sekanslarını yönetir |

## Ses Tepkimeli İfade Sistemi

### Genel Bakış (v0.5.0)

Ses tepkimeli ifade sistemi, mikrofon aracılığıyla ortam sesini analiz ederek robot yüzünün daha doğal ve etkileşimli bir şekilde tepki vermesini sağlar. Bu sistem şunları yapabilir:

- Ortam ses seviyesini gerçek zamanlı olarak ölçer ve normalize eder
- Konuşma desenleri ile sessizlik arasında ayrım yapar
- Ses seviyesiyle ağız hareketlerini senkronize eder
- Ses karakteristiğine göre duygusal tepkiler üretir
- Dashboard üzerinden gerçek zamanlı ses verileri sunar

### Yapılandırma

`config.json` dosyasında ses tepkimeli ifade sistemi için aşağıdaki ayarları özelleştirebilirsiniz:

```json
{
  "sound_processor": {
    "enabled": true,
    "sample_rate": 16000,
    "chunk_size": 1024,
    "device_index": null,
    "volume_sensitivity": 2.0,
    "speech_threshold": 0.15,
    "silence_duration": 0.5,
    "simulation_mode": false,
    "update_interval_ms": 50
  }
}
```

### Kullanım

Ses tepkimeli ifade sistemi hakkında daha fazla bilgi için şu dokümanlara bakın:
- `docs/sound_processor.md`: Ayrıntılı teknik dokümantasyon
- `docs/changes.md`: v0.5.0 sürümüyle ilgili tüm değişiklikler

## Özelleştirme

### Tema Oluşturma

Yeni bir tema oluşturmak için:

1. `themes/` dizininde yeni bir klasör oluşturun
2. Bu klasörde `theme.json` dosyası oluşturun
3. Göz ve ağız ifadeleri için gerekli resim dosyalarını ekleyin
4. Dashboard veya API üzerinden yeni temayı seçin

### Animasyon Oluşturma

Yeni animasyonları `animation/custom/` klasöründe JSON formatında oluşturabilirsiniz. Ses tepkimeli animasyonlar için konuşma ve ses seviyesine tepki veren özel adımlar ekleyebilirsiniz.

## Test Etme

Farklı bileşenleri test etmek için:

```bash
python test_drivers.py --platform  # Platform testleri
python test_drivers.py --i2c       # I2C testleri
python test_drivers.py --led       # LED kontrolcü testleri
python test_drivers.py --oled      # OLED kontrolcü testleri
python test_drivers.py --theme     # Tema yöneticisi testleri
python test_drivers.py --io        # I/O yöneticisi testleri
python test_drivers.py --dashboard # Dashboard sunucusu testleri
python test_drivers.py --sound     # Ses işleme testleri (v0.5.0+)
```

## Geliştirme

Geliştirme süreciniz için aşağıdaki adımları takip edin:

1. Sanal ortamı aktifleştirin: `source venv/bin/activate`
2. İlgili modülü düzenleyin
3. Değişiklik yapmadan önce `docs/changes.md` dosyasını güncelleyin
4. Yeni işlevsellikler eklerken `docs/function_list.md` dosyasını güncelleyin
5. Dokümantasyonu güncel tutun
6. Değişiklikleri test edin

## Proje Yapısı

```
face1/
├── docs/                    # Dokümantasyon dosyaları
│   ├── sound_processor.md   # Ses tepkimeli sistem dokümantasyonu (v0.5.0+)
│   └── changes.md           # Değişiklik kaydı
├── src/                     # Kaynak kodlar
│   ├── face_plugin.py       # Ana kontrol sınıfı
│   └── modules/             # Alt modüller
│       └── sound_processor.py # Ses işleme modülü (v0.5.0+)
├── config/                  # Yapılandırma dosyaları
├── themes/                  # Tema dosyaları
├── animation/               # Animasyon sekansları
│   ├── standard/            # Standart animasyonlar
│   │   └── speaking.json    # Konuşma animasyonu
│   └── custom/              # Özel animasyonlar
├── utils/                   # Yardımcı araçlar
├── web/                     # Web arayüzü dosyaları
├── simulation/              # Simülasyon çıktıları
├── create_venv.py           # Sanal ortam oluşturma scripti
└── run_face.sh              # Çalıştırma scripti
```

## Lisans

Bu proje açık kaynak olarak kullanılabilir. Tüm hakları saklıdır.

## İletişim

Sorularınız veya önerileriniz için lütfen [issue açın](https://github.com/kullaniciadi/face1/issues) veya doğrudan iletişime geçin.