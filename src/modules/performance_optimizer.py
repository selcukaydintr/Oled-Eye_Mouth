#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: performance_optimizer.py
# Açıklama: Performans izleme ve otomatik optimizasyon modülü
# Bağımlılıklar: psutil, logging, threading
# Bağlı Dosyalar: face_plugin.py, oled_controller.py, led_controller.py, sound_processor.py

# Versiyon: 0.5.0
# Değişiklikler:
# - [0.5.0] Ses işleme modülü (sound_processor) desteği eklendi
# - [0.4.0] İlk sürüm - Faz 4 Performans Optimizasyonu
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-04
===========================================================
"""

import logging
import threading
import time
import os
from typing import Dict, Optional, Tuple, List, Any
import psutil

# Loglama yapılandırması
logger = logging.getLogger("PerformanceOptimizer")

class PerformanceOptimizer:
    """
    FACE1 için performans optimizasyon modülü
    
    Bu modül:
    1. Sistem kaynaklarını (CPU, RAM, sıcaklık) izler
    2. Yük durumuna göre FPS ve parlaklık ayarlarını otomatik olarak değiştirir
    3. Pil durumunu (varsa) izler ve düşük pil durumunda enerji tasarruf önlemleri alır
    """
    
    def __init__(self, config: Dict):
        """
        PerformanceOptimizer sınıfını başlatır
        
        Args:
            config (Dict): Yapılandırma ayarları
        """
        logger.info("Performans optimize edici başlatılıyor...")
        
        self.config = config
        self.performance_config = config.get("performance", {})
        
        # Durum değişkenleri
        self.is_running = False
        self.shutdown_requested = False
        
        # Controller referansları
        self.oled_controller = None
        self.led_controller = None
        
        # İzleme değişkenleri
        self.cpu_usage = 0
        self.memory_usage = 0
        self.temperature = 0
        self.battery_level = 100
        self.has_battery = self._check_battery_available()
        
        # İzleme ayarları
        self.check_interval = self.performance_config.get("check_interval", 5.0)
        self.cpu_threshold = self.performance_config.get("cpu_threshold", 70)
        self.memory_threshold = self.performance_config.get("memory_threshold", 80)
        self.temp_threshold = self.performance_config.get("temperature_threshold", 70)
        self.battery_threshold = self.performance_config.get("battery_threshold", 20)
        
        # Performans kademeleri [cpu_yuk, fps, parlaklık]
        self.performance_tiers = self.performance_config.get("performance_tiers", [
            [80, 15, 0.5],  # Yüksek yük: Düşük FPS, orta parlaklık
            [60, 20, 0.7],  # Orta yük: Orta FPS, yüksek parlaklık
            [30, 30, 0.9],  # Düşük yük: Yüksek FPS, tam parlaklığa yakın
            [0, 60, 1.0]    # Boşta: Maksimum FPS, tam parlaklık
        ])
        
        # Optimizasyon ayarları
        self.auto_adjust_fps = self.performance_config.get("auto_adjust_fps", True)
        self.auto_adjust_brightness = self.performance_config.get("auto_adjust_brightness", True)
        self.battery_saver = self.performance_config.get("battery_saver_enabled", False)
        
        # İzleme iş parçacığı
        self.monitor_thread = None
        
        logger.info("Performans optimize edici başlatıldı.")

    def set_controllers(self, oled_controller=None, led_controller=None):
        """
        Controller referanslarını ayarlar
        
        Args:
            oled_controller: OLED kontrolcü referansı
            led_controller: LED kontrolcü referansı
        """
        self.oled_controller = oled_controller
        self.led_controller = led_controller
        logger.debug("Controller referansları ayarlandı")

    def start(self) -> bool:
        """
        Performans optimize ediciyi başlatır
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            if self.is_running:
                logger.warning("Performans optimize edici zaten çalışıyor.")
                return True
                
            enabled = self.performance_config.get("enabled", True)
            if not enabled:
                logger.info("Performans optimize edici devre dışı bırakıldı (yapılandırma).")
                return False
            
            # Gerekli controller'lar mevcut mu kontrol et
            if not self.oled_controller:
                logger.warning("OLED controller referansı ayarlanmamış.")
                return False
                
            if not self.led_controller:
                logger.warning("LED controller referansı ayarlanmamış.")
                return False
                
            # İzleme iş parçacığını başlat
            self.is_running = True
            self.shutdown_requested = False
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()
            
            logger.info("Performans izleme başlatıldı.")
            return True
            
        except Exception as e:
            logger.error(f"Performans optimize edici başlatılırken hata: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return False

    def stop(self) -> bool:
        """
        Performans optimize ediciyi durdurur
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            if not self.is_running:
                return True
                
            logger.info("Performans optimize edici durduruluyor...")
            self.shutdown_requested = True
            
            # İş parçacığının sonlanmasını bekle
            if self.monitor_thread and self.monitor_thread.is_alive():
                self.monitor_thread.join(timeout=2.0)
                
            self.is_running = False
            logger.info("Performans optimize edici durduruldu.")
            return True
            
        except Exception as e:
            logger.error(f"Performans optimize edici durdurulurken hata: {e}")
            return False

    def update_config(self, new_config: Dict) -> bool:
        """
        Yapılandırmayı günceller
        
        Args:
            new_config (Dict): Yeni yapılandırma ayarları
            
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            if "performance" in new_config:
                logger.info("Performans optimize edici yapılandırması güncelleniyor...")
                
                # Eski yapılandırmayı yedekle
                old_config = self.performance_config.copy()
                
                # Yeni yapılandırmayı ayarla
                self.performance_config = new_config.get("performance", {})
                
                # Yapılandırma değerlerini güncelle
                self.check_interval = self.performance_config.get("check_interval", 5.0)
                self.cpu_threshold = self.performance_config.get("cpu_threshold", 70)
                self.memory_threshold = self.performance_config.get("memory_threshold", 80)
                self.temp_threshold = self.performance_config.get("temperature_threshold", 70)
                self.battery_threshold = self.performance_config.get("battery_threshold", 20)
                self.auto_adjust_fps = self.performance_config.get("auto_adjust_fps", True)
                self.auto_adjust_brightness = self.performance_config.get("auto_adjust_brightness", True)
                self.battery_saver = self.performance_config.get("battery_saver_enabled", False)
                
                # Performans kademeleri
                if "performance_tiers" in self.performance_config:
                    self.performance_tiers = self.performance_config["performance_tiers"]
                
                # Optimize edici etkinleştirilmiş/devre dışı bırakılmış mı?
                enabled = self.performance_config.get("enabled", True)
                
                # Duruma göre başlat/durdur
                if enabled and not self.is_running:
                    self.start()
                elif not enabled and self.is_running:
                    self.stop()
                
                logger.info("Performans optimize edici yapılandırması güncellendi.")
                
            return True
            
        except Exception as e:
            logger.error(f"Performans yapılandırması güncellenirken hata: {e}")
            return False

    def _monitor_loop(self) -> None:
        """
        Sistem kaynaklarını izleme döngüsü
        """
        logger.info("Sistem kaynakları izleme döngüsü başlatıldı.")
        
        while not self.shutdown_requested and self.is_running:
            try:
                # Sistem kaynaklarını izle
                self._update_system_metrics()
                
                # Performans ayarlamalarını yap
                self._adjust_performance()
                
                # Pil seviyesini kontrol et
                if self.has_battery and self.battery_saver:
                    self._check_battery_status()
                
                # Bir sonraki kontrole kadar bekle
                time.sleep(self.check_interval)
                
            except Exception as e:
                logger.error(f"İzleme döngüsünde hata: {e}")
                time.sleep(self.check_interval)
                
        logger.info("Sistem kaynakları izleme döngüsü sonlandırıldı.")

    def _update_system_metrics(self) -> None:
        """
        Sistem metriklerini günceller (CPU, bellek, sıcaklık, pil)
        """
        try:
            # CPU kullanımı
            self.cpu_usage = psutil.cpu_percent(interval=0.5)
            
            # Bellek kullanımı
            mem = psutil.virtual_memory()
            self.memory_usage = mem.percent
            
            # Sıcaklık (Raspberry Pi için)
            self.temperature = self._get_cpu_temperature()
            
            # Pil seviyesi (eğer varsa)
            if self.has_battery:
                self.battery_level = self._get_battery_level()
            
            logger.debug(f"Sistem metrikleri - CPU: {self.cpu_usage}%, "
                         f"Bellek: {self.memory_usage}%, "
                         f"Sıcaklık: {self.temperature}°C, "
                         f"Pil: {self.battery_level}%")
                         
        except Exception as e:
            logger.error(f"Sistem metrikleri güncellenirken hata: {e}")

    def _adjust_performance(self) -> None:
        """
        Performansı sistem yüküne göre ayarlar
        """
        try:
            # Kaynak kullanımı kritik mi?
            is_cpu_high = self.cpu_usage > self.cpu_threshold
            is_memory_high = self.memory_usage > self.memory_threshold
            is_temp_high = self.temperature > self.temp_threshold
            
            # Hangi performans kademesini kullanacağız?
            tier = self._get_performance_tier()
            fps = tier[1]
            brightness = tier[2]
            
            # Kritik durumda çok daha agresif önlemler al
            if is_cpu_high and is_memory_high and is_temp_high:
                logger.warning("Sistem kaynakları kritik seviyede! Performans kısıtlanıyor.")
                fps = 10  # Minimum FPS
                brightness = 0.3  # Düşük parlaklık
            
            # FPS'i ayarla
            if self.auto_adjust_fps and self.oled_controller:
                current_fps = self.oled_controller.get_fps()
                if abs(current_fps - fps) > 2:  # Küçük değişimleri yoksay
                    logger.debug(f"FPS ayarlanıyor: {current_fps} -> {fps}")
                    self.oled_controller.set_fps(fps)
            
            # Parlaklığı ayarla
            if self.auto_adjust_brightness and self.led_controller:
                current_brightness = self.led_controller.get_brightness()
                if abs(current_brightness - brightness) > 0.05:  # Küçük değişimleri yoksay
                    logger.debug(f"Parlaklık ayarlanıyor: {current_brightness} -> {brightness}")
                    self.led_controller.set_brightness(brightness)
            
        except Exception as e:
            logger.error(f"Performans ayarlanırken hata: {e}")

    def _get_performance_tier(self) -> List:
        """
        CPU kullanım oranına göre uygun performans kademesini döndürür
        
        Returns:
            List: [cpu_threshold, fps, brightness]
        """
        # Performans kademelerini CPU kullanım oranına göre gez
        for tier in sorted(self.performance_tiers):
            if self.cpu_usage >= tier[0]:
                return tier
                
        # Son kademeyi kullan
        return self.performance_tiers[-1]

    def _check_battery_status(self) -> None:
        """
        Pil seviyesini kontrol eder ve düşük pil durumunda önlem alır
        """
        if not self.has_battery:
            return
            
        # Pil seviyesi düşük mü?
        if self.battery_level < self.battery_threshold:
            logger.warning(f"Düşük pil seviyesi: {self.battery_level}%. Pil tasarruf modu etkinleştiriliyor.")
            
            # Düşük pil modu için FPS ve parlaklık ayarları
            if self.auto_adjust_fps and self.oled_controller:
                self.oled_controller.set_fps(15)  # Düşük FPS
                
            if self.auto_adjust_brightness and self.led_controller:
                self.led_controller.set_brightness(0.3)  # Düşük parlaklık
                
            # Ekstra pil tasarrufu için güç tasarrufu modunu etkinleştir
            if hasattr(self.oled_controller, "enable_power_save"):
                self.oled_controller.enable_power_save(timeout=60)  # 60 saniye hareketsizlik sonrası

    def _get_cpu_temperature(self) -> float:
        """
        CPU sıcaklığını döndürür
        
        Returns:
            float: CPU sıcaklığı (C)
        """
        try:
            # Raspberry Pi için sıcaklık okuma
            if os.path.exists('/sys/class/thermal/thermal_zone0/temp'):
                with open('/sys/class/thermal/thermal_zone0/temp') as f:
                    temp = float(f.read()) / 1000.0
                return temp
            
            # Alternatif sıcaklık okuma
            if hasattr(psutil, "sensors_temperatures"):
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        for entry in entries:
                            return entry.current
                            
            # Sıcaklık ölçümü başarısız oldu
            return 0.0
            
        except Exception as e:
            logger.error(f"CPU sıcaklığı okunurken hata: {e}")
            return 0.0

    def _check_battery_available(self) -> bool:
        """
        Sistemde pil olup olmadığını kontrol eder
        
        Returns:
            bool: Pil varsa True, yoksa False
        """
        try:
            if hasattr(psutil, "sensors_battery"):
                battery = psutil.sensors_battery()
                return battery is not None
            return False
        except Exception:
            return False
            
    def _get_battery_level(self) -> int:
        """
        Pil seviyesini döndürür
        
        Returns:
            int: Pil seviyesi (%)
        """
        try:
            if hasattr(psutil, "sensors_battery"):
                battery = psutil.sensors_battery()
                if battery:
                    return int(battery.percent)
            return 100
        except Exception:
            return 100

    def get_status(self) -> Dict:
        """
        Mevcut performans durumu bilgilerini döndürür
        
        Returns:
            Dict: Performans durumu bilgileri
        """
        return {
            "enabled": self.is_running,
            "cpu_usage": self.cpu_usage,
            "memory_usage": self.memory_usage,
            "temperature": self.temperature,
            "battery_level": self.battery_level if self.has_battery else None,
            "battery_saver_active": self.has_battery and self.battery_level < self.battery_threshold and self.battery_saver,
            "current_fps": self.oled_controller.get_fps() if self.oled_controller else None,
            "current_brightness": self.led_controller.get_brightness() if self.led_controller else None,
            "auto_adjusting": {
                "fps": self.auto_adjust_fps,
                "brightness": self.auto_adjust_brightness
            }
        }

if __name__ == "__main__":
    # Doğrudan çalıştırıldığında performans optimizasyonunu test et
    logging.basicConfig(level=logging.DEBUG)
    
    config = {
        "performance": {
            "enabled": True,
            "check_interval": 1.0,
            "cpu_threshold": 70,
            "memory_threshold": 80,
            "temperature_threshold": 70,
            "auto_adjust_fps": True,
            "auto_adjust_brightness": True
        }
    }
    
    optimizer = PerformanceOptimizer(config)
    
    # Test için mocked controllers
    class MockController:
        def get_fps(self):
            return 30
            
        def set_fps(self, fps):
            print(f"FPS ayarlandı: {fps}")
            
        def get_brightness(self):
            return 0.8
            
        def set_brightness(self, brightness):
            print(f"Parlaklık ayarlandı: {brightness}")
            
    optimizer.set_controllers(
        oled_controller=MockController(),
        led_controller=MockController()
    )
    
    optimizer.start()
    
    try:
        for i in range(60):
            time.sleep(1)
            status = optimizer.get_status()
            print(f"CPU: {status['cpu_usage']}%, Bellek: {status['memory_usage']}%, "
                  f"Sıcaklık: {status['temperature']}°C")
    except KeyboardInterrupt:
        pass
    finally:
        optimizer.stop()
        print("Performans optimizasyon testi tamamlandı.")