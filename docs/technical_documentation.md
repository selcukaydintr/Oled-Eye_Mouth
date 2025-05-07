# FACE1 Teknik Dokümantasyonu

## İçindekiler
- [Giriş](#giriş)
- [Mimari Genel Bakış](#mimari-genel-bakış)
- [Modül Açıklamaları](#modül-açıklamaları)
- [Arayüzler ve API'ler](#arayüzler-ve-api-ler)
- [Veri Akışı](#veri-akışı)
- [Yapılandırma Sistemi](#yapılandırma-sistemi)
- [Tema Sistemi](#tema-sistemi)
- [Animasyon Sistemi](#animasyon-sistemi)
- [Ses Tepkimeli İfade Sistemi](#ses-tepkimeli-i̇fade-sistemi)
- [IFrame Entegrasyonu](#iframe-entegrasyonu)
- [Performans Optimizasyonu](#performans-optimizasyonu)
- [Güvenlik Hususları](#güvenlik-hususları)
- [Sorun Giderme](#sorun-giderme)

## Giriş

FACE1, Raspberry Pi 5 tabanlı robotlar için duygu ifadeleri gösterebilen bir yüz eklentisidir. Bu teknik dokümantasyon, sistemin mimari yapısını, bileşenlerini ve çalışma prensiplerini detaylı olarak açıklamaktadır. Bu dokümantasyon, geliştiricilere FACE1 sistemini anlamaları, değiştirmeleri ve genişletmeleri için gerekli teknik bilgileri sağlar.

### Doküman Kapsamı

Bu dokümantasyon aşağıdaki konuları kapsar:
- Mimari tasarım ve sistem bileşenleri
- Kaynak kod organizasyonu
- API ve iletişim protokolleri
- Yapılandırma ve tema sistemleri
- Animasyon ve ses tepkimeli ifade sistemleri
- Performans optimizasyonu ve sorun giderme

### Teknoloji Yığını

FACE1 aşağıdaki teknolojileri kullanmaktadır:
- **Programlama Dilleri**: Python 3.9+
- **Web Teknolojileri**: HTML5, CSS3, JavaScript, WebSockets
- **Donanım Arayüzleri**: I2C, GPIO
- **Web Çerçeveleri**: FastAPI
- **Görüntü İşleme**: Pillow
- **Ses İşleme**: PyAudio, NumPy
- **Veri Formatları**: JSON

## Mimari Genel Bakış

FACE1 mimarisi, modüler bir yaklaşım kullanılarak geliştirilmiştir. Sistem, birbirleriyle iletişim kuran bir dizi alt modülden oluşur. Bu modüler yapı, kodun bakımını kolaylaştırır ve belirli bileşenlerin bağımsız olarak geliştirilmesine ve test edilmesine olanak tanır.

### Sistem Mimarisi

```
                ┌─────────────────┐
                │   FacePlugin    │
                │  (Ana Kontrolcü)│
                └─────────────────┘
                        │
          ┌─────────────┼─────────────────┐
          │             │                 │
┌─────────▼────────┐ ┌──▼─────────────┐ ┌─▼────────────────┐
│  OLEDController  │ │  EmotionEngine  │ │  LEDController  │
│ (Göz/Ağız Ekran) │ │ (Duygu Motoru)  │ │  (LED Kontrol)  │
└─────────┬────────┘ └──┬─────────────┘ └─┬────────────────┘
          │             │                 │
┌─────────▼────────┐ ┌──▼─────────────┐ ┌─▼────────────────┐
│ ThemeManager     │ │AnimationEngine │ │ SoundProcessor   │
│ (Tema Yönetimi)  │ │(Animasyonlar)  │ │ (Ses İşleme)     │
└─────────┬────────┘ └──┬─────────────┘ └─┬────────────────┘
          │             │                 │
          └─────────────▼─────────────────┘
                        │
              ┌─────────▼────────┐
              │ DashboardServer  │
              │ (Web Arayüzü)    │
              └─────────┬────────┘
                        │
                ┌───────▼───────┐
                │  WebSockets   │
                │    REST API   │
                └───────┬───────┘
                        │
                ┌───────▼───────┐
                │Üst Proje      │
                │Entegrasyonu   │
                └───────────────┘
```

### Modül Organizasyonu

FACE1, işlevselliğe göre düzenlenen çeşitli modüllerden oluşur:

1. **Ana Kontrolcü (FacePlugin)**: Tüm modülleri bir arada tutar ve yaşam döngüsünü yönetir.
2. **OLED Kontrolcü**: Göz ve ağız ekranlarını yönetir.
3. **Duygu Motoru**: Duygu durumlarını ve geçişlerini yönetir.
4. **LED Kontrolcü**: LED şeritleri üzerinden ışık efektlerini kontrol eder.
5. **Tema Yöneticisi**: Görsel temalara ait kaynakları yönetir.
6. **Animasyon Motoru**: Senkronize animasyonları çalıştırır.
7. **I/O Yöneticisi**: Harici iletişim protokollerini yönetir.
8. **Dashboard Sunucusu**: Web tabanlı yönetim arayüzünü sağlar.
9. **Ses İşleme Modülü**: Ses tepkimeli ifadeler için sesi analiz eder.
10. **Plugin Altyapısı**: Üst projeyle entegrasyon için yaşam döngüsü ve konfigürasyon yönetimini sağlar.
11. **IFrame Bridge**: Üst projeyle GUI entegrasyonu sağlar.

### Bağımlılık Yönetimi

FACE1, modüller arasında bağımlılıkları yönetmek için çeşitli tasarım desenleri kullanır:

- **Mixin Sınıfları**: İşlevselliği parçalara ayırmak ve kod tekrarını önlemek için
- **Bağımlılık Enjeksiyonu**: Modüller arasındaki bağımlılıkları yönetmek ve test edilebilirliği artırmak için
- **Observer Pattern**: Durum değişikliklerini izlemek ve bildirmek için
- **Factory Pattern**: Nesnelerin oluşturulmasını standartlaştırmak için

## Modül Açıklamaları

### Ana Kontrolcü (FacePlugin)

Ana kontrolcü, FACE1 sisteminin merkezi bileşenidir. Diğer tüm modülleri başlatır, yapılandırır ve yönetir. Yaşam döngüsü yönetimi, hata işleme ve modüller arası koordinasyon sağlar.

#### Sınıf Hiyerarşisi

Ana kontrolcü aşağıdaki mixin sınıflarından oluşur:

```
FacePlugin
├── FacePluginBase
├── FacePluginCallbacks
├── FacePluginSystem
├── FacePluginAPI
├── FacePluginConfigMixin
├── FacePluginMetricsMixin
└── FacePluginEnvironmentMixin
```

#### Yaşam Döngüsü Durumları

FacePlugin aşağıdaki durum geçişlerini destekler:

1. `UNINITIALIZED`: Başlangıç durumu
2. `INITIALIZING`: Başlatma işlemi devam ediyor
3. `INITIALIZED`: Başlatma tamamlandı
4. `STARTING`: Başlama işlemi devam ediyor
5. `RUNNING`: Normal çalışma durumu
6. `PAUSED`: Geçici olarak duraklatıldı
7. `MAINTENANCE`: Bakım modu
8. `STOPPING`: Durdurma işlemi devam ediyor
9. `STOPPED`: Tamamen durdurulmuş
10. `ERROR`: Hata durumu
11. `RECOVERING`: Hata durumundan kurtarılıyor
12. `SHUTDOWN`: Tamamen kapatıldı

### OLED Kontrolcü

OLED kontrolcü, göz ve ağız ekranlarını yöneten modüldür. Bu ekranlar üzerinde duygu ifadelerini görselleştirme, animasyonları çalıştırma ve özel efektleri gösterme işlevselliği sağlar.

#### Temel Sınıflar

```
OLEDController
├── OLEDControllerBase
├── OLEDDisplayMixin
└── OLEDAnimationsMixin
```

#### İşlevsellik

- SSD1306 OLED ekranların I2C üzerinden kontrolü
- Piksel bazlı görüntü oluşturma ve manipülasyon
- Tema tabanlı görsel ifade desteği
- Animasyon sıralarının işlenmesi
- Mikro ifadeler ve göz takibi özellikleri
- Çevresel faktörlere göre tepki verme

### Duygu Motoru (EmotionEngine)

Duygu motoru, robotun duygusal durumunu belirleyen ve yöneten bileşendir. Duygu geçişleri, duygu hafızası ve ifade yönetimi sağlar.

#### Temel Sınıflar

```
EmotionEngine
├── EmotionEngineBase
├── EmotionExpressionsMixin
├── EmotionTransitionsMixin
└── EmotionMemoryMixin
```

#### Desteklenen Duygular

Duygu motoru aşağıdaki temel duyguları destekler:
- NEUTRAL: Nötr ifade
- HAPPY: Mutlu ifade
- SAD: Üzgün ifade
- ANGRY: Kızgın ifade
- SURPRISED: Şaşkın ifade
- SCARED: Korkmuş ifade
- DISGUSTED: Tiksinmiş ifade
- SLEEPY: Uykulu ifade

Her duygu için farklı yoğunluk seviyeleri (0.0-1.0) ve alt tipler desteklenir. Örneğin, HAPPY duygusu için "excited", "content", "amused" gibi alt tipler mevcuttur.

#### Duygu Geçişleri

Duygu geçişleri, bir duygudan diğerine doğal ve kademeli geçişler sağlar. Bu geçişler, belirli bir süre boyunca iki duygunun karıştırılmasıyla gerçekleştirilir.

## Arayüzler ve API'ler

FACE1, dış sistemlerle iletişim kurmak ve sistem durumunu kontrol etmek için çeşitli arayüzler sunar.

### REST API

FACE1, HTTP üzerinden bir REST API sağlar. Bu API, duygu durumları, tema yönetimi, yapılandırma ve yaşam döngüsü yönetimi için endpoint'ler içerir.

#### Temel Endpoint'ler

- `GET /status`: Sistemin durumunu döndürür
- `POST /emotion/{emotion}`: Belirtilen duyguyu ayarlar
- `POST /theme/{theme_name}`: Belirtilen temayı etkinleştirir

Detaylı API dokümantasyonu için [API Referansı](api_reference.md) belgesine bakın.

### WebSocket Arayüzü

Gerçek zamanlı güncellemeler için WebSocket arayüzü sağlanır. Bu arayüz, duygu durumu değişiklikleri, tema güncellemeleri ve sistem olayları gibi bildirimler gönderir.

#### WebSocket Olayları

- `emotion_update`: Duygu durumu değişikliklerini bildirir
- `theme_change`: Tema değişikliklerini bildirir
- `animation_update`: Animasyon durumu değişikliklerini bildirir
- `system_stats`: Sistem istatistiklerini bildirir

### IFrame Entegrasyonu

FACE1, üst projelere entegre edilmek için bir IFrame köprüsü sağlar. Bu köprü, postMessage API'si üzerinden iki yönlü iletişim sağlar.

#### IFrame Mesaj Protokolü

IFrame üzerinden gönderilen mesajlar şu formata sahiptir:

```json
{
  "type": "FACE1_COMMAND_TYPE",
  "data": {
    // Komut verileri
  },
  "timestamp": 1714806420000
}
```

Desteklenen komut tipleri:
- `FACE1_SET_EMOTION`: Duygu durumunu ayarlar
- `FACE1_PLAY_ANIMATION`: Animasyon oynatır
- `FACE1_SET_THEME`: Temayı değiştirir

## Veri Akışı

FACE1 içindeki veri akışı, modüller arasındaki etkileşimler ve olayların nasıl işlendiğiyle ilgilidir.

### Duygu Durumu Akışı

Duygu durumu değişikliği şu şekilde gerçekleşir:

1. Duygu değişikliği talep edilir (API, WebSocket, animasyon veya ses tepkisi)
2. EmotionEngine duygu durumunu günceller
3. EmotionEngine duygu değişikliği olayını tetikler
4. Olay dinleyicileri (OLED, LED, Web arayüzü) bu değişikliğe tepki verir
5. Görsel ifadeler güncellenir

### Ses Tepki Akışı

Ses tepkimeli ifade sistemi şu şekilde çalışır:

1. SoundProcessor mikrofon verilerini toplar
2. Ses seviyesi ve konuşma durumu analiz edilir
3. Analiz sonuçları yayınlanır
4. OLED Kontrolcü ağız animasyonlarını günceller
5. EmotionEngine uygun duygu önerilerini değerlendirir

## Yapılandırma Sistemi

FACE1, davranışını ve özelliklerini özelleştirmek için kapsamlı bir yapılandırma sistemi kullanır.

### Yapılandırma Dosyası Formatı

Yapılandırma, config.json dosyasında JSON formatında saklanır:

```json
{
  "system": {
    "log_level": "INFO",
    "watchdog_enabled": true,
    "watchdog_timeout": 10
  },
  "oled": {
    "brightness": 128,
    "power_save": true,
    "power_save_timeout": 300,
    "random_eye_movement": true,
    "blink_frequency": 4.5
  },
  "leds": {
    "brightness": 128,
    "enabled": true,
    "animate_emotions": true
  },
  "emotions": {
    "default_emotion": "neutral",
    "emotion_decay_time": 300,
    "micro_expressions_enabled": true,
    "personality_profile": "balanced"
  },
  "animation": {
    "startup_animation_enabled": true,
    "fps": 30
  }
}
```

### Donanım Profilleri

Farklı donanım yapılandırmaları için donanım profilleri sağlanır:
- `rpi5.json`: Raspberry Pi 5 için optimize edilmiş ayarlar
- `rpi4.json`: Raspberry Pi 4 için optimize edilmiş ayarlar
- `custom_hw.json`: Özelleştirilmiş donanım için ayarlar

## Tema Sistemi

Tema sistemi, FACE1'in görsel stilini özelleştirmeyi sağlar. Her tema, göz ve ağız ifadeleri için bir dizi görsel kaynak içerir.

### Tema Yapısı

Her tema aşağıdaki yapıya sahiptir:

```
themes/
└── theme_name/
    ├── theme.json       # Tema tanımı
    ├── eyes/            # Göz ifadeleri
    │   ├── neutral.png
    │   ├── happy.png
    │   └── ...
    └── mouth/           # Ağız ifadeleri
        ├── neutral.png
        ├── smile.png
        └── ...
```

### Tema Tanımı

Tema tanımı, `theme.json` dosyasında saklanır:

```json
{
  "name": "theme_name",
  "display_name": "Görünen Ad",
  "description": "Tema açıklaması",
  "author": "Tema yaratıcısı",
  "version": "1.0.0",
  "emotion_mappings": {
    "happy": {
      "eyes": "happy.png",
      "mouth": "smile.png",
      "led_color": [0, 255, 0]
    },
    "sad": {
      "eyes": "sad.png",
      "mouth": "frown.png",
      "led_color": [0, 0, 255]
    }
  }
}
```

## Animasyon Sistemi

Animasyon sistemi, FACE1'e dinamik ve senkronize göz, ağız ve LED animasyonları sağlar.

### Animasyon Formatı

Animasyonlar, JSON formatında tanımlanır:

```json
{
  "metadata": {
    "name": "animation_name",
    "display_name": "Görünen Ad",
    "description": "Animasyon açıklaması",
    "duration": 5.0,
    "version": "1.0.0",
    "author": "Animasyon yaratıcısı"
  },
  "sequence": [
    {
      "time": 0.0,
      "eyes": {
        "action": "clear",
        "params": {}
      }
    },
    {
      "time": 1.0,
      "mouth": {
        "action": "smile",
        "params": {
          "width": 0.8,
          "height": 0.6
        }
      }
    }
  ]
}
```

### Animasyon Motoru

AnimationEngine sınıfı, animasyon sekanslarını yükler, çalıştırır ve yönetir. Zamanlayıcı tabanlı bir sistem kullanarak belirtilen zamanlarda eylemleri gerçekleştirir.

## Ses Tepkimeli İfade Sistemi

Ses tepkimeli ifade sistemi, mikrofon aracılığıyla ortam sesini analiz ederek robot yüzünün gerçek zamanlı tepkiler vermesini sağlar.

### Ana Bileşenler

- **Ses İşleme**: Mikrofon verisini elde etme ve işleme
- **Ses Analizi**: Ses seviyesi ve konuşma durumu tespiti
- **Reaktif Gösterge**: Ses seviyesiyle senkronize ağız animasyonları
- **Duygu Önerileri**: Ses karakteristiğine göre duygu durumu önerileri

### İşlem Akışı

1. Mikrofon verisini sürekli olarak örnekleme
2. RMS (Root Mean Square) değeri hesaplayarak ses seviyesi analizi
3. Ses seviyesi eşik değerine göre konuşma durumu tespiti
4. Ağız animasyonlarını ses seviyesiyle senkronize etme
5. Üst projeye WebSocket üzerinden ses analiz sonuçlarını iletme

### Yapılandırma

Ses tepkimeli ifade sistemi aşağıdaki parametrelerle yapılandırılabilir:

```json
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
```

## Performans Optimizasyonu

FACE1, sınırlı kaynaklara sahip Raspberry Pi platformlarında verimli çalışmak için çeşitli performans optimizasyon teknikleri kullanır.

### Bellek Optimizasyonu

- **LRU Önbelleği**: Tema varlıkları için Least Recently Used (LRU) algoritması
- **Referans İşaretleme**: Gereksiz kopya işlemlerini önlemek için referans paylaşımı
- **Kaynak Temizliği**: Kullanılmayan kaynakların zamanında temizlenmesi
- **Piksel İşleme Optimizasyonu**: Bitmap önbelleği ve kısmen güncelleme mekanizmaları

### CPU Optimizasyonu

- **İşleme Planlaması**: FPS sınırlaması ve öncelikli işleme sırası
- **Animasyon Adım Optimizasyonu**: En az 50-100ms adım aralıkları
- **Koşullu Yürütme**: Sadece gerektiğinde kod blokları çalıştırılır
- **Önbellekleme**: Sık kullanılan hesaplamalar için önbellekleme

### Benchmark Sonuçları

Farklı donanımlarda yapılan performans test sonuçları:

| Donanım | Ortalama FPS | Bellek Kullanımı | CPU Kullanımı (Boşta) | CPU Kullanımı (Animasyon) |
|---------|-------------:|----------------:|---------------------:|-------------------------:|
| Raspberry Pi 5 (8GB) | 45-60 | 28MB | %2-3 | %10-15 |
| Raspberry Pi 4 (4GB) | 35-45 | 30MB | %3-4 | %15-20 |
| Raspberry Pi 3B+ | 25-30 | 32MB | %5-6 | %20-30 |

## Güvenlik Hususları

FACE1 sistemi, güvenlikle ilgili çeşitli hususları ele alır:

### API Güvenliği

- **Kaynak Sınırlandırma**: API istekleri için hız sınırlaması
- **İsteğe Bağlı API Anahtarı Doğrulaması**: Yapılandırılabilir API anahtarı kontrolü
- **İzin Kontrolleri**: Belirli API operasyonları için yetkilendirme kontrolleri

### IFrame Güvenliği

- **Origin Kontrolü**: IFrame mesajları için origin doğrulaması
- **Geçerli Komut Doğrulaması**: Yalnızca tanımlı komutların işlenmesi
- **Cross-Origin İzinleri**: Güvenli cross-origin iletişim için CORS yapılandırması

### Genel Güvenlik Önlemleri

- **Kaynak İzolasyonu**: Plugin izolasyon katmanı ile sistem kaynaklarının korunması
- **Doğru Hata İşleme**: Hassas bilgileri açığa çıkarmayan güvenli hata mesajları
- **Günlük Dosyası Güvenliği**: Hassas bilgilerin günlük dosyalarından filtrelenmesi

## Sorun Giderme

Bu bölüm, FACE1 sisteminde karşılaşılabilecek yaygın sorunları ve çözümlerini açıklar.

### Yaygın Sorunlar ve Çözümleri

#### OLED Ekran Sorunları

- **Ekran Görüntülenmiyor**
  - I2C bağlantılarını kontrol edin
  - I2C adreslerini doğrulayın (`i2cdetect -y 1` komutunu kullanarak)
  - Güç kaynağını kontrol edin

- **Karışık veya Eksik Görüntüler**
  - Tema dosyalarının doğru yapılandırıldığını kontrol edin
  - Simülasyon klasöründeki çıktıları inceleyerek görsellerin doğru oluşturulduğunu doğrulayın

#### LED Kontrol Sorunları

- **LED'ler Yanmıyor**
  - GPIO pin yapılandırmasını kontrol edin
  - LED şeridinin güç kaynağını kontrol edin
  - config.json içinde `leds.enabled` ayarını kontrol edin

#### Web Arayüzü Sorunları

- **Dashboard Erişilemiyor**
  - Sunucunun çalıştığını kontrol edin (`ps aux | grep dashboard` ile)
  - Bağlantı noktasının (port) başka bir uygulama tarafından kullanılmadığını doğrulayın
  - Güvenlik duvarı ayarlarını kontrol edin

### Tanılama Araçları

FACE1, sorun tespiti için çeşitli tanılama araçları sağlar:

- **Test Sürücüleri**: Her bir bileşeni ayrı ayrı test eden test_drivers.py betiği
- **Durum Raporlama**: API aracılığıyla erişilebilen sistem durum raporu
- **Günlük Dosyaları**: logs/ klasöründe bulunan detaylı günlük kayıtları

#### Tanılama Komutları

```bash
# Platform testi
python test_drivers.py --platform

# I2C testi
python test_drivers.py --i2c

# OLED kontrolcü testi
python test_drivers.py --oled

# LED kontrolcü testi
python test_drivers.py --led

# Ses işleme testi
python test_drivers.py --sound
```

### Günlük Dosyaları

Günlük dosyaları `/logs` dizininde bulunur:
- `face_plugin.log`: Ana günlük dosyası
- `errors.log`: Yalnızca hata mesajları
- `performance.log`: Performans metrikleri

### İletişim ve Destek

Sorunlar ve destek için şu kaynaklara başvurabilirsiniz:
- GitHub üzerinden issue açma: [issues](https://github.com/kullaniciadi/face1/issues)
- Proje dokümantasyonunu inceleme
- Test araçlarını kullanma

---

Bu dokümantasyon, FACE1 sisteminin teknik detaylarını kapsar. Belirli bileşenler hakkında daha fazla bilgi için ilgili dokümantasyon dosyalarına başvurun:
- [API Referansı](api_reference.md)
- [Animasyon Sistemi](animation_system.md)
- [Ses İşleme Sistemi](sound_processor.md)
- [IFrame Entegrasyonu](iframe_bridge_integration.md)