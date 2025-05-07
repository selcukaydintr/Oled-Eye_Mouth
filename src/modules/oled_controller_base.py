#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: oled_controller_base.py
# Açıklama: OLED ekranları kontrol eden temel modül. Başlatma, yapılandırma ve ana sınıfı içerir.
# Bağımlılıklar: PIL, adafruit_ssd1306, threading, logging, time
# Bağlı Dosyalar: hardware_defines.py, oled_controller_display.py, oled_controller_animations.py

# Versiyon: 0.3.2
# Değişiklikler:
# - [0.3.2] Çevresel faktörlere tepki veren ifadeler için altyapı eklendi
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
from PIL import Image, ImageDraw, ImageFont

# Proje dizinini ve include dizinini Python yoluna ekle
PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(str(PROJECT_DIR))

from include import hardware_defines

# Logger yapılandırması
logger = logging.getLogger("OLEDController")

# Gerekli modülleri koşullu olarak içe aktarma
try:
    import adafruit_ssd1306
    import board
    import busio
    HARDWARE_AVAILABLE = True
except ImportError:
    logger.warning("Adafruit SSD1306 kütüphaneleri bulunamadı, simülasyon modu zorunlu")
    HARDWARE_AVAILABLE = False

# Çevresel sensör modüllerini koşullu içe aktarma
try:
    import adafruit_tsl2591  # Işık sensörü
    LIGHT_SENSOR_AVAILABLE = True
except ImportError:
    LIGHT_SENSOR_AVAILABLE = False
    logger.info("Işık sensörü kütüphanesi bulunamadı, ışık sensörü simüle edilecek")

try:
    import adafruit_ahtx0  # Sıcaklık ve nem sensörü
    TEMP_SENSOR_AVAILABLE = True
except ImportError:
    TEMP_SENSOR_AVAILABLE = False
    logger.info("Sıcaklık sensörü kütüphanesi bulunamadı, sıcaklık ve nem simüle edilecek")


class SimulatedDisplay:
    """
    SSD1306 ekranı simüle eden sınıf
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.buffer = Image.new("1", (width, height))
        self.draw = ImageDraw.Draw(self.buffer)
        self.contrast_value = 255
        self.powered_on = True
        
        # Simülasyon için ekran kaydını izleme amaçlı kayıt dosyası yolu
        self.frame_counter = 0
        simulation_dir = os.path.join(PROJECT_DIR, "simulation")
        os.makedirs(simulation_dir, exist_ok=True)
        self.sim_dir = simulation_dir
        
        # Görüntü sayısı sınırlaması için parametreler
        self.max_simulation_files = 100  # Saklanacak maksimum dosya sayısı
        self.cleanup_counter = 0  # Temizleme işlemi sayacı
        self.cleanup_interval = 50  # Kaç kayıt işleminde bir temizlik yapılacağı
    
    def image(self, img):
        """Görüntüyü tampona yükler"""
        self.buffer = img.copy()
        self.draw = ImageDraw.Draw(self.buffer)
    
    def fill(self, color):
        """Ekranı belirtilen renkle doldurur"""
        self.draw.rectangle((0, 0, self.width, self.height), fill=color)
    
    def show(self):
        """Tamponu ekrana çizer (simüle edilen)"""
        # Burada gerçek ekrana yazma işlemi yapılacaktı, ancak simüle edildiği için sadece log çıktısı alıyoruz
        # İsteğe bağlı olarak son tamponu bir dosyaya kaydediyoruz
        self.save_frame()
        logger.debug("Simüle edilen ekran güncellendi")
    
    def contrast(self, value):
        """Kontrast ayarı (0-255)"""
        self.contrast_value = value
        logger.debug(f"Simüle edilen ekran kontrastı ayarlandı: {value}")
    
    def poweroff(self):
        """Ekranı kapatır"""
        self.powered_on = False
        logger.debug("Simüle edilen ekran kapatıldı")
    
    def poweron(self):
        """Ekranı açar"""
        self.powered_on = True
        logger.debug("Simüle edilen ekran açıldı")
    
    def save_frame(self, display_name="unknown"):
        """Güncel ekran görüntüsünü kaydeder"""
        # Her 10 karede bir görüntüyü dosyaya kaydet (performans için)
        if self.frame_counter % 10 != 0:
            self.frame_counter += 1
            return
            
        try:
            # Dosya adı oluştur
            timestamp = int(time.time())
            filename = os.path.join(
                self.sim_dir, 
                f"display_{display_name}_{timestamp}_{self.frame_counter:04d}.png"
            )
            
            # PNG olarak kaydet, siyah-beyaz renkleri RGB'ye dönüştür
            rgb_img = self.buffer.convert("RGB")
            rgb_img.save(filename)
            self.frame_counter += 1
            
            # Belirli sayıda frame'de bir temizlik işlemi yap
            self.cleanup_counter += 1
            if self.cleanup_counter >= self.cleanup_interval:
                self._cleanup_old_simulation_files(display_name)
                self.cleanup_counter = 0
                
        except Exception as e:
            logger.debug(f"Simüle edilen ekran kaydedilemedi: {e}")
    
    def _cleanup_old_simulation_files(self, display_name):
        """
        Eski simülasyon görüntülerini temizler
        
        Args:
            display_name (str): Temizlenecek ekran adı
        """
        try:
            # Bu ekran için olan tüm görüntü dosyalarını listele
            pattern = f"display_{display_name}_*.png"
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
                        logger.debug(f"Eski simülasyon dosyası silindi: {os.path.basename(old_file)}")
                    except Exception as e:
                        logger.debug(f"Dosya silinirken hata: {e}")
                
                logger.info(f"Simülasyon temizleme: {display_name} için {len(files) - self.max_simulation_files} eski dosya silindi")
        except Exception as e:
            logger.error(f"Simülasyon dosyaları temizlenirken hata: {e}")


class OLEDController:
    """
    OLED ekranları kontrol eden temel sınıf
    
    Bu sınıf, SSD1306 OLED ekranları üzerinde göz ve ağız animasyonları oluşturur.
    Hem doğrudan I2C hem de TCA9548A I2C çoğaltıcı üzerinden çoklu ekran desteği sağlar.
    """
    
    # Mikro ifade süre ayarları
    MIN_MICRO_EXPRESSION_DURATION = 0.1  # saniye
    MAX_MICRO_EXPRESSION_DURATION = 1.0  # saniye
    
    # Enerji tasarrufu modu ayarları
    POWER_SAVE_DIM_DELAY = 120  # saniye
    POWER_SAVE_OFF_DELAY = 300  # saniye
    
    def __init__(self, config):
        """
        OLED kontrolcü sınıfını başlatır
        
        Args:
            config (dict): Yapılandırma ayarları
        """
        logger.info("OLED Kontrolcü başlatılıyor...")
        self.config = config
        
        # Ekran nesneleri
        self.displays = {
            "left_eye": None,
            "right_eye": None,
            "mouth": None
        }
        
        # Tampon görüntüleri (memory buffers)
        self.buffers = {
            "left_eye": None,
            "right_eye": None,
            "mouth": None
        }
        
        # Çizim nesneleri
        self.draw_objects = {
            "left_eye": None,
            "right_eye": None,
            "mouth": None
        }
        
        # Font yükleme
        self.font_path = str(PROJECT_DIR / "themes" / "fonts")
        self.fonts = {}
        self._load_fonts()
        
        # Göz kırpma değişkenleri
        self.blink_state = False
        self.next_blink_time = time.time() + self._get_random_blink_interval()
        
        # Göz takip değişkenleri (göz bebeklerinin nereye baktığı)
        self.eye_position = (0, 0)  # x, y (-1.0 - 1.0 arası)
        self.target_eye_position = (0, 0)
        self.eye_move_speed = 0.1
        self.random_eye_move = True  # Otomatik göz hareketi
        self.next_eye_move_time = time.time() + random.uniform(1.0, 3.0)
        
        # Mikro ifade değişkenleri
        self.micro_expression = None
        self.micro_expression_end_time = 0
        self.micro_expression_intensity = 0.0
        
        # Güç tasarrufu modu
        self.power_mode = "on"  # "on", "dim", "off"
        self.last_activity_time = time.time()
        
        # Animasyon döngüsü kontrol değişkenleri
        self.is_running = False
        self.animation_thread = None
        self.fps = config.get("animation", {}).get("fps", 30)
        self.frame_delay = 1.0 / self.fps
        
        # I2C ve ekran başlatma
        self.i2c = None
        self.multiplexer = None
        
        # Platform tespiti
        self.platform_type = hardware_defines.detect_platform()
        logger.info(f"Platform türü tespit edildi: {self.platform_type}")
        
        # Simülasyon modu kontrolü
        self.simulation_mode = (
            config.get("hardware", {}).get("simulation_mode", False) or 
            self.platform_type != "raspberry_pi" or 
            not HARDWARE_AVAILABLE or
            "Raspberry Pi 5" in hardware_defines.get_platform_info()
        )
        
        if self.simulation_mode:
            if self.platform_type == "raspberry_pi":
                logger.info("Simülasyon modu etkin (Raspberry Pi 5 henüz tam olarak desteklenmiyor veya yapılandırmada seçildi)")
            else:
                logger.info("Simülasyon modu etkin (Raspberry Pi platformu değil)")
            
            # Simülasyon dizinini oluştur
            self.sim_dir = os.path.join(PROJECT_DIR, "simulation")
            os.makedirs(self.sim_dir, exist_ok=True)
            logger.info(f"Simülasyon görüntüleri şurada saklanacak: {self.sim_dir}")
        
        # Çevresel sensörler
        self.light_sensor = None
        self.temp_sensor = None
        self._init_sensors()
    
    def _get_random_blink_interval(self) -> float:
        """
        Rastgele göz kırpma aralığı oluşturur
        
        Returns:
            float: Göz kırpma aralığı (saniye)
        """
        min_interval = self.config.get("animation", {}).get("blink_interval_min", 2.0)
        max_interval = self.config.get("animation", {}).get("blink_interval_max", 10.0)
        return random.uniform(min_interval, max_interval)
    
    def _load_fonts(self):
        """
        Kullanılacak fontları yükler
        """
        try:
            # Font boyutlarını belirle
            font_sizes = [8, 10, 12, 14, 16, 20, 24, 32]
            
            # PIL ile birlikte gelen fontları kullan
            for size in font_sizes:
                try:
                    # TrueType font kullanımı (eğer dosya mevcutsa)
                    # Önce projedeki font dosyalarını kontrol et
                    font_files = [
                        str(Path(self.font_path) / "roboto.ttf"),
                        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                        "/System/Library/Fonts/Helvetica.ttc",
                        "C:\\Windows\\Fonts\\arial.ttf"
                    ]
                    
                    font = None
                    for font_file in font_files:
                        if os.path.exists(font_file):
                            try:
                                font = ImageFont.truetype(font_file, size)
                                break
                            except Exception:
                                pass
                    
                    # TrueType font yoksa, PIL varsayılan fontunu kullan
                    if font is None:
                        font = ImageFont.load_default()
                    
                    self.fonts[size] = font
                    
                except Exception as e:
                    logger.error(f"Font yüklenirken hata oluştu, boyut {size}: {e}")
                    # Varsayılan font
                    self.fonts[size] = ImageFont.load_default()
            
        except Exception as e:
            logger.error(f"Fontlar yüklenirken hata: {e}")
            # En azından varsayılan fontu yükle
            self.fonts[8] = ImageFont.load_default()
    
    def start(self) -> bool:
        """
        OLED ekranları başlatır ve animasyon döngüsünü çalıştırır
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            # I2C başlat
            if not self._init_displays():
                return False
            
            # Animasyon döngüsünü başlat
            self.is_running = True
            self.animation_thread = threading.Thread(target=self._animation_loop)
            self.animation_thread.daemon = True
            self.animation_thread.start()
            
            logger.info("OLED Kontrolcü başlatıldı")
            return True
            
        except Exception as e:
            logger.error(f"OLED Kontrolcü başlatılırken hata: {e}")
            return False
    
    def stop(self) -> None:
        """
        Animasyon döngüsünü durdurur ve ekranları temizler
        """
        self.is_running = False
        
        if self.animation_thread:
            try:
                self.animation_thread.join(timeout=1.0)
            except Exception:
                pass
        
        # Ekranları temizle
        self.clear_displays()
        
        logger.info("OLED Kontrolcü durduruldu")
    
    def _init_displays(self) -> bool:
        """
        OLED ekranları başlatır
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            # Yapılandırmadan ekran ayarlarını al
            displays_config = self.config.get("hardware", {}).get("oled_displays", {})
            
            # Simülasyon modu kontrolü
            if self.simulation_mode:
                # Simülasyon modu - fiziksel donanım kullanmadan ekranları simüle et
                logger.info("Simülasyon modunda ekranlar başlatılıyor...")
                
                for display_name in self.displays.keys():
                    display_config = displays_config.get(display_name, {})
                    
                    # Simüle edilen ekranı oluştur
                    width = display_config.get("width", hardware_defines.DISPLAY_WIDTH)
                    height = display_config.get("height", hardware_defines.DISPLAY_HEIGHT)
                    
                    # Simüle edilmiş ekran nesnesi oluştur
                    display = SimulatedDisplay(width, height)
                    display.sim_dir = self.sim_dir  # Simülasyon dizinini ayarla
                    
                    # Ekranı temizle ve başlat
                    display.fill(0)
                    display.show()
                    
                    self.displays[display_name] = display
                    
                    # Tampon görüntü oluştur
                    buffer_image = Image.new("1", (width, height))
                    self.buffers[display_name] = buffer_image
                    self.draw_objects[display_name] = ImageDraw.Draw(buffer_image)
                    
                    logger.info(f"Simüle edilen OLED ekran başlatıldı: {display_name}")
                
                return True
            else:
                # Gerçek donanım modu
                # I2C başlat
                self.i2c = hardware_defines.get_platform_i2c()
                if self.i2c is None:
                    logger.error("I2C başlatılamadı")
                    return False
                
                # TCA9548A multiplexer kullanımı kontrolü
                use_multiplexer = self.config.get("hardware", {}).get("use_multiplexer", False)
                
                if use_multiplexer:
                    # TCA9548A I2C multiplexer başlat
                    self.multiplexer = hardware_defines.init_i2c_multiplexer(self.i2c)
                    if self.multiplexer is None:
                        logger.error("I2C multiplexer başlatılamadı")
                        return False
                    
                    # Multiplexer üzerindeki ekranları başlat
                    for display_name in self.displays.keys():
                        display_config = displays_config.get(display_name, {})
                        channel = display_config.get("channel", 0)
                        width = display_config.get("width", hardware_defines.DISPLAY_WIDTH)
                        height = display_config.get("height", hardware_defines.DISPLAY_HEIGHT)
                        
                        try:
                            # Multiplexer kanalını seç
                            self.multiplexer.select_channel(channel)
                            
                            # SSD1306 OLED ekranı başlat
                            display = adafruit_ssd1306.SSD1306_I2C(
                                width, height, self.i2c,
                                addr=int(display_config.get("i2c_address", "0x3C"), 16)
                            )
                            
                            # Ekranı temizle ve başlat
                            display.fill(0)
                            display.show()
                            
                            self.displays[display_name] = display
                            
                            # Tampon görüntü oluştur
                            buffer_image = Image.new("1", (width, height))
                            self.buffers[display_name] = buffer_image
                            self.draw_objects[display_name] = ImageDraw.Draw(buffer_image)
                            
                            logger.info(f"OLED ekran başlatıldı (multiplexer kanal {channel}): {display_name}")
                        except Exception as e:
                            logger.error(f"Multiplexer kanal {channel} üzerinde ekran başlatılırken hata: {e}")
                else:
                    # Doğrudan I2C bağlantısı ile ekranları başlat
                    default_addresses = {
                        "left_eye": hardware_defines.DEFAULT_LEFT_EYE_ADDR,
                        "right_eye": hardware_defines.DEFAULT_RIGHT_EYE_ADDR,
                        "mouth": hardware_defines.DEFAULT_MOUTH_ADDR
                    }
                    
                    for display_name, default_addr in default_addresses.items():
                        display_config = displays_config.get(display_name, {})
                        width = display_config.get("width", hardware_defines.DISPLAY_WIDTH)
                        height = display_config.get("height", hardware_defines.DISPLAY_HEIGHT)
                        addr = int(display_config.get("i2c_address", default_addr), 16)
                        
                        try:
                            # SSD1306 OLED ekranı başlat
                            display = adafruit_ssd1306.SSD1306_I2C(
                                width, height, self.i2c, addr=addr
                            )
                            
                            # Ekranı temizle ve başlat
                            display.fill(0)
                            display.show()
                            
                            self.displays[display_name] = display
                            
                            # Tampon görüntü oluştur
                            buffer_image = Image.new("1", (width, height))
                            self.buffers[display_name] = buffer_image
                            self.draw_objects[display_name] = ImageDraw.Draw(buffer_image)
                            
                            logger.info(f"OLED ekran başlatıldı (I2C adres 0x{addr:02X}): {display_name}")
                        except Exception as e:
                            logger.error(f"I2C adres 0x{addr:02X} üzerinde ekran başlatılırken hata: {e}")
                
                # Ekranların başarılı bir şekilde başlatılıp başlatılmadığını kontrol et
                if not any(self.displays.values()):
                    logger.error("Hiçbir OLED ekran başlatılamadı")
                    return False
                
                return True
            
        except Exception as e:
            logger.error(f"Ekranlar başlatılırken beklenmeyen hata: {e}")
            return False
    
    def _init_sensors(self) -> None:
        """
        Çevresel sensörleri başlatır
        """
        try:
            if LIGHT_SENSOR_AVAILABLE:
                self.light_sensor = adafruit_tsl2591.TSL2591(self.i2c)
                logger.info("Işık sensörü başlatıldı")
            else:
                logger.info("Işık sensörü simüle edilecek")
            
            if TEMP_SENSOR_AVAILABLE:
                self.temp_sensor = adafruit_ahtx0.AHTx0(self.i2c)
                logger.info("Sıcaklık ve nem sensörü başlatıldı")
            else:
                logger.info("Sıcaklık ve nem sensörü simüle edilecek")
        
        except Exception as e:
            logger.error(f"Çevresel sensörler başlatılırken hata: {e}")
    
    def update_display(self) -> None:
        """
        Tüm ekranları günceller (tamponları ekranlara gönderir)
        """
        for display_name, display in self.displays.items():
            if display is not None and self.buffers[display_name] is not None:
                try:
                    # PIL görüntüsünü ekran tamponuna dönüştür
                    display.image(self.buffers[display_name])
                    display.show()
                    
                    # Simülasyon modunda, ekranların son durumunu bir dosyaya kaydediyoruz
                    if self.simulation_mode and hasattr(display, 'save_frame'):
                        display.save_frame(display_name)
                        
                except Exception as e:
                    logger.error(f"Ekran güncellenirken hata: {display_name}, hata: {e}")
    
    def clear_displays(self) -> None:
        """
        Tüm ekranları temizler
        """
        for display_name, display in self.displays.items():
            if display is not None:
                try:
                    display.fill(0)
                    display.show()
                    
                    # Tampon görüntüleri de temizle
                    if self.buffers[display_name] is not None:
                        draw = self.draw_objects[display_name]
                        draw.rectangle((0, 0, self.buffers[display_name].width, 
                                       self.buffers[display_name].height), fill=0)
                except Exception as e:
                    logger.error(f"Ekran temizlenirken hata: {display_name}, hata: {e}")
    
    def _animation_loop(self) -> None:
        """
        Ana animasyon döngüsü
        """
        logger.info("Animasyon döngüsü başlatıldı")
        
        while self.is_running:
            loop_start = time.time()
            
            try:
                # Güç tasarrufu kontrolü
                self._check_power_saving_mode()
                
                # Göz pozisyonu güncelleme
                self._update_eye_position()
                
                # Göz kırpma kontrolü
                self._update_blink_state()
                
                # Mikro ifade kontrolü
                self._update_micro_expression()
                
                # Çevresel faktörleri kontrol et
                self._check_environmental_factors()
                
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
    
    def _update_eye_position(self) -> None:
        """
        Göz pozisyonunu günceller (göz bebeklerinin hareketi için)
        """
        # Rastgele göz hareketi kontrolü
        if self.random_eye_move:
            current_time = time.time()
            if current_time >= self.next_eye_move_time:
                # Yeni hedef pozisyon belirle (-0.7 ve 0.7 arasında)
                self.target_eye_position = (
                    random.uniform(-0.7, 0.7),
                    random.uniform(-0.7, 0.7)
                )
                # Sonraki hareket zamanını belirle
                self.next_eye_move_time = current_time + random.uniform(1.0, 3.0)
        
        # Mevcut pozisyondan hedef pozisyona doğru yumuşak geçiş
        self.eye_position = (
            self.eye_position[0] + (self.target_eye_position[0] - self.eye_position[0]) * self.eye_move_speed,
            self.eye_position[1] + (self.target_eye_position[1] - self.eye_position[1]) * self.eye_move_speed
        )
    
    def _update_blink_state(self) -> None:
        """
        Göz kırpma durumunu günceller
        """
        current_time = time.time()
        if current_time >= self.next_blink_time:
            self.blink_state = not self.blink_state
            
            if self.blink_state:
                # Göz açık
                self.next_blink_time = current_time + self._get_random_blink_interval()
            else:
                # Göz kapalı
                self.next_blink_time = current_time + 0.15  # Göz kapalı kalma süresi
    
    def _update_micro_expression(self) -> None:
        """
        Mikro ifadeyi günceller
        """
        if self.micro_expression and time.time() > self.micro_expression_end_time:
            logger.debug(f"Mikro ifade sona erdi: {self.micro_expression}")
            self.micro_expression = None
    
    def _check_power_saving_mode(self) -> None:
        """
        Güç tasarrufu modunu kontrol eder ve günceller
        """
        if not self.config.get("system", {}).get("power_save_enabled", True):
            return
            
        idle_time = time.time() - self.last_activity_time
        
        # Güç tasarrufu modunu güncelle
        # Sadece mod değiştiğinde log oluştur
        if self.power_mode == "on" and idle_time > self.POWER_SAVE_DIM_DELAY:
            # Önceki güç modunu bir değişkende tut
            previous_mode = self.power_mode
            # Güç modunu değiştir
            self.set_power_mode("dim")
            # Sadece mod değiştiyse log oluştur
            if previous_mode != "dim":
                logger.info(f"Güç tasarrufu: Dim modu aktif ({self.POWER_SAVE_DIM_DELAY}s)")
        elif self.power_mode == "dim" and idle_time > self.POWER_SAVE_OFF_DELAY:
            # Önceki güç modunu bir değişkende tut
            previous_mode = self.power_mode
            # Güç modunu değiştir
            self.set_power_mode("off")
            # Sadece mod değiştiyse log oluştur
            if previous_mode != "off":
                logger.info(f"Güç tasarrufu: Kapalı modu aktif ({self.POWER_SAVE_OFF_DELAY}s)")
    
    def _check_environmental_factors(self) -> None:
        """
        Çevresel faktörleri kontrol eder ve günceller
        """
        if self.light_sensor:
            try:
                light_level = self.light_sensor.lux
                logger.debug(f"Işık seviyesi: {light_level} lux")
                # Işık seviyesine göre parlaklık ayarı yap
                if (light_level < 10):
                    self.set_brightness(0.2)
                elif (light_level < 100):
                    self.set_brightness(0.5)
                else:
                    self.set_brightness(1.0)
            except Exception as e:
                logger.error(f"Işık sensörü okunurken hata: {e}")
        
        if self.temp_sensor:
            try:
                temperature = self.temp_sensor.temperature
                humidity = self.temp_sensor.relative_humidity
                logger.debug(f"Sıcaklık: {temperature} °C, Nem: {humidity} %")
                # Sıcaklık ve neme göre ifadeleri güncelle
                if temperature > 30:
                    self.micro_expression = "hot"
                    self.micro_expression_end_time = time.time() + 5
                elif temperature < 10:
                    self.micro_expression = "cold"
                    self.micro_expression_end_time = time.time() + 5
                elif humidity > 70:
                    self.micro_expression = "humid"
                    self.micro_expression_end_time = time.time() + 5
                elif humidity < 30:
                    self.micro_expression = "dry"
                    self.micro_expression_end_time = time.time() + 5
            except Exception as e:
                logger.error(f"Sıcaklık sensörü okunurken hata: {e}")
    
    def set_brightness(self, brightness: float) -> None:
        """
        OLED ekranların parlaklığını ayarlar
        
        Args:
            brightness (float): Parlaklık seviyesi (0.0 - 1.0)
        """
        # SSD1306 doğrudan parlaklık kontrolü sağlamıyor
        # Ancak contrast ayarı benzer etki yapabilir
        brightness = max(0.0, min(1.0, brightness))  # 0.0-1.0 aralığına sınırla
        
        for display_name, display in self.displays.items():
            if display is not None:
                try:
                    contrast_value = int(brightness * 255)
                    display.contrast(contrast_value)
                    logger.debug(f"Ekran parlaklığı ayarlandı: {display_name}, değer: {brightness:.2f}")
                except Exception as e:
                    logger.error(f"Ekran parlaklığı ayarlanırken hata: {display_name}, hata: {e}")
    
    def set_power_mode(self, mode: str) -> None:
        """
        OLED ekranların güç modunu ayarlar
        
        Args:
            mode (str): Güç modu ('on', 'off', 'dim')
        """
        for display_name, display in self.displays.items():
            if display is not None:
                try:
                    if mode == "off":
                        display.poweroff()
                    elif mode == "on":
                        display.poweron()
                        display.contrast(255)  # Tam parlaklık
                    elif mode == "dim":
                        display.poweron()
                        display.contrast(50)  # Düşük parlaklık
                except Exception as e:
                    logger.error(f"Ekran güç modu ayarlanırken hata: {display_name}, mod: {mode}, hata: {e}")
        
        self.power_mode = mode
    
    def reset_activity_timer(self) -> None:
        """
        Aktivite zamanlayıcısını sıfırlar (güç tasarrufu modu için)
        """
        self.last_activity_time = time.time()
        
        # Eğer ekranlar kapalı veya dim modundaysa, açık moda geç
        if self.power_mode != "on":
            self.set_power_mode("on")
            logger.debug("Aktivite algılandı, ekranlar açıldı")

# Diğer modülleri içe aktarma 
try:
    from .oled_controller_display import OLEDDisplayMixin
    from .oled_controller_animations import OLEDAnimationsMixin
except ImportError:
    logger.warning("OLED Display ve Animation modüllerinin içe aktarılması ertelendi.")

# Eğer bu dosya doğrudan çalıştırılıyorsa, test özelliklerini etkinleştir
if __name__ == "__main__":
    # Test kodu buraya gelecek, ancak modüller bölündüğü için main kodu oled_controller.py'ye taşınacak
    pass