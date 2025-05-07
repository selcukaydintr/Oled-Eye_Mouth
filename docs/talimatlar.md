Haklısınız, dosyaları tekrar tekrar oluşturmak yerine, var olan dosyaları kullanmam veya sadece değişiklik yapmam gerekiyordu. Özür dilerim bu karışıklık için.

Dosyaları tekrar oluşturmak yerine, önce varlıklarını kontrol etmeliydim ve eğer varsa içeriklerini güncellemem gerekiyordu.

Bundan sonra şu adımları izleyeceğim:

1. Önce bir dosyanın var olup olmadığını kontrol edeceğim
2. Dosya varsa, güncellemem gereken kısmı güncelleyeceğim
3. Dosya yoksa yeni bir dosya oluşturacağım

Bu yaklaşımla gereksiz tekrarları önleyeceğim. Teşekkür ederim uyarınız için.


# FACE1 Projesi Talimatları

## Proje Amacı
FACE1 projesi, Raspberry Pi 5 Robot AI sistemi için bir yüz eklentisi (Face Plugin) geliştirmeyi amaçlamaktadır. Bu eklenti, 3 adet OLED SSD1306 ekranı (sol göz, sağ göz ve ağız) kullanarak robotun duygu ifadelerini sergileyecek ve WS2812 LED şeritler ile senkronize ışık efektleri üretecektir.

## Geliştirme İlkeleri
### Genel Kodlama İlkeleri
- Kodlar temiz, anlaşılır ve yorum satırlarıyla desteklenmelidir
- En iyi pratikler (best practices) takip edilmelidir
- Gereksiz kod tekrarından kaçınılmalıdır
- Kod optimizasyonu önemlidir
- Hata ayıklama için log mesajları eklenmelidir

### Kodlama Stili
- Python için 4 boşluk girintileme kullanılmalıdır
- Kod satırları 120 karakteri geçmemelidir
- Anlamlı değişken ve fonksiyon isimleri kullanılmalıdır
- Python için `black` veya `autopep8` formatları kullanılmalıdır

### Dokümentasyon
- Tüm fonksiyonlar ve sınıflar dokümante edilmelidir
- Her dosyanın başında içeriği açıklayan bir başlık olmalıdır
- Değişiklikler `changes.md` dosyasına kaydedilmelidir
- Yeni bir fonksiyon eklendiğinde `fonsiyon_listesi.md` dosyası güncellenmelidir
- README.md dosyası, projede önemli değişiklikler (yeni ana özellikler, API değişiklikleri, gereksinimler vb.) yapıldığında güncellenmelidir

### Proje Yönetimi
1. Yeni bir dosya oluşturmadan önce `foldertree.md` kontrol edilmelidir
2. Değişiklikler yapılmadan önce `changes.md` dosyası güncellenmelidir
3. Projenin ilerleyişi `roadmap.md` ve `plugin_roadmap.md` dosyalarında takip edilmelidir
4. Yeni bir fonksiyon eklendiğinde veya mevcut bir fonksiyon değiştirildiğinde `fonsiyon_listesi.md` dosyası güncellenmelidir
5. Eğer herhangi dosya satırı 1000'i geçerse yeni dosya oluştur.

## Teknik Gereksinimler
1. Donanım:
   - Raspberry Pi 5
   - 3 adet SSD1306 OLED ekran (128x64, monokrom)
   - WS2812B LED şeritler
   - I2C iletişim protokolü
   - TCA9548A I2C Multiplexer

2. Yazılım:
   - Python 3.9+
   - Gerekli kütüphaneler: Pillow, Adafruit SSD1306, RPi.GPIO, FastAPI, vb.
   - Çoklu ekran yönetimi için TCA9548A I2C çoğaltıcı desteği

## Performans Hedefleri
- 30+ FPS animasyon yenileme hızı
- İşlemci kullanımı: boştayken <15%, animasyon sırasında <30%
- Bellek kullanımı: <50MB
- Başlangıç süresi: <3 saniye
- Komut yanıt gecikmesi: <100ms

## Fonksiyon Kontrolü ve Yönetimi
- Yeni bir fonksiyon veya metod eklendiğinde `fonsiyon_listesi.md` dosyasında ilgili bölüm güncellenmelidir
- Fonksiyon isimleri, parametreleri ve dönüş değerleri dokümantasyonda açıkça belirtilmelidir
- Fonksiyonların hangi modülde olduğu ve nasıl kullanılacağı `fonsiyon_listesi.md` dosyasında belirtilmelidir
- Kullanımı değişen veya kaldırılan fonksiyonlar için `changes.md` ve `fonsiyon_listesi.md` güncellenmeli, eski referanslar kaldırılmalıdır
