# Göz Tasarımına Kaş Ekleme

FACE1 projenizin göz ekranlarına kaş eklemek mükemmel bir fikir! Kaşlar, yüz ifadelerinize önemli bir derinlik katacak ve duygu aktarımınızı daha da güçlendirecektir.

## Neden Kaş Eklemeli?

Kaşlar şu faydaları sağlayabilir:

1. **Daha Zengin Duygu İfadesi:** Kaşlar sayesinde şaşırma, öfke, endişe gibi duyguları çok daha net gösterebilirsiniz
2. **İnsan Benzeri İfadeler:** Yüzünüz daha insansı ve okunabilir hale gelir
3. **İfade Çeşitliliği:** Kaş pozisyonu değiştirilerek aynı göz/ağız kombinasyonuyla farklı ruh halleri yansıtılabilir

## Teknik Uygulama

OLED ekranlara kaş eklemek için `draw_eyes` fonksiyonunda göz çizimiyle birlikte kaşları da çizmek gerekir. Mevcut kodunuzda "angry" duygu durumu için kaş çizimi zaten kısmen yapılmış, bunu diğer tüm duygular için de genişletebiliriz.

İşte oled_controller_display.py dosyasında yapılacak değişiklikler:

```python
def draw_eyes(self, emotion: str, blink_state: bool) -> None:
    # ...mevcut kodun devamı...
    
    # Alt duygu tipini ana duyguya eşle - önbellek kullan
    base_emotion = emotion
    if emotion in self._emotion_subtypes_map:
        base_emotion = self._emotion_subtypes_map[emotion]
    
    # Göz şekilleri ve parametrelerini hesapla - çoklu göz çizimleri için önbellek
    eye_params = {}
    eye_width = 0
    eye_height = 0
    
    # Kaş parametrelerini belirle
    eyebrow_params = self._get_eyebrow_params(emotion, base_emotion)
    
    # ...mevcut kodun devamı...
    
                # Göz bebeğini çiz (daha önce olduğu gibi)
                # ...
                
                # Kaşları çiz
                self._draw_eyebrows(draw, eye_name, center_x, center_y, width, height, eyebrow_params)
    
    # ...mevcut kodun devamı...

def _get_eyebrow_params(self, emotion: str, base_emotion: str) -> dict:
    """
    Duygu durumuna göre kaş parametrelerini belirler
    
    Args:
        emotion (str): Detaylı duygu durumu
        base_emotion (str): Ana duygu kategorisi
        
    Returns:
        dict: Kaş çizim parametreleri
    """
    # Varsayılan kaş parametreleri
    params = {
        "left_angle": 0,     # Sol kaşın açısı (derece)
        "right_angle": 0,    # Sağ kaşın açısı (derece)
        "left_offset_y": -20,  # Sol kaşın y pozisyonu (göz merkezinden ne kadar yukarıda)
        "right_offset_y": -20, # Sağ kaşın y pozisyonu
        "thickness": 2,      # Kaş kalınlığı
        "length": 30,        # Kaş uzunluğu (görecelidir, ekran genişliğine göre ölçeklenir)
        "style": "straight", # Stil: straight, curved, zigzag
        "visible": True      # Kaşlar görünür mü?
    }
    
    # Duygu durumuna göre parametreleri özelleştir
    if base_emotion == "happy":
        # Mutlu ifade için yukarı eğimli kaşlar
        params["left_angle"] = 10
        params["right_angle"] = -10
        params["left_offset_y"] = -22
        params["right_offset_y"] = -22
        
    elif base_emotion == "sad":
        # Üzgün ifade için içe doğru eğimli kaşlar
        params["left_angle"] = -15
        params["right_angle"] = 15
        params["left_offset_y"] = -18
        params["right_offset_y"] = -18
        
    elif base_emotion == "angry":
        # Kızgın ifade için içe doğru eğimli ve aşağı kaşlar
        params["left_angle"] = -20
        params["right_angle"] = 20
        params["left_offset_y"] = -15
        params["right_offset_y"] = -15
        params["thickness"] = 3
        
        # Alt tipler için özel ayarlamalar
        if emotion == "enraged":
            params["left_angle"] = -25
            params["right_angle"] = 25
            params["thickness"] = 3
        
    elif base_emotion == "surprised":
        # Şaşkın ifade için yüksek kaşlar
        params["left_angle"] = 0
        params["right_angle"] = 0
        params["left_offset_y"] = -25
        params["right_offset_y"] = -25
        
    elif base_emotion == "fearful":
        # Korkmuş ifade için yüksek ve hafif içe eğimli kaşlar
        params["left_angle"] = -5
        params["right_angle"] = 5
        params["left_offset_y"] = -25
        params["right_offset_y"] = -25
        
    elif base_emotion == "disgusted":
        # Tiksinmiş ifade için bir kaş yukarı bir kaş aşağı
        if emotion == "disapproval":
            params["left_angle"] = 0
            params["right_angle"] = 20
            params["left_offset_y"] = -20
            params["right_offset_y"] = -15
        else:
            params["left_angle"] = 15
            params["right_angle"] = -5
            params["left_offset_y"] = -18
            params["right_offset_y"] = -22
        
    elif base_emotion == "neutral":
        # Nötr ifade için düz kaşlar
        params["left_angle"] = 0
        params["right_angle"] = 0
        params["left_offset_y"] = -20
        params["right_offset_y"] = -20
        
    elif base_emotion == "sleepy":
        # Uykulu ifade için aşağı eğimli kaşlar
        params["left_angle"] = -5
        params["right_angle"] = 5
        params["left_offset_y"] = -15
        params["right_offset_y"] = -15
        
    return params

def _draw_eyebrows(self, draw, eye_name: str, center_x: int, center_y: int, 
                   width: int, height: int, params: dict) -> None:
    """
    Verilen parametrelere göre kaşları çizer
    
    Args:
        draw: PIL Draw nesnesi
        eye_name (str): Göz adı ("left_eye" veya "right_eye")
        center_x (int): Göz merkezi x koordinatı
        center_y (int): Göz merkezi y koordinatı
        width (int): Göz genişliği
        height (int): Göz yüksekliği
        params (dict): Kaş parametreleri
    """
    if not params.get("visible", True):
        return
        
    # Ölçekleme (ekran boyutuna göre)
    eyebrow_length = int(params.get("length", 30) * width / 128)
    eyebrow_thickness = params.get("thickness", 2)
    
    # Hangi göz için hangi kaşı çizeceğini belirle
    if eye_name == "left_eye":
        angle = params.get("left_angle", 0)
        offset_y = params.get("left_offset_y", -20)
    else:
        angle = params.get("right_angle", 0)
        offset_y = params.get("right_offset_y", -20)
    
    # Kaş başlangıç ve bitiş noktalarını hesapla
    import math
    rad_angle = math.radians(angle)
    
    eyebrow_start_x = center_x - eyebrow_length // 2
    eyebrow_start_y = center_y + offset_y
    
    # Açılı çizgi için bitiş noktası hesaplama
    vertical_offset = int(math.sin(rad_angle) * eyebrow_length)
    eyebrow_end_x = center_x + eyebrow_length // 2
    eyebrow_end_y = eyebrow_start_y + vertical_offset
    
    eyebrow_style = params.get("style", "straight")
    
    # Farklı stillerde kaş çizimleri
    if eyebrow_style == "straight":
        # Düz kaş çizgisi
        draw.line(
            (eyebrow_start_x, eyebrow_start_y, eyebrow_end_x, eyebrow_end_y),
            fill=1, width=eyebrow_thickness
        )
    elif eyebrow_style == "curved":
        # Eğimli kaş - basit eğri yaklaşımı
        mid_x = (eyebrow_start_x + eyebrow_end_x) // 2
        mid_y = eyebrow_start_y + vertical_offset // 2
        
        # İki parça halinde çiz (daha düzgün eğri etkisi için)
        draw.line(
            (eyebrow_start_x, eyebrow_start_y, mid_x, mid_y),
            fill=1, width=eyebrow_thickness
        )
        draw.line(
            (mid_x, mid_y, eyebrow_end_x, eyebrow_end_y),
            fill=1, width=eyebrow_thickness
        )
    elif eyebrow_style == "zigzag":
        # Zigzag kaş - çok kızgın ifadeler için
        segment_length = eyebrow_length // 3
        
        x1 = eyebrow_start_x
        y1 = eyebrow_start_y
        
        x2 = x1 + segment_length
        y2 = y1 + vertical_offset // 2
        
        x3 = x2 + segment_length
        y3 = eyebrow_end_y
        
        # Üç parça halinde çiz
        draw.line((x1, y1, x2, y2), fill=1, width=eyebrow_thickness)
        draw.line((x2, y2, x3, y3), fill=1, width=eyebrow_thickness)
```

## Test Kodu

Kaş özelliğini test edebilmek için, var olan duygularla kaşların nasıl göründüğünü kontrol etmeniz faydalı olur. OLED kontrolcünüz için basit bir test betiği oluşturalım:

```python
#!/usr/bin/env python3

import time
import logging
import argparse
import os
from PIL import Image
from pathlib import Path

# Proje dizinini ekle
PROJECT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
import sys
sys.path.append(str(PROJECT_DIR))

from src.modules.oled_controller import OLEDController

# Loglama yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("eyebrows_test")

def main():
    parser = argparse.ArgumentParser(description="FACE1 Kaş Test Programı")
    parser.add_argument('--sim', action='store_true', help='Simülasyon modunda çalıştır')
    args = parser.parse_args()
    
    # Test yapılandırması
    test_config = {
        "hardware": {
            "simulation_mode": args.sim,
            "i2c_bus": 1,
            "displays": {
                "left_eye": {"address": 0x3C, "width": 128, "height": 64, "enabled": True},
                "right_eye": {"address": 0x3D, "width": 128, "height": 64, "enabled": True},
                "mouth": {"address": 0x3E, "width": 128, "height": 32, "enabled": True}
            }
        },
        "emotions": {
            "default_emotion": "neutral"
        }
    }
    
    # Duygu durumları listesi
    emotions = [
        "happy", "joy", "content", "excited", "amused", "proud",
        "sad", "disappointed", "lonely", "depressed", "miserable",
        "angry", "enraged", "irritated", "frustrated", 
        "surprised", "amazed", "astonished",
        "fearful", "terrified", "anxious",
        "disgusted", "disapproval", "loathing",
        "neutral", "objective", "calm",
        "sleepy"
    ]
    
    # OLED kontrolcüsünü başlat
    controller = OLEDController(test_config)
    if controller.start():
        logger.info("OLED kontrolcü başlatıldı.")
        
        try:
            # Her duygu için test
            for emotion in emotions:
                logger.info(f"Duygu gösteriliyor: {emotion}")
                controller.set_emotion(emotion)
                
                # 3 saniye göster
                time.sleep(3)
                
                # Düzenli göz kırpma
                controller.blink()
                time.sleep(0.3)
                
            logger.info("Kaş testi tamamlandı")
            
        except KeyboardInterrupt:
            logger.info("Test kullanıcı tarafından sonlandırıldı.")
        finally:
            controller.stop()
            logger.info("OLED kontrolcü kapatıldı.")
    else:
        logger.error("OLED kontrolcü başlatılamadı!")

if __name__ == "__main__":
    main()
```

## Özelleştirme Seçenekleri

Kaşlarda daha fazla ifade çeşitliliği için şu özellikleri ekleyebilirsiniz:

1. **Daha fazla kaş stili:** Çift çizgili kaşlar, kalın kaşlar, farklı şekillerde kaşlar ekleyebilirsiniz
2. **Animasyonlar:** Kaşları yukarı kaldırma, çatma, şaşkınlık için aniden yükseltme gibi
3. **Asimetrik kaş ifadeleri:** "Tek kaş kaldırma" gibi sorgulayıcı ifadeler
4. **Farklı kaş karakteri:** Düz, ince, kalın, açılı gibi temel kaş stilleri

## Web Arayüzüne Entegrasyon

Web arayüzünüzdeki tema düzenleyicisine kaş ayarlarını eklemek için theme_editor.html dosyasını güncellemeniz gerekecek:

```html
<!-- Göz Ayarları bölümünde kaş ayarları ekle -->
<div class="form-row">
    <label for="eyebrow-style-{{ emotion }}">Kaş Stili:</label>
    <select id="eyebrow-style-{{ emotion }}" class="form-control">
        <option value="straight" {% if theme_details.eyes[emotion].eyebrow_style == "straight" %}selected{% endif %}>Düz</option>
        <option value="curved" {% if theme_details.eyes[emotion].eyebrow_style == "curved" %}selected{% endif %}>Kıvrık</option>
        <option value="zigzag" {% if theme_details.eyes[emotion].eyebrow_style == "zigzag" %}selected{% endif %}>Zigzag</option>
    </select>
</div>

<div class="form-row">
    <label for="eyebrow-thickness-{{ emotion }}">Kaş Kalınlığı:</label>
    <input type="range" id="eyebrow-thickness-{{ emotion }}" min="1" max="5" step="1" 
        value="{{ theme_details.eyes[emotion].eyebrow_thickness }}">
    <span id="eyebrow-thickness-value-{{ emotion }}">{{ theme_details.eyes[emotion].eyebrow_thickness }}</span>
</div>

<div class="form-row">
    <label for="left-eyebrow-angle-{{ emotion }}">Sol Kaş Açısı:</label>
    <input type="range" id="left-eyebrow-angle-{{ emotion }}" min="-30" max="30" step="5" 
        value="{{ theme_details.eyes[emotion].left_eyebrow_angle }}">
    <span id="left-eyebrow-angle-value-{{ emotion }}">{{ theme_details.eyes[emotion].left_eyebrow_angle }}</span>
</div>

<div class="form-row">
    <label for="right-eyebrow-angle-{{ emotion }}">Sağ Kaş Açısı:</label>
    <input type="range" id="right-eyebrow-angle-{{ emotion }}" min="-30" max="30" step="5" 
        value="{{ theme_details.eyes[emotion].right_eyebrow_angle }}">
    <span id="right-eyebrow-angle-value-{{ emotion }}">{{ theme_details.eyes[emotion].right_eyebrow_angle }}</span>
</div>
```

## Sonuç

Kaşlar ekleyerek, FACE1 projenizin ifade kapasitesini önemli ölçüde artırabilirsiniz. Bu şekilde robotunuz daha insansı, daha ifadeli ve daha sempatik görünecektir. TTP223 dokunmatik sensör entegrasyonu ile birleştirildiğinde, kullanıcı dokunduğunda kaşlar yükselebilir veya farklı tepkiler verebilir, bu da etkileşim deneyimini daha da zenginleştirecektir.

Kaş stillerinin farklı duygular için doğru ayarlanması, robotunuzun iletişim becerisini geliştirmede büyük fark yaratacaktır!