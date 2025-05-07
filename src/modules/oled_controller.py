#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: oled_controller.py
# Açıklama: OLED ekranları kontrol eden ana modül. Tüm alt modülleri birleştirir.
# Bağımlılıklar: PIL, adafruit_ssd1306, threading, logging, time
# Bağlı Dosyalar: hardware_defines.py, oled_controller_base.py, oled_controller_display.py, oled_controller_animations.py

# Versiyon: 0.3.2
# Değişiklikler:
# - [0.3.2] Çevresel faktörlere tepki veren ifadeler eklendi
# - [0.3.1] Modül 3'e bölündü: temel, gösterim ve animasyon modülleri
# - [0.3.0] Duygu alt tiplerinin görsel ifadeleri geliştirildi, duygu geçişleri daha akıcı hale getirildi
# - [0.2.0] Göz takibi özelliği ve mikro ifadeler eklendi, enerji tasarrufu modu geliştirildi
# - [0.1.1] Simülasyon modu eklendi ve geliştirildi
# - [0.1.0] Temel OLED kontrolcü sınıfı oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-04-30
===========================================================
"""
import os
import sys
import time
import random
import logging
import threading
from typing import Dict, List, Tuple, Optional, Union
from pathlib import Path

# Proje dizinini ve include dizinini Python yoluna ekle
PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(str(PROJECT_DIR))

from include import hardware_defines

# Logger yapılandırması
logger = logging.getLogger("OLEDController")

# Alt modülleri içe aktar
from .oled_controller_base import OLEDController as OLEDControllerBase
from .oled_controller_display import OLEDDisplayMixin
from .oled_controller_animations import OLEDAnimationsMixin

class OLEDController(OLEDControllerBase, OLEDDisplayMixin, OLEDAnimationsMixin):
    """
    OLED ekranları kontrol eden ana sınıf
    
    Bu sınıf, temel OLED kontrolcü, çizim fonksiyonları ve animasyon fonksiyonlarını birleştirir.
    """
    
    def __init__(self, config):
        """
        OLED kontrolcü sınıfını başlatır
        
        Args:
            config (dict): Yapılandırma ayarları
        """
        # Temel sınıfı başlat
        OLEDControllerBase.__init__(self, config)
        
        # Animasyon döngüsüne emotion_transition güncelleme işlevi ekle
        self._original_animation_loop = self._animation_loop
        self._animation_loop = self._extended_animation_loop
    
    def _extended_animation_loop(self) -> None:
        """
        Genişletilmiş animasyon döngüsü (duygu geçişlerini destekler)
        """
        logger.info("Genişletilmiş animasyon döngüsü başlatıldı")
        
        while self.is_running:
            loop_start = time.time()
            
            try:
                # Güç tasarrufu kontrolü
                self._check_power_saving_mode()
                
                # Duygu geçişi güncelleme
                self.update_emotion_transition()
                
                # Göz pozisyonu güncelleme
                self._update_eye_position()
                
                # Göz kırpma kontrolü
                self._update_blink_state()
                
                # Mikro ifade kontrolü
                self._update_micro_expression()
                
                # Çevresel faktörlere tepki kontrolü
                self.react_to_environmental_factors()
                
                # Ekranlara çizim yap
                self._draw_all_displays()
                
                # Ekranları güncelle
                if self.power_mode != "off":
                    self.update_display()
                
            except Exception as e:
                logger.error(f"Animasyon döngüsünde hata: {e}")
            
            # FPS kontrolü
            elapsed = time.time() - loop_start
            sleep_time = max(0, self.frame_delay - elapsed)
            
            if sleep_time > 0:
                time.sleep(sleep_time)
            elif elapsed > 1.5 * self.frame_delay:
                logger.warning(f"Animasyon döngüsü yavaş çalışıyor: {elapsed:.4f} saniye (hedef: {self.frame_delay:.4f})")
    
    def _get_random_blink_interval(self) -> float:
        """
        Rastgele göz kırpma aralığı üretir
        
        Returns:
            float: Göz kırpma aralığı (saniye)
        """
        min_interval = self.config.get("animation", {}).get("blink_interval_min", 2.0)
        max_interval = self.config.get("animation", {}).get("blink_interval_max", 10.0)
        return random.uniform(min_interval, max_interval)
    
    def show_startup_animation(self) -> None:
        """
        Başlangıç animasyonunu gösterir
        """
        logger.info("Başlangıç animasyonu gösteriliyor")
        
        try:
            # Güç modunu açık olarak ayarla
            self.set_power_mode("on")
            
            # Başlangıç durumunu temizle
            self._clear_all_displays()
            self.update_display()
            time.sleep(0.2)
            
            # Göz kırpma animasyonu
            self.animate_blink(immediate=True)
            time.sleep(0.3)
            
            # Göz açılma
            self._update_blink_state(False)
            self._draw_all_displays()
            self.update_display()
            time.sleep(0.3)
            
            # Göz bakışı
            look_sequence = [
                (-0.7, 0), (0.7, 0), (0, -0.5), (0, 0.5), (0, 0)
            ]
            
            for pos in look_sequence:
                self.look_at(pos[0], pos[1], 0.3)
                time.sleep(0.4)
            
            # Başlangıç duygu durumu
            default_emotion = self.config.get("emotions", {}).get("default_emotion", "neutral")
            self.set_emotion(default_emotion)
            
            # Son göz kırpma
            time.sleep(0.5)
            self.animate_blink(immediate=True)
            
            # Aktivite zamanını güncelle
            self.last_activity_time = time.time()
            
            # Rastgele göz hareketini etkinleştir
            self.enable_random_eye_movement(True)
            
            logger.info("Başlangıç animasyonu tamamlandı")
            
        except Exception as e:
            logger.error(f"Başlangıç animasyonu gösterilirken hata: {e}")
            
            # Hata durumunda varsayılan duygu durumunu göster
            try:
                default_emotion = self.config.get("emotions", {}).get("default_emotion", "neutral")
                self.set_emotion(default_emotion)
            except Exception:
                pass

# Test kodu
if __name__ == "__main__":
    # Logging yapılandırması
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Varsayılan yapılandırma
    test_config = {
        "hardware": {
            "platform": "desktop",  # "raspberry_pi" veya "desktop"
            "simulation_mode": True,  # Simülasyon modunu zorla
            "oled_displays": {
                "left_eye": {"i2c_address": "0x3C", "width": 128, "height": 64},
                "right_eye": {"i2c_address": "0x3D", "width": 128, "height": 64},
                "mouth": {"i2c_address": "0x3E", "width": 128, "height": 64}
            },
            "use_multiplexer": False
        },
        "animation": {
            "fps": 30,
            "blink_interval_min": 2.0,
            "blink_interval_max": 10.0
        },
        "emotions": {
            "default_emotion": "calm"
        }
    }
    
    print("OLED Kontrolcü Test")
    print("-------------------")
    
    platform_type = hardware_defines.detect_platform()
    print(f"Platform: {platform_type}")
    
    # OLED kontrolcü örneği oluştur
    controller = OLEDController(test_config)
    
    # Kontrolcüyü başlat
    if controller.start():
        print("OLED kontrolcü başarıyla başlatıldı")
        
        # Başlangıç animasyonunu göster
        controller.show_startup_animation()
        
        # Farklı duygu durumlarını test et
        emotions = ["happy", "sad", "angry", "surprised", "confused", "sleepy", "excited", "bored", "love", "calm"]
        
        for emotion in emotions:
            print(f"Duygu test ediliyor: {emotion}")
            # Yumuşak geçiş ile duygu değişimi
            controller.start_emotion_transition(emotion, duration=1.5)
            time.sleep(3)  # Her duygu durumunu 3 saniye göster
        
        # Mikro ifade testi
        print("Mikro ifadeler test ediliyor")
        for emotion in ["surprised", "happy", "angry"]:
            print(f"Mikro ifade gösteriliyor: {emotion}")
            controller.show_micro_expression(emotion, duration=0.5)
            time.sleep(1.5)
        
        # Göz takibi testi
        print("Göz takibi test ediliyor")
        for pos in [(-0.8, 0), (0.8, 0), (0, -0.8), (0, 0.8), (0, 0)]:
            print(f"Göz pozisyonu: {pos}")
            controller.look_at(pos[0], pos[1])
            time.sleep(1.5)
        
        # Otomatik göz hareketini yeniden etkinleştir
        controller.enable_random_eye_movement(True)
        
        # Çevresel faktör tepkilerini test et
        print("\nÇevresel faktörlere tepki testi")
        for reaction_type in ["hot", "cold", "bright", "dark", "sleepy", "energetic"]:
            print(f"Çevresel tepki test ediliyor: {reaction_type}")
            controller.show_environmental_reaction(reaction_type, 25.0)
            time.sleep(3)
        
        time.sleep(2)
        
        # Temizle ve kapat
        controller.stop()
        print("OLED kontrolcü durduruldu")
        
        print("Simülasyon dosyalarını kontrol edin: " + os.path.join(PROJECT_DIR, "simulation"))
    else:
        print("OLED kontrolcü başlatılamadı!")
    
    print("Test tamamlandı")
