#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: led_controller_patterns.py
# Açıklama: LED ışık desenleri ve duygu-animasyon eşleştirmeleri için modül.
# Bağımlılıklar: logging
# Bağlı Dosyalar: led_controller_base.py, led_controller_animations.py

# Versiyon: 0.4.0
# Değişiklikler:
# - [0.4.0] led_controller.py dosyasından bölündü (modüler mimari)
# - [0.2.0] Duygu bazlı animasyon ve renk eşleştirme geliştirildi
# - [0.1.0] Temel LED kontrol işlevleri oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-02
===========================================================
"""

import logging
import time
import threading
from typing import Dict, Optional, Tuple

from .led_controller_base import AnimationPattern, LEDControllerBase

# Logger yapılandırması
logger = logging.getLogger("LEDController")


class LEDControllerPatterns:
    """
    LED ışık desenleri için karışım (mixin) sınıfı
    
    Bu sınıf, LED kontrolcü için ışık desenleri ve duygu-animasyon eşleştirmelerini sağlar.
    LEDControllerBase sınıfını genişletir.
    """
    
    # Duygu-animasyon eşleştirmeleri
    EMOTION_ANIMATIONS = {
        "happy": AnimationPattern.PULSE,
        "sad": AnimationPattern.BREATHE,
        "angry": AnimationPattern.WIPE,
        "surprised": AnimationPattern.SPARKLE,
        "fearful": AnimationPattern.CHASE,
        "disgusted": AnimationPattern.FADE,
        "calm": AnimationPattern.RAINBOW,
        "neutral": AnimationPattern.STATIC,
        "confused": AnimationPattern.WAVE,
        "sleepy": AnimationPattern.FADE,
        "excited": AnimationPattern.TWINKLE,
        "bored": AnimationPattern.STATIC,
        "love": AnimationPattern.COLOR_FADE
    }
    
    def animate_emotion(self, emotion: str, speed: Optional[int] = None, zone_name: str = "all") -> None:
        """
        Duygu durumuna göre animasyon başlatır
        
        Args:
            emotion (str): Duygu durumu ("happy", "sad", vb.)
            speed (int, optional): Animasyon hızı (ms). Belirtilmezse duygu için varsayılan hız kullanılır.
            zone_name (str, optional): Bölge adı. Varsayılan: "all"
        """
        # Gerekli özelliklere sahip olup olmadığını kontrol et
        required_attributes = ['EMOTION_ANIMATIONS', 'EMOTION_SPEEDS', 'EMOTION_COLORS', 'animate', 'get_color_for_emotion']
        for attr in required_attributes:
            if not hasattr(self, attr):
                logger.error(f"animate_emotion metodunun kullanılabilmesi için '{attr}' özelliği gerekli")
                return
        
        # Duygu durumuna göre animasyon tipi seç
        animation_map = self.EMOTION_ANIMATIONS
        
        # Duygu geçerliliğini kontrol et
        emotion = emotion.lower()
        if emotion not in animation_map:
            logger.warning(f"Bilinmeyen duygu: {emotion}, 'neutral' kullanılıyor")
            emotion = "neutral"
        
        # Hız ayarı (belirtilmemişse duyguya özel hız)
        if speed is None:
            speed = self.EMOTION_SPEEDS.get(emotion, 50)
        
        # Duygu rengini al
        color = self.get_color_for_emotion(emotion)
        
        # Animasyonu başlat
        self.animate(animation_map[emotion], color, speed, zone_name)
    
    def start_power_save_timer(self) -> None:
        """
        Enerji tasarrufu zamanlayıcısını başlatır
        """
        if not hasattr(self, 'power_save_enabled') or not self.power_save_enabled:
            return
            
        # Daha önce başlatılmış bir zamanlayıcı varsa iptal et
        if hasattr(self, 'power_save_timer') and self.power_save_timer:
            self.power_save_timer.cancel()
        
        # Yeni zamanlayıcı başlat
        self.power_save_timer = threading.Timer(self.power_save_dim_delay, self._enter_power_save_mode)
        self.power_save_timer.daemon = True
        self.power_save_timer.start()
        
        logger.debug(f"Enerji tasarrufu zamanlayıcısı başlatıldı: {self.power_save_dim_delay} saniye")
    
    def _enter_power_save_mode(self) -> None:
        """
        Enerji tasarrufu moduna girer
        """
        # Son aktivite üzerinden geçen süre
        elapsed_time = time.time() - self.last_activity_time
        
        # Dim modu
        if elapsed_time >= self.power_save_dim_delay:
            # Animasyon çalışıyorsa dokunma
            if not hasattr(self, 'animation_running') or not self.animation_running:
                current_brightness = self.led_brightness
                # Parlaklığı yarıya düşür
                self.set_brightness(current_brightness * 0.5)
                logger.info("Enerji tasarrufu - dim modu aktif")
        
        # Off modu
        if elapsed_time >= self.power_save_off_delay:
            # Animasyon çalışıyorsa durdur
            if hasattr(self, 'animation_running') and self.animation_running:
                self.stop()
            
            # Tüm LEDleri kapat
            self.clear()
            logger.info("Enerji tasarrufu - off modu aktif")
    
    def run_startup_animation(self) -> None:
        """
        Başlangıç animasyonunu çalıştırır
        """
        # Yapılandırmayı kontrol et
        if hasattr(self, 'config') and not self.config.get("animation", {}).get("startup_animation_enabled", True):
            logger.debug("Başlangıç animasyonu devre dışı bırakılmış")
            return
        
        # İlgili özelliklerin bulunup bulunmadığını kontrol et
        if not (hasattr(self, 'animate') and hasattr(self, 'clear')):
            logger.error("run_startup_animation metodunun kullanılabilmesi için 'animate' ve 'clear' metotları gerekli")
            return
            
        logger.info("Başlangıç animasyonu çalıştırılıyor...")
        
        try:
            # Önce temizle
            self.clear()
            time.sleep(0.5)
            
            # Örnek bir başlangıç animasyonu
            # 1. Gökkuşağı animasyonu
            self.animate(AnimationPattern.RAINBOW, speed=20, zone_name="all")
            time.sleep(2.0)
            
            # 2. Tarama animasyonu
            self.stop()
            self.animate(AnimationPattern.SCAN, (0, 0, 255), speed=20, zone_name="all")
            time.sleep(2.0)
            
            # 3. Solma animasyonu ve son renk
            self.stop()
            self.animate(AnimationPattern.FADE, (255, 255, 255), speed=40, zone_name="all")
            time.sleep(2.0)
            
            # Animasyonu durdur ve varsayılan durum için sabit rengi ayarla
            self.stop()
            self.set_emotion_color("neutral")
            
            logger.info("Başlangıç animasyonu tamamlandı")
            
        except Exception as e:
            logger.error(f"Başlangıç animasyonu çalıştırılırken hata: {e}")
    
    def create_pattern(self, pattern_type: str, **kwargs) -> Dict:
        """
        Özel bir desen yapılandırması oluşturur
        
        Args:
            pattern_type (str): Desen tipi
            **kwargs: Desene özgü parametreler
        
        Returns:
            Dict: Desen yapılandırması
        """
        pattern = {
            "type": pattern_type,
            "params": kwargs
        }
        
        logger.debug(f"Özel desen oluşturuldu: {pattern}")
        return pattern
    
    def run_pattern(self, pattern: Dict) -> None:
        """
        Bir deseni çalıştırır
        
        Args:
            pattern (Dict): Desen yapılandırması
        """
        if not isinstance(pattern, dict) or "type" not in pattern:
            logger.error("Geçersiz desen yapılandırması")
            return
        
        pattern_type = pattern["type"]
        params = pattern.get("params", {})
        
        logger.debug(f"Desen çalıştırılıyor: {pattern_type}")
        
        if pattern_type == "sequence":
            self._run_sequence_pattern(**params)
        elif pattern_type == "alternate":
            self._run_alternate_pattern(**params)
        elif pattern_type == "chase":
            self._run_chase_pattern(**params)
        elif pattern_type == "custom":
            self._run_custom_pattern(**params)
        else:
            # Varsayılan olarak animate metodunu kullanır
            try:
                animation = AnimationPattern(pattern_type)
                color = params.get("color", (255, 255, 255))
                speed = params.get("speed", 50)
                zone = params.get("zone", "all")
                
                self.animate(animation, color, speed, zone)
                
            except ValueError:
                logger.warning(f"Bilinmeyen desen tipi: {pattern_type}")
    
    def _run_sequence_pattern(self, colors, speed=50, repeat=1, **kwargs):
        """
        Renk sırası desenini çalıştırır
        
        Args:
            colors (list): Renklerin listesi
            speed (int, optional): Hız. Varsayılan: 50
            repeat (int, optional): Tekrar sayısı. Varsayılan: 1
        """
        if not hasattr(self, '_set_zone_color'):
            logger.error("_run_sequence_pattern metodunun kullanılabilmesi için '_set_zone_color' metodu gerekli")
            return
            
        zone_name = kwargs.get("zone", "all")
        zone = self.zones[zone_name]
        start = zone.start_index
        count = zone.count
        
        for _ in range(repeat):
            for color in colors:
                if isinstance(color, tuple) and len(color) == 3:
                    self._set_zone_color(color, start, count)
                    time.sleep(speed / 1000.0)
    
    def _run_alternate_pattern(self, colors, speed=50, repeat=5, **kwargs):
        """
        Dönüşümlü renk desenini çalıştırır
        
        Args:
            colors (list): Renklerin listesi (en az 2)
            speed (int, optional): Hız. Varsayılan: 50
            repeat (int, optional): Tekrar sayısı. Varsayılan: 5
        """
        if not hasattr(self, '_set_zone_color'):
            logger.error("_run_alternate_pattern metodunun kullanılabilmesi için '_set_zone_color' metodu gerekli")
            return
            
        if len(colors) < 2:
            logger.warning("Alternatif desenler için en az 2 renk gerekli")
            return
            
        zone_name = kwargs.get("zone", "all")
        zone = self.zones[zone_name]
        start = zone.start_index
        count = zone.count
        
        for _ in range(repeat):
            for color in colors:
                if isinstance(color, tuple) and len(color) == 3:
                    self._set_zone_color(color, start, count)
                    time.sleep(speed / 1000.0)
    
    def _run_chase_pattern(self, color=(255, 255, 255), bg_color=(0, 0, 0), width=3, speed=50, repeat=3, **kwargs):
        """
        Takip ışık desenini çalıştırır
        
        Args:
            color (tuple, optional): Işık rengi. Varsayılan: (255, 255, 255)
            bg_color (tuple, optional): Arka plan rengi. Varsayılan: (0, 0, 0)
            width (int, optional): Işık genişliği. Varsayılan: 3
            speed (int, optional): Hız. Varsayılan: 50
            repeat (int, optional): Tekrar sayısı. Varsayılan: 3
        """
        if not hasattr(self, '_set_pixel_color') or not hasattr(self, '_set_zone_color'):
            logger.error("_run_chase_pattern metodunun kullanılabilmesi için gerekli metotlar eksik")
            return
            
        zone_name = kwargs.get("zone", "all")
        zone = self.zones[zone_name]
        start = zone.start_index
        count = zone.count
        
        for _ in range(repeat):
            for i in range(count):
                # Arka planı ayarla
                self._set_zone_color(bg_color, start, count)
                
                # Işık noktalarını ayarla
                for j in range(width):
                    idx = (i + j) % count
                    self._set_pixel_color(color, start + idx)
                
                # LEDleri güncelle
                if not self.simulation_mode and self.strip:
                    self.strip.show()
                else:
                    self._save_simulation_image()
                
                time.sleep(speed / 1000.0)
    
    def _run_custom_pattern(self, steps, **kwargs):
        """
        Özel bir deseni çalıştırır
        
        Args:
            steps (list): Adımların listesi. Her adımda {"color": (r, g, b), "duration": ms} olmalı.
        """
        if not hasattr(self, '_set_zone_color'):
            logger.error("_run_custom_pattern metodunun kullanılabilmesi için '_set_zone_color' metodu gerekli")
            return
            
        zone_name = kwargs.get("zone", "all")
        zone = self.zones[zone_name]
        start = zone.start_index
        count = zone.count
        
        for step in steps:
            color = step.get("color", (0, 0, 0))
            duration = step.get("duration", 100)  # ms
            
            if isinstance(color, tuple) and len(color) == 3:
                self._set_zone_color(color, start, count)
                time.sleep(duration / 1000.0)