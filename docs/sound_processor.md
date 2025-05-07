# FACE1 Ses İşleme Sistemi Dokümantasyonu

## İçindekiler

- [Genel Bakış](#genel-bakış)
- [Mimari Tasarım](#mimari-tasarım)
- [Kurulum ve Yapılandırma](#kurulum-ve-yapılandırma)
- [Ses Analiz Algoritmaları](#ses-analiz-algoritmaları)
- [Ses Tepkimeli İfadeler](#ses-tepkimeli-i̇fadeler)
- [Dashboard Entegrasyonu](#dashboard-entegrasyonu)
- [API Referansı](#api-referansı)
- [Gelişmiş Özelleştirme](#gelişmiş-özelleştirme)
- [Performans Optimizasyonu](#performans-optimizasyonu)
- [Sorun Giderme](#sorun-giderme)

## Genel Bakış

Ses İşleme Sistemi, FACE1 v0.5.0 ile eklenen ve robotun insan konuşmalarına tepki vermesini sağlayan bir özelliktir. Bu sistem, mikrofon aracılığıyla ortam seslerini analiz eder, ses seviyesini ve konuşma durumunu tespit eder, ardından robot yüzüne ağız hareketleri ve duygu önerileri şeklinde gerçek zamanlı tepkiler üretir.

### Temel Özellikler

- **Gerçek Zamanlı Ses Analizi**: Mikrofon girişinden ses verilerinin sürekli örneklenmesi ve analizi
- **Konuşma Tespiti**: İnsan konuşmasının tespiti ve süreölçümü
- **Ağız Senkronizasyonu**: Ses seviyesiyle senkronize ağız hareketleri
- **Reaktif İfadeler**: Ses karakteristiğine dayalı duygu durumu önerileri
- **Simülasyon Desteği**: Fiziksel mikrofon olmadan test için simülasyon modu
- **Dashboard Görselleştirmesi**: Ses seviyesi ve konuşma durumu için gerçek zamanlı görselleştirme

### Kullanım Senaryoları

Ses işleme sistemi aşağıdaki senaryolarda faydalıdır:

1. **İnsan-Robot Etkileşimi**: Kullanıcının konuşmasına tepki verme
2. **Ortam Farkındalığı**: Ortamdaki ses seviyesine göre reaktif ifadeler
3. **Konuşma Asistanı Arayüzleri**: Ses kontrollü uygulamalar için görsel geri bildirim
4. **İnteraktif Gösteriler**: Ses ve müziğe tepki veren robot yüz ifadeleri

## Mimari Tasarım

Ses İşleme Sistemi, FACE1'in modüler mimarisine entegre olmuş bir bileşendir.

### Bileşen Şeması

```
             ┌─────────────┐
             │  Mikrofon   │
             └──────┬──────┘
                    │
                    ▼
┌───────────────────────────────────┐
│         SoundProcessor            │
├───────────────────────────────────┤
│ ┌─────────────┐  ┌──────────────┐ │
│ │Audio Capture│  │ Ses Analizi  │ │
│ └──────┬──────┘  └───────┬──────┘ │
│        │                 │        │
│        ▼                 ▼        │
│ ┌─────────────┐  ┌──────────────┐ │
│ │  Konuşma    │  │Tepki Üreteci │ │
│ │  Dedektörü  │  │              │ │
│ └──────┬──────┘  └───────┬──────┘ │
└────────┼──────────────────┼───────┘
         │                  │
         ▼                  ▼
┌────────────────┐  ┌─────────────────┐
│ OLEDController │  │  EmotionEngine  │
│  (Ağız Hrkti)  │  │(Duygu Önerisi)  │
└────────────────┘  └─────────────────┘
         │                  │
         └──────────┬───────┘
                    ▼
             ┌─────────────┐
             │  Dashboard  │
             │(Görselleştirme)
             └─────────────┘
```

### Veri Akışı

1. Mikrofon, ses dalga formunu yakalar
2. AudioCapture modülü, ses verilerini çerçevelere böler
3. Ses Analizi modülü, ses seviyesi ve frekans özelliklerini hesaplar
4. Konuşma Dedektörü, ses seviyesi ve süreye dayalı konuşma tespiti yapar
5. Tepki Üreteci, analiz sonuçlarına dayalı tepkileri formüle eder
6. OLEDController, ağız hareketlerini ses seviyesine göre günceller
7. EmotionEngine, ses karakteristiğine dayalı duygu önerileri alır
8. Dashboard, ses analiz sonuçlarını canlı olarak görselleştirir

## Kurulum ve Yapılandırma

### Donanım Gereksinimleri

- USB Mikrofon veya 3.5mm jak mikrofonlu ses kartı
- Raspberry Pi 5 (veya uyumlu bilgisayar)

### Yazılım Bağımlılıkları

- PyAudio: Ses yakalama için
- NumPy: Sinyal işleme için
- SciPy (opsiyonel): Gelişmiş ses analizi için

### Kurulum

1. Mikrofon bağlantısını test edin:
   ```bash
   # Mikrofon cihazlarını listele
   arecord -l
   ```

2. PyAudio'yu yükleyin:
   ```bash
   # Debian/Ubuntu/Raspberry Pi OS
   sudo apt-get install python3-pyaudio
   
   # Veya pip ile
   pip install pyaudio
   ```

3. FACE1 yapılandırma dosyasında ses işlemeyi etkinleştirin:
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

### Yapılandırma Parametreleri

| Parametre | Açıklama | Varsayılan | Aralık |
|-----------|----------|------------|--------|
| `enabled` | Ses işleme sistemini etkinleştir/devre dışı bırak | `true` | `true`/`false` |
| `sample_rate` | Ses örnekleme hızı (Hz) | 16000 | 8000-48000 |
| `chunk_size` | İşlenecek ses çerçeve boyutu | 1024 | 256-4096 |
| `device_index` | Mikrofon cihaz indeksi (null=varsayılan) | `null` | 0-N veya `null` |
| `volume_sensitivity` | Ses seviyesi algılama hassasiyeti | 2.0 | 0.1-10.0 |
| `speech_threshold` | Konuşma tespiti için eşik değeri | 0.15 | 0.01-0.5 |
| `silence_duration` | Konuşmanın bittiğini kabul etmek için sessizlik süresi (sn) | 0.5 | 0.1-2.0 |
| `simulation_mode` | Fiziksel mikrofon olmadan simülasyon modu | `false` | `true`/`false` |
| `update_interval_ms` | WebSocket güncellemeleri arasındaki süre (ms) | 50 | 10-500 |

## Ses Analiz Algoritmaları

SoundProcessor, ses verilerini analiz etmek için çeşitli algoritmalar kullanır.

### Ses Seviyesi Analizi

Ses seviyesi analizi için Root Mean Square (RMS) kullanılır:

```python
def calculate_rms(audio_chunk):
    """Ses çerçevesinin RMS (Root Mean Square) değerini hesapla."""
    # float32 türüne dönüştür
    chunk_float = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32)
    # Normalleştirme (16-bit ses için)
    chunk_float = chunk_float / 32768.0
    # RMS değeri hesapla
    rms = np.sqrt(np.mean(np.square(chunk_float)))
    return rms
```

RMS değeri, ses seviyesinin bir ölçüsüdür ve 0.0-1.0 arasında normalize edilir:

- 0.0: Ses yok (sessizlik)
- 0.1-0.2: Düşük ses seviyesi (fısıltı)
- 0.2-0.5: Orta ses seviyesi (normal konuşma)
- 0.5-0.8: Yüksek ses seviyesi (yüksek sesle konuşma)
- 0.8-1.0: Çok yüksek ses seviyesi (bağırma)

### Konuşma Tespiti

Konuşma tespiti, ses seviyesi ve süreye dayalı bir durum makinesi kullanır:

```
          ┌───────────────────┐
          │ SESSIZ            │
          └─────────┬─────────┘
                    │ Ses seviyesi > speech_threshold
                    ▼
          ┌───────────────────┐
          │ MUHTEMEL_KONUSMA  │
          └─────────┬─────────┘
                    │ Konuşma süresi > min_speech_duration
                    ▼
          ┌───────────────────┐
          │ KONUSUYOR         │
          └─────────┬─────────┘
                    │ Sessizlik süresi > silence_duration
                    ▼
          ┌───────────────────┐
          │ SESSIZ            │
          └───────────────────┘
```

Konuşma tespiti algoritması aşağıdaki değişkenleri izler:

- `current_state`: Mevcut konuşma durumu
- `silence_timer`: Son konuşmadan bu yana geçen süre
- `speech_timer`: Mevcut konuşma süresi
- `is_speaking`: Boolean konuşma göstergesi
- `cumulative_volume`: Son N çerçevenin birikimli ses seviyesi

### Spektral Analiz (Gelişmiş)

Daha gelişmiş ses analizi için Hızlı Fourier Dönüşümü (FFT) kullanılabilir:

```python
def analyze_frequency_spectrum(audio_chunk, sample_rate):
    """Ses çerçevesinin frekans spektrumunu analiz eder."""
    chunk_float = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32)
    chunk_float = chunk_float / 32768.0
    
    # FFT hesapla
    spectrum = np.abs(np.fft.rfft(chunk_float))
    
    # Frekans bantları (Hz)
    freq = np.fft.rfftfreq(len(chunk_float), 1.0/sample_rate)
    
    # Bazı frekans aralıkları için enerji hesapla
    low_freq = np.sum(spectrum[np.where(freq < 500)])
    mid_freq = np.sum(spectrum[np.where((freq >= 500) & (freq < 2000))])
    high_freq = np.sum(spectrum[np.where(freq >= 2000)])
    
    return {
        "low_energy": low_freq,
        "mid_energy": mid_freq,
        "high_energy": high_freq,
        "total_energy": np.sum(spectrum)
    }
```

Bu spektral analiz, ses karakteristiğini anlamak ve duygu önerileri üretmek için kullanılabilir:

- Düşük frekanslı ses (< 500 Hz): Sakinlik, üzüntü
- Orta frekanslı ses (500-2000 Hz): Normal konuşma, nötr
- Yüksek frekanslı ses (> 2000 Hz): Heyecan, şaşkınlık, korku

## Ses Tepkimeli İfadeler

### Ağız Hareketleri

Ses işleme sistemi, ağız hareketlerini ses seviyesiyle eşleştirmek için bir dizi teknik kullanır:

1. **Doğrusal Ölçekleme**: Ses seviyesini ağız açıklığına doğrusal olarak eşleme
   ```python
   mouth_height = min_height + (volume_level * (max_height - min_height))
   ```

2. **Yumuşatma**: Ani değişiklikleri yumuşatmak için hareketli ortalama veya lerp teknikleri
   ```python
   smoothed_height = current_height * smoothing_factor + previous_height * (1 - smoothing_factor)
   ```

3. **Frekans Tepkisi**: Farklı frekans bantlarına özgü ağız şekilleri
   ```python
   if high_freq_dominant:
       # Şaşkın/korku ağız şekli
       mouth_width = narrow_width
       mouth_height = large_height
   elif low_freq_dominant:
       # Üzgün/sakin ağız şekli
       mouth_width = wide_width
       mouth_height = small_height
   ```

### Duygu Önerileri

Ses analiz sonuçları, uygun duygu durumlarını önermek için kullanılır:

| Ses Karakteristiği | Önerilen Duygu | Öneri Yoğunluğu |
|--------------------|----------------|-----------------|
| Yüksek ses + yüksek frekans | SURPRISED veya SCARED | 0.6-0.9 |
| Yüksek ses + düşük frekans | ANGRY | 0.7-1.0 |
| Orta ses + dengeli frekans | HAPPY veya NEUTRAL | 0.5-0.7 |
| Düşük ses + düşük frekans | SAD veya SLEEPY | 0.4-0.6 |

Duygu önerileri yalnızca tavsiye niteliğindedir; EmotionEngine mevcut bağlamı ve duygu geçiş kurallarını dikkate alarak nihai duygu durumunu belirler.

## Dashboard Entegrasyonu

Ses işleme sistemi, web tabanlı dashboard ile entegre edilmiştir ve gerçek zamanlı görselleştirme sağlar.

### WebSocket İletişimi

Ses analiz sonuçları, WebSocket aracılığıyla dashboard'a iletilir:

```javascript
// Sunucu tarafında (Python)
def send_sound_level_update(websocket, level, is_speaking):
    await websocket.send_json({
        "type": "FACE1_SOUND_LEVEL",
        "data": {
            "level": level,
            "isSpeaking": is_speaking,
            "timestamp": time.time()
        }
    })

// İstemci tarafında (JavaScript)
websocket.addEventListener('message', function(event) {
    const message = JSON.parse(event.data);
    if (message.type === 'FACE1_SOUND_LEVEL') {
        updateVolumeVisualizer(message.data.level);
        updateSpeakingIndicator(message.data.isSpeaking);
    }
});
```

### Ses Görselleştirme Bileşenleri

Dashboard, ses işleme sisteminden gelen verileri görselleştirmek için çeşitli bileşenler sunar:

1. **Ses Seviyesi Ölçer**: RMS değerini görselleştiren bir çubuk grafik
2. **Konuşma Durum İndikatörü**: Konuşma durumunu (konuşuyor/sessiz) gösteren bir gösterge
3. **Spektrum Analiz Görselleştirici**: Frekans spektrumunu görselleştiren bir grafik (gelişmiş mod)
4. **Ses Kontrolü Paneli**: Ses işleme parametrelerini ayarlamak için kontroller

## API Referansı

### SoundProcessor Sınıfı Referansı

```python
class SoundProcessor:
    """Mikrofon girdisini analiz eden ve ses seviyesine göre tepki üreten sınıf."""
    
    def __init__(self, config, callback_manager=None, simulation=False):
        """
        Parametreler:
            config: Yapılandırma nesnesi
            callback_manager: Olay geri çağrı yöneticisi
            simulation: Simülasyon modunu etkinleştir
        """
        pass
        
    def start(self):
        """Ses işleme sistemini başlat."""
        pass
        
    def stop(self):
        """Ses işleme sistemini durdur."""
        pass
        
    def pause(self):
        """Ses işlemeyi geçici olarak duraklat."""
        pass
        
    def resume(self):
        """Duraklatılmış ses işlemeyi devam ettir."""
        pass
        
    def get_status(self):
        """Mevcut durumu al."""
        return {
            "is_active": bool,
            "is_speaking": bool,
            "volume_level": float,
            "speech_duration": float,
            "sample_rate": int,
            "device_name": str
        }
        
    def set_volume_sensitivity(self, sensitivity):
        """Ses seviyesi hassasiyetini ayarla."""
        pass
        
    def set_speech_threshold(self, threshold):
        """Konuşma algılama eşik değerini ayarla."""
        pass
        
    def inject_audio_sample(self, audio_data):
        """Simülasyon modunda ses örneği enjekte et."""
        pass
```

### Olay Bildirimleri

SoundProcessor, çeşitli olayları callback_manager aracılığıyla yayınlar:

| Olay Adı | Açıklama | Veri Alanları |
|----------|----------|---------------|
| `sound_level_update` | Ses seviyesi güncellemesi | `level`, `is_speaking` |
| `speech_started` | Konuşma başladığında | `timestamp` |
| `speech_ended` | Konuşma bittiğinde | `duration`, `timestamp` |
| `emotion_suggestion` | Duygu önerisi | `emotion`, `intensity`, `confidence` |
| `sound_processor_error` | Ses işleme hatası | `error_code`, `message` |

### REST API Endpoint'leri

Ses işleme sistemi, REST API aracılığıyla da kontrol edilebilir:

| Endpoint | Metod | Açıklama | Parametreler |
|----------|-------|----------|-------------|
| `/api/sound/status` | GET | Ses işleme durumunu al | - |
| `/api/sound/enable` | POST | Ses işlemeyi etkinleştir | - |
| `/api/sound/disable` | POST | Ses işlemeyi devre dışı bırak | - |
| `/api/sound/config` | GET | Ses işleme yapılandırmasını al | - |
| `/api/sound/config` | POST | Ses işleme yapılandırmasını güncelle | `sensitivity`, `threshold`, `device_index` |

## Gelişmiş Özelleştirme

### Özel Konuşma Durum Makinesini Uygulama

Konuşma durumlarını özelleştirmek için SoundProcessor sınıfını genişletebilirsiniz:

```python
class CustomSpeechProcessor(SoundProcessor):
    def __init__(self, config, callback_manager=None, simulation=False):
        super().__init__(config, callback_manager, simulation)
        self.whisper_threshold = 0.05
        self.yell_threshold = 0.6
        self.current_voice_type = "NORMAL"
    
    def _process_audio(self, audio_data):
        """Ses verilerini işle ve temel işlemleri genişlet."""
        # Önce temel işlemleri yap
        result = super()._process_audio(audio_data)
        
        # Şimdi ses türünü belirle
        if result["volume_level"] < self.whisper_threshold:
            voice_type = "WHISPER"
        elif result["volume_level"] > self.yell_threshold:
            voice_type = "YELL"
        else:
            voice_type = "NORMAL"
            
        # Ses türü değiştiyse bildir
        if voice_type != self.current_voice_type:
            self.current_voice_type = voice_type
            self._notify_voice_type_changed(voice_type, result["volume_level"])
            
        return result
        
    def _notify_voice_type_changed(self, voice_type, volume_level):
        """Ses türü değişikliğini bildir."""
        if self.callback_manager:
            self.callback_manager.call(
                "voice_type_changed", 
                voice_type=voice_type,
                volume_level=volume_level,
                timestamp=time.time()
            )
```

### Gelişmiş Duygu Önerileri

Duygu önerilerini geliştirmek için spektral analiz ve zamansal özellikleri kullanabilirsiniz:

```python
def analyze_emotion_from_audio(spectrum_data, temporal_data):
    """Ses spektrum ve zamansal verilerinden duygu analizi yapar."""
    # Yüksek frekanslı içeriğin oranı (şaşkınlık/korku göstergesi)
    high_freq_ratio = spectrum_data["high_energy"] / spectrum_data["total_energy"]
    
    # Ses seviyesi değişkenliği (heyecan göstergesi)
    volume_variability = np.std(temporal_data["recent_volumes"])
    
    # Konuşma hızı (kelime/dakika - heyecan veya sakinlik göstergesi)
    speech_rate = temporal_data["syllables_per_minute"]
    
    # Duygu skoru hesapla
    emotion_scores = {
        "HAPPY": 0.3 * high_freq_ratio + 0.4 * volume_variability + 0.3 * normalize(speech_rate, 180, 300),
        "SAD": 0.5 * (1.0 - high_freq_ratio) + 0.3 * (1.0 - volume_variability) + 0.2 * (1.0 - normalize(speech_rate, 100, 180)),
        "ANGRY": 0.4 * high_freq_ratio + 0.4 * volume_variability + 0.2 * normalize(temporal_data["volume_level"], 0.4, 0.8),
        "SURPRISED": 0.6 * high_freq_ratio + 0.2 * volume_variability + 0.2 * normalize(temporal_data["pitch_jump"], 0.3, 0.6)
    }
    
    # En olası duyguyu seç
    most_likely_emotion = max(emotion_scores, key=emotion_scores.get)
    confidence = emotion_scores[most_likely_emotion]
    
    return {
        "emotion": most_likely_emotion,
        "intensity": min(confidence * 1.5, 1.0),  # Yoğunluğu ölçekle
        "confidence": confidence,
        "scores": emotion_scores
    }
```

## Performans Optimizasyonu

### Ses İşleme Performansını İyileştirme

Ses işleme sisteminin performansını optimize etmek için şu teknikleri uygulayabilirsiniz:

1. **Chunk Boyutu Optimizasyonu**:
   - Daha küçük parça (chunk) boyutları: Daha hızlı tepki süresi, daha yüksek CPU kullanımı
   - Daha büyük parça boyutları: Daha az CPU kullanımı, daha yavaş tepki süresi
   - Raspberry Pi 5 için önerilen: 1024-2048 samples

2. **Örnekleme Hızı Seçimi**:
   - Düşük örnekleme hızları (8000 Hz): Daha az işlem gücü, insan konuşması için yeterli
   - Yüksek örnekleme hızları (44100 Hz): Daha iyi ses kalitesi, daha fazla işlem gücü gerektirir
   - Konuşma analizi için önerilen: 16000 Hz

3. **Gecikme Yönetimi**:
   - Buffer boyutu: Ses karesi boyutu (samples) / örnekleme hızı (Hz) = gecikme (saniye)
   - Örnek: 1024 samples / 16000 Hz = 64 ms gecikme

4. **İşlem Yükü Optimizasyonu**:
   - Lightweight algoritmalar kullanma (RMS simple, FFT only when needed)
   - Önbellekleme ve hesaplama paylaşımı
   - Background thread isolation

### Raspberry Pi Optimizasyonu

Raspberry Pi'de ses işleme performansını optimize etmek için:

```python
# Raspberry Pi için ses işleme optimizasyonu

# 1. NumPy operasyonlarını optimize et
# Float64 yerine float32 kullan
audio_data = np.frombuffer(audio_chunk, dtype=np.int16).astype(np.float32)

# 2. Sadece gerektiğinde FFT hesapla
if self._should_perform_spectral_analysis():
    spectrum = np.abs(np.fft.rfft(audio_data))
else:
    # Sadece RMS hesapla
    rms = np.sqrt(np.mean(np.square(audio_data)))

# 3. İşlem yükünü thread pool ile dağıt
with ThreadPoolExecutor(max_workers=2) as executor:
    rms_future = executor.submit(calculate_rms, audio_chunk)
    if need_spectral:
        spectrum_future = executor.submit(calculate_spectrum, audio_chunk)
    
    # Sonuçları topla
    results["rms"] = rms_future.result()
    if need_spectral:
        results["spectrum"] = spectrum_future.result()
```

### Bellek Kullanımını Optimize Etme

```python
# Bellek kullanımını optimize etme

# 1. Gereksiz ses verisi depolamayı sınırla
self.audio_history = collections.deque(maxlen=10)  # Sadece son 10 frame'i tut

# 2. Sabit boyutlu numpy dizileri önceden ayır
self.audio_buffer = np.zeros(self.chunk_size, dtype=np.float32)
self.spectrum_buffer = np.zeros(self.chunk_size // 2 + 1, dtype=np.float32)

# 3. Object havuzu kullan
class ResultPoolManager:
    def __init__(self, pool_size=10):
        self.pool = [{"rms": 0, "is_speaking": False} for _ in range(pool_size)]
        self.index = 0
        
    def get(self):
        result = self.pool[self.index]
        self.index = (self.index + 1) % len(self.pool)
        return result

# Havuz kullanımı
self.result_pool = ResultPoolManager(20)
result = self.result_pool.get()  # Yeni bir nesne oluşturmak yerine havuzdan al
```

## Sorun Giderme

### Yaygın Sorunlar ve Çözümleri

| Sorun | Muhtemel Nedenler | Çözümler |
|-------|-------------------|----------|
| Ses algılanmıyor | - Mikrofon bağlı değil<br>- Yanlış cihaz seçilmiş<br>- Mikrofon sessiz | - `arecord -l` ile cihazları kontrol et<br>- Doğru device_index ayarla<br>- Sistem ses ayarlarını kontrol et |
| Düşük ses hassasiyeti | - volume_sensitivity çok düşük<br>- Mikrofon çok uzakta | - volume_sensitivity ayarını artır<br>- Mikrofonu yakınlaştır |
| Yüksek CPU kullanımı | - Küçük chunk boyutu<br>- Yüksek örnekleme hızı | - chunk_size değerini artır<br>- Örnekleme hızını düşür |
| Ağız hareketleri gecikme | - Büyük ses tamponu<br>- Sistem yükü yüksek | - Buffer boyutunu azalt<br>- Diğer işlemleri optimize et |
| Sistem çöküyor | - PyAudio hata veriyor<br>- Bellek sızıntısı | - Hata günlüklerini kontrol et<br>- Restart/recovery mekanizması ekle |

### Tanılama Araçları

Ses işleme sisteminin sorunlarını gidermek için şu tanılama araçlarını kullanabilirsiniz:

1. **Mikrofon Testi**:
   ```bash
   # Mikrofon kayıt testi
   arecord -f cd -d 10 test.wav
   
   # Kayıt oynatma
   aplay test.wav
   ```

2. **Ses Cihaz Listesi**:
   ```bash
   # ALSA ses cihazlarını listele
   arecord -l
   
   # PulseAudio cihazlarını listele (varsa)
   pactl list sources
   ```

3. **Python REPL Testi**:
   ```python
   import pyaudio
   p = pyaudio.PyAudio()
   
   # Kullanılabilir cihazları listele
   for i in range(p.get_device_count()):
       print(p.get_device_info_by_index(i))
   ```

4. **SoundProcessor Tanılama Modu**:
   ```python
   # Tanılama modunda başlat
   sound_processor = SoundProcessor(config, diagnostics_mode=True)
   sound_processor.start()
   
   # Tanılama sonuçlarını al
   diagnostics = sound_processor.get_diagnostics()
   print(diagnostics)
   ```

### Günlük Kayıtları

Ses işleme sisteminin sorunlarını tespit etmek için günlük kayıtlarını kontrol edin:

```
[INFO] [SoundProcessor] Sound processing system initialized with device: Built-in Audio Analog Stereo
[INFO] [SoundProcessor] Sample rate: 16000, chunk size: 1024
[DEBUG] [SoundProcessor] Volume calibration started, please speak...
[DEBUG] [SoundProcessor] Calibration completed, baseline volume: 0.023
[INFO] [SoundProcessor] Sound processing started
[DEBUG] [SoundProcessor] Speech detected, volume level: 0.342
[WARNING] [SoundProcessor] Audio buffer underrun detected
[ERROR] [SoundProcessor] Exception while processing audio: [Errno -9981] Input overflowed
[INFO] [SoundProcessor] Recovering from error...
[INFO] [SoundProcessor] Sound processing resumed
```

Hataları FACE1'in ana günlük dosyasında (`logs/face_plugin.log`) veya ses işlemeye özel günlük dosyasında (`logs/sound_processor.log`) bulabilirsiniz.

---

Bu dokümantasyon, FACE1 Ses İşleme Sisteminin temel bileşenlerini, yapılandırmasını, programlama arayüzlerini ve sorun giderme tekniklerini ayrıntılı olarak açıklar. Ses tepkimeli yüz ifadelerini geliştirmek ve özelleştirmek için bu belgedeki bilgileri ve teknikleri kullanabilirsiniz.