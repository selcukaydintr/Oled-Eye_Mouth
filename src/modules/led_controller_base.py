#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: led_controller_base.py
# Açıklama: WS2812B LED şeritleri için temel kontrolcü modülü. Temel işlevler ve yapılandırmayı içerir.
# Bağımlılıklar: rpi_ws281x, logging, threading, time
# Bağlı Dosyalar: hardware_defines.py

# Versiyon: 0.4.0
# Değişiklikler:
# - [0.4.0] led_controller.py dosyasından bölündü (modüler mimari)
# - [0.2.0] Duygu bazlı renk harmonileri, gelişmiş animasyon seçenekleri ve tema entegrasyonu eklendi
# - [0.1.1] Simülasyon modu geliştirildi ve görselleştirme eklendi
# - [0.1.0] Temel LED kontrolcü sınıfı oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-02
===========================================================
"""

import os
import sys
import time
import logging
import threading
from typing import Dict, List, Tuple, Optional, Union, Callable
from pathlib import Path
from enum import Enum

# Proje dizinini ve include dizinini Python yoluna ekle
PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(str(PROJECT_DIR))

from include import hardware_defines

# Raspberry Pi platformlarında rpi_ws281x kütüphanesini yükle
try:
    from rpi_ws281x import PixelStrip, Color
    LED_LIBRARY_AVAILABLE = True
except ImportError:
    LED_LIBRARY_AVAILABLE = False
    
# PIL kütüphanesini yükle (simülasyon modu için)
try:
    from PIL import Image, ImageDraw
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

# Logger yapılandırması
logger = logging.getLogger("LEDController")


class AnimationPattern(Enum):
    """LED animasyon desenleri için enum"""
    STATIC = "static"           # Sabit renk
    PULSE = "pulse"             # Nabız gibi yanıp sönme
    BREATHE = "breathe"         # Nefes alma efekti
    FADE = "fade"               # Yavaşça solma
    CHASE = "chase"             # Takip eden ışıklar
    RAINBOW = "rainbow"         # Gökkuşağı renk geçişi
    SPARKLE = "sparkle"         # Pırıltı efekti
    WIPE = "wipe"               # Silme efekti
    THEATER_CHASE = "theater_chase"  # Tiyatro stili takip
    COLOR_FADE = "color_fade"   # Renkler arası geçiş
    SCAN = "scan"               # Tarama animasyonu
    TWINKLE = "twinkle"         # Yıldız parıltısı
    WAVE = "wave"               # Dalga animasyonu


class LEDZone:
    """LED şeritlerinin bölgesi için yardımcı sınıf"""
    
    def __init__(self, name: str, start_index: int, count: int):
        """
        LED bölgesi oluşturur
        
        Args:
            name (str): Bölge adı
            start_index (int): Başlangıç LED indeksi
            count (int): LED sayısı
        """
        self.name = name
        self.start_index = start_index
        self.count = count
        self.end_index = start_index + count - 1
    
    def __str__(self) -> str:
        return f"LEDZone({self.name}, start={self.start_index}, count={self.count})"


class LEDControllerBase:
    """
    WS2812B LED şeritlerini kontrol eden temel sınıf
    
    Bu sınıf, LED şeritlerini kontrol etmek için temel işlevleri sağlar.
    Raspberry Pi platformlarında rpi_ws281x kütüphanesi kullanır.
    """
    
    def __init__(self, config):
        """
        LED kontrolcüsünü başlatır
        
        Args:
            config (dict): Yapılandırma ayarları
        """
        logger.info("LED Kontrolcü başlatılıyor...")
        self.config = config
        
        # LED yapılandırması
        self.led_config = config.get("hardware", {}).get("led_strip", {})
        self.led_pin = self.led_config.get("pin", hardware_defines.DEFAULT_LED_PIN)
        self.led_count = self.led_config.get("count", hardware_defines.DEFAULT_LED_COUNT)
        self.led_brightness = self.led_config.get("brightness", hardware_defines.DEFAULT_LED_BRIGHTNESS)
        
        # LED nesnesi
        self.strip = None
        
        # LED bölgeleri
        self.zones = self._create_default_zones()
        
        # Animasyon değişkenleri
        self.current_animation = AnimationPattern.STATIC
        self.animation_speed = 50  # ms
        self.animation_color = (255, 255, 255)  # varsayılan beyaz
        self.animation_running = False
        self.animation_thread = None
        self.stop_animation = threading.Event()
        
        # Tema değişimi için callback
        self.theme_callback = None
        
        # Enerji tasarrufu seçenekleri
        self.power_save_enabled = config.get("system", {}).get("power_save_enabled", True)
        self.power_save_dim_delay = config.get("system", {}).get("power_save_dim_delay", 120)  # saniye
        self.power_save_off_delay = config.get("system", {}).get("power_save_off_delay", 300)  # saniye
        self.last_activity_time = time.time()
        
        # Platformu tespit et
        self.platform_type = hardware_defines.detect_platform()
        logger.info(f"Platform türü tespit edildi: {self.platform_type}")
        
        # Simülasyon modu kontrolü
        self.simulation_mode = (
            config.get("hardware", {}).get("simulation_mode", False) or
            self.platform_type != "raspberry_pi" or 
            not LED_LIBRARY_AVAILABLE or
            "Raspberry Pi 5" in hardware_defines.get_platform_info()
        )
        
        if self.simulation_mode:
            if self.platform_type == "raspberry_pi":
                logger.info("Simülasyon modu etkin (Raspberry Pi 5 henüz tam olarak desteklenmiyor veya yapılandırmada seçildi)")
            else:
                logger.info("Simülasyon modu etkin (Raspberry Pi platformu değil)")
            
            # Simülasyon LED durumu
            self.sim_leds = [(0, 0, 0) for _ in range(self.led_count)]
            
            # Simülasyon görüntü dosyaları için dizin
            self.sim_dir = os.path.join(PROJECT_DIR, "simulation")
            os.makedirs(self.sim_dir, exist_ok=True)
            logger.info(f"Simülasyon görüntüleri şurada saklanacak: {self.sim_dir}")
            
            # Görselleştirme için frame sayacı
            self.frame_counter = 0
            
            # Görüntü sayısı sınırlaması için parametreler
            self.max_simulation_files = 100  # Saklanacak maksimum dosya sayısı
            self.cleanup_counter = 0  # Temizleme işlemi sayacı
            self.cleanup_interval = 50  # Kaç kayıt işleminde bir temizlik yapılacağı
    
    def _create_default_zones(self) -> Dict[str, LEDZone]:
        """
        Varsayılan LED bölgelerini oluşturur
        
        Returns:
            Dict[str, LEDZone]: LED bölgeleri sözlüğü
        """
        zones = {}
        led_count = self.led_count
        
        # Toplam LED sayısına göre bölgeleri belirle
        if led_count <= 10:
            # Çok az LED varsa sadece tek bölge
            zones["all"] = LEDZone("all", 0, led_count)
        elif led_count <= 30:
            # Az-orta sayıda LED için üç bölge
            third = led_count // 3
            zones["left"] = LEDZone("left", 0, third)
            zones["middle"] = LEDZone("middle", third, third)
            zones["right"] = LEDZone("right", 2 * third, led_count - 2 * third)
        else:
            # Çok sayıda LED için beş bölge
            fifth = led_count // 5
            zones["left_outer"] = LEDZone("left_outer", 0, fifth)
            zones["left_inner"] = LEDZone("left_inner", fifth, fifth)
            zones["middle"] = LEDZone("middle", 2 * fifth, fifth)
            zones["right_inner"] = LEDZone("right_inner", 3 * fifth, fifth)
            zones["right_outer"] = LEDZone("right_outer", 4 * fifth, led_count - 4 * fifth)
        
        # Tüm LEDler için bir bölge de ekle
        if "all" not in zones:
            zones["all"] = LEDZone("all", 0, led_count)
        
        return zones
    
    def start(self) -> bool:
        """
        LED kontrolcüsünü başlatır
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            if self.simulation_mode:
                logger.info("LED kontrolcü (simülasyon modu) başlatılıyor...")
                # İlk görselleştirmeyi oluştur
                self._save_simulation_image()
                return True
            
            # Gerçek donanım için
            if not LED_LIBRARY_AVAILABLE:
                logger.error("rpi_ws281x kütüphanesi yüklü değil.")
                return False
            
            logger.info(f"LED şeridi başlatılıyor: pin={self.led_pin}, sayı={self.led_count}")
            
            # LED nesnesi oluştur
            # Parametre açıklamaları:
            # - led_count: LED sayısı
            # - led_pin: GPIO pin numarası
            # - freq_hz: Sinyal frekansı (Hz), genellikle 800000 kullanılır
            # - dma: DMA kanalı, genellikle 10 kullanılır
            # - invert: Sinyal polaritesini tersine çevir (genellikle False)
            # - brightness: Parlaklık (0-255)
            # - channel: PWM kanalı (0 veya 1)
            freq_hz = 800000
            dma = 10
            channel = 0
            invert = False
            brightness = int(self.led_brightness * 255)  # 0.0-1.0 aralığını 0-255'e dönüştür
            
            self.strip = PixelStrip(
                self.led_count, self.led_pin, freq_hz, dma, invert, brightness, channel
            )
            self.strip.begin()
            
            # LEDleri sıfırla
            self.clear()
            
            logger.info("LED kontrolcü başlatıldı")
            return True
            
        except Exception as e:
            logger.error(f"LED kontrolcü başlatılırken hata: {e}")
            return False
    
    def stop(self) -> None:
        """
        Animasyonu durdurur ve LEDleri kapatır
        """
        # Çalışan animasyonu durdur
        self.stop_animation.set()
        if self.animation_thread:
            self.animation_thread.join(timeout=1.0)
            self.animation_thread = None
        
        # LEDleri kapat
        self.clear()
        
        logger.info("LED kontrolcü durduruldu")
    
    def clear(self) -> None:
        """
        Tüm LEDleri kapatır (siyah yapar)
        """
        if self.simulation_mode:
            # Simülasyon modunda
            self.sim_leds = [(0, 0, 0) for _ in range(self.led_count)]
            self._save_simulation_image()
            logger.debug("Tüm LEDler temizlendi (simülasyon)")
        else:
            # Gerçek donanımda
            if self.strip:
                for i in range(self.strip.numPixels()):
                    self.strip.setPixelColor(i, Color(0, 0, 0))
                self.strip.show()
                logger.debug("Tüm LEDler temizlendi")
    
    def set_color(self, r: int, g: int, b: int, zone_name: str = "all") -> None:
        """
        Belirli bir bölgenin rengini ayarlar
        
        Args:
            r (int): Kırmızı bileşeni (0-255)
            g (int): Yeşil bileşeni (0-255)
            b (int): Mavi bileşeni (0-255)
            zone_name (str, optional): Bölge adı. Varsayılan: "all"
        """
        # Renk değerlerini sınırla
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        
        # Bölgeyi kontrol et
        if zone_name not in self.zones:
            logger.warning(f"Geçersiz bölge adı: {zone_name}, 'all' kullanılıyor")
            zone_name = "all"
        
        zone = self.zones[zone_name]
        
        if self.simulation_mode:
            # Simülasyon modunda
            for i in range(zone.start_index, zone.start_index + zone.count):
                if 0 <= i < len(self.sim_leds):
                    self.sim_leds[i] = (r, g, b)
            self._save_simulation_image()
            logger.debug(f"LED rengi ayarlandı: ({r}, {g}, {b}) bölge: {zone_name} (simülasyon)")
        else:
            # Gerçek donanımda
            if self.strip:
                color = Color(r, g, b)
                for i in range(zone.start_index, zone.start_index + zone.count):
                    if 0 <= i < self.strip.numPixels():
                        self.strip.setPixelColor(i, color)
                self.strip.show()
                logger.debug(f"LED rengi ayarlandı: ({r}, {g}, {b}) bölge: {zone_name}")
    
    def set_brightness(self, brightness: float) -> None:
        """
        LED parlaklığını ayarlar
        
        Args:
            brightness (float): Parlaklık seviyesi (0.0 - 1.0)
        """
        # Parlaklık değerini sınırla
        brightness = max(0.0, min(1.0, brightness))
        self.led_brightness = brightness
        
        if self.simulation_mode:
            # Simülasyon modunda parlaklık değişimi için LEDleri güncelle
            new_leds = []
            for r, g, b in self.sim_leds:
                new_r = int(r * brightness)
                new_g = int(g * brightness)
                new_b = int(b * brightness)
                new_leds.append((new_r, new_g, new_b))
            
            self.sim_leds = new_leds
            self._save_simulation_image()
            logger.debug(f"LED parlaklığı ayarlandı: {brightness} (simülasyon)")
        else:
            if self.strip:
                # 0-255 aralığına dönüştür
                brightness_int = int(brightness * 255)
                self.strip.setBrightness(brightness_int)
                self.strip.show()
                logger.debug(f"LED parlaklığı ayarlandı: {brightness}")
    
    def _set_pixel_color(self, color: Tuple[int, int, int], index: int) -> None:
        """
        Bir LED'in rengini ayarlar
        
        Args:
            color (Tuple[int, int, int]): RGB renk değerleri
            index (int): LED indeksi
        """
        if self.simulation_mode:
            # Simülasyon modunda
            if 0 <= index < len(self.sim_leds):
                self.sim_leds[index] = color
        else:
            # Gerçek donanımda
            if self.strip and 0 <= index < self.strip.numPixels():
                self.strip.setPixelColor(index, Color(color[0], color[1], color[2]))
    
    def _set_zone_color(self, color: Tuple[int, int, int], start: int, count: int) -> None:
        """
        Bir bölgenin rengini ayarlar
        
        Args:
            color (Tuple[int, int, int]): RGB renk değerleri
            start (int): Başlangıç LED indeksi
            count (int): LED sayısı
        """
        for i in range(start, start + count):
            self._set_pixel_color(color, i)
            
        # Gerçek donanımda LEDleri güncelle
        if not self.simulation_mode and self.strip:
            self.strip.show()

    def _save_simulation_image(self, skip_frames: int = 1) -> None:
        """
        Simülasyon modunda LED durumunu bir görüntü dosyasına kaydeder
        
        Args:
            skip_frames (int, optional): Kaç karede bir görüntü kaydedileceği. Varsayılan: 1
        """
        if not self.simulation_mode or not PIL_AVAILABLE:
            return
            
        # Performans için frame skip kontrolü
        self.frame_counter += 1
        if self.frame_counter % skip_frames != 0:
            return
        
        try:
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
            timestamp = int(time.time())
            frame_num = (self.frame_counter // skip_frames) * 10
            filename = f"led_simulation_{timestamp}_{frame_num:04d}.png"
            filepath = os.path.join(self.sim_dir, filename)
            
            # Görüntüyü kaydet
            image.save(filepath)
            logger.debug(f"Simülasyon görüntüsü kaydedildi: {filename}")
            
            # Belirli aralıklarla eski dosyaları temizle
            self.cleanup_counter += 1
            if self.cleanup_counter >= self.cleanup_interval:
                self._cleanup_old_simulation_files()
                self.cleanup_counter = 0
                
        except Exception as e:
            logger.error(f"Simülasyon görüntüsü kaydedilirken hata: {e}")
            
    def _cleanup_old_simulation_files(self) -> None:
        """
        Eski LED simülasyon görüntülerini temizler
        """
        try:
            # LED için olan tüm görüntü dosyalarını listele
            pattern = "led_simulation_*.png"
            file_pattern = os.path.join(self.sim_dir, pattern)
            
            import glob
            files = glob.glob(file_pattern)
            
            # Dosyaları zaman damgasına göre sırala (en yeniler önce)
            files.sort(key=os.path.getmtime, reverse=True)
            
            # Maksimum dosya sayısından fazlasını sil
            if len(files) > self.max_simulation_files:
                for old_file in files[self.max_simulation_files:]:
                    try:
                        os.unlink(old_file)
                        logger.debug(f"Eski LED simülasyon dosyası silindi: {os.path.basename(old_file)}")
                    except Exception as e:
                        logger.debug(f"LED dosyası silinirken hata: {e}")
                
                logger.info(f"Simülasyon temizleme: LED için {len(files) - self.max_simulation_files} eski dosya silindi")
        except Exception as e:
            logger.error(f"LED simülasyon dosyaları temizlenirken hata: {e}")
    
    def reset_activity_timer(self) -> None:
        """
        Aktivite zamanlayıcısını sıfırlar
        """
        self.last_activity_time = time.time()
    
    def register_theme_callback(self, callback: Callable) -> None:
        """
        Tema değişikliği için callback kaydeder
        
        Args:
            callback (Callable): Çağrılacak fonksiyon
        """
        self.theme_callback = callback
        logger.debug("Tema değişikliği callback kaydedildi")
    
    def get_state(self) -> Dict:
        """
        LED kontrolcünün mevcut durumunu döndürür
        
        Returns:
            Dict: Mevcut durum bilgisi
        """
        return {
            "simulation_mode": self.simulation_mode,
            "led_count": self.led_count,
            "brightness": self.led_brightness,
            "animation_running": self.animation_running,
            "current_animation": self.current_animation.value if self.animation_running else None,
            "zones": {name: {"start": zone.start_index, "count": zone.count} for name, zone in self.zones.items()}
        }