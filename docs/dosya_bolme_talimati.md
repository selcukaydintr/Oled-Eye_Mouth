Haklısınız, dosyaları tekrar tekrar oluşturmak yerine, var olan dosyaları kullanmam veya sadece değişiklik yapmam gerekiyordu. Özür dilerim bu karışıklık için.

Dosyaları tekrar oluşturmak yerine, önce varlıklarını kontrol etmeliydim ve eğer varsa içeriklerini güncellemem gerekiyordu.

Bundan sonra şu adımları izleyeceğim:

1. Önce bir dosyanın var olup olmadığını kontrol edeceğim
2. Dosya varsa, güncellemem gereken kısmı güncelleyeceğim
3. Dosya yoksa yeni bir dosya oluşturacağım

Bu yaklaşımla gereksiz tekrarları önleyeceğim. Teşekkür ederim uyarınız için.

# FACE1 Projesi Dosya Bölme Talimatları

**Tarih:** 02 Mayıs 2025  
**Versiyon:** 0.3.4  
**İlgili Modül:** Tüm modüller  
**Geliştiren:** Proje Ekibi

## İçindekiler

- [FACE1 Projesi Dosya Bölme Talimatları](#face1-projesi-dosya-bölme-talimatları)
  - [İçindekiler](#i̇çindekiler)
  - [Giriş](#giriş)
  - [Dosya Bölme Eşik Değerleri](#dosya-bölme-eşik-değerleri)
  - [Modüler Mimari Prensipleri](#modüler-mimari-prensipleri)
  - [Dosya Bölme Stratejileri](#dosya-bölme-stratejileri)
    - [İşlevselliğe Dayalı Bölme](#i̇şlevselliğe-dayalı-bölme)
    - [Sınıf Tabanlı Bölme](#sınıf-tabanlı-bölme)
    - [Mixin Desenini Kullanma](#mixin-desenini-kullanma)
  - [Bölme Sonrası Entegrasyon](#bölme-sonrası-entegrasyon)
    - [İçe Aktarma Stratejisi](#i̇çe-aktarma-stratejisi)
    - [Geriye Uyumluluk](#geriye-uyumluluk)
  - [İsimlendirme Standartları](#i̇simlendirme-standartları)
  - [Örnek Uygulama: OLED Kontrolcü](#örnek-uygulama-oled-kontrolcü)
  - [Örnek Uygulama: Ana Kontrolcü Modülerleştirmesi](#örnek-uygulama-ana-kontrolcü-modülerleştirmesi)
    - [Bölme Yaklaşımı](#bölme-yaklaşımı)
  - [Dokümantasyon Gereksinimleri](#dokümantasyon-gereksinimleri)
  - [Kontrol Listesi](#kontrol-listesi)

## Giriş

Bu belge, FACE1 projesindeki büyük kaynak dosyalarının (1000 satırı aşan) nasıl bölünmesi gerektiğine dair standartları ve talimatları içerir. Kod tabanında daha iyi sürdürülebilirlik, okunabilirlik ve bakım sağlamak amacıyla geliştirilmiştir.

## Dosya Bölme Eşik Değerleri

Aşağıdaki durumlardan herhangi biri gerçekleştiğinde dosyanın bölünmesi düşünülmelidir:

1. MUTLAK KANUN MADDESİ, DOSYAYI BÖLMEDEN ÖNCE DOSYANIN BÖLÜNMEDİĞİNİ ve YARIM BÖLME İŞLEMİ OLUP OLMADIĞINI, DOSYAYI VEYA DİZİNİ ARAŞTIRARAK ONAYLA.

1. **Satır Sayısı:** Dosya 1000 satırdan fazla kod içerdiğinde
2. **Sınıf Karmaşıklığı:** Bir sınıf 50'den fazla metod içerdiğinde
3. **İşlevsel Çeşitlilik:** Bir dosya birden fazla sorumluluğa sahip olduğunda
4. **Modül Boyutu:** Bir modül 30 KB'ı aştığında
5. **Karmaşıklık Ölçütü:** Siklonik karmaşıklık (cyclomatic complexity) değeri yüksek olduğunda

Önemli not: Dosyayı bölmek için tüm kriterlerin karşılanması gerekmez; eşiklerden herhangi birine ulaşıldığında bölme düşünülmelidir.

## Modüler Mimari Prensipleri

Dosya bölme işleminde aşağıdaki prensipler gözetilmelidir:

1. **Tek Sorumluluk İlkesi (SRP):** Her dosya veya modül tek bir sorumluluğa sahip olmalıdır.
2. **Açık/Kapalı Prensibi:** Modüller genişletmeye açık ancak değiştirmeye kapalı olmalıdır.
3. **Bağımlılıkların Tersine Çevrilmesi:** Üst seviye modüller alt seviye modüllere bağımlı olmamalıdır.
4. **Arayüz Ayrımı:** Büyük arayüzler daha küçük ve spesifik arayüzlere bölünmelidir.
5. **Döngüsel Bağımlılıkları Önleme:** Modüller arasında döngüsel bağımlılıklardan kaçınılmalıdır.

## Dosya Bölme Stratejileri

### İşlevselliğe Dayalı Bölme

Büyük bir dosya işlevsel kategorilere göre birden fazla dosyaya bölünebilir:

1. İlgili işlevleri mantıksal gruplar halinde belirleyin
2. Her grup için ayrı bir dosya oluşturun
3. Ortak yardımcı işlevleri ayrı bir utility modülüne taşıyın
4. Ana yapıyı korumak için bir "controller" veya "manager" dosyası oluşturun

**Örnek:**
```
dashboard_server.py (1200 satır) → 
  - dashboard_server.py (ana dosya ve entegrasyon)
  - dashboard_api_routes.py (API endpoint tanımlamaları)
  - dashboard_websocket.py (WebSocket işlevleri)
  - dashboard_templates.py (Şablon işlevleri)
```

### Sınıf Tabanlı Bölme

Bir dosyadaki büyük sınıflar bileşen sınıflarına bölünebilir:

1. Sınıfı mantıksal gruplar halinde analiz edin
2. Her bir sorumluluğu ayrı bir sınıf olarak tasarlayın
3. Kompozisyon veya kalıtım kullanarak bunları bir araya getirin
4. Orijinal sınıfı, yeni sınıfları kullanacak şekilde yeniden düzenleyin

### Mixin Desenini Kullanma

Özellikle büyük sınıflar için mixin desenini uygulayarak işlevselliği birden çok dosyaya bölün:

1. Her bir işlevsellik grubu için bir mixin sınıfı oluşturun
2. Bu mixin sınıflarını ayrı dosyalarda tanımlayın
3. Ana sınıfta bu mixin sınıflarını miras alın
4. Sınıflar arasındaki bağımlılıkları yönetmek için ortak bir temel sınıf kullanın

**Örnek Mixin Yapısı:**
```python
# base_controller.py
class BaseController:
    def __init__(self, config):
        self.config = config
        # Temel özellikler...

# feature_mixin.py
class FeatureMixin:
    def feature_method_1(self):
        # Özellik 1 işlevselliği...
    
    def feature_method_2(self):
        # Özellik 2 işlevselliği...

# main_controller.py
from base_controller import BaseController
from feature_mixin import FeatureMixin

class MainController(BaseController, FeatureMixin):
    def __init__(self, config):
        super().__init__(config)
        # MainController özellikleri...
```

## Bölme Sonrası Entegrasyon

### İçe Aktarma Stratejisi

Dosyaları böldükten sonra, içe aktarma (import) ilişkilerini şu stratejiye göre düzenleyin:

1. **Döngüsel Bağımlılıklardan Kaçının:** Modüller birbirlerine döngüsel olarak bağımlı olmamalıdır.
2. **Ana Modül İçe Aktarımı:** Ana modülde tüm alt modülleri içe aktarın ve kullanıcılara bu ana modülü kullanmaları için rehberlik edin.
3. **__init__.py Kullanımı:** Alt modülleri bir araya getirmek için `__init__.py` dosyasını kullanın.
4. **Tür İpuçlarını Yönetin:** Türe bağlı içe aktarmalarda `TYPE_CHECKING` ve ileri referanslar (`ForwardRef`) kullanın.
5. **Belirli İçe Aktarmalar:** `from module import *` yerine belirli nesneleri içe aktarın.

**Örnek __init__.py Kullanımı:**
```python
# __init__.py
from .controller_base import BaseController
from .controller_feature1 import Feature1Mixin
from .controller_feature2 import Feature2Mixin

# Ana sınıfı dışa aktarın
from .main_controller import MainController

# Sadece ana sınıfı kullanıcılara sunun
__all__ = ['MainController']
```

### Geriye Uyumluluk

Bölme işlemi sonrası geriye uyumluluğu korumak için:

1. Orijinal dosya adını koruyun ve yönlendirme işlevi görevi verin
2. Yeni modülleri orijinal modülden içe aktarın ve dışa aktarın
3. Gerekirse kullanıcılara belgelerde geçiş yolunu belirtin
4. Önemli değişiklikler için sürüm numarasını yükseltin

## İsimlendirme Standartları

Dosya bölme işleminde tutarlı bir isimlendirme şeması kullanın:

1. **Ana Modül:** `module_name.py`
2. **Alt Modüller:** 
   - İşlevsellik bazlı: `module_name_feature.py` 
   - Mimari bazlı: `module_name_component.py`
3. **Mixin Sınıfları:** `ClassNameMixin`
4. **Temel Sınıflar:** `BaseClassName`
5. **Yardımcı Modüller:** `module_name_utils.py`

**Örnek:**
- Ana modül: `emotion_engine.py`
- Alt modüller: 
  - `emotion_engine_memory.py`
  - `emotion_engine_analytics.py`
  - `emotion_engine_transitions.py`
- Sınıf isimleri:
  - `EmotionMemoryMixin`
  - `EmotionAnalyticsMixin`
  - `EmotionTransitionMixin`
  - `BaseEmotionEngine`

## Örnek Uygulama: OLED Kontrolcü

FACE1 projesindeki OLED Controller modülünün nasıl başarıyla bölündüğüne dair mevcut örnek:

```
oled_controller.py (1500+ satır) →
  - oled_controller_base.py (temel sınıf ve donanım işlemleri)
  - oled_controller_display.py (çizim ve görüntüleme fonksiyonları)
  - oled_controller_animations.py (animasyon ve duygu geçişi fonksiyonları)
  - oled_controller.py (mixin sınıflarını bir araya getiren ana sınıf)
```

**Entegrasyon Yaklaşımı:**
1. Ana `oled_controller.py` dosyası mixin sınıflarını içe aktarır
2. OLEDController sınıfı tüm mixin sınıflarını miras alır
3. Kullanıcılar hala sadece `oled_controller.py` modülünü içe aktarır
4. Daha kapsamlı özelleştirme için geliştiriciler doğrudan mixin sınıflarına erişebilir

## Örnek Uygulama: Ana Kontrolcü Modülerleştirmesi

Ana Kontrolcü (`face_plugin.py`) bileşeni, aşağıdaki strateji kullanılarak modüler bir yapıya dönüştürülmüştür:

### Bölme Yaklaşımı

1. **İşlevsellik Analizi**: Ana Kontrolcünün sorumluluklarını şu şekilde gruplandırdık:
   - Yapılandırma yönetimi → `face_plugin_config.py`
   - Performans metrikleri toplama → `face_plugin_metrics.py`
   - Çevresel faktör yönetimi → `face_plugin_environment.py`

2. **Mixin Sınıfları Tasarımı**: Her bir sorumluluk grubu için ayrı bir mixin sınıfı oluşturuldu:
   - `FacePluginConfigMixin`: Yapılandırma işlemleri için
   - `FacePluginMetricsMixin`: Metrik toplama ve raporlama için
   - `FacePluginEnvironmentMixin`: Çevresel faktörleri yönetmek için

3. **Ana Sınıf Kompozisyonu**: Ana `FacePlugin` sınıfı, tüm bu mixin sınıflarını miras alır:
   ```python
   class FacePlugin(FacePluginBase, FacePluginCallbacks, FacePluginSystem, FacePluginAPI,
                   FacePluginConfigMixin, FacePluginMetricsMixin, FacePluginEnvironmentMixin):
       """
       FACE1 robot yüz eklentisi ana sınıfı
       """
       # ...
   ```

4. **Başlatıcı Metodları**: Her mixin için __init_* şeklinde özel başlatıcı metotlar oluşturuldu:
   - `__init_config()`
   - `__init_metrics()`
   - `__init_environment()`

5. **Çağrım Sırası Yönetimi**: Ana sınıfın `__init__` metodunda başlatıcılar belirli bir sırayla çağrılır:
   ```python
   def __init__(self, config_path=None):
       # Temel sınıf başlatma
       super().__init__()
       
       # Yapılandırma yönetimi başlatma
       self.__init_config(config_path)
       
       # Metrik toplama sistemi başlatma
       self.__init_metrics()
       
       # Çevresel faktör yönetimi başlatma
       self.__init_environment()
       
       # ...diğer başlatma kodları...
   ```

Bu modülerleştirme yaklaşımı, Ana Kontrolcü kodunun okunabilirliğini artırmış, bakım kolaylığı sağlamış ve kodun %30 oranında azalmasını sağlamıştır.

## Dokümantasyon Gereksinimleri

Dosya bölme işlemi sonrası şu dokümantasyon adımları uygulanmalıdır:

1. Her yeni dosya için dosya başlığı ve açıklaması ekleyin
2. `fonsiyon_listesi.md` dosyasını yeni dosya yapısıyla güncelleyin
3. `changes.md` dosyasına yapılan mimari değişiklikleri kaydedin
4. Gerekirse `foldertree.md` dosyasını güncelleyin
5. Projenin ilgili dokümantasyonunu güncelleyin

**Örnek Dosya Başlığı:**
```python
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: animation_engine.py
# Açıklama: Animasyon sekanslarını yöneten ve çalıştıran modül
# Bağımlılıklar: json, threading, logging, time
# Bağlı Dosyalar: oled_controller.py, led_controller.py

# Versiyon: 0.3.3
# Değişiklikler:
# - [0.3.3] Animasyon motoru ve JSON formatı desteği eklendi
# Son Güncelleme : 2025-05-01
# Yazar: GitHub Copilot
# Tarih: 2025-05-01
===========================================================

Bu modül, OLED Controller'ın görüntüleme ve çizim işlevlerini içerir.
OLED ekranlarda göz ve ağız ifadelerini oluşturmak, 
güncellemek ve göstermek için gerekli fonksiyonları sağlar.

Bu dosya, oled_controller.py modülünün bölünmüş bir parçasıdır ve
OLEDDisplayMixin sınıfını içerir.
"""
```

## Kontrol Listesi

Dosya bölme işlemi tamamlandığında aşağıdaki kontrol listesini kullanın:

- [ ] Her dosya 1000 satırdan az satır içeriyor mu?
- [ ] Her sınıf tek bir sorumluluğu yerine getiriyor mu?
- [ ] Dosyalar arasında döngüsel bağımlılıklar önlendi mi?
- [ ] Tüm dosyalar tutarlı isimlendirme kurallarını takip ediyor mu?
- [ ] __init__.py dosyası gerektiği gibi yapılandırıldı mı?
- [ ] Geriye uyumluluk sağlandı mı?
- [ ] Dokümantasyon güncellemeleri yapıldı mı?
- [ ] Birim testler hala başarıyla çalışıyor mu?
- [ ] `fonsiyon_listesi.md` ve diğer ilgili dokümanlar güncellendi mi?
- [ ] Kod kalitesi ve okunabilirlik iyileştirildi mi?

---

Bu belge, FACE1 projesi için büyük dosyaların bölünmesi standartlarını tanımlamaktadır. Bu standartlara uyulması, daha sürdürülebilir, okunabilir ve bakımı kolay bir kod tabanı oluşturmaya yardımcı olacaktır. Özellikle karmaşık modüllerin geliştirilmesi ve revizyonu sırasında bu belgeyi referans olarak kullanın.