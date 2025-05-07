FACE1 Robot projenizdeki tüm web panel adreslerini listeleyeceğim. Bu adreslere web tarayıcınız üzerinden erişebilirsiniz.

İlk olarak, proje yapısını ve ilgili dosyaları inceleyerek web adreslerini toplayacağım.FACE1 Robot projesinin tüm web panel adreslerini derledim. Bu adreslere erişmek için dashboard sunucusunu çalıştırmanız gerekir. Sunucuyu başlatmak için şu komutu kullanabilirsiniz:

```
python src/modules/dashboard_server.py
```

Sunucu varsayılan olarak http://localhost:8000 adresinde çalışır.

## Ana Sayfalar ve Web Arayüzleri:

1. **Ana Dashboard**: http://localhost:8000
   - Robot durumunu görüntüleme ve kontrol etme

2. **Tema Editörü**: http://localhost:8000/theme-editor/{tema_adi}
   - Belirli bir temayı düzenleme (örn: http://localhost:8000/theme-editor/default)

3. **Animasyon Editörü**: http://localhost:8000/animation-editor
   - Animasyonları düzenleme ve test etme

4. **Yapılandırma Editörü**: http://localhost:8000/config-editor
   - Robot ayarlarını yapılandırma

5. **IFrame Entegrasyon Demossu**: http://localhost:8000/iframe-integration
   - IFrame entegrasyon testleri

6. **Üst Proje Entegrasyon Örneği**: http://localhost:8000/parent-integration-example
   - Üst projelere entegrasyon örnekleri

7. **Embed Sayfası**: http://localhost:8000/embed
   - Dış projelere gömülebilecek basit sayfa

## API Endpoint'leri:

### Durum ve Bilgi API'leri:

1. **Sistem Durumu**: http://localhost:8000/api/status
   - Robot durumu, çalışma süresi ve sistem bilgileri

2. **Yapılandırma**:
   - Yapılandırma Bilgisi: http://localhost:8000/api/config
   - Yapılandırma Güncelleme: http://localhost:8000/api/config/update (POST)
   - Varsayılan Yapılandırmaya Sıfırlama: http://localhost:8000/api/config/reset (POST)

### Tema API'leri:

1. **Tema Bilgileri**:
   - Tüm Temalar: http://localhost:8000/api/themes
   - Tema Detayları: http://localhost:8000/api/themes/{tema_adi}/details

2. **Tema İşlemleri**:
   - Tema Ayarlama: http://localhost:8000/api/themes/{tema_adi} (POST)
   - Tema Düzenleme: http://localhost:8000/api/themes/{tema_adi}/edit (POST)
   - Tema Oluşturma: http://localhost:8000/api/themes/create (POST)
   - Tema Kopyalama: http://localhost:8000/api/themes/{kaynak_tema}/copy/{hedef_tema} (POST)

### Animasyon API'leri:

1. **Animasyon Bilgileri**:
   - Tüm Animasyonlar: http://localhost:8000/api/animations
   - Animasyon Detayları: http://localhost:8000/api/animations/{animasyon_adi}/details
   - Animasyon Durumu: http://localhost:8000/api/animations/status

2. **Animasyon İşlemleri**:
   - Animasyon Oynatma: http://localhost:8000/api/animations/{animasyon_adi}/play (POST)
   - Animasyon Durdurma: http://localhost:8000/api/animations/stop (POST)
   - Animasyon Kaydetme: http://localhost:8000/api/animations/{animasyon_adi}/save (POST)
   - Animasyon Silme: http://localhost:8000/api/animations/{animasyon_adi}/delete (DELETE)

### Duygu API'leri:

1. **Duygu Ayarlama**: http://localhost:8000/api/emotions/{duygu} (POST)
   - Duygular: happy, sad, angry, surprised, fearful, disgusted, calm, neutral

### Simülasyon API'leri:

1. **Simülasyon Görüntüleri**: http://localhost:8000/api/simulation

### Widget API'leri:

1. **Widget Bilgileri**:
   - Tüm Widget'lar: http://localhost:8000/api/widgets
   - Widget Detayları: http://localhost:8000/api/widgets/{widget_id}
   - Widget Verileri: http://localhost:8000/api/widgets/{widget_id}/data
   - Widget Yapılandırması: http://localhost:8000/api/widgets/{widget_id}/config
   - Widget HTML Render: http://localhost:8000/api/widgets/{widget_id}/render

2. **Widget İşlemleri**:
   - Widget Verileri Güncelleme: http://localhost:8000/api/widgets/{widget_id}/data (POST)
   - Widget Yapılandırması Güncelleme: http://localhost:8000/api/widgets/{widget_id}/config (POST)
   - Widget Eylem Çalıştırma: http://localhost:8000/api/widgets/{widget_id}/action/{eylem_adi} (POST)

3. **Özel Widget Endpoint'leri**:
   - Duygu Geçişi Tetikleme: http://localhost:8000/api/widgets/emotion_transitions/trigger/{duygu} (POST)
   - Yüz İfadesi Ayarlama: http://localhost:8000/api/widgets/expression_control/set_expression (POST)
   - Durum Geçmişi: http://localhost:8000/api/widgets/state_history/history

### WebSocket Endpoint'leri:

1. **Ana WebSocket**: ws://localhost:8000/ws
   - Gerçek zamanlı sistem durumu güncellemeleri için

2. **Simülasyon WebSocket**: ws://localhost:8000/ws/simulation
   - Gerçek zamanlı simülasyon görüntüleri için

Bu endpoint'lerin çoğu, yüz eklentisi çalışırken ve gerekli bileşenler (animasyon motoru, tema yöneticisi vb.) aktifken kullanılabilir. API kullanımı sırasında hata alırsanız, ilgili bileşenlerin düzgün çalıştığından emin olun.