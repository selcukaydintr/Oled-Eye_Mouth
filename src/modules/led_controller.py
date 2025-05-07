#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: led_controller.py
# Açıklama: LED kontrolcü ana sınıfı (mixin sınıfları bir araya getirir)
# Bağımlılıklar: rpi_ws281x, PIL, logging
# Bağlı Dosyalar: led_controller_base.py, led_controller_animations.py, led_controller_colors.py, led_controller_patterns.py

# Versiyon: 0.4.0
# Değişiklikler:
# - [0.4.0] Modüler mimariye dönüştürüldü (mixin sınıflar kullanılarak)
# - [0.2.0] Gelişmiş renk harmonileri ve animasyon desenleri eklendi
# - [0.1.1] Simülasyon modu geliştirildi
# - [0.1.0] Temel LED kontrolcü sınıfı oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-02
===========================================================
"""

import logging
from typing import Dict, Tuple, Optional

from .led_controller_base import LEDControllerBase, AnimationPattern
from .led_controller_animations import LEDControllerAnimations
from .led_controller_colors import LEDControllerColors
from .led_controller_patterns import LEDControllerPatterns

# Logger yapılandırması
logger = logging.getLogger("LEDController")


class LEDController(LEDControllerBase, LEDControllerAnimations, LEDControllerColors, LEDControllerPatterns):
    """
    WS2812B LED şeritlerini kontrol etmek için ana sınıf
    
    Bu sınıf, LED kontrolcü mixin sınıflarını bir araya getiren kompozitör sınıfıdır.
    Mixin sınıflar:
    - LEDControllerBase: Temel işlevler (başlatma, durdurma, temizleme)
    - LEDControllerAnimations: Animasyon işlevleri
    - LEDControllerColors: Renk işlevleri ve duygu-renk eşleştirmeleri
    - LEDControllerPatterns: Işık desenleri ve duygu-animasyon eşleştirmeleri
    """
    
    def __init__(self, config):
        """
        LED kontrolcüsünü başlatır
        
        Args:
            config (dict): Yapılandırma ayarları
        """
        # Temel sınıf başlatıcılarını çağır
        LEDControllerBase.__init__(self, config)
        
        # Diğer mixin sınıflar için başlatma özelliklerini ayarla
        # LEDControllerAnimations için özellikle bir başlatıcı çağrısı gerekmez
        # LEDControllerColors için başlatıcı çağrısı
        if hasattr(LEDControllerColors, '__init__'):
            LEDControllerColors.__init__(self)
            
        # LEDControllerPatterns için özellikle bir başlatıcı çağrısı gerekmez
        
        logger.info("LED Kontrolcü (modüler mimari) başlatıldı")
    
    def _save_simulation_image(self, skip_frames: int = 1) -> None:
        """
        Simülasyon modunda LED durumunu bir görüntü dosyasına kaydeder (override)
        
        Args:
            skip_frames (int, optional): Kaç karede bir görüntü kaydedileceği. Varsayılan: 1
        """
        # Önce temel sınıftaki metodu çağır
        try:
            # Super() ile temel sınıfın metodunu çağırmayı dene
            super()._save_simulation_image(skip_frames)
            return
        except Exception as e:
            logger.debug(f"Temel sınıftaki _save_simulation_image metodu çağrılamadı: {e}")
        
        # Temel sınıftaki metot çalışmazsa, kendi implementasyonumuzu dene
        if not self.simulation_mode or not hasattr(self, 'sim_leds'):
            return
            
        # Performans için frame skip kontrolü
        if hasattr(self, 'frame_counter'):
            self.frame_counter += 1
            if self.frame_counter % skip_frames != 0:
                return
        
        try:
            from PIL import Image, ImageDraw
            
            # Görüntü boyutunu belirle
            led_radius = 10
            spacing = 5
            width = max(100, self.led_count * (led_radius * 2 + spacing))
            height = led_radius * 2 + 20  # Üst ve alt kenar boşlukları
            
            # Görüntü oluştur
            image = Image.new('RGB', (width, height), (0, 0, 0))
            draw = ImageDraw.Draw(image)
            
            # LED'lerin konumlarını hesapla
            led_width = led_radius * 2 + spacing
            total_width = led_width * self.led_count - spacing
            start_x = (width - total_width) // 2
            
            # Her LED'i çiz
            for i, color in enumerate(self.sim_leds):
                x = start_x + i * led_width
                y = height // 2
                
                # LED dairesini çiz
                draw.ellipse(
                    (x - led_radius, y - led_radius, x + led_radius, y + led_radius),
                    fill=color
                )
            
            # Zaman damgalı dosya adı oluştur
            import time
            timestamp = int(time.time())
            frame_num = getattr(self, 'frame_counter', 0)
            if skip_frames > 1:
                frame_num = (frame_num // skip_frames) * 10
            filename = f"led_simulation_{timestamp}_{frame_num:04d}.png"
            
            # Görüntüyü kaydet
            if hasattr(self, 'sim_dir'):
                import os
                filepath = os.path.join(self.sim_dir, filename)
                image.save(filepath)
                logger.debug(f"Simülasyon görüntüsü kaydedildi: {filename}")
                
        except Exception as e:
            logger.error(f"Simülasyon görüntüsü kaydedilirken hata: {e}")
    
    def on_emotion_changed(self, emotion_data: Dict) -> None:
        """
        Duygu değişikliğinde çağrılan metod
        
        Args:
            emotion_data (Dict): Duygu verileri
        """
        # Duygu verilerinden ana duyguyu al
        emotion = emotion_data.get("emotion", "neutral")
        
        # Eğer duygulara göre LED animasyonu etkinse
        animate_emotions = self.config.get("leds", {}).get("animate_emotions", True)
        
        if animate_emotions:
            self.animate_emotion(emotion)
        else:
            # Sadece rengi değiştir
            self.set_emotion_color(emotion)
            
        logger.debug(f"LED duygu değişikliği işlendi: {emotion}")
    
    def get_state(self) -> Dict:
        """
        LED kontrolcünün mevcut durumunu döndürür
        
        Returns:
            Dict: Mevcut durum bilgisi
        """
        # Temel durum bilgilerini al
        state = super().get_state()
        
        # Ek durum bilgileri
        if hasattr(self, 'color_harmony'):
            state["color_harmony"] = self.color_harmony
        
        return state