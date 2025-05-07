#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: led_controller_colors.py
# Açıklama: LED renk işlemleri ve duygu-renk eşleştirmeleri için modül.
# Bağımlılıklar: logging
# Bağlı Dosyalar: led_controller_base.py

# Versiyon: 0.4.0
# Değişiklikler:
# - [0.4.0] led_controller.py dosyasından bölündü (modüler mimari)
# - [0.2.0] Renk harmonileri sistemi ve gelişmiş renk işleme fonksiyonları eklendi
# - [0.1.0] Temel LED kontrolcü sınıfı ve renk ayarları oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-02
===========================================================
"""

import logging
from typing import Dict, List, Tuple

from .led_controller_base import LEDControllerBase

# Logger yapılandırması
logger = logging.getLogger("LEDController")


class LEDControllerColors:
    """
    LED renk işlemleri için karışım (mixin) sınıfı
    
    Bu sınıf, LED kontrolcü için renk işlevlerini ve duygu-renk eşleştirmelerini sağlar.
    LEDControllerBase sınıfını genişletir.
    """
    
    # Duygu renkleri (r, g, b)
    EMOTION_COLORS = {
        "happy": (255, 255, 0),      # Sarı
        "sad": (0, 0, 255),          # Mavi
        "angry": (255, 0, 0),        # Kırmızı
        "surprised": (255, 0, 255),  # Mor
        "calm": (0, 255, 255),       # Cyan
        "disgusted": (0, 128, 0),    # Koyu yeşil
        "fearful": (128, 0, 128),    # Koyu mor
        "neutral": (255, 255, 255),  # Beyaz
        "confused": (200, 100, 255), # Mor-pembe
        "sleepy": (100, 100, 150),   # Açık mavi
        "excited": (255, 150, 0),    # Turuncu
        "bored": (100, 100, 100),    # Gri
        "love": (255, 50, 150)       # Pembe
    }
    
    # Duygu bazlı animasyon hızları (ms)
    EMOTION_SPEEDS = {
        "happy": 30,       # Hızlı ve enerji dolu
        "sad": 120,        # Yavaş ve kasvetli
        "angry": 20,       # Çok hızlı, agresif
        "surprised": 40,   # Hızlı ve dikkat çekici
        "calm": 80,        # Rahatlatıcı, yavaş tempo
        "disgusted": 70,   # Orta-yavaş
        "fearful": 30,     # Hızlı, tedirgin
        "neutral": 60,     # Normal, standart hız
        "confused": 50,    # Kararsız, değişken
        "sleepy": 150,     # Çok yavaş
        "excited": 25,     # Çok hızlı, enerjik
        "bored": 100,      # Yavaş, tekdüze
        "love": 60         # Normal, yumuşak
    }
    
    # Gelişmiş renk harmonileri
    COLOR_HARMONIES = {
        "monochromatic": lambda self, color, idx: self._adjust_brightness(color, 0.5 + 0.5 * (idx / 5)),
        "complementary": lambda self, color, idx: self._complement_color(color) if idx % 2 else color,
        "analogous": lambda self, color, idx: self._rotate_hue(color, (idx - 2) * 30),
        "triadic": lambda self, color, idx: self._rotate_hue(color, (idx % 3) * 120),
        "tetradic": lambda self, color, idx: self._rotate_hue(color, (idx % 4) * 90),
        "split_complementary": lambda self, color, idx: self._rotate_hue(self._complement_color(color), (idx % 2) * 60 - 30)
    }
    
    def __init__(self):
        """
        Renk modülünün başlatıcısı
        
        Not: Mixin sınıf olarak kullanıldığından, bu başlatıcı genelde çağrılmaz.
        """
        # Renk harmonisi ayarları
        self.color_harmony = "monochromatic"  # varsayılan
    
    def set_emotion_color(self, emotion: str, zone_name: str = "all") -> None:
        """
        Duygu durumuna göre renk ayarlar
        
        Args:
            emotion (str): Duygu durumu ("happy", "sad", vb.)
            zone_name (str, optional): Bölge adı. Varsayılan: "all"
        """
        # Duygu rengini al
        color = self.get_color_for_emotion(emotion)
        
        # Rengi ayarla
        self.set_color(color[0], color[1], color[2], zone_name)
        
        # Aktivite zamanlayıcısını sıfırla
        self.reset_activity_timer()
        
        logger.info(f"Duygu rengi ayarlandı: {emotion} -> {color}, bölge: {zone_name}")
    
    def get_color_for_emotion(self, emotion: str) -> Tuple[int, int, int]:
        """
        Duygu durumuna göre renk döndürür
        
        Args:
            emotion (str): Duygu durumu ("happy", "sad", vb.)
            
        Returns:
            Tuple[int, int, int]: RGB renk değerleri
        """
        # Duygu geçerliliğini kontrol et
        emotion = emotion.lower()
        if emotion not in self.EMOTION_COLORS:
            logger.warning(f"Bilinmeyen duygu: {emotion}, 'neutral' kullanılıyor")
            emotion = "neutral"
        
        return self.EMOTION_COLORS[emotion]
    
    def set_color_harmony(self, harmony_type: str) -> None:
        """
        Renk harmonisi tipini ayarlar
        
        Args:
            harmony_type (str): Harmoni tipi (monochromatic, complementary, analogous, triadic, tetradic, split_complementary)
        """
        if harmony_type in self.COLOR_HARMONIES:
            self.color_harmony = harmony_type
            logger.info(f"Renk harmonisi ayarlandı: {harmony_type}")
        else:
            logger.warning(f"Geçersiz renk harmonisi: {harmony_type}, 'monochromatic' kullanılıyor")
            self.color_harmony = "monochromatic"
    
    def _generate_harmony_colors(self, base_color: Tuple[int, int, int], count: int = 5) -> List[Tuple[int, int, int]]:
        """
        Temel bir renkten, seçilen harmoni tipine göre bir dizi uyumlu renk oluşturur
        
        Args:
            base_color (Tuple[int, int, int]): Temel RGB renk
            count (int, optional): Oluşturulacak renk sayısı. Varsayılan: 5
        
        Returns:
            List[Tuple[int, int, int]]: Uyumlu renklerin listesi
        """
        harmony_func = self.COLOR_HARMONIES.get(self.color_harmony, self.COLOR_HARMONIES["monochromatic"])
        
        colors = []
        for i in range(count):
            colors.append(harmony_func(self, base_color, i))
        
        return colors
    
    def _adjust_brightness(self, color: Tuple[int, int, int], factor: float) -> Tuple[int, int, int]:
        """
        Rengin parlaklığını ayarlar
        
        Args:
            color (Tuple[int, int, int]): RGB renk değerleri
            factor (float): Parlaklık faktörü (0.0-1.0+)
        
        Returns:
            Tuple[int, int, int]: Ayarlanmış RGB renk değerleri
        """
        return (
            int(min(255, max(0, color[0] * factor))),
            int(min(255, max(0, color[1] * factor))),
            int(min(255, max(0, color[2] * factor)))
        )
    
    def _complement_color(self, color: Tuple[int, int, int]) -> Tuple[int, int, int]:
        """
        Rengin tamamlayıcısını (complementary) döndürür
        
        Args:
            color (Tuple[int, int, int]): RGB renk değerleri
        
        Returns:
            Tuple[int, int, int]: Tamamlayıcı RGB renk değerleri
        """
        return (
            255 - color[0],
            255 - color[1],
            255 - color[2]
        )
    
    def _rotate_hue(self, color: Tuple[int, int, int], degrees: int) -> Tuple[int, int, int]:
        """
        Rengin tonunu belirli bir derece döndürür
        
        Args:
            color (Tuple[int, int, int]): RGB renk değerleri
            degrees (int): Döndürme derecesi (0-360)
        
        Returns:
            Tuple[int, int, int]: Döndürülmüş RGB renk değerleri
        """
        # RGB'yi HSV'ye dönüştür
        r, g, b = color
        r, g, b = r/255.0, g/255.0, b/255.0
        
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        delta = max_val - min_val
        
        # Ton (hue)
        if delta == 0:
            h = 0
        elif max_val == r:
            h = ((g - b) / delta) % 6
        elif max_val == g:
            h = (b - r) / delta + 2
        else:
            h = (r - g) / delta + 4
        
        h = (h * 60) % 360
        
        # Doygunluk (saturation)
        s = 0 if max_val == 0 else delta / max_val
        
        # Değer (value)
        v = max_val
        
        # Tonu döndür
        h = (h + degrees) % 360
        
        # HSV'yi RGB'ye geri dönüştür
        c = v * s
        x = c * (1 - abs((h / 60) % 2 - 1))
        m = v - c
        
        if 0 <= h < 60:
            r, g, b = c, x, 0
        elif 60 <= h < 120:
            r, g, b = x, c, 0
        elif 120 <= h < 180:
            r, g, b = 0, c, x
        elif 180 <= h < 240:
            r, g, b = 0, x, c
        elif 240 <= h < 300:
            r, g, b = x, 0, c
        else:
            r, g, b = c, 0, x
        
        r, g, b = int((r + m) * 255), int((g + m) * 255), int((b + m) * 255)
        
        return (r, g, b)
    
    def on_theme_changed(self, theme_data: Dict) -> None:
        """
        Tema değiştiğinde çağrılan fonksiyon
        
        Args:
            theme_data (Dict): Tema verileri
        """
        try:
            # Tema verilerinden LED ayarlarını al
            led_config = theme_data.get("led", {})
            
            # Renk harmonisini güncelle
            harmony = led_config.get("color_harmony")
            if harmony:
                self.set_color_harmony(harmony)
            
            # Mevcut duygu rengini güncelle (eğer animasyon çalışmıyorsa)
            if hasattr(self, 'animation_running') and not self.animation_running and "default_emotion" in theme_data:
                emotion = theme_data["default_emotion"]
                self.set_emotion_color(emotion)
                
            logger.info(f"LED teması güncellendi: {theme_data.get('theme_name', 'unknown')}")
            
        except Exception as e:
            logger.error(f"Tema değişikliği işlenirken hata: {e}")