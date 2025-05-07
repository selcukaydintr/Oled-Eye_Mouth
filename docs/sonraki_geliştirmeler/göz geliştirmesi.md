# Gözlere Göz Bebeği ve Işıltı Ekleme

FACE1 projenizin göz tasarımına göz bebeği ve ışıltı eklemek harika bir fikir! Bu eklenti, yüz ifadenizi daha canlı ve gerçekçi gösterecek, duygu ifadenizi zenginleştirecektir.

## Mevcut Durum

Şu anda oled_controller_display.py dosyasında göz bebeği çizimi zaten var, ancak ışıltı efekti henüz eklenmemiş. Göz bebeği çizimi bu şekilde yapılıyor:

```python
# Göz bebeği çizimi (duyguya ve göz pozisyonuna göre)
pupil_size = min(width, height) // 8

# Duyguya göre göz bebeği boyutunu ayarla
if base_emotion == "fearful" or base_emotion == "surprised":
    pupil_size = min(width, height) // 6  # Daha büyük göz bebeği
elif base_emotion == "disgusted" or base_emotion == "angry":
    pupil_size = min(width, height) // 10  # Daha küçük göz bebeği
    
# Göz bebeği pozisyonunu hesapla
max_offset_x = eye_width // 4
max_offset_y = eye_height // 4
pupil_offset_x = int(self.eye_position[0] * max_offset_x)
pupil_offset_y = int(self.eye_position[1] * max_offset_y)

# Göz bebeği çiz
ellipse_coords = (center_x - pupil_size + pupil_offset_x, 
                center_y - pupil_size + pupil_offset_y, 
                center_x + pupil_size + pupil_offset_x, 
                center_y + pupil_size + pupil_offset_y)
draw.ellipse(ellipse_coords, fill=1)
```

## Önerilen Değişiklikler

### 1. Göz Bebeği İyileştirmesi ve Işıltı Ekleme

oled_controller_display.py dosyasında `draw_eyes` metoduna ışıltı ekleyelim:

```python
def draw_eyes(self, emotion: str, blink_state: bool) -> None:
    # ...mevcut kod...
    
                    # Göz bebeği çizimi (duyguya ve göz pozisyonuna göre)
                    pupil_size = min(width, height) // 8
                    
                    # Duyguya göre göz bebeği boyutunu ayarla
                    if base_emotion == "fearful" or base_emotion == "surprised":
                        pupil_size = min(width, height) // 6  # Daha büyük göz bebeği
                    elif base_emotion == "disgusted" or base_emotion == "angry":
                        pupil_size = min(width, height) // 10  # Daha küçük göz bebeği
                        
                    # Performans optimizasyonu: Göz bebeği pozisyonunu tek seferde hesapla
                    max_offset_x = eye_width // 4
                    max_offset_y = eye_height // 4
                    
                    pupil_offset_x = int(self.eye_position[0] * max_offset_x)
                    pupil_offset_y = int(self.eye_position[1] * max_offset_y)
                    
                    # Kısıtlamaları uygula
                    pupil_offset_x = max(-max_offset_x, min(max_offset_x, pupil_offset_x))
                    pupil_offset_y = max(-max_offset_y, min(max_offset_y, pupil_offset_y))
                    
                    # Love duygusu haricinde göz bebeği çiz
                    if base_emotion != "love":
                        # Göz bebeği çiz
                        ellipse_coords = (center_x - pupil_size + pupil_offset_x, 
                                        center_y - pupil_size + pupil_offset_y, 
                                        center_x + pupil_size + pupil_offset_x, 
                                        center_y + pupil_size + pupil_offset_y)
                        draw.ellipse(ellipse_coords, fill=1)
                        
                        # Işıltı ekle (göz bebeğinin üst sol köşesinde küçük beyaz nokta)
                        highlight_size = max(1, pupil_size // 4)
                        highlight_offset_x = pupil_offset_x - pupil_size // 2
                        highlight_offset_y = pupil_offset_y - pupil_size // 2
                        
                        # Duygulara göre ışıltı pozisyonunu ayarla
                        if base_emotion == "happy" or base_emotion == "excited":
                            # Mutlu duygularda büyük ışıltı
                            highlight_size = max(2, pupil_size // 3)
                        elif base_emotion == "sad":
                            # Üzgün duygularda küçük ışıltı
                            highlight_size = max(1, pupil_size // 5)
                        
                        # Işıltı çiz (göz bebeğinin içinde beyaz nokta - fill=0)
                        highlight_coords = (
                            center_x - pupil_size//2 + pupil_offset_x + highlight_offset_x, 
                            center_y - pupil_size//2 + pupil_offset_y + highlight_offset_y,
                            center_x - pupil_size//2 + pupil_offset_x + highlight_offset_x + highlight_size,
                            center_y - pupil_size//2 + pupil_offset_y + highlight_offset_y + highlight_size
                        )
                        draw.ellipse(highlight_coords, fill=0)
```

### 2. İris Ekleme (Göz Bebeğini Geliştirme)

Daha detaylı bir göz için göz bebeğine iris de ekleyebiliriz:

```python
def draw_eyes(self, emotion: str, blink_state: bool) -> None:
    # ...mevcut kod...
    
                    # Love duygusu haricinde göz bebeği çiz
                    if base_emotion != "love":
                        # İlk önce iris çiz (göz bebeğinin çevresindeki renkli kısım)
                        iris_size = int(pupil_size * 1.5)
                        iris_coords = (
                            center_x - iris_size + pupil_offset_x, 
                            center_y - iris_size + pupil_offset_y, 
                            center_x + iris_size + pupil_offset_x, 
                            center_y + iris_size + pupil_offset_y
                        )
                        # İrisi çiz - outline=1, fill=0 ile sadece çevre çizilir
                        draw.ellipse(iris_coords, outline=1, fill=0)
                        
                        # Göz bebeği çiz
                        ellipse_coords = (
                            center_x - pupil_size + pupil_offset_x, 
                            center_y - pupil_size + pupil_offset_y, 
                            center_x + pupil_size + pupil_offset_x, 
                            center_y + pupil_size + pupil_offset_y
                        )
                        draw.ellipse(ellipse_coords, fill=1)
                        
                        # Işıltı ekle (göz bebeğinin üst sol köşesinde küçük beyaz nokta)
                        # ...mevcut ışıltı kodu...
```

### 3. Duygu Durumlarına Göre Göz Bebeği ve Işıltı Özelleştirme

Farklı duygu durumlarına göre göz bebeklerini daha detaylı özelleştirebiliriz:

```python
def _get_pupil_params(self, emotion: str, base_emotion: str) -> dict:
    """
    Duygu durumuna göre göz bebeği parametrelerini döndürür
    
    Args:
        emotion (str): Detaylı duygu durumu
        base_emotion (str): Ana duygu kategorisi
        
    Returns:
        dict: Göz bebeği parametreleri
    """
    # Varsayılan göz bebeği parametreleri
    params = {
        "size": 8,             # Bölme faktörü (pupil_size = min(width, height) // size)
        "highlight_size": 4,   # Bölme faktörü (highlight_size = pupil_size // highlight_size)
        "highlight_offset_x": -2,  # Piksel cinsinden ışıltı x ofseti
        "highlight_offset_y": -2,  # Piksel cinsinden ışıltı y ofseti
        "iris_ratio": 1.5,     # iris_size = pupil_size * iris_ratio
        "iris_visible": True   # İris görünür olsun mu?
    }
    
    # Duygu durumuna göre parametreleri ayarla
    if base_emotion == "happy":
        params["size"] = 7
        params["highlight_size"] = 3
        params["iris_ratio"] = 1.6
    elif base_emotion == "sad":
        params["size"] = 9
        params["highlight_size"] = 5
        params["highlight_offset_x"] = -1
        params["highlight_offset_y"] = -1
    elif base_emotion == "angry":
        params["size"] = 10
        params["highlight_size"] = 6
        params["iris_ratio"] = 1.3
    elif base_emotion == "surprised":
        params["size"] = 6
        params["highlight_size"] = 3
        params["iris_ratio"] = 1.7
    elif base_emotion == "fearful":
        params["size"] = 6
        params["highlight_size"] = 4
        params["iris_ratio"] = 1.8
    elif base_emotion == "disgusted":
        params["size"] = 10
        params["highlight_size"] = 5
    
    # Alt duygu tiplerinin özel ayarları
    if emotion == "excited":
        params["size"] = 6
        params["highlight_size"] = 2
    elif emotion == "terrified":
        params["size"] = 5
        params["highlight_size"] = 3
    elif emotion == "enraged":
        params["size"] = 11
        params["highlight_size"] = 7
    
    return params
```

Ve bu fonksiyonu `draw_eyes` metodunda kullanalım:

```python
def draw_eyes(self, emotion: str, blink_state: bool) -> None:
    # ...mevcut kod...
    
    # Kaş parametrelerini belirle
    eyebrow_params = self._get_eyebrow_params(emotion, base_emotion)
    
    # Göz bebeği parametrelerini belirle
    pupil_params = self._get_pupil_params(emotion, base_emotion)
    
    # ...mevcut kod devamı...
    
                    # Göz bebeği çizimi
                    pupil_size = min(width, height) // pupil_params["size"]
                    
                    # ...mevcut kod devamı...
                    
                    # Love duygusu haricinde göz bebeği çiz
                    if base_emotion != "love":
                        # İrisi çiz (göz bebeğinin çevresi)
                        if pupil_params["iris_visible"]:
                            iris_size = int(pupil_size * pupil_params["iris_ratio"])
                            iris_coords = (
                                center_x - iris_size + pupil_offset_x, 
                                center_y - iris_size + pupil_offset_y, 
                                center_x + iris_size + pupil_offset_x, 
                                center_y + iris_size + pupil_offset_y
                            )
                            # İrisi çiz
                            draw.ellipse(iris_coords, outline=1, fill=0)
                        
                        # Göz bebeği çiz
                        ellipse_coords = (
                            center_x - pupil_size + pupil_offset_x, 
                            center_y - pupil_size + pupil_offset_y, 
                            center_x + pupil_size + pupil_offset_x, 
                            center_y + pupil_size + pupil_offset_y
                        )
                        draw.ellipse(ellipse_coords, fill=1)
                        
                        # Işıltı ekle
                        highlight_size = max(1, pupil_size // pupil_params["highlight_size"])
                        highlight_offset_x = pupil_params["highlight_offset_x"]
                        highlight_offset_y = pupil_params["highlight_offset_y"]
                        
                        highlight_coords = (
                            center_x - pupil_size//2 + pupil_offset_x + highlight_offset_x, 
                            center_y - pupil_size//2 + pupil_offset_y + highlight_offset_y,
                            center_x - pupil_size//2 + pupil_offset_x + highlight_offset_x + highlight_size,
                            center_y - pupil_size//2 + pupil_offset_y + highlight_offset_y + highlight_size
                        )
                        draw.ellipse(highlight_coords, fill=0)
                        
                    # Kaşları çiz (eğer kaş_ekleme.md dokümantasyonundaki değişiklikler yapıldıysa)
                    if hasattr(self, '_draw_eyebrows'):
                        self._draw_eyebrows(draw, eye_name, center_x, center_y, width, height, eyebrow_params)
```

## Test Kodu

Göz bebeği ve ışıltı özelliklerini test etmek için basit bir test betiği oluşturalım:

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

logger = logging.getLogger("eye_details_test")

def main():
    parser = argparse.ArgumentParser(description="FACE1 Göz Detayları Test Programı")
    parser.add_argument('--sim', action='store_true', help='Simülasyon modunda çalıştır')
    parser.add_argument('--emotion', type=str, default='all', help='Test edilecek duygu (tüm duygular için "all")')
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
        "sleepy", "love"
    ]
    
    # OLED kontrolcüsünü başlat
    controller = OLEDController(test_config)
    if controller.start():
        logger.info("OLED kontrolcü başlatıldı.")
        
        try:
            # Belirli bir duygu test edilecekse
            if args.emotion != 'all' and args.emotion in emotions:
                test_emotions = [args.emotion]
            else:
                test_emotions = emotions
                
            # Her duygu için test
            for emotion in test_emotions:
                logger.info(f"Duygu gösteriliyor: {emotion}")
                controller.set_emotion(emotion)
                
                # Gösterimi daha rahat görebilmek için 3 saniye bekle
                time.sleep(3)
                
                # Göz hareketi testi (gözler farklı yönlere bakarken göz bebeği ve ışıltı pozisyonlarını test et)
                if args.emotion == 'all':
                    # Tüm duygular test ediliyorsa her duygu için göz hareketi testi yapma
                    continue
                
                # Sağa bak
                controller.look_at(0.8, 0)
                time.sleep(1)
                
                # Sola bak
                controller.look_at(-0.8, 0)
                time.sleep(1)
                
                # Yukarı bak
                controller.look_at(0, -0.8)
                time.sleep(1)
                
                # Aşağı bak
                controller.look_at(0, 0.8)
                time.sleep(1)
                
                # Merkeze bak
                controller.look_at(0, 0)
                time.sleep(1)
                
                # Düzenli göz kırpma
                controller.blink()
                time.sleep(0.3)
                
            logger.info("Göz detayları testi tamamlandı")
            
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

## Ekstra Özellikler

### 1. Farklı Göz Bebeği Şekilleri

Farklı duygu durumları için farklı göz bebeği şekilleri ekleyebilirsiniz:

```python
def _draw_pupil(self, draw, center_x, center_y, pupil_offset_x, pupil_offset_y, params, emotion):
    """
    Göz bebeğini çizer
    
    Args:
        draw: PIL Draw nesnesi
        center_x: Göz merkezi x koordinatı
        center_y: Göz merkezi y koordinatı
        pupil_offset_x: Göz bebeği x ofseti
        pupil_offset_y: Göz bebeği y ofseti
        params: Göz bebeği parametreleri
        emotion: Duygu durumu
    """
    pupil_size = params["size"]
    
    # Konum hesapla
    pupil_x = center_x + pupil_offset_x
    pupil_y = center_y + pupil_offset_y
    
    # Göz bebeği türünü belirle
    pupil_type = params.get("type", "circle")
    
    if pupil_type == "circle":
        # Normal yuvarlak göz bebeği
        draw.ellipse(
            (pupil_x - pupil_size, pupil_y - pupil_size,
             pupil_x + pupil_size, pupil_y + pupil_size),
            fill=1
        )
    elif pupil_type == "cat":
        # Kedi gözü (dikey elips)
        draw.ellipse(
            (pupil_x - pupil_size//2, pupil_y - pupil_size,
             pupil_x + pupil_size//2, pupil_y + pupil_size),
            fill=1
        )
    elif pupil_type == "heart":
        # Kalp şeklinde göz bebeği (love duygusu için)
        heart_size = pupil_size
        
        # İki daire yan yana
        left_circle = (pupil_x - heart_size//2, pupil_y - heart_size//2, 
                     pupil_x, pupil_y)
        right_circle = (pupil_x, pupil_y - heart_size//2, 
                      pupil_x + heart_size//2, pupil_y)
        
        draw.ellipse(left_circle, fill=1)
        draw.ellipse(right_circle, fill=1)
        
        # Üçgen (kalp alt kısmı)
        heart_points = [
            (pupil_x - heart_size//2, pupil_y - heart_size//4),
            (pupil_x + heart_size//2, pupil_y - heart_size//4),
            (pupil_x, pupil_y + heart_size//2)
        ]
        draw.polygon(heart_points, fill=1)
    
    # Işıltı ekle (göz bebeğinin üst köşesinde)
    if params.get("highlight", True):
        highlight_size = max(1, pupil_size // params.get("highlight_size", 4))
        highlight_offset_x = params.get("highlight_offset_x", -2)
        highlight_offset_y = params.get("highlight_offset_y", -2)
        
        draw.ellipse(
            (pupil_x + highlight_offset_x, pupil_y + highlight_offset_y,
             pupil_x + highlight_offset_x + highlight_size, 
             pupil_y + highlight_offset_y + highlight_size),
            fill=0
        )
```

### 2. Web Arayüzüne Göz Bebeği ve Işıltı Ayarları Ekleme

Web arayüzünden göz bebeği ve ışıltı ayarlarını kontrol edebilmek için theme_editor.html dosyasını güncelleyin:

```html
<!-- Göz Ayarları bölümüne göz bebeği ve ışıltı ekle -->
<div class="form-row">
    <label for="pupil-style-{{ emotion }}">Göz Bebeği Stili:</label>
    <select id="pupil-style-{{ emotion }}" class="form-control">
        <option value="circle" {% if theme_details.eyes[emotion].pupil_style == "circle" %}selected{% endif %}>Yuvarlak</option>
        <option value="cat" {% if theme_details.eyes[emotion].pupil_style == "cat" %}selected{% endif %}>Kedi Gözü</option>
        <option value="heart" {% if theme_details.eyes[emotion].pupil_style == "heart" %}selected{% endif %}>Kalp</option>
    </select>
</div>

<div class="form-row">
    <label for="iris-visible-{{ emotion }}">İris Görünür:</label>
    <input type="checkbox" id="iris-visible-{{ emotion }}" 
        {% if theme_details.eyes[emotion].iris_visible %}checked{% endif %}>
</div>

<div class="form-row">
    <label for="highlight-visible-{{ emotion }}">Işıltı Görünür:</label>
    <input type="checkbox" id="highlight-visible-{{ emotion }}" 
        {% if theme_details.eyes[emotion].highlight_visible %}checked{% endif %}>
</div>

<div class="form-row">
    <label for="highlight-size-{{ emotion }}">Işıltı Boyutu:</label>
    <input type="range" id="highlight-size-{{ emotion }}" min="2" max="6" step="1" 
        value="{{ theme_details.eyes[emotion].highlight_size }}">
    <span id="highlight-size-value-{{ emotion }}">{{ theme_details.eyes[emotion].highlight_size }}</span>
</div>
```

## Sonuç

Göz bebeği ve ışıltı eklemek, FACE1 projenizin görsel ifadesini önemli ölçüde iyileştirecektir. Göz bebekleri duyguları ifade etmede önemli bir rol oynar ve ışıltı efekti gözlere canlılık katar. Bu değişiklikler, robotunuza daha insansı ve etkileyici bir görünüm kazandıracaktır.

TTP223 dokunmatik sensör ve kaş özelliklerinin ardından, göz bebeği ve ışıltı eklemek robotunuzu daha da etkileyici ve ifade dolu yapacaktır!