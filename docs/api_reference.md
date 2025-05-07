# FACE1 API Referans Kılavuzu

## İçindekiler

- [Genel Bakış](#genel-bakış)
- [REST API](#rest-api)
  - [Durum Endpoint'leri](#durum-endpointleri)
  - [Duygu Kontrol Endpoint'leri](#duygu-kontrol-endpointleri)
  - [Tema Kontrol Endpoint'leri](#tema-kontrol-endpointleri)
  - [Animasyon Kontrol Endpoint'leri](#animasyon-kontrol-endpointleri)
  - [Yapılandırma Endpoint'leri](#yapılandırma-endpointleri)
  - [Ses İşleme Endpoint'leri](#ses-i̇şleme-endpointleri)
  - [Simülasyon Endpoint'leri](#simülasyon-endpointleri)
- [WebSocket API](#websocket-api)
  - [Mesaj Formatı](#mesaj-formatı)
  - [Client-Server Mesajları](#client-server-mesajları)
  - [Server-Client Mesajları](#server-client-mesajları)
  - [Hata İşleme](#hata-i̇şleme)
- [Python API](#python-api)
  - [FacePlugin Sınıfı](#faceplugin-sınıfı)
  - [EmotionEngine Sınıfı](#emotionengine-sınıfı)
  - [OLEDController Sınıfı](#oledcontroller-sınıfı)
  - [AnimationEngine Sınıfı](#animationengine-sınıfı)
  - [SoundProcessor Sınıfı](#soundprocessor-sınıfı)
- [Veri Tipleri ve Enum'lar](#veri-tipleri-ve-enumlar)
- [Örnekler](#örnekler)

## Genel Bakış

FACE1 API'si, dış sistemlerin FACE1 ile etkileşimde bulunmasına olanak tanır. API şu üç şekilde kullanılabilir:

1. **REST API**: HTTP üzerinden standart RESTful API çağrıları
2. **WebSocket API**: Gerçek zamanlı, çift yönlü iletişim için
3. **Python API**: FACE1'i modül olarak kullanan Python uygulamaları için

API'ler şu ana işlevleri destekler:
- Durum sorgulama ve yönetimi
- Duygu durumlarını ayarlama ve sorgulama
- Temaları kontrol etme
- Animasyonları oynatma ve durdurma
- Yapılandırma parametrelerini sorgulama ve değiştirme
- Ses işleme özelliklerini kontrol etme
- Simülasyon modu yönetimi

## REST API

REST API, HTTP üzerinden JSON formatında veri alışverişi yapan standart bir arayüzdür. Varsayılan olarak `http://localhost:8000` adresinde çalışır.

### Durum Endpoint'leri

#### Sistem Durumunu Alma

```
GET /status
```

**Yanıt:**

```json
{
  "status": "running",
  "version": "0.5.0",
  "uptime": 3650,
  "current_emotion": {
    "name": "happy",
    "intensity": 0.8,
    "source": "api"
  },
  "current_theme": "default",
  "active_animation": null,
  "is_speaking": false
}
```

#### Durum Ayarlama

```
POST /status
```

**İstek Gövdesi:**

```json
{
  "action": "pause" | "resume" | "restart" | "shutdown"
}
```

**Yanıt:**

```json
{
  "success": true,
  "message": "System paused successfully",
  "status": "paused"
}
```

### Duygu Kontrol Endpoint'leri

#### Duygu Durumu Ayarlama

```
POST /emotion/{emotion}
```

**URL Parametreleri:**

- `{emotion}`: Ayarlanacak duygu (örn. "happy", "sad", "angry", vb.)

**İstek Parametreleri:**

- `intensity` (opsiyonel): Duygu yoğunluğu (0.0-1.0 arası, varsayılan: 1.0)
- `duration` (opsiyonel): Geçerlilik süresi (saniye, null = kalıcı)
- `subtype` (opsiyonel): Duygunun alt tipi (örn. "excited" for "happy")

**Yanıt:**

```json
{
  "success": true,
  "emotion": "happy",
  "intensity": 0.8,
  "previous_emotion": "neutral"
}
```

#### Duygular Arası Yumuşak Geçiş

```
POST /transition/{emotion}
```

**URL Parametreleri:**

- `{emotion}`: Hedef duygu

**İstek Parametreleri:**

- `intensity` (opsiyonel): Hedef duygu yoğunluğu (0.0-1.0 arası)
- `duration` (opsiyonel): Geçiş süresi (saniye, varsayılan: 1.0)

**Yanıt:**

```json
{
  "success": true,
  "from_emotion": "neutral",
  "to_emotion": "happy",
  "transition_duration": 1.5
}
```

#### Mevcut Duyguyu Alma

```
GET /emotion
```

**Yanıt:**

```json
{
  "name": "happy",
  "intensity": 0.8,
  "source": "api",
  "timestamp": 1714806420,
  "duration": null
}
```

#### Tüm Desteklenen Duyguları Alma

```
GET /emotions
```

**Yanıt:**

```json
{
  "emotions": [
    {
      "name": "neutral",
      "display_name": "Nötr",
      "subtypes": []
    },
    {
      "name": "happy",
      "display_name": "Mutlu",
      "subtypes": ["excited", "content", "amused", "proud", "loving"]
    },
    {
      "name": "sad",
      "display_name": "Üzgün",
      "subtypes": ["disappointed", "lonely", "guilty"]
    }
    // ... diğer duygular
  ]
}
```

### Tema Kontrol Endpoint'leri

#### Tema Ayarlama

```
POST /theme/{theme_name}
```

**URL Parametreleri:**

- `{theme_name}`: Etkinleştirilecek tema adı

**Yanıt:**

```json
{
  "success": true,
  "theme": "pixel",
  "previous_theme": "default"
}
```

#### Mevcut Temayı Alma

```
GET /theme
```

**Yanıt:**

```json
{
  "name": "pixel",
  "display_name": "Pixel Art",
  "author": "FACE1 Team",
  "version": "1.0.0"
}
```

#### Kullanılabilir Temaları Listeleme

```
GET /themes
```

**Yanıt:**

```json
{
  "themes": [
    {
      "name": "default",
      "display_name": "Default Theme",
      "author": "FACE1 Team",
      "version": "1.0.0"
    },
    {
      "name": "pixel",
      "display_name": "Pixel Art",
      "author": "FACE1 Team",
      "version": "1.0.0"
    },
    {
      "name": "minimal",
      "display_name": "Minimal",
      "author": "FACE1 Team",
      "version": "1.0.0"
    }
  ],
  "current_theme": "pixel"
}
```

### Animasyon Kontrol Endpoint'leri

#### Animasyon Oynatma

```
POST /api/animations/{animation_name}/play
```

**URL Parametreleri:**

- `{animation_name}`: Oynatılacak animasyonun adı

**İstek Parametreleri:**

- `loop` (opsiyonel): Animasyonu döngüye almak için boolean değer (varsayılan: false)
- `speed` (opsiyonel): Animasyon hızı çarpanı (varsayılan: 1.0)

**Yanıt:**

```json
{
  "success": true,
  "animation": "hello_animation",
  "duration": 4.5,
  "loop": false
}
```

#### Animasyon Durdurma

```
POST /api/animations/stop
```

**Yanıt:**

```json
{
  "success": true,
  "stopped_animation": "hello_animation",
  "playback_position": 2.3
}
```

#### Tüm Animasyonları Listeleme

```
GET /api/animations
```

**Yanıt:**

```json
{
  "animations": [
    {
      "name": "startup_animation",
      "display_name": "Startup Animation",
      "duration": 5.0,
      "description": "Robot startup sequence"
    },
    {
      "name": "hello_animation",
      "display_name": "Hello",
      "duration": 4.5,
      "description": "Greeting animation"
    },
    {
      "name": "thinking_animation",
      "display_name": "Thinking",
      "duration": 3.0,
      "description": "Contemplation animation"
    }
    // ... diğer animasyonlar
  ]
}
```

#### Animasyon Durumunu Alma

```
GET /api/animations/status
```

**Yanıt:**

```json
{
  "playing": true,
  "current_animation": "hello_animation",
  "position": 2.3,
  "duration": 4.5,
  "loop": false,
  "speed": 1.0
}
```

### Yapılandırma Endpoint'leri

#### Mevcut Yapılandırmayı Alma

```
GET /api/config
```

**Yanıt:**

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
  // ... diğer yapılandırma bölümleri
}
```

#### Yapılandırmayı Güncelleme

```
POST /api/config/update
```

**İstek Gövdesi:**

```json
{
  "oled": {
    "brightness": 200,
    "blink_frequency": 5.2
  },
  "leds": {
    "brightness": 150
  }
}
```

**Yanıt:**

```json
{
  "success": true,
  "updated_fields": [
    "oled.brightness",
    "oled.blink_frequency",
    "leds.brightness"
  ]
}
```

### Ses İşleme Endpoint'leri

#### Ses İşleme Durumunu Alma

```
GET /api/sound/status
```

**Yanıt:**

```json
{
  "enabled": true,
  "is_speaking": false,
  "volume_level": 0.12,
  "speech_duration": 0,
  "device_name": "Built-in Audio Analog Stereo"
}
```

#### Ses İşleme Etkinleştirme/Devre Dışı Bırakma

```
POST /api/sound/enable
```

veya

```
POST /api/sound/disable
```

**Yanıt:**

```json
{
  "success": true,
  "enabled": true,
  "device_name": "Built-in Audio Analog Stereo"
}
```

#### Ses İşleme Yapılandırmasını Güncelleme

```
POST /api/sound/config
```

**İstek Gövdesi:**

```json
{
  "sensitivity": 2.5,
  "threshold": 0.18,
  "device_index": 1
}
```

**Yanıt:**

```json
{
  "success": true,
  "updated_fields": [
    "sensitivity",
    "threshold",
    "device_index"
  ]
}
```

### Simülasyon Endpoint'leri

#### Simülasyon Durumu Alma

```
GET /api/simulation/status
```

**Yanıt:**

```json
{
  "enabled": true,
  "output_directory": "simulation/",
  "frame_count": 142,
  "current_frame": 143
}
```

#### Simülasyonu Etkinleştirme/Devre Dışı Bırakma

```
POST /api/simulation/enable
```

veya

```
POST /api/simulation/disable
```

**Yanıt:**

```json
{
  "success": true,
  "enabled": true,
  "output_directory": "simulation/"
}
```

#### Simülasyon Verisi Enjekte Etme (Test İçin)

```
POST /api/simulation/inject
```

**İstek Gövdesi:**

```json
{
  "type": "audio",
  "data": "base64_encoded_audio_data",
  "duration": 2.5
}
```

**Yanıt:**

```json
{
  "success": true,
  "processed": true,
  "result": {
    "volume_level": 0.45,
    "is_speaking": true
  }
}
```

## WebSocket API

WebSocket API, gerçek zamanlı veri güncellemeleri ve komut gönderimi için kullanılır. Varsayılan olarak `ws://localhost:8000/ws` adresinde çalışır.

### Mesaj Formatı

Tüm WebSocket mesajları JSON formatındadır ve şu genel yapıya sahiptir:

```json
{
  "type": "MESSAGE_TYPE",
  "data": {
    // mesaj tipine özgü veri alanları
  },
  "timestamp": 1714806420000
}
```

### Client-Server Mesajları

Client'tan (kontrol eden uygulama) server'a (FACE1) gönderilen mesajlar:

#### Bağlantı İsteği

```json
{
  "type": "FACE1_CONNECT_REQUEST",
  "data": {
    "version": "1.0",
    "clientName": "MyApplication"
  }
}
```

#### Duygu Ayarlama

```json
{
  "type": "FACE1_SET_EMOTION",
  "data": {
    "emotion": "happy",
    "intensity": 0.8,
    "duration": null
  }
}
```

#### Animasyon Oynatma

```json
{
  "type": "FACE1_PLAY_ANIMATION",
  "data": {
    "animation": "hello_animation",
    "loop": false,
    "speed": 1.0
  }
}
```

#### Animasyonu Durdurma

```json
{
  "type": "FACE1_STOP_ANIMATION",
  "data": {}
}
```

#### Tema Değiştirme

```json
{
  "type": "FACE1_SET_THEME",
  "data": {
    "theme": "pixel"
  }
}
```

#### Yapılandırma Değiştirme

```json
{
  "type": "FACE1_UPDATE_CONFIG",
  "data": {
    "oled": {
      "brightness": 200
    }
  }
}
```

#### Ses Tepkimeli Modu Ayarlama

```json
{
  "type": "FACE1_SET_SOUND_REACTIVE",
  "data": {
    "enabled": true
  }
}
```

#### Durum Sorgusu

```json
{
  "type": "FACE1_GET_STATUS",
  "data": {}
}
```

### Server-Client Mesajları

Server'dan (FACE1) client'a (kontrol eden uygulama) gönderilen mesajlar:

#### Bağlantı Yanıtı

```json
{
  "type": "FACE1_CONNECT_RESPONSE",
  "data": {
    "success": true,
    "version": "0.5.0",
    "message": "Connected successfully"
  }
}
```

#### Duygu Değişikliği Bildirimi

```json
{
  "type": "FACE1_EMOTION_CHANGE",
  "data": {
    "emotion": "happy",
    "intensity": 0.8,
    "source": "api",
    "previous_emotion": "neutral"
  }
}
```

#### Animasyon Durumu Bildirimi

```json
{
  "type": "FACE1_ANIMATION_UPDATE",
  "data": {
    "animation": "hello_animation",
    "progress": 0.5,
    "playing": true,
    "loop": false
  }
}
```

#### Animasyon Tamamlandı Bildirimi

```json
{
  "type": "FACE1_ANIMATION_COMPLETED",
  "data": {
    "animation": "hello_animation",
    "duration": 4.5
  }
}
```

#### Sistem Durumu Bildirimi

```json
{
  "type": "FACE1_SYSTEM_STATUS",
  "data": {
    "status": "running",
    "uptime": 3650,
    "cpu": 15.2,
    "memory": 28.4
  }
}
```

#### Ses Seviyesi Bildirimi

```json
{
  "type": "FACE1_SOUND_LEVEL",
  "data": {
    "level": 0.42,
    "isSpeaking": true
  }
}
```

#### Tema Değişikliği Bildirimi

```json
{
  "type": "FACE1_THEME_CHANGE",
  "data": {
    "theme": "pixel",
    "previous_theme": "default"
  }
}
```

#### Hata Bildirimi

```json
{
  "type": "FACE1_ERROR",
  "data": {
    "code": "ANIMATION_NOT_FOUND",
    "message": "Animation 'unknown_animation' not found",
    "details": {
      "requested_animation": "unknown_animation",
      "available_animations": ["hello_animation", "thinking_animation"]
    }
  }
}
```

### Hata İşleme

WebSocket API, hataları `FACE1_ERROR` tipi ile bildirir. Genel hata kodları:

| Hata Kodu | Açıklama |
|-----------|----------|
| `INVALID_MESSAGE_FORMAT` | Mesaj formatı geçersiz |
| `UNKNOWN_MESSAGE_TYPE` | Bilinmeyen mesaj tipi |
| `INVALID_PARAMETERS` | Geçersiz veya eksik parametreler |
| `EMOTION_NOT_FOUND` | Belirtilen duygu bulunamadı |
| `ANIMATION_NOT_FOUND` | Belirtilen animasyon bulunamadı |
| `THEME_NOT_FOUND` | Belirtilen tema bulunamadı |
| `OPERATION_FAILED` | İşlem başarısız oldu |
| `RESOURCE_BUSY` | Kaynak başka bir işlem tarafından kullanılıyor |
| `INTERNAL_ERROR` | Dahili sistem hatası |

## Python API

FACE1, Python modülü olarak da kullanılabilir. İşte temel sınıfların API referansı:

### FacePlugin Sınıfı

`FacePlugin` sınıfı, FACE1'in ana sınıfıdır ve tüm modüllere erişim sağlar.

```python
from face1 import FacePlugin

# Örnek kullanım
plugin = FacePlugin(config_path="config/config.json")
plugin.start()
plugin.set_emotion("happy", intensity=0.8)
plugin.play_animation("hello_animation")
plugin.stop()
```

#### Yapıcı ve Yaşam Döngüsü Metodları

```python
def __init__(self, config_path=None, config=None, simulation=False):
    """
    FacePlugin örneği oluşturur.
    
    Args:
        config_path (str, optional): Yapılandırma dosyasının yolu
        config (dict, optional): Alternatif olarak doğrudan yapılandırma nesnesi
        simulation (bool): Simülasyon modunu etkinleştirir
    """
    pass

def start(self):
    """FACE1 sistemini başlatır."""
    pass
    
def stop(self):
    """FACE1 sistemini durdurur."""
    pass
    
def pause(self):
    """Sistemi geçici olarak duraklatır."""
    pass
    
def resume(self):
    """Duraklatılmış sistemi devam ettirir."""
    pass
    
def restart(self):
    """Sistemi yeniden başlatır."""
    pass
```

#### Duygu Kontrol Metodları

```python
def set_emotion(self, emotion, intensity=1.0, duration=None, subtype=None):
    """
    Duygu durumunu ayarlar.
    
    Args:
        emotion (str): Duygu adı
        intensity (float): Duygu yoğunluğu (0.0-1.0)
        duration (float, optional): Duygunun süreceği saniye
        subtype (str, optional): Duygunun alt tipi
        
    Returns:
        dict: Ayarlanan duygu bilgileri
    """
    pass
    
def transition_to_emotion(self, emotion, intensity=1.0, duration=1.0):
    """
    Belirtilen duyguya yumuşak geçiş yapar.
    
    Args:
        emotion (str): Hedef duygu
        intensity (float): Hedef yoğunluk
        duration (float): Geçiş süresi (saniye)
        
    Returns:
        dict: Geçiş bilgileri
    """
    pass
    
def get_current_emotion(self):
    """
    Mevcut duygu durumunu döndürür.
    
    Returns:
        dict: Mevcut duygu bilgileri
    """
    pass
    
def get_emotions(self):
    """
    Tüm desteklenen duyguları döndürür.
    
    Returns:
        list: Duygu nesneleri listesi
    """
    pass
```

#### Tema ve Animasyon Metodları

```python
def set_theme(self, theme_name):
    """
    Temayı değiştirir.
    
    Args:
        theme_name (str): Tema adı
        
    Returns:
        dict: Tema değişikliği bilgileri
    """
    pass
    
def get_current_theme(self):
    """
    Mevcut temayı döndürür.
    
    Returns:
        dict: Tema bilgileri
    """
    pass
    
def get_themes(self):
    """
    Tüm kullanılabilir temaları döndürür.
    
    Returns:
        list: Tema nesneleri listesi
    """
    pass
    
def play_animation(self, animation_name, loop=False, speed=1.0):
    """
    Animasyon oynatır.
    
    Args:
        animation_name (str): Animasyon adı
        loop (bool): Döngü modu
        speed (float): Oynatma hızı
        
    Returns:
        dict: Animasyon bilgileri
    """
    pass
    
def stop_animation(self):
    """
    Mevcut animasyonu durdurur.
    
    Returns:
        dict: Durdurulan animasyon bilgileri
    """
    pass
    
def get_animations(self):
    """
    Tüm kullanılabilir animasyonları döndürür.
    
    Returns:
        list: Animasyon nesneleri listesi
    """
    pass
```

#### Ses İşleme Kontrol Metodları

```python
def enable_sound_processing(self, enable=True):
    """
    Ses işleme sistemini etkinleştirir veya devre dışı bırakır.
    
    Args:
        enable (bool): Etkinleştirmek için True, devre dışı bırakmak için False
        
    Returns:
        dict: Ses işleme durumu
    """
    pass
    
def get_sound_status(self):
    """
    Ses işleme sisteminin durumunu döndürür.
    
    Returns:
        dict: Ses işleme durumu bilgileri
    """
    pass
```

#### Yapılandırma ve Durum Metodları

```python
def get_config(self):
    """
    Mevcut yapılandırmayı döndürür.
    
    Returns:
        dict: Yapılandırma nesnesi
    """
    pass
    
def update_config(self, config_updates):
    """
    Yapılandırmayı günceller.
    
    Args:
        config_updates (dict): Güncellenecek yapılandırma alanları
        
    Returns:
        dict: Güncelleme sonucu
    """
    pass
    
def get_status(self):
    """
    Sistem durumunu döndürür.
    
    Returns:
        dict: Durum bilgileri
    """
    pass
```

### EmotionEngine Sınıfı

`EmotionEngine` sınıfı, duygu durumlarını ve geçişlerini yönetir.

```python
# Örnek kullanım
emotion_engine = plugin.emotion_engine
emotion_engine.set_emotion("happy", intensity=0.8)
```

#### Temel Metodlar

```python
def set_emotion(self, emotion, intensity=1.0, duration=None, subtype=None, source="api"):
    """Duygu durumunu ayarlar."""
    pass
    
def transition_to(self, emotion, intensity=1.0, duration=1.0):
    """Duyguya yumuşak geçiş yapar."""
    pass
    
def show_micro_expression(self, emotion, duration=0.5, intensity=1.0):
    """Kısa süreli mikro ifade gösterir."""
    pass
    
def get_current_emotion(self):
    """Mevcut duygu durumunu döndürür."""
    pass
    
def is_valid_emotion(self, emotion):
    """Duygunun geçerli olup olmadığını kontrol eder."""
    pass
    
def get_emotions(self):
    """Tüm desteklenen duyguları döndürür."""
    pass
```

### OLEDController Sınıfı

`OLEDController` sınıfı, OLED ekranları (göz ve ağız) kontrol eder.

```python
# Örnek kullanım
oled_controller = plugin.oled_controller
oled_controller.set_brightness(200)
```

#### Temel Metodlar

```python
def display_emotion(self, emotion, intensity=1.0, subtype=None):
    """Belirtilen duyguya ait göz ve ağız ifadelerini gösterir."""
    pass
    
def blink(self):
    """Göz kırpma animasyonu gösterir."""
    pass
    
def set_brightness(self, brightness):
    """Ekran parlaklığını ayarlar (0-255)."""
    pass
    
def set_power_save(self, enable=True, timeout=300):
    """Güç tasarrufu modunu yapılandırır."""
    pass
    
def clear(self):
    """Ekranları temizler."""
    pass
```

### AnimationEngine Sınıfı

`AnimationEngine` sınıfı, göz, ağız ve LED animasyonlarını yönetir.

```python
# Örnek kullanım
animation_engine = plugin.animation_engine
animation_engine.play_animation("hello_animation")
```

#### Temel Metodlar

```python
def play_animation(self, animation_name, loop=False, speed=1.0):
    """Animasyon oynatır."""
    pass
    
def stop_animation(self):
    """Mevcut animasyonu durdurur."""
    pass
    
def pause_animation(self):
    """Animasyonu duraklatır."""
    pass
    
def resume_animation(self):
    """Duraklatılmış animasyonu devam ettirir."""
    pass
    
def get_animation_status(self):
    """Animasyon durumunu döndürür."""
    pass
    
def get_animations(self):
    """Tüm kullanılabilir animasyonları döndürür."""
    pass
    
def load_animation(self, animation_path):
    """Özel animasyon yükler."""
    pass
```

### SoundProcessor Sınıfı

`SoundProcessor` sınıfı, ses analizi ve tepkimeli ifadeler için kullanılır.

```python
# Örnek kullanım
sound_processor = plugin.sound_processor
sound_processor.set_volume_sensitivity(2.5)
```

#### Temel Metodlar

```python
def start(self):
    """Ses işleme sistemini başlatır."""
    pass
    
def stop(self):
    """Ses işleme sistemini durdurur."""
    pass
    
def pause(self):
    """Ses işlemeyi geçici olarak duraklatır."""
    pass
    
def resume(self):
    """Duraklatılmış ses işlemeyi devam ettirir."""
    pass
    
def get_status(self):
    """Mevcut durumu döndürür."""
    pass
    
def set_volume_sensitivity(self, sensitivity):
    """Ses seviyesi hassasiyetini ayarlar."""
    pass
    
def set_speech_threshold(self, threshold):
    """Konuşma algılama eşik değerini ayarlar."""
    pass
```

## Veri Tipleri ve Enum'lar

### EmotionType Enum

Desteklenen temel duygular:

```python
class EmotionType(Enum):
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    ANGRY = "angry"
    SURPRISED = "surprised"
    SCARED = "scared"
    DISGUSTED = "disgusted"
    SLEEPY = "sleepy"
```

### SystemStatus Enum

Sistem durumları:

```python
class SystemStatus(Enum):
    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing"
    INITIALIZED = "initialized"
    STARTING = "starting"
    RUNNING = "running"
    PAUSED = "paused"
    MAINTENANCE = "maintenance"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"
    RECOVERING = "recovering"
    SHUTDOWN = "shutdown"
```

### Emotion Sınıfı

```python
class Emotion:
    """Duygu durumunu temsil eder."""
    
    def __init__(self, name, intensity=1.0, subtype=None, source="system"):
        self.name = name
        self.intensity = intensity
        self.subtype = subtype
        self.source = source
        self.timestamp = time.time()
```

### Animation Sınıfı

```python
class Animation:
    """Animasyon verilerini temsil eder."""
    
    def __init__(self, name, display_name, duration, description=None):
        self.name = name
        self.display_name = display_name
        self.duration = duration
        self.description = description
```

### Theme Sınıfı

```python
class Theme:
    """Tema verilerini temsil eder."""
    
    def __init__(self, name, display_name, author=None, version="1.0.0"):
        self.name = name
        self.display_name = display_name
        self.author = author
        self.version = version
```

## Örnekler

### REST API Örneği (cURL)

```bash
# Sistem durumunu al
curl -X GET http://localhost:8000/status

# Duygu durumunu ayarla
curl -X POST http://localhost:8000/emotion/happy -d "intensity=0.8"

# Animasyon oynat
curl -X POST http://localhost:8000/api/animations/hello_animation/play

# Yapılandırma güncelle
curl -X POST http://localhost:8000/api/config/update \
  -H "Content-Type: application/json" \
  -d '{"oled":{"brightness":200}}'
```

### WebSocket API Örneği (JavaScript)

```javascript
// WebSocket bağlantısı
const ws = new WebSocket('ws://localhost:8000/ws');

// Bağlantı açıldığında
ws.onopen = function() {
  // Bağlantı isteği gönder
  ws.send(JSON.stringify({
    type: 'FACE1_CONNECT_REQUEST',
    data: {
      version: '1.0',
      clientName: 'WebSocketExample'
    }
  }));
  
  // Duygu ayarla
  ws.send(JSON.stringify({
    type: 'FACE1_SET_EMOTION',
    data: {
      emotion: 'happy',
      intensity: 0.8
    }
  }));
};

// Mesaj alındığında
ws.onmessage = function(event) {
  const message = JSON.parse(event.data);
  
  // Mesaj tipine göre işleme
  switch(message.type) {
    case 'FACE1_CONNECT_RESPONSE':
      console.log('Bağlantı kuruldu:', message.data);
      break;
    case 'FACE1_EMOTION_CHANGE':
      console.log('Duygu değişti:', message.data);
      break;
    case 'FACE1_SOUND_LEVEL':
      updateVolumeVisualization(message.data.level);
      break;
    case 'FACE1_ERROR':
      console.error('Hata:', message.data);
      break;
  }
};
```

### Python API Örneği

```python
from face1 import FacePlugin
import time

# Plugin örneği oluştur ve başlat
plugin = FacePlugin(config_path="config/config.json")
plugin.start()

try:
    # Temayı değiştir
    plugin.set_theme("pixel")
    
    # Mutlu duygu göster
    plugin.set_emotion("happy", intensity=0.8)
    time.sleep(2)
    
    # Selamlama animasyonu oynat
    plugin.play_animation("hello_animation")
    time.sleep(5)
    
    # Duyguları geçişli olarak göster
    emotions = ["neutral", "happy", "sad", "surprised", "angry"]
    for emotion in emotions:
        plugin.transition_to_emotion(emotion, duration=1.5)
        time.sleep(2)
    
    # Ses işlemeyi etkinleştir
    plugin.enable_sound_processing(True)
    print("Ses işleme etkin. Konuşmayı deneyin...")
    time.sleep(10)
    
    # Plugin'i durdur
    plugin.stop()
    
except KeyboardInterrupt:
    # Temiz çıkış
    plugin.stop()
    print("Program sonlandırıldı.")
```

Bu API referansı, FACE1'in tüm arayüzlerini detaylı olarak açıklar ve uygulamanızı FACE1 ile entegre etmek için gereken tüm bilgileri sağlar.