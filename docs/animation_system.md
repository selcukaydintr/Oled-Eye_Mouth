# FACE1 Animasyon Sistemi Dokümantasyonu

## İçindekiler

- [Genel Bakış](#genel-bakış)
- [Animasyon Yapısı](#animasyon-yapısı)
- [Animasyon Dosya Formatı](#animasyon-dosya-formatı)
- [AnimationEngine Açıklaması](#animationengine-açıklaması)
- [Animasyon Oluşturma](#animasyon-oluşturma)
- [Animasyon Çalma ve Kontrol](#animasyon-çalma-ve-kontrol)
- [İleri Düzey Özellikler](#i̇leri-düzey-özellikler)
- [Animasyon Optimizasyon](#animasyon-optimizasyon)
- [API Referansı](#api-referansı)
- [Örnekler](#örnekler)

## Genel Bakış

FACE1 Animasyon Sistemi, robotun yüz ifadelerini, göz ve ağız hareketlerini zamanla değiştirerek canlandırmak için kullanılan bir sistemdir. Bu sistem, önceden tanımlanmış veya dinamik olarak oluşturulan animasyon sekanslarını oynatarak robotun daha doğal ve etkileşimli görünmesini sağlar.

### Temel Özellikler

- **Kare-Tabanlı Animasyon**: Animasyonun her anında göz ve ağız pozisyonlarını tanımlayan kare (frame) tabanlı sistem
- **JSON Tanım Formatı**: Animasyonlar kolay düzenlenebilir JSON formatında tanımlanır
- **Keyframe İnterpolasyonu**: Anahtar kareler arasında yumuşak geçişler sağlar
- **Paralel Kanal Sistemi**: Göz, ağız ve LED kanalları paralel olarak kontrol edilebilir
- **Döngü ve Tekrar**: Animasyonlar döngüye alınabilir veya belirli sayıda tekrar edilebilir
- **Hız Ayarı**: Animasyon oynatma hızı dinamik olarak değiştirilebilir
- **Olay (Event) Tetikleme**: Animasyon sırasında belirli noktalarda olaylar tetiklenebilir
- **Standart ve Özel Animasyonlar**: Sistem önceden tanımlı temel animasyonlar sağlar ve kullanıcı tanımlı animasyonları destekler

### Kullanım Senaryoları

Animasyon sistemi aşağıdaki senaryolarda kullanılabilir:

1. **İfade Geçişleri**: Bir duygu durumundan diğerine yumuşak geçişler
2. **İnteraktif Yanıtlar**: Kullanıcı veya çevre etkileşimlerine karşılık tepkiler
3. **İletişim Destekleri**: Sözel iletişimi destekleyici görsel işaretler (kafa sallama, göz kırpma, vb.)
4. **Sistem Durumu Göstergeleri**: Başlatma, kapanma, bekleme vb. sistem durumlarını gösterme
5. **Hikaye Anlatımı**: Karakter anlatımını destekleyen sekanslar

## Animasyon Yapısı

FACE1 animasyon sistemi çoklu kanal yapısını kullanır, bu sayede farklı yüz bileşenleri eş zamanlı olarak kontrol edilebilir.

### Animasyon Kanalları

Her animasyon bir veya daha fazla kanaldan oluşur:

1. **`eyes`**: Göz ifadelerini ve hareketlerini kontrol eder
2. **`mouth`**: Ağız şeklini ve hareketlerini kontrol eder
3. **`leds`**: LED ışıkları kontrol eder (varsa)
4. **`events`**: Animasyon sürecinde tetiklenen olayları tanımlar

Her kanal, kendi anahtar karelerini (keyframes) ve zamanlamalarını bağımsız olarak tanımlayabilir.

### Anahtar Kareler (Keyframes)

Keyframe'ler, animasyonun belirli anlarında bir kanalın durumunu tanımlar:

- **Zaman**: Animasyon başlangıcından itibaren geçen süre (saniye)
- **Değer**: Kanalın o andaki durumu (pozisyon, şekil, renk vb.)
- **Easing**: Bu keyframe'e geçiş eğrisi (doğrusal, ease-in, ease-out vb.)

Sistem, iki keyframe arasındaki ara değerleri otomatik olarak hesaplar (interpolasyon).

### Zaman Çizelgesi (Timeline)

Animasyon zaman çizelgesi şöyle işler:

```
 0s         1s         2s         3s         4s
 │          │          │          │          │
 ▼          ▼          ▼          ▼          ▼
┌──────────────────────────────────────────────┐
│                  eyes kanalı                 │
└──────────────────────────────────────────────┘
 ●----------●----------●--------------------●
 K1         K2         K3                   K4

┌──────────────────────────────────────────────┐
│                 mouth kanalı                 │
└──────────────────────────────────────────────┘
 ●-----●----------●-----●---------------------●
 K1    K2         K3    K4                    K5

┌──────────────────────────────────────────────┐
│                 events kanalı                │
└──────────────────────────────────────────────┘
       ▲                    ▲
      0.5s                 2.5s
   "blink_start"        "expression_change"
```

- Animasyon oynatıcı, mevcut zamanı takip eder ve her kanalın o andaki durumunu hesaplar
- Her kanal bağımsız olarak çalışır ve kendi keyframe'lerini takip eder
- Events kanalı, belirli zamanlarda diğer sistemiç bileşenlerini tetikleyen olaylar oluşturur

## Animasyon Dosya Formatı

FACE1 animasyonları, JSON formatında tanımlanır ve `.anim.json` uzantılı dosyalarda saklanır.

### Temel Format

```json
{
  "name": "greeting_animation",
  "display_name": "Greeting",
  "version": "1.0",
  "duration": 4.5,
  "loop": false,
  "author": "FACE1 Team",
  "description": "A friendly greeting animation with wave motion",
  "channels": {
    "eyes": {
      "keyframes": [
        {
          "time": 0.0,
          "value": {
            "shape": "neutral",
            "openness": 1.0,
            "position": [0, 0]
          },
          "easing": "linear"
        },
        {
          "time": 1.0,
          "value": {
            "shape": "happy",
            "openness": 0.8,
            "position": [2, 0]
          },
          "easing": "easeInOut"
        }
        // ... diğer keyframe'ler
      ]
    },
    "mouth": {
      "keyframes": [
        {
          "time": 0.0,
          "value": {
            "shape": "neutral",
            "width": 100,
            "height": 20
          },
          "easing": "linear"
        },
        {
          "time": 0.5,
          "value": {
            "shape": "smile",
            "width": 120,
            "height": 30
          },
          "easing": "easeOut"
        }
        // ... diğer keyframe'ler
      ]
    },
    "events": {
      "keyframes": [
        {
          "time": 0.5,
          "value": {
            "type": "blink_start",
            "parameters": {}
          }
        },
        {
          "time": 2.5,
          "value": {
            "type": "expression_change",
            "parameters": {
              "expression": "excited"
            }
          }
        }
        // ... diğer olaylar
      ]
    }
  }
}
```

### Kanal Değer Formatları

#### Gözler Kanalı (`eyes`)

```json
{
  "shape": "happy|sad|angry|surprised|neutral|...",
  "openness": 0.0-1.0,
  "position": [x, y],
  "pupil_size": 0.0-1.0,
  "pupil_position": [x, y],
  "blink": true|false
}
```

#### Ağız Kanalı (`mouth`)

```json
{
  "shape": "smile|frown|neutral|open|...",
  "width": 0-255,
  "height": 0-128,
  "position": [x, y],
  "expression_intensity": 0.0-1.0
}
```

#### LED Kanalı (`leds`)

```json
{
  "brightness": 0-255,
  "color": [r, g, b],
  "pattern": "solid|pulse|blink|...",
  "speed": 0.0-10.0
}
```

#### Olaylar Kanalı (`events`)

```json
{
  "type": "event_name",
  "parameters": {
    // olaya özgü parametreler
  }
}
```

Sık kullanılan olaylar:
- `blink_start`: Göz kırpma başlat
- `blink_end`: Göz kırpma bitir
- `expression_change`: İfadeyi değiştir
- `sound_effect`: Ses efekti çal
- `animation_callback`: Üst sisteme geri çağrı bildir

### Easing (Geçiş) Fonksiyonları

Keyframe'ler arasındaki geçişin karakterini tanımlayan easing fonksiyonları:

- `linear`: Doğrusal geçiş (sabit hız)
- `easeIn`: Başlangıçta yavaş, sonda hızlı
- `easeOut`: Başlangıçta hızlı, sonda yavaş
- `easeInOut`: Başlangıç ve sonda yavaş, ortada hızlı
- `bounce`: Sıçrama efekti
- `elastic`: Elastik geçiş efekti
- `step`: Ani geçiş (ara değer hesaplanmaz)

## AnimationEngine Açıklaması

AnimationEngine, tüm animasyon sistemini kontrol eden merkezi bileşendir. Animasyonları yükler, oynatır ve senkronize eder.

### Temel Bileşenler

```
┌─────────────────────────┐
│    AnimationEngine      │
├─────────────────────────┤
│ - AnimationLoader       │ ──── Dosyadan animasyonları yükler
│ - AnimationPlayer       │ ──── Animasyon oynatma mantığı
│ - AnimationScheduler    │ ──── Animasyon zamanlaması
│ - InterpolationManager  │ ──── Keyframe arası değer hesaplama
│ - EventDispatcher       │ ──── Animasyon olaylarını dağıtır
└─────────────┬───────────┘
              │
              │ kontrol
              ▼
┌─────────────────────────┐
│    AnimationRenderer    │
├─────────────────────────┤
│ - EyeRenderer           │ ──── Göz animasyonlarını ekrana çizer
│ - MouthRenderer         │ ──── Ağız animasyonlarını ekrana çizer
│ - LEDController         │ ──── LED ışıkları kontrol eder
└─────────────────────────┘
```

### Çalışma Prensibi

1. **Animasyon Yükleme**: AnimationLoader, JSON animasyon dosyalarını okur ve bellek içi temsillere dönüştürür
2. **Oynatma Kontrolü**: AnimationPlayer, kullanıcı komutlarına dayalı olarak oynatma durumunu yönetir (oynat, duraklat, durdur)
3. **Zamanlama**: AnimationScheduler, animasyon zamanlayıcısını çalıştırır ve mevcut zaman pozisyonunu hesaplar
4. **İnterpolasyon**: InterpolationManager, mevcut zaman için her kanalın değerlerini hesaplar
5. **Render**: AnimationRenderer, hesaplanan değerleri kullanarak OLED ekranlar ve LED'ler için çıktı üretir
6. **Olay İşleme**: EventDispatcher, animasyon olaylarını tespit eder ve ilgili işleyicileri çağırır

## Animasyon Oluşturma

Yeni animasyonlar iki şekilde oluşturulabilir: manuel olarak JSON düzenleme veya Animation Editor kullanılarak.

### Manuel JSON Oluşturma

1. `animation/custom/` dizininde yeni bir `.anim.json` dosyası oluşturun
2. [Animasyon Dosya Formatı](#animasyon-dosya-formatı) bölümündeki yapıyı takip edin
3. Kanallar için keyframe'leri zamana göre tanımlayın
4. Dosyayı kaydedin ve FACE1'i yeniden başlatın veya `reload_animations` API çağrısı yapın

### Animation Editor (Geliştirilme Aşamasında)

Animation Editor, grafiksel bir arayüz kullanarak animasyon oluşturmayı kolaylaştıran bir araçtır. Bu araç şu anda geliştirme aşamasındadır, ancak temel kullanımı şöyledir:

1. Tarayıcıda `http://localhost:8000/editor/animations` adresine gidin
2. "Yeni Animasyon" düğmesine tıklayın
3. Animasyon meta verilerini (ad, süre, döngü vb.) girin
4. Zaman çizelgesinde her kanal için keyframe'leri yerleştirin
5. Keyframe değerlerini ve easing özelliklerini düzenleyin
6. "Kaydet" düğmesine tıklayarak animasyonu `.anim.json` formatında dışa aktarın

### Özel Animasyon Klasörleri

FACE1, animasyonlar için belirli klasörleri tarar:

- `/animation/standard/` - Sistem tarafından sağlanan animasyonlar
- `/animation/custom/` - Kullanıcı tanımlı animasyonlar

Özel animasyonlarınızı `custom` klasörüne yerleştirin; bu sayede sistem güncellemeleri standart animasyonlarınızı etkilemez.

## Animasyon Çalma ve Kontrol

Animasyonlar çeşitli yöntemlerle kontrol edilebilir.

### REST API ile Kontrol

```
# Animasyon oynatma
POST /api/animations/{animation_name}/play
Content-Type: application/json
{
  "loop": false,
  "speed": 1.0
}

# Animasyon durdurma
POST /api/animations/stop

# Animasyon duraklatma
POST /api/animations/pause

# Animasyon devam ettirme
POST /api/animations/resume

# Animasyon listesini alma
GET /api/animations
```

### WebSocket API ile Kontrol

```javascript
// Animasyon oynatma
websocket.send(JSON.stringify({
  "type": "FACE1_PLAY_ANIMATION",
  "data": {
    "animation": "greeting_animation",
    "loop": false,
    "speed": 1.0
  }
}));

// Animasyon durdurma
websocket.send(JSON.stringify({
  "type": "FACE1_STOP_ANIMATION",
  "data": {}
}));
```

### Python API ile Kontrol

```python
# FacePlugin üzerinden
plugin = FacePlugin(config_path="config/config.json")
plugin.play_animation("greeting_animation", loop=False, speed=1.0)
plugin.stop_animation()

# AnimationEngine'e doğrudan erişerek
animation_engine = plugin.animation_engine
animation_engine.play_animation("greeting_animation", loop=False, speed=1.0)
animation_engine.stop_animation()
```

### Animasyon Olaylarını Dinleme

Animasyon durumundaki değişiklikleri dinlemek için olay dinleyicileri kullanılabilir:

```python
# Python API ile
def animation_event_handler(event_type, data):
    if event_type == "animation_completed":
        print(f"Animasyon tamamlandı: {data['animation']}")
        
plugin.add_event_listener("animation_completed", animation_event_handler)
```

```javascript
// WebSocket API ile
websocket.addEventListener('message', function(event) {
  const message = JSON.parse(event.data);
  
  if (message.type === 'FACE1_ANIMATION_COMPLETED') {
    console.log(`Animasyon tamamlandı: ${message.data.animation}`);
  }
});
```

## İleri Düzey Özellikler

### Animasyon Zincirleme

Bir animasyon tamamlandığında otomatik olarak başka bir animasyon başlatabilirsiniz:

```python
def chain_animations():
    def on_completed(data):
        if data['animation'] == 'greeting_animation':
            plugin.play_animation('thinking_animation')
            
    plugin.add_event_listener("animation_completed", on_completed)
    plugin.play_animation('greeting_animation')
```

### Koşullu Animasyon Değişiklikleri

Sistem durumuna bağlı olarak animasyon davranışını değiştirme:

```python
class ConditionalAnimationController:
    def __init__(self, plugin):
        self.plugin = plugin
        self.is_happy = False
        
    def set_mood(self, is_happy):
        self.is_happy = is_happy
        
    def greet(self):
        if self.is_happy:
            self.plugin.play_animation('happy_greeting')
        else:
            self.plugin.play_animation('neutral_greeting')
```

### Dinamik Animasyon Oluşturma

Çalışma zamanında programlı olarak animasyon oluşturma:

```python
def create_blink_sequence(count, interval=0.5):
    """Belirli sayıda göz kırpma içeren bir animasyon oluşturur."""
    animation = {
        "name": f"blink_sequence_{count}",
        "display_name": f"Blink Sequence ({count})",
        "version": "1.0",
        "duration": count * interval,
        "loop": False,
        "channels": {
            "eyes": {
                "keyframes": []
            }
        }
    }
    
    # Her göz kırpma için keyframe'ler oluştur
    for i in range(count):
        # Göz açık
        animation["channels"]["eyes"]["keyframes"].append({
            "time": i * interval,
            "value": {
                "shape": "neutral",
                "openness": 1.0
            },
            "easing": "linear"
        })
        
        # Göz kapalı
        animation["channels"]["eyes"]["keyframes"].append({
            "time": i * interval + 0.1,  # 100ms sonra
            "value": {
                "shape": "neutral",
                "openness": 0.0
            },
            "easing": "easeOut"
        })
        
        # Göz tekrar açık
        animation["channels"]["eyes"]["keyframes"].append({
            "time": i * interval + 0.2,  # 200ms sonra
            "value": {
                "shape": "neutral",
                "openness": 1.0
            },
            "easing": "easeIn"
        })
    
    return animation

# Kullanım:
plugin.animation_engine.load_animation_data(create_blink_sequence(3))
plugin.play_animation("blink_sequence_3")
```

### Paralel Animasyonlar

Bazı durumlarda farklı bileşenler için paralel animasyonlar çalıştırmak isteyebilirsiniz:

```python
def run_parallel_animations():
    # Gözler için ayrı kanalla animasyon çal
    plugin.animation_engine.play_channel_animation(
        "eyes",
        "looking_around",
        loop=True
    )
    
    # Ağız için farklı bir animasyon çal
    plugin.animation_engine.play_channel_animation(
        "mouth",
        "talking",
        loop=True
    )
    
    # 5 saniye sonra tüm animasyonları durdur
    import threading
    threading.Timer(5, plugin.stop_animation).start()
```

## Animasyon Optimizasyon

Kompleks animasyonlar için performans optimizasyonu önemlidir.

### Performans İpuçları

1. **Keyframe Sayısını Optimum Tut**
   - Çok az keyframe: Pürüzsüz animasyon yetersiz
   - Çok fazla keyframe: İşlemci yükünü artırır
   - Önerilen: Sadece önemli değişiklikler için keyframe kullan

2. **Easing Fonksiyonlarını Akıllıca Kullan**
   - `linear`: Basit ve hızlı, ama doğal değil
   - `easeInOut`: Doğal görünüm, ama daha fazla hesaplama gerektirir
   - En iyi strateji: Küçük hareketler için linear, büyük hareketler için easing

3. **Kanal Kompleksitesini Dengele**
   - Her çerçeve her kanal için hesaplama yapılır
   - Kullanılmayan kanalları animasyondan çıkarın
   - En fazla değişen kanalları optimize edin

4. **Animasyon Süresini Sınırla**
   - Uzun animasyonlar bellek ve işlemci kaynakları tüketir
   - Döngü kullanımı: Uzun animasyonlar yerine kısa döngüler kullanın
   - Maksimum önerilen süre: 10-15 saniye

### RAM ve CPU Kullanımı

Raspberry Pi 5'te animasyon sisteminin kaynak kullanımı:

- **RAM Kullanımı**: Ortalama 5-20MB (karmaşıklığa bağlı)
- **CPU Yükü**: %1-5 (60 FPS'de tek animasyon oynatırken)
- **Maksimum Paralel Animasyon**: 3-4 (tüm kanallar aktif)

## API Referansı

### AnimationEngine Sınıfı

```python
class AnimationEngine:
    """FACE1 animasyon sisteminin ana sınıfı."""
    
    def __init__(self, config, renderer, event_dispatcher=None):
        """
        AnimationEngine örneği oluşturur.
        
        Args:
            config: Yapılandırma nesnesi
            renderer: Animasyon rendereri
            event_dispatcher: Olay dağıtıcı (opsiyonel)
        """
        pass
        
    def load_animations(self):
        """Tüm animasyon dizinlerini tarar ve animasyonları yükler."""
        pass
        
    def load_animation(self, animation_path):
        """Belirtilen dosyadan bir animasyon yükler."""
        pass
        
    def load_animation_data(self, animation_data):
        """Bellek içi animasyon verisinden bir animasyon yükler."""
        pass
        
    def get_animations(self):
        """Tüm yüklenmiş animasyonları döndürür."""
        pass
        
    def play_animation(self, animation_name, loop=False, speed=1.0):
        """
        Bir animasyon oynatır.
        
        Args:
            animation_name: Animasyon adı
            loop: Döngü modu (True/False)
            speed: Hız çarpanı (1.0 = normal hız)
        
        Returns:
            bool: Başarılıysa True, yoksa False
        """
        pass
        
    def play_channel_animation(self, channel, animation_name, loop=False, speed=1.0):
        """Belirli bir kanal için animasyon oynatır."""
        pass
        
    def stop_animation(self):
        """Mevcut animasyonu durdurur."""
        pass
        
    def pause_animation(self):
        """Mevcut animasyonu duraklatır."""
        pass
        
    def resume_animation(self):
        """Duraklatılmış animasyonu devam ettirir."""
        pass
        
    def get_animation_status(self):
        """Mevcut animasyon durumunu döndürür."""
        pass
        
    def set_animation_speed(self, speed):
        """Mevcut animasyonun hızını ayarlar."""
        pass
        
    def create_animation(self, animation_data):
        """Yeni bir animasyon oluşturur ve kaydeder."""
        pass
```

### AnimationEvent Türleri

```python
# AnimationEngine tarafından tetiklenen olaylar
ANIMATION_STARTED = "animation_started"            # Animasyon başladığında
ANIMATION_COMPLETED = "animation_completed"        # Animasyon tamamlandığında
ANIMATION_STOPPED = "animation_stopped"            # Animasyon durdurulduğunda
ANIMATION_PAUSED = "animation_paused"              # Animasyon duraklatıldığında
ANIMATION_RESUMED = "animation_resumed"            # Animasyon devam ettirildiğinde
ANIMATION_LOOP = "animation_loop"                  # Animasyon döngüsü tekrarlandığında
ANIMATION_ERROR = "animation_error"                # Animasyon oynatma hatası

# Animasyon olayları kanalından tetiklenen olaylar
ANIMATION_CUSTOM_EVENT = "animation_custom_event"  # Özel animasyon olayı
ANIMATION_BLINK = "animation_blink"                # Göz kırpma olayı
ANIMATION_EXPRESSION = "animation_expression"      # İfade değişikliği
```

### Animation Sınıfı

```python
class Animation:
    """Bir animasyonu temsil eden sınıf."""
    
    def __init__(self, name, data=None, file_path=None):
        """
        Animation örneği oluşturur.
        
        Args:
            name: Animasyon adı
            data: Animasyon verisi (dict, opsiyonel)
            file_path: Animasyon dosya yolu (str, opsiyonel)
        """
        pass
        
    @property
    def duration(self):
        """Animasyon süresini döndürür."""
        pass
        
    @property
    def channels(self):
        """Animasyon kanallarını döndürür."""
        pass
        
    def get_value_at_time(self, channel, time):
        """
        Belirli bir zamanda belirli bir kanalın değerini hesaplar.
        
        Args:
            channel: Kanal adı
            time: Zaman (saniye)
            
        Returns:
            dict: Hesaplanan kanal değeri
        """
        pass
        
    def has_event_at_time(self, time, event_type=None):
        """Belirli bir zamanda olay olup olmadığını kontrol eder."""
        pass
        
    def get_events_in_range(self, start_time, end_time):
        """Belirli bir zaman aralığındaki olayları döndürür."""
        pass
        
    def to_json(self):
        """Animasyonu JSON formatına dönüştürür."""
        pass
        
    @classmethod
    def from_json(cls, json_data):
        """JSON verisinden bir Animation örneği oluşturur."""
        pass
```

## Örnekler

### Temel "Merhaba Dünya" Animasyonu

```json
{
  "name": "hello_world",
  "display_name": "Hello World",
  "version": "1.0",
  "duration": 3.0,
  "loop": false,
  "author": "FACE1 User",
  "description": "Basic greeting animation",
  "channels": {
    "eyes": {
      "keyframes": [
        {
          "time": 0.0,
          "value": {
            "shape": "neutral",
            "openness": 1.0,
            "position": [0, 0]
          },
          "easing": "linear"
        },
        {
          "time": 1.0,
          "value": {
            "shape": "happy",
            "openness": 0.8,
            "position": [0, 0]
          },
          "easing": "easeInOut"
        },
        {
          "time": 2.0,
          "value": {
            "shape": "happy",
            "openness": 0.0,  // Göz kırpma
            "position": [0, 0]
          },
          "easing": "easeOut"
        },
        {
          "time": 2.3,
          "value": {
            "shape": "happy",
            "openness": 1.0,  // Göz açma
            "position": [0, 0]
          },
          "easing": "easeIn"
        },
        {
          "time": 3.0,
          "value": {
            "shape": "happy",
            "openness": 1.0,
            "position": [0, 0]
          },
          "easing": "linear"
        }
      ]
    },
    "mouth": {
      "keyframes": [
        {
          "time": 0.0,
          "value": {
            "shape": "neutral",
            "width": 100,
            "height": 20
          },
          "easing": "linear"
        },
        {
          "time": 1.0,
          "value": {
            "shape": "smile",
            "width": 120,
            "height": 40
          },
          "easing": "easeOut"
        },
        {
          "time": 3.0,
          "value": {
            "shape": "smile",
            "width": 120,
            "height": 40
          },
          "easing": "linear"
        }
      ]
    }
  }
}
```

### İleri Düzey Animasyon Örneği

```json
{
  "name": "complex_reaction",
  "display_name": "Complex Reaction",
  "version": "1.0",
  "duration": 8.0,
  "loop": false,
  "author": "FACE1 Team",
  "description": "A complex emotional reaction with multiple phases",
  "channels": {
    "eyes": {
      "keyframes": [
        {
          "time": 0.0,
          "value": {"shape": "neutral", "openness": 1.0, "position": [0, 0]},
          "easing": "linear"
        },
        {
          "time": 1.0,
          "value": {"shape": "surprised", "openness": 1.0, "position": [0, -5]},
          "easing": "easeOut"
        },
        {
          "time": 2.0,
          "value": {"shape": "surprised", "openness": 0.0, "position": [0, -5]},
          "easing": "step"
        },
        {
          "time": 2.2,
          "value": {"shape": "surprised", "openness": 1.0, "position": [0, -5]},
          "easing": "step"
        },
        {
          "time": 3.5,
          "value": {"shape": "angry", "openness": 0.8, "position": [0, 0]},
          "easing": "easeInOut"
        },
        {
          "time": 5.0,
          "value": {"shape": "sad", "openness": 0.9, "position": [0, 3]},
          "easing": "easeInOut"
        },
        {
          "time": 7.0,
          "value": {"shape": "happy", "openness": 0.9, "position": [0, -2]},
          "easing": "easeIn"
        },
        {
          "time": 8.0,
          "value": {"shape": "happy", "openness": 1.0, "position": [0, 0]},
          "easing": "linear"
        }
      ]
    },
    "mouth": {
      "keyframes": [
        {
          "time": 0.0,
          "value": {"shape": "neutral", "width": 100, "height": 20},
          "easing": "linear"
        },
        {
          "time": 1.0,
          "value": {"shape": "o_shape", "width": 80, "height": 80},
          "easing": "easeOut"
        },
        {
          "time": 3.5,
          "value": {"shape": "frown", "width": 120, "height": 30},
          "easing": "easeInOut"
        },
        {
          "time": 5.0,
          "value": {"shape": "sad", "width": 100, "height": 20},
          "easing": "easeInOut"
        },
        {
          "time": 7.0,
          "value": {"shape": "smile", "width": 120, "height": 40},
          "easing": "easeIn"
        },
        {
          "time": 8.0,
          "value": {"shape": "smile", "width": 120, "height": 40},
          "easing": "linear"
        }
      ]
    },
    "leds": {
      "keyframes": [
        {
          "time": 0.0,
          "value": {"brightness": 100, "color": [255, 255, 255], "pattern": "solid"},
          "easing": "linear"
        },
        {
          "time": 1.0,
          "value": {"brightness": 255, "color": [255, 255, 0], "pattern": "pulse"},
          "easing": "easeOut"
        },
        {
          "time": 3.5,
          "value": {"brightness": 200, "color": [255, 0, 0], "pattern": "solid"},
          "easing": "easeIn"
        },
        {
          "time": 5.0,
          "value": {"brightness": 150, "color": [0, 0, 255], "pattern": "solid"},
          "easing": "easeIn"
        },
        {
          "time": 7.0,
          "value": {"brightness": 200, "color": [0, 255, 0], "pattern": "solid"},
          "easing": "easeIn"
        },
        {
          "time": 8.0,
          "value": {"brightness": 100, "color": [255, 255, 255], "pattern": "solid"},
          "easing": "linear"
        }
      ]
    },
    "events": {
      "keyframes": [
        {
          "time": 1.0,
          "value": {
            "type": "expression_change",
            "parameters": {"expression": "surprised"}
          }
        },
        {
          "time": 2.0,
          "value": {
            "type": "blink_start",
            "parameters": {}
          }
        },
        {
          "time": 3.5,
          "value": {
            "type": "expression_change",
            "parameters": {"expression": "angry"}
          }
        },
        {
          "time": 4.0,
          "value": {
            "type": "sound_effect",
            "parameters": {"sound": "grumble"}
          }
        },
        {
          "time": 5.0,
          "value": {
            "type": "expression_change",
            "parameters": {"expression": "sad"}
          }
        },
        {
          "time": 7.0,
          "value": {
            "type": "expression_change",
            "parameters": {"expression": "happy"}
          }
        },
        {
          "time": 7.5,
          "value": {
            "type": "animation_callback",
            "parameters": {"callback_id": "emotion_cycle_complete"}
          }
        }
      ]
    }
  }
}
```

### Python API Örneği

```python
from face1 import FacePlugin
import time

# Plugin örneği oluştur
plugin = FacePlugin(config_path="config/config.json")
plugin.start()

# Özel animasyon tanımla
custom_animation = {
  "name": "custom_greeting",
  "display_name": "Custom Greeting",
  "version": "1.0",
  "duration": 2.0,
  "loop": False,
  "channels": {
    "eyes": {
      "keyframes": [
        {
          "time": 0.0,
          "value": {"shape": "neutral", "openness": 1.0},
          "easing": "linear"
        },
        {
          "time": 1.0,
          "value": {"shape": "happy", "openness": 0.8},
          "easing": "easeOut"
        },
        {
          "time": 2.0,
          "value": {"shape": "happy", "openness": 1.0},
          "easing": "linear"
        }
      ]
    },
    "mouth": {
      "keyframes": [
        {
          "time": 0.0,
          "value": {"shape": "neutral", "width": 100, "height": 20},
          "easing": "linear"
        },
        {
          "time": 1.0,
          "value": {"shape": "smile", "width": 120, "height": 40},
          "easing": "easeOut"
        },
        {
          "time": 2.0,
          "value": {"shape": "smile", "width": 120, "height": 40},
          "easing": "linear"
        }
      ]
    }
  }
}

# Özel animasyonu yükle
plugin.animation_engine.load_animation_data(custom_animation)

# Animasyon tamamlandığında çağrılacak olay dinleyici
def on_animation_completed(data):
    print(f"Animasyon tamamlandı: {data['animation']}")
    if data['animation'] == 'custom_greeting':
        print("Özel karşılama tamamlandı, temel animasyona geçiliyor...")
        plugin.play_animation('hello_animation')

# Olay dinleyiciyi kaydet
plugin.add_event_listener("animation_completed", on_animation_completed)

# Özel animasyonu oynat
plugin.play_animation("custom_greeting")

# Ana iş parçacığını beklet
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Program sonlandırılıyor...")
    plugin.stop()
```

Bu dokümantasyon, FACE1 Animasyon Sisteminin tüm yönlerini kapsamlı bir şekilde açıklar. Geliştiriciler bu bilgileri kullanarak özel animasyonlar oluşturabilir, mevcut animasyonları değiştirebilir ve FACE1 robotu için interaktif davranışlar programlayabilir.