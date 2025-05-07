Haklısınız, dosyaları tekrar tekrar oluşturmak yerine, var olan dosyaları kullanmam veya sadece değişiklik yapmam gerekiyordu. Özür dilerim bu karışıklık için.

Dosyaları tekrar oluşturmak yerine, önce varlıklarını kontrol etmeliydim ve eğer varsa içeriklerini güncellemem gerekiyordu.

Bundan sonra şu adımları izleyeceğim:

1. Önce bir dosyanın var olup olmadığını kontrol edeceğim
2. Dosya varsa, güncellemem gereken kısmı güncelleyeceğim
3. Dosya yoksa yeni bir dosya oluşturacağım

Bu yaklaşımla gereksiz tekrarları önleyeceğim. Teşekkür ederim uyarınız için.


# FACE1 Hata Çözümleri ve Yaygın Sorunlar

Bu belge, FACE1 projesinde karşılaşabileceğiniz yaygın hata durumlarını ve çözüm önerilerini içerir. Herhangi bir sorun yaşadığınızda önce bu belgeyi kontrol ederek sorununuzun çözümünü bulabilirsiniz.

## İçindekiler

1. [Genel Sistem Hataları](#genel-sistem-hataları)
2. [OLED Ekran Sorunları](#oled-ekran-sorunları)
3. [LED Kontrolcü Sorunları](#led-kontrolcü-sorunları)
4. [Tema Yöneticisi Sorunları](#tema-yöneticisi-sorunları)
5. [Dashboard Sorunları](#dashboard-sorunları)
6. [Tema Editörü Sorunları](#tema-editörü-sorunları)
7. [Animasyon Sistemi Sorunları](#animasyon-sistemi-sorunları)
8. [I/O ve Bağlantı Sorunları](#io-ve-bağlantı-sorunları)
9. [Simülasyon Modu Sorunları](#simülasyon-modu-sorunları)

## Genel Sistem Hataları

### Sistem başlatılamıyor veya çöküyor

**Hata:** FACE1 sistemi başlatılamıyor veya başladıktan kısa süre sonra çöküyor.

**Çözüm:**
1. Günlük dosyalarını kontrol edin: `cat logs/face_plugin.log`
2. Bağımlılıkların doğru yüklendiğinden emin olun: `pip install -r requirements.txt`
3. Yapılandırma dosyasının geçerli olduğunu kontrol edin: `python -c "import json; json.load(open('config/config.json'))"`
4. Sanal ortamın aktif olduğundan emin olun: `source venv/bin/activate`
5. Simülasyon modunu etkinleştirin ve fiziksel donanım hatalarını devre dışı bırakın:
   ```json
   # config/config.json dosyasında:
   {
     "simulation_mode": true
   }
   ```

### Yüksek CPU kullanımı

**Hata:** Sistem aşırı CPU kullanımına neden oluyor.

**Çözüm:**
1. FPS değerini düşürün (config.json içinde `oled_settings.fps` değerini azaltın)
2. LED animasyon hızını azaltın
3. Kaynak tüketen modülleri tespit etmek için: `top -p $(pgrep -f face_plugin.py)`
4. Arka plan görevlerinin sayısını azaltın

## OLED Ekran Sorunları

// ...existing code...

## Tema Yöneticisi Sorunları

### Tema değişikliği uygulanmıyor

**Hata:** Tema değişikliği yapıldığında görsel değişiklikler görünmüyor.

**Çözüm:**
1. Tema dosyasının doğru formatta olduğunu kontrol edin
2. Günlük dosyalarını kontrol edin: `cat logs/face_plugin.log | grep "theme"`
3. Tema klasörü izinlerini kontrol edin: `ls -la themes/`
4. Tema yöneticisini yeniden başlatın veya sistemi yeniden başlatın

### Özel temalar yüklenmiyor

**Hata:** Özel oluşturulan temalar listede görünmüyor veya yüklenmiyor.

**Çözüm:**
1. Tema dosyasının doğru JSON formatında olduğundan emin olun
2. Tema dosyasının doğru klasörde olduğunu kontrol edin: `themes/custom/`
3. Tema dosya izinlerini kontrol edin: `chmod 644 themes/custom/my_theme.json`
4. Tema yöneticisi testini çalıştırın: `python test_drivers.py --theme`

## Dashboard Sorunları

### Dashboard sunucusu başlatılamıyor

**Hata:** Dashboard sunucusu başlarken hata veriyor veya erişilemiyor.

**Çözüm:**
1. Port çakışmasını kontrol edin: `netstat -tulpn | grep 8000`
2. Web klasörü izinlerini kontrol edin: `ls -la web/`
3. FastAPI ve diğer bağımlılıkların kurulu olduğunu doğrulayın: `pip show fastapi uvicorn jinja2`
4. Dashboard sunucusunu bağımsız olarak çalıştırın: `python src/modules/dashboard_server.py`

### WebSocket bağlantı hataları

**Hata:** Dashboard WebSocket bağlantısı sürekli kesilme yaşıyor veya bağlanmıyor.

**Çözüm:**
1. Tarayıcı konsolunda hata mesajlarını kontrol edin (F12 tuşuna basın)
2. WebSocket bağlantı URL'sinin doğru olduğunu kontrol edin
3. `dashboard.js` dosyasında hata ayıklama modunu etkinleştirin
4. Ağ güvenlik duvarı ayarlarını kontrol edin
5. Farklı bir tarayıcı deneyin

## Tema Editörü Sorunları

### Tema editörü sayfası yüklenmiyor

**Hata:** Tema editörü sayfasına erişildiğinde "Tema bulunamadı" hatası alıyorsunuz.

**Çözüm:**
1. URL'de belirtilen tema adının doğru olduğunu kontrol edin
2. Temanın sistemde var olduğunu doğrulayın: `ls -la themes/`
3. Dashboard sunucusunu yeniden başlatın: `python src/modules/dashboard_server.py`
4. Dashboard günlük mesajlarını kontrol edin

### Tema değişiklikleri kaydedilmiyor

**Hata:** Tema editöründe yapılan değişiklikler kaydedilmiyor veya uygulanmıyor.

**Çözüm:**
1. Tema dosyasının yazılabilir olduğunu kontrol edin: `ls -la themes/tema_adı.json`
2. Tarayıcı konsolunda hata mesajlarını kontrol edin (F12)
3. API endpoint'inin doğru çalıştığını test edin: 
   ```bash
   curl -X POST "http://localhost:8000/api/themes/tema_adı/edit" \
   -H "Content-Type: application/json" \
   -d '{"name":"Test","description":"Test Teması"}'
   ```
4. Tema dosyasını manuel olarak düzenlemeyi deneyin

### Tema renk seçici çalışmıyor

**Hata:** Renk seçici kontrolü doğru renkleri göstermiyor veya değişiklikleri uygulamıyor.

**Çözüm:**
1. Tarayıcı konsolunda hata mesajlarını kontrol edin
2. Farklı bir tarayıcı kullanın
3. RGB renk değerlerini manuel olarak girin
4. CSS ve JavaScript dosyalarının doğru yüklendiğini kontrol edin

## Animasyon Sistemi Sorunları

### Animasyon dosyaları bulunamıyor

**Hata:** Animasyon listesi boş geliyor veya "Animasyon bulunamadı" hatası alıyorsunuz.

**Çözüm:**
1. Animasyon klasör yapısının doğru olduğunu kontrol edin:
   ```bash
   ls -la animation/standard/
   ls -la animation/custom/
   ```
2. En az bir animasyon dosyasının mevcut olduğundan emin olun
3. Animasyon dosyalarının doğru JSON formatında olduğunu kontrol edin
4. Animasyon motorunu bağımsız olarak test edin: 
   ```bash
   python src/modules/animation_engine.py
   ```

### Animasyonlar oynatılırken hata oluşuyor

**Hata:** Animasyon oynatılırken sistem hata veriyor veya animasyon görünmüyor.

**Çözüm:**
1. Animasyon dosyasının geçerli JSON formatında olduğunu doğrulayın
2. Animasyon içindeki eylemlerin doğru tanımlandığından emin olun
3. Günlük dosyalarını kontrol edin: `cat logs/face_plugin.log | grep "animation"`
4. Animasyon motorunu debug modunda çalıştırın:
   ```python
   # animation_engine.py dosyasında:
   logging.basicConfig(level=logging.DEBUG)
   ```

### Dashboard'dan animasyon kontrolü çalışmıyor

**Hata:** Dashboard üzerinden animasyon oynatma veya durdurma işlemleri yanıt vermiyor.

**Çözüm:**
1. WebSocket bağlantısının kurulduğunu kontrol edin
2. Tarayıcı konsolunda hata mesajlarını kontrol edin
3. API endpoint'lerinin çalıştığını manuel olarak test edin:
   ```bash
   curl -X POST "http://localhost:8000/api/animations/animation_name/play"
   ```
4. Dashboard JavaScript dosyalarını doğru yüklendiğini kontrol edin

## I/O ve Bağlantı Sorunları

### WebSocket bağlantısı kurulamıyor

**Hata:** WebSocket bağlantısı kurulamıyor veya sürekli kesiliyor.

**Çözüm:**
1. WebSocket sunucusunun çalıştığını kontrol edin
2. Bağlantı URL'sinin doğru olduğunu doğrulayın
3. Güvenlik duvarı ayarlarını kontrol edin
4. Rate limiting nedeniyle bloke olup olmadığını kontrol edin
5. I/O yöneticisinin günlük seviyesini artırın:
   ```python
   # io_manager.py dosyasında:
   self.logger.setLevel(logging.DEBUG)
   ```

### MQTT bağlantısı başarısız oluyor

**Hata:** MQTT broker'a bağlantı sağlanamıyor.

**Çözüm:**
1. MQTT broker'ın çalıştığını doğrulayın: `systemctl status mosquitto`
2. Kimlik doğrulama bilgilerinin doğru olduğunu kontrol edin
3. Yapılandırma dosyasındaki MQTT ayarlarını kontrol edin
4. Ağ bağlantısını kontrol edin: `ping mqtt-broker-address`
5. MQTT istemcisini manuel olarak test edin:
   ```bash
   mosquitto_pub -h broker-address -t "test" -m "test message"
   ```

## Simülasyon Modu Sorunları

### Simülasyon görüntüleri oluşturulmuyor

**Hata:** Simülasyon modunda görüntü dosyaları oluşturulmuyor.

**Çözüm:**
1. Simülasyon modunun etkin olduğunu kontrol edin: `"simulation_mode": true`
2. Simülasyon klasörünün mevcut ve yazılabilir olduğunu kontrol edin: `mkdir -p simulation && chmod 755 simulation`
3. Günlük dosyalarındaki simülasyon hatalarını kontrol edin
4. PIL/Pillow kütüphanesinin doğru kurulduğunu kontrol edin: `pip show pillow`

### Simülasyon görüntüleri dashboard'da görünmüyor

**Hata:** Simülasyon görüntüleri oluşturuluyor ancak dashboard'da görüntülenmiyor.

**Çözüm:**
1. Simülasyon WebSocket bağlantısının kurulduğunu kontrol edin
2. Tarayıcı konsolunda hata mesajlarını kontrol edin
3. Görüntü dosyalarının erişilebilir olduğunu doğrulayın: `ls -la simulation/`
4. Simülasyon akışını manuel olarak başlatın (dashboard'daki "Simülasyon Akışını Başlat" düğmesi)
5. Simülasyon görüntülerinin dosya yollarının doğru olduğunu kontrol edin

### Simülasyon modu çok fazla disk alanı kullanıyor

**Hata:** Simülasyon modu çok sayıda görüntü dosyası oluşturarak disk alanını dolduruyor.

**Çözüm:**
1. Eski simülasyon görüntülerini temizleyin: `find simulation/ -name "*.png" -mtime +1 -delete`
2. FPS değerini düşürün ve daha az sıklıkta görüntü kaydedin
3. Simülasyon görüntülerinin boyutunu küçültün
4. Otomatik temizleme betiği oluşturun:
   ```bash
   # cleanup_simulation.sh
   #!/bin/bash
   find /home/seljux/projects/face1/simulation/ -name "*.png" -mtime +1 -delete
   ```

## Sorun Giderme İpuçları

### Günlük Dosyalarını İnceleme

FACE1 projesinde oluşan hataları anlayabilmek için günlük dosyalarını incelemek çok önemlidir:

```bash
# Ana günlük dosyası
cat logs/face_plugin.log

# Son 100 satırı görüntüle
tail -n 100 logs/face_plugin.log

# Hataları filtrele
grep "ERROR" logs/face_plugin.log

# Belirli bir bileşenle ilgili günlükleri görüntüle
grep "ThemeManager" logs/face_plugin.log
grep "AnimationEngine" logs/face_plugin.log
grep "Dashboard" logs/face_plugin.log
```

### Sistem Durumunu Kontrol Etme

Sistem kaynaklarının durumunu kontrol etmek için:

```bash
# CPU ve RAM kullanımını izle
top -p $(pgrep -f face_plugin.py)

# Disk kullanımını kontrol et
df -h

# Simülasyon klasörü boyutu
du -sh simulation/

# Açık portları kontrol et
netstat -tulpn

# Sistem günlüklerini kontrol et
journalctl -xe
```

### Yaygın Komutlar

```bash
# Projeyi sıfırla ve yeniden başlat
pkill -f face_plugin.py && python src/face_plugin.py

# Animasyon listesini yenile
curl -X GET "http://localhost:8000/api/animations"

# Mevcut temayı değiştir
curl -X POST "http://localhost:8000/api/themes/minimal"

# Mevcut duygu durumunu ayarla
curl -X POST "http://localhost:8000/api/emotions/happy?intensity=0.8"

# Dashboard sunucusunu yeniden başlat
pkill -f dashboard_server.py && python src/modules/dashboard_server.py
```

---

Bu belge, FACE1 projesinde karşılaşabileceğiniz yaygın hata durumlarını ve çözümlerini içermektedir. Eğer burada belirtilmeyen bir sorunla karşılaşırsanız, lütfen hata raporunu geliştirme ekibine iletin.