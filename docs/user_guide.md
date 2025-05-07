# FACE1 Kullanıcı Kılavuzu

## İçindekiler
- [Giriş](#giriş)
- [Kurulum](#kurulum)
- [Başlangıç](#başlangıç)
- [Dashboard Arayüzü](#dashboard-arayüzü)
- [Duygu Kontrolü](#duygu-kontrolü)
- [Temalar ve Görünüm](#temalar-ve-görünüm)
- [Animasyonlar](#animasyonlar)
- [Ses Tepkimeli Özellikler](#ses-tepkimeli-özellikler)
- [Simülasyon Modu](#simülasyon-modu)
- [API Kullanımı](#api-kullanımı)
- [Üst Proje Entegrasyonu](#üst-proje-entegrasyonu)
- [Yapılandırma Ayarları](#yapılandırma-ayarları)
- [Sorun Giderme](#sorun-giderme)
- [SSS](#sss)

## Giriş

Bu kılavuz, FACE1 yüz eklentisinin kurulumu, yapılandırılması ve günlük kullanımı için kapsamlı bir rehberdir. FACE1, Raspberry Pi 5 tabanlı robotlar için geliştirilen ve duygu ifadeleri gösterebilen bir yüz eklentisidir. OLED ekranlar ve LED şeritler kullanarak çeşitli duygu durumlarını görselleştirme yeteneğine sahiptir.

### FACE1 Nedir?

FACE1, üç OLED ekran (sol göz, sağ göz ve ağız) ve WS2812 LED şeritler kullanarak robotunuza duygu ifadeleri kazandıran bir sistemdir. Özellikler:

- Çeşitli duygu ifadeleri (mutlu, üzgün, kızgın, şaşkın vb.)
- Duygu geçişleri ve mikro ifadeler
- Özelleştirilebilir temalar ve animasyonlar
- Web tabanlı kontrol paneli
- Ses tepkimeli ifadeler (mikrofon aracılığıyla)
- Üst projelere entegrasyon için API

### Kullanım Senaryoları

FACE1 aşağıdaki senaryolar için idealdir:
- İnsan-robot etkileşimi uygulamaları
- Eğitim amaçlı robotlar
- Sosyal robotlar ve asistanlar
- Sanat ve eğlence projeleri
- Araştırma ve geliştirme platformları

## Kurulum

### Donanım Gereksinimleri

- Raspberry Pi 5 (veya uyumlu bir bilgisayar)
- 3 adet SSD1306 OLED ekran (128x64, monokrom)
- TCA9548A I2C çoğaltıcı (çoklu ekran yönetimi için)
- WS2812B LED şeritleri
- Mikrofon (ses tepkimeli sistem için)

### Donanım Bağlantıları

#### OLED Ekran Bağlantıları (I2C)

| OLED Pin | Raspberry Pi Pin |
|----------|-----------------|
| VCC      | 3.3V/5V         |
| GND      | GND             |
| SCL      | GPIO 3 (SCL1)   |
| SDA      | GPIO 2 (SDA1)   |

#### TCA9548A (I2C Çoğaltıcı) Bağlantıları

| TCA9548A Pin | Raspberry Pi Pin |
|--------------|-----------------|
| VCC          | 3.3V/5V         |
| GND          | GND             |
| SCL          | GPIO 3 (SCL1)   |
| SDA          | GPIO 2 (SDA1)   |
| A0-A2        | GND (adres 0x70 için) |

#### WS2812B LED Şeridi Bağlantıları

| LED Pin | Raspberry Pi Pin |
|---------|-----------------|
| VCC     | 5V (harici güç kaynağı önerilir) |
| GND     | GND             |
| DIN     | GPIO 18 (PWM)   |

### Yazılım Kurulumu

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

3. Mikrofon kurulumu (ses tepkimeli özellikler için):
   ```bash
   # Debian/Ubuntu/Raspberry Pi OS
   sudo apt-get install python3-pyaudio
   
   # veya pip ile kurulum
   pip install pyaudio
   ```

4. Yapılandırmayı özelleştirin:
   ```bash
   cp config/default_config.json config/user_config.json
   # Metin editörü ile user_config.json dosyasını düzenleyin
   ```

## Başlangıç

### İlk Çalıştırma

FACE1'i başlatmak için şu komutu çalıştırın:

```bash
./run_face.sh
```

Bu komut aşağıdakileri yapar:
1. Sanal ortamı etkinleştirir
2. Yapılandırma dosyasını yükler
3. Donanımı başlatır
4. Web sunucusunu başlatır
5. WebSocket sunucusunu başlatır

### Dashboard'a Erişim

Web tarayıcınızda aşağıdaki URL'yi açarak dashboard'a erişebilirsiniz:

```
http://localhost:8000
```

veya Raspberry Pi'nizin IP adresi üzerinden:

```
http://[RaspberryPi-IP-Adresi]:8000
```

## Dashboard Arayüzü

Dashboard arayüzü, FACE1'in tüm özelliklerini kontrol etmenizi sağlar.

### Ana Bileşenler

![Dashboard Arayüzü](images/dashboard_layout.png)

1. **Durum Paneli**: Sistemin genel durumu, çalışma süresi ve mevcut duygu durumu
2. **Duygu Kontrol Paneli**: Duygu durumunu ve yoğunluğunu ayarlama kontrolleri
3. **Tema Seçici**: Farklı görsel temalar arasında geçiş yapma
4. **Animasyon Kontrolleri**: Animasyonları oynatma ve durdurma
5. **Simülasyon Görüntüleri**: Ekranların ve LED'lerin gerçek zamanlı simülasyonu
6. **Yapılandırma Editörü**: Sistem ayarlarını düzenleme
7. **Ses Görselleştirici**: Ses seviyesi ve konuşma durumu göstergeleri (v0.5.0+)

### Klavye Kısayolları

| Kısayol       | İşlev                       |
|---------------|----------------------------|
| F1            | Yardım menüsünü göster     |
| 1-8           | Ana duyguları seç          |
| +/-           | Duygu yoğunluğunu ayarla   |
| A             | Animasyon listesini göster |
| T             | Tema seçiciyi göster       |
| S             | Simülasyon modunu aç/kapat |
| P             | Sistemi duraklat/devam et  |

## Duygu Kontrolü

FACE1, çeşitli duygu durumlarını ve ifadeleri destekler.

### Temel Duygular

| Duygu    | Tanım                                       | Örnek Kullanım               |
|----------|---------------------------------------------|------------------------------|
| NEUTRAL  | Nötr, ifadesiz durum                        | Bekleme veya dinleme durumu |
| HAPPY    | Mutluluk, neşe                              | Olumlu sonuçlar, başarılar  |
| SAD      | Üzüntü, keder                              | Olumsuz sonuçlar, başarısızlıklar |
| ANGRY    | Kızgınlık, öfke                            | Hata durumları, engeller    |
| SURPRISED| Şaşkınlık, hayret                          | Beklenmedik olaylar        |
| SCARED   | Korku, endişe                              | Tehlike durumları           |
| DISGUSTED| Tiksinti, hoşnutsuzluk                     | Uygun olmayan durumlar      |
| SLEEPY   | Uykulu, yorgun                             | Düşük pil, bekleme modu     |

### Duygu Alt Tipleri

Her temel duygu için farklı alt tipler (varyasyonlar) mevcuttur. Örneğin:

- **HAPPY** duygusu için alt tipler:
  - `excited`: Heyecanlı, enerjik
  - `content`: Memnun, tatmin
  - `amused`: Eğlenen, gülen
  - `proud`: Gururlu
  - `loving`: Sevgi dolu

### Duygu Yoğunluğu

Duygular farklı yoğunluk seviyelerinde (0.0-1.0) ifade edilebilir:
- 0.0: Hiç (nötr ifadeye yakın)
- 0.5: Orta yoğunlukta
- 1.0: Tam yoğunlukta

### Duygu Kontrol Yöntemleri

Duygu durumlarını ayarlamanın çeşitli yolları:

1. **Dashboard Arayüzü**: Duygu kontrol panelini kullanarak
2. **REST API**: HTTP istekleri göndererek
   ```bash
   curl -X POST http://localhost:8000/emotion/happy -d "intensity=0.8"
   ```
3. **WebSocket**: Gerçek zamanlı komutlar göndererek
4. **Ses Tepkileri**: Mikrofonla algılanan seslere tepki olarak (otomatik)

## Temalar ve Görünüm

FACE1, çeşitli görsel temalar sunar.

### Varsayılan Temalar

FACE1, şu varsayılan temalarla gelir:
- **default**: Standart, dengeli ifadeler
- **pixel**: Piksel sanatı tarzında ifadeler
- **minimal**: Minimalist, basitleştirilmiş ifadeler
- **realistic**: Daha detaylı, gerçekçi ifadeler

### Tema Seçimi

Temayı değiştirmenin birkaç yolu vardır:

1. **Dashboard**: Tema seçici bölümünden seçim yaparak
2. **API**: REST API kullanarak
   ```bash
   curl -X POST http://localhost:8000/theme/pixel
   ```
3. **Yapılandırma**: Config dosyasında varsayılan temayı ayarlayarak

### Özel Tema Oluşturma

Özel bir tema oluşturmak için:

1. `themes/` klasöründe yeni bir klasör oluşturun:
   ```bash
   mkdir -p themes/my_theme/{eyes,mouth}
   ```

2. `theme.json` dosyası oluşturun:
   ```json
   {
     "name": "my_theme",
     "display_name": "Benim Temam",
     "description": "Özel temam",
     "author": "Adınız",
     "version": "1.0.0",
     "emotion_mappings": { ... }
   }
   ```

3. Göz ve ağız ifadeleri için PNG dosyaları ekleyin
4. Tema Editörü'nü kullanarak temayı düzenleyin ve test edin

## Animasyonlar

FACE1, çeşitli senkronize animasyonlar çalıştırabilir.

### Yerleşik Animasyonlar

| Animasyon Adı      | Açıklama                                     | Süre (sn) |
|--------------------|----------------------------------------------|-----------|
| startup_animation  | Başlangıç animasyonu                         | 5.0       |
| emotion_transition | Duygu geçişi animasyonu                      | 2.0       |
| speaking           | Konuşma animasyonu                           | 3.0       |
| happy_dance        | Mutlu duygu animasyonu                       | 4.0       |
| surprise_reaction  | Şaşkınlık tepkisi animasyonu                 | 2.5       |
| hello_animation    | Selamlama animasyonu                         | 4.0       |

### Animasyon Oynatma

Animasyonları oynatmanın çeşitli yolları:

1. **Dashboard**: Animasyon kontrol panelinden seçerek
2. **API**: REST API kullanarak
   ```bash
   curl -X POST http://localhost:8000/api/animations/hello_animation/play
   ```
3. **WebSocket**: Gerçek zamanlı komutlar göndererek
4. **Programlanmış Olaylar**: Belirli sistem olayları sırasında otomatik olarak

### Özel Animasyon Oluşturma

Özel animasyonlar, JSON formatında tanımlanır ve `animation/custom/` klasöründe saklanır:

1. Yeni bir JSON dosyası oluşturun:
   ```bash
   touch animation/custom/my_animation.json
   ```

2. Animasyonu tanımlayın:
   ```json
   {
     "metadata": {
       "name": "my_animation",
       "display_name": "Özel Animasyonum",
       "description": "Benim özel animasyonum",
       "duration": 3.0
     },
     "sequence": [
       {
         "time": 0.0,
         "eyes": { "action": "clear", "params": {} }
       },
       {
         "time": 1.0,
         "mouth": { "action": "smile", "params": { "width": 0.8 } }
       }
     ]
   }
   ```

3. Dashboard'daki Animasyon Editörü'nü kullanarak animasyonu test edin ve düzenleyin

## Ses Tepkimeli Özellikler

FACE1 v0.5.0'dan itibaren ses tepkimeli özellikler sunar, bu sayede robot yüzü konuşma ve ses seviyesine göre tepki verebilir.

### Temel Özellikler

- **Ses Seviyesi Algılama**: Ortam ses seviyesini gerçek zamanlı ölçer
- **Konuşma Tespiti**: İnsan konuşmasını tespit eder
- **Ağız Senkronizasyonu**: Ağız hareketlerini ses seviyesiyle senkronize eder
- **Duygu Önerileri**: Ses karakteristiğine göre duygu durumları önerir

### Kurulum ve Yapılandırma

1. Mikrofon bağlantısını kontrol edin
2. Yapılandırma dosyasında ses işleme ayarlarını düzenleyin:
   ```json
   "sound_processor": {
     "enabled": true,
     "sample_rate": 16000,
     "volume_sensitivity": 2.0,
     "speech_threshold": 0.15
   }
   ```

3. Dashboard'daki Ses İşleme bölümünden ayarları yapın

### Kullanım

Ses tepkimeli özellikleri kullanmak için:

1. Dashboard'da Ses İşleme panelini açın
2. "Ses Tepkimeli İfadeler" özelliğini etkinleştirin
3. Konuştuğunuzda, FACE1 ağız hareketlerini konuşmanızla senkronize edecektir
4. Sesinizin karakteristiğine göre duygu önerileri sunacaktır

## Simülasyon Modu

FACE1, fiziksel donanım olmadan geliştirme ve test yapmanıza olanak tanıyan bir simülasyon modu sunar.

### Simülasyon Modunu Etkinleştirme

Simülasyon modunu etkinleştirmek için:

1. Yapılandırma dosyasında ayarı değiştirin:
   ```json
   "simulation": {
     "enabled": true,
     "output_directory": "simulation/",
     "frame_rate": 10
   }
   ```

2. Veya dashboard'dan "Simülasyon Modu" düğmesini kullanın

### Simülasyon Çıktıları

Simülasyon çıktıları `simulation/` klasöründe saklanır:
- `display_left_eye_*.png`: Sol göz simülasyon görüntüleri
- `display_right_eye_*.png`: Sağ göz simülasyon görüntüleri
- `display_mouth_*.png`: Ağız simülasyon görüntüleri
- `leds_*.png`: LED simülasyon görüntüleri

### Dashboard'da İzleme

Simülasyon görüntülerini dashboard üzerinden gerçek zamanlı olarak izleyebilirsiniz:

1. Dashboard'da "Simülasyon" sekmesini açın
2. Resimlerin gerçek zamanlı olarak güncellendiğini göreceksiniz
3. "Kaydet" düğmesiyle mevcut durumu kaydedebilirsiniz

## API Kullanımı

FACE1, harici sistemler ve uygulamalar için kapsamlı bir API sunar.

### REST API

#### Temel Endpoint'ler

| Endpoint                      | Metod | Açıklama                           |
|------------------------------|-------|-----------------------------------|
| `/status`                    | GET   | Sistem durumunu döndürür           |
| `/emotion/{emotion}`         | POST  | Belirtilen duyguyu ayarlar         |
| `/transition/{emotion}`      | POST  | Duyguya yumuşak geçiş yapar       |
| `/theme/{theme_name}`        | POST  | Temayı değiştirir                 |
| `/api/animations/{name}/play`| POST  | Animasyonu oynatır                |
| `/api/animations/stop`       | POST  | Animasyonu durdurur               |

#### Örnek API Kullanımı

```bash
# Sistem durumunu sorgulama
curl -X GET http://localhost:8000/status

# Duygu durumunu ayarlama
curl -X POST http://localhost:8000/emotion/happy -d "intensity=0.8"

# Tema değiştirme
curl -X POST http://localhost:8000/theme/pixel

# Animasyon oynatma
curl -X POST http://localhost:8000/api/animations/hello_animation/play
```

### WebSocket API

WebSocket API, gerçek zamanlı güncellemeler ve komutlar için kullanılır.

#### Bağlantı

```javascript
const ws = new WebSocket('ws://localhost:8000/ws');

ws.onopen = () => {
  console.log('Bağlantı kuruldu');
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  console.log('Mesaj alındı:', message);
};
```

#### Komut Gönderme

```javascript
// Duygu ayarlama
ws.send(JSON.stringify({
  type: 'command',
  command: 'setEmotion',
  data: {
    emotion: 'happy',
    intensity: 0.8
  }
}));

// Animasyon oynatma
ws.send(JSON.stringify({
  type: 'command',
  command: 'playAnimation',
  data: {
    animation: 'hello_animation'
  }
}));
```

## Üst Proje Entegrasyonu

FACE1, başka projelere kolayca entegre edilebilir.

### IFrame Entegrasyonu

FACE1'i IFrame olarak üst projenize entegre etmek için:

1. FACE1 dashboard'unu bir IFrame içinde gösterin:
   ```html
   <iframe id="face1-frame" src="http://localhost:8000/embed" width="800" height="600"></iframe>
   ```

2. postMessage API'sini kullanarak iletişim kurun:
   ```javascript
   // FACE1'e mesaj gönderme
   function sendMessageToFace1(type, data) {
     document.getElementById('face1-frame').contentWindow.postMessage({
       type: type,
       data: data,
       timestamp: Date.now()
     }, 'http://localhost:8000');
   }

   // Örnek: Duygu ayarlama
   sendMessageToFace1('FACE1_SET_EMOTION', { 
     emotion: 'happy', 
     intensity: 0.8 
   });
   ```

3. FACE1'den gelen mesajları dinleyin:
   ```javascript
   window.addEventListener('message', function(event) {
     if (event.origin !== 'http://localhost:8000') return;
     console.log('FACE1\'den mesaj:', event.data);
   });
   ```

### Durum Yansıtma Protokolü

Üst proje ve FACE1 arasında durum senkronizasyonu için:

1. StateReflector sınıfını kullanın:
   ```javascript
   // FACE1 tarafında durum değişikliğini üst projeye bildirme
   stateReflector.notifyParent('emotionChanged', {
     emotion: 'happy', 
     intensity: 0.8
   });
   
   // Üst projede durum değişikliklerini dinleme
   window.addEventListener('message', function(event) {
     if (event.data.type === 'FACE1_STATE_CHANGE') {
       console.log('Durum değişikliği:', event.data.stateType, event.data.state);
     }
   });
   ```

## Yapılandırma Ayarları

FACE1'in davranışını yapılandırmak için çeşitli ayarlar mevcuttur.

### Yapılandırma Dosyası Yapısı

Yapılandırma dosyası (`config.json`), farklı bölümlere ayrılmıştır:

1. **system**: Genel sistem ayarları
2. **oled**: Ekran kontrol ayarları
3. **leds**: LED kontrol ayarları
4. **emotions**: Duygu motoru ayarları
5. **animation**: Animasyon sistemi ayarları
6. **sound_processor**: Ses işleme ayarları
7. **simulation**: Simülasyon modu ayarları
8. **dashboard**: Web arayüzü ayarları

### Önemli Yapılandırma Ayarları

| Ayar                           | Açıklama                                | Varsayılan Değer |
|--------------------------------|-----------------------------------------|-----------------|
| `system.log_level`             | Günlük kaydı ayrıntı seviyesi           | "INFO"          |
| `oled.brightness`              | OLED ekran parlaklığı (0-255)           | 128             |
| `oled.blink_frequency`         | Göz kırpma sıklığı (kere/dakika)        | 4.5             |
| `leds.brightness`              | LED parlaklığı (0-255)                  | 128             |
| `emotions.default_emotion`     | Varsayılan duygu durumu                 | "neutral"       |
| `emotions.micro_expressions_enabled` | Mikro ifadeleri etkinleştir/devre dışı bırak | true |
| `sound_processor.enabled`      | Ses işleme özelliklerini etkinleştir    | true            |
| `sound_processor.volume_sensitivity` | Ses seviyesi hassasiyeti (1.0-5.0) | 2.0           |
| `animation.fps`                | Saniyedeki kare sayısı                  | 30              |

### Ayarları Değiştirme

Yapılandırma ayarlarını değiştirmenin yolları:

1. **Metin Editörü**: `config/user_config.json` dosyasını doğrudan düzenleyerek
2. **Dashboard**: Yapılandırma Editörü arayüzünü kullanarak
3. **API**: REST API üzerinden:
   ```bash
   curl -X POST http://localhost:8000/api/config/update \
     -H "Content-Type: application/json" \
     -d '{"oled":{"brightness":200}}'
   ```

## Sorun Giderme

FACE1 ile ilgili yaygın sorunların çözümleri.

### Başlangıç Sorunları

| Sorun                         | Çözüm                                   |
|------------------------------|----------------------------------------|
| FACE1 başlatılamıyor         | - Bağımlılıkların kurulduğunu doğrulayın<br>- Günlük dosyalarını kontrol edin<br>- İzinleri kontrol edin |
| "Port zaten kullanımda" hatası | - Başka bir dashboard örneğinin çalışmadığını doğrulayın<br>- `ps aux \| grep dashboard` ile kontrol edin<br>- Portu değiştirin |
| Yapılandırma hatası          | - `config.json` dosyasının doğru JSON formatında olduğunu doğrulayın |

### Donanım Sorunları

| Sorun                         | Çözüm                                   |
|------------------------------|----------------------------------------|
| OLED ekranlar çalışmıyor     | - I2C bağlantılarını kontrol edin<br>- `i2cdetect -y 1` ile I2C adreslerini doğrulayın<br>- OLED ekranları başka bir projede test edin |
| LED'ler yanmıyor             | - Güç kaynağını kontrol edin<br>- GPIO pin yapılandırmasını doğrulayın<br>- `config.json` içinde `leds.enabled` ayarını kontrol edin |
| Mikrofon çalışmıyor          | - Ses kartı/mikrofon bağlantısını kontrol edin<br>- `arecord -l` ile ses cihazlarını listeleyin<br>- Yapılandırma dosyasında doğru cihazı ayarlayın |

### Yazılım Sorunları

| Sorun                         | Çözüm                                   |
|------------------------------|----------------------------------------|
| Yanlış/eksik ifadeler        | - Tema dosyalarını kontrol edin<br>- `animation/` klasöründeki dosyaları doğrulayın<br>- Simülasyon modunu kullanarak görsel çıktıyı doğrulayın |
| Dashboard erişim sorunu      | - Web sunucusunun çalıştığını doğrulayın<br>- Ağ ayarlarını ve güvenlik duvarını kontrol edin<br>- Farklı bir tarayıcı deneyin |
| API/WebSocket hatası         | - URL ve port numaralarını doğrulayın<br>- İstek formatını kontrol edin<br>- Tarayıcı hata konsolunu kontrol edin |

## SSS

### Genel Sorular

**S: FACE1 hangi Raspberry Pi modelleriyle çalışır?**  
C: FACE1 öncelikle Raspberry Pi 5 için geliştirilmiştir, ancak Raspberry Pi 4 ve 3B+ ile de uyumludur. Daha eski modellerde performans sınırlamaları olabilir.

**S: LED şeritler için ayrı bir güç kaynağı gerekli mi?**  
C: Evet, özellikle uzun LED şeritler kullanıyorsanız veya yüksek parlaklık ayarlarında çalıştırıyorsanız ayrı bir 5V güç kaynağı önerilir. Raspberry Pi'nin güç sınırlamaları, çok sayıda LED için yeterli olmayabilir.

**S: Maksimum kaç LED kullanabilirim?**  
C: Varsayılan yapılandırma, 60 LED'e kadar test edilmiştir. Daha fazla LED kullanmak istiyorsanız performans ve güç tüketimi sorunlarını dikkate almanız gerekecektir.

### Özelleştirme Soruları

**S: Farklı boyutlarda veya türlerde OLED ekranlar kullanabilir miyim?**  
C: FACE1 varsayılan olarak 128x64 piksel monokrom SSD1306 OLED ekranlar için tasarlanmıştır. Farklı ekran türleri veya çözünürlükleri kullanmak için kaynak kodunun ilgili bölümleri değiştirilmelidir.

**S: Yeni duygu türleri ekleyebilir miyim?**  
C: Evet, `emotion_states.py` dosyasını düzenleyerek ve yeni duygular için tema varlıkları ekleyerek yeni duygular tanımlayabilirsiniz.

**S: FACE1 uzaktan kontrol edilebilir mi?**  
C: Evet, FACE1 REST API ve WebSocket arayüzleri üzerinden uzaktan kontrol edilebilir. Güvenli erişim için ağ yapılandırmanızı uygun şekilde ayarlamanız önerilir.

### Teknik Sorular

**S: FACE1 ne kadar bellek kullanır?**  
C: Normal çalışmada yaklaşık 30MB RAM kullanır. Bu, kullanılan tema ve animasyonların karmaşıklığına bağlı olarak değişebilir.

**S: FACE1'i donanım olmadan test edebilir miyim?**  
C: Evet, simülasyon modunu etkinleştirerek fiziksel donanım olmadan geliştirme yapabilirsiniz. Bu mod, ekranların ve LED'lerin durumunu görsel olarak simüle eder.

**S: Ses tanıma özellikleri var mı?**  
C: FACE1, ses seviyesi ve konuşma durumunu algılayan basit ses analizi özellikleri içerir, ancak tam ses tanıma işlevselliği sunmaz. İleri ses tanıma için harici bir sistemle entegre edilmesi gerekir.

---

Bu kılavuz, FACE1 yüz eklentisinin temel ve ileri kullanımı hakkında kapsamlı bilgiler sağlar. Daha fazla bilgi veya yardım için proje dokümantasyonuna veya destek kanallarına başvurun.