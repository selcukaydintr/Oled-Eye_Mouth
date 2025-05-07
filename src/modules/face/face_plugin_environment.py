#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: face_plugin_environment.py
# Açıklama: FacePlugin çevresel faktör yönetimi ve tepki işlevleri
# Bağımlılıklar: logging, time, random
# Bağlı Dosyalar: face_plugin_base.py, face_plugin_system.py

# Versiyon: 0.4.4
# Değişiklikler:
# - [0.4.4] Çevresel faktör yönetim işlevleri modülerleştirildi
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-04
===========================================================
"""

import time
import random
import logging
from typing import Dict, List, Any, Optional, Tuple
import threading

# Çevresel sensör kütüphanelerini içe aktarmaya çalış
try:
    import board
    import adafruit_tsl2591  # Işık sensörü
    LIGHT_SENSOR_AVAILABLE = True
except ImportError:
    LIGHT_SENSOR_AVAILABLE = False

try:
    import adafruit_dht  # Sıcaklık ve nem sensörü
    TEMP_SENSOR_AVAILABLE = True
except ImportError:
    TEMP_SENSOR_AVAILABLE = False

try:
    import RPi.GPIO as GPIO  # GPIO erişimi
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False

# Loglama yapılandırması
logger = logging.getLogger("FacePluginEnvironment")

class FacePluginEnvironmentMixin:
    """
    FacePlugin çevresel faktör yönetimi mixin sınıfı
    
    Bu sınıf FacePlugin için çevresel faktör yönetimi işlevlerini içerir:
    - Işık, sıcaklık, nem gibi çevresel faktörleri algılama
    - Çevresel faktörlere göre tepki oluşturma
    - Dokunmatik sensörler gibi fiziksel etkileşimleri izleme
    - Periyodik ortam kontrolü ve raporlama
    """
    
    def __init_environment__(self):
        """
        Çevresel faktör sistemini başlatır - ana __init__ metodundan sonra çağrılmalıdır
        """
        # Çevresel sensörler için değişkenler
        self.light_sensor = None
        self.temp_sensor = None
        self.touch_sensor_pins = []
        self.motion_sensor_pin = None
        
        # Çevresel faktör değerleri
        self.environment_data = {
            "light_level": 0.0,  # lux
            "temperature": 20.0,  # derece C
            "humidity": 50.0,    # %
            "motion_detected": False,
            "touch_detected": False
        }
        
        # Tepki durumları
        self.environmental_reactions = {
            "light": None,    # "dark", "normal", "bright", None
            "temperature": None,  # "cold", "normal", "hot", None
            "humidity": None,     # "dry", "normal", "humid", None
            "motion": None,       # "detected", None
            "touch": None         # "detected", None
        }
        
        # Çevresel değişikliklerin son değerlerini saklamak için
        self.last_environment_values = {
            "light": 0.0,
            "temperature": 0.0,
            "humidity": 0.0,
            "motion": 0.0,
            "touch": 0.0
        }
        
        # Sensör yenileme aralıkları (saniye)
        self.light_read_interval = 2.0
        self.temp_read_interval = 5.0
        self.touch_read_interval = 0.1
        self.motion_read_interval = 0.5
        
        # Son okuma zamanları
        self.last_light_read = 0.0
        self.last_temp_read = 0.0
        self.last_touch_read = 0.0
        self.last_motion_read = 0.0
        
        # Çevresel faktörler için eşik değerler
        self.light_thresholds = {
            "dark": 10,    # lux altı
            "bright": 1000  # lux üstü
        }
        self.temp_thresholds = {
            "cold": 15,  # derece C altı
            "hot": 28    # derece C üstü
        }
        self.humidity_thresholds = {
            "dry": 30,   # % altı
            "humid": 70  # % üstü
        }
        
        # Periyodik okuma için iş parçacığı
        self.environment_thread = None
        self.environment_thread_running = False
        
        # Geri çağırma işlevleri
        self.environment_callbacks = []
        
        logger.debug("Çevresel faktör sistemi başlatıldı")
    
    def setup_environment_sensors(self) -> bool:
        """
        Çevresel sensörleri yapılandırır
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        success = True
        
        # Işık sensörü yapılandırması
        if LIGHT_SENSOR_AVAILABLE:
            try:
                i2c = board.I2C()
                self.light_sensor = adafruit_tsl2591.TSL2591(i2c)
                logger.info("Işık sensörü başarıyla yapılandırıldı")
            except Exception as e:
                logger.error(f"Işık sensörü yapılandırılamadı: {e}")
                self.light_sensor = None
                success = False
        else:
            logger.warning("Işık sensörü kütüphanesi mevcut değil, simülasyon modu kullanılacak")
        
        # Sıcaklık ve nem sensörü yapılandırması
        if TEMP_SENSOR_AVAILABLE:
            try:
                # DHT22 sensörü için pin numarası (Raspberry Pi GPIO pin numarası)
                dht_pin = 4
                self.temp_sensor = adafruit_dht.DHT22(dht_pin)
                logger.info("Sıcaklık ve nem sensörü başarıyla yapılandırıldı")
            except Exception as e:
                logger.error(f"Sıcaklık ve nem sensörü yapılandırılamadı: {e}")
                self.temp_sensor = None
                success = False
        else:
            logger.warning("Sıcaklık ve nem sensörü kütüphanesi mevcut değil, simülasyon modu kullanılacak")
        
        # Dokunmatik sensör pinleri yapılandırması
        if GPIO_AVAILABLE:
            try:
                # Dokunmatik sensörler için GPIO pin numaraları
                self.touch_sensor_pins = [17, 27]  # Örnek: GPIO17 ve GPIO27
                
                # GPIO'yu ayarla
                GPIO.setmode(GPIO.BCM)
                for pin in self.touch_sensor_pins:
                    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                
                # Hareket sensörü pin yapılandırması
                self.motion_sensor_pin = 22  # Örnek: GPIO22
                GPIO.setup(self.motion_sensor_pin, GPIO.IN)
                
                logger.info("Dokunmatik ve hareket sensörleri başarıyla yapılandırıldı")
            except Exception as e:
                logger.error(f"Dokunmatik veya hareket sensörleri yapılandırılamadı: {e}")
                self.touch_sensor_pins = []
                self.motion_sensor_pin = None
                success = False
        else:
            logger.warning("GPIO kütüphanesi mevcut değil, dokunmatik ve hareket sensörleri kullanılamayacak")
        
        return success
    
    def start_environment_monitoring(self) -> bool:
        """
        Çevresel faktör izleme döngüsünü başlatır
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        if self.environment_thread is not None and self.environment_thread.is_alive():
            logger.warning("Çevresel faktör izleme döngüsü zaten çalışıyor")
            return False
        
        self.environment_thread_running = True
        self.environment_thread = threading.Thread(
            target=self._environment_monitoring_loop,
            daemon=True,
            name="EnvironmentMonitoringThread"
        )
        self.environment_thread.start()
        
        logger.info("Çevresel faktör izleme döngüsü başlatıldı")
        return True
    
    def stop_environment_monitoring(self) -> None:
        """
        Çevresel faktör izleme döngüsünü durdurur
        """
        self.environment_thread_running = False
        if self.environment_thread and self.environment_thread.is_alive():
            self.environment_thread.join(timeout=2.0)
            logger.info("Çevresel faktör izleme döngüsü durduruldu")
    
    def _environment_monitoring_loop(self) -> None:
        """
        Çevresel faktör izleme döngüsünün ana işlevi
        """
        try:
            while self.environment_thread_running:
                try:
                    current_time = time.time()
                    
                    # Işık seviyesi kontrolü
                    if current_time - self.last_light_read >= self.light_read_interval:
                        self.read_light_level()
                        self.last_light_read = current_time
                    
                    # Sıcaklık ve nem kontrolü
                    if current_time - self.last_temp_read >= self.temp_read_interval:
                        self.read_temperature_humidity()
                        self.last_temp_read = current_time
                    
                    # Dokunmatik sensör kontrolü
                    if current_time - self.last_touch_read >= self.touch_read_interval:
                        self.read_touch_sensors()
                        self.last_touch_read = current_time
                    
                    # Hareket sensörü kontrolü
                    if current_time - self.last_motion_read >= self.motion_read_interval:
                        self.read_motion_sensor()
                        self.last_motion_read = current_time
                    
                    # Çevresel faktörlere göre tepki oluştur
                    self.process_environmental_reactions()
                    
                    # Kısa bir süre bekle
                    time.sleep(0.1)
                    
                except Exception as e:
                    logger.error(f"Çevresel faktör izleme döngüsünde hata: {e}")
                    time.sleep(1.0)  # Hata durumunda daha uzun bir bekleme
        
        except Exception as e:
            logger.error(f"Çevresel faktör izleme döngüsü beklenmeyen şekilde sonlandı: {e}")
        finally:
            logger.info("Çevresel faktör izleme döngüsü durdu")
    
    def read_light_level(self) -> float:
        """
        Işık seviyesini okur
        
        Returns:
            float: Lux cinsinden ışık seviyesi
        """
        try:
            if self.light_sensor:
                # Gerçek ışık sensöründen oku
                lux = self.light_sensor.lux
                self.environment_data["light_level"] = lux
                
                # Işık durumunu güncelle
                if lux < self.light_thresholds["dark"]:
                    new_light_state = "dark"
                elif lux > self.light_thresholds["bright"]:
                    new_light_state = "bright"
                else:
                    new_light_state = "normal"
                
                # Durum değişikliği varsa tepkiyi güncelle
                if new_light_state != self.environmental_reactions["light"]:
                    self.environmental_reactions["light"] = new_light_state
                    self.on_environment_change("light", new_light_state, lux)
            else:
                # Simülasyon modu: Rastgele ışık seviyesi üret
                hour = time.localtime().tm_hour
                
                # Gündüz ve gece simülasyonu
                if 7 <= hour < 19:  # Gündüz
                    base_lux = random.uniform(500, 2000)
                else:  # Gece
                    base_lux = random.uniform(0, 50)
                
                # Küçük rastgele değişimler
                lux = base_lux + random.uniform(-50, 50)
                lux = max(0, lux)  # Negatif değer olmamasını sağla
                
                self.environment_data["light_level"] = lux
            
            return self.environment_data["light_level"]
            
        except Exception as e:
            logger.error(f"Işık seviyesi okunurken hata: {e}")
            return self.environment_data["light_level"]
    
    def read_temperature_humidity(self) -> Tuple[float, float]:
        """
        Sıcaklık ve nem değerlerini okur
        
        Returns:
            Tuple[float, float]: Sıcaklık (derece C) ve nem (%) değerleri
        """
        try:
            if self.temp_sensor:
                # Gerçek sıcaklık sensöründen oku
                temperature = self.temp_sensor.temperature
                humidity = self.temp_sensor.humidity
                
                self.environment_data["temperature"] = temperature
                self.environment_data["humidity"] = humidity
                
                # Sıcaklık durumunu güncelle
                if temperature < self.temp_thresholds["cold"]:
                    new_temp_state = "cold"
                elif temperature > self.temp_thresholds["hot"]:
                    new_temp_state = "hot"
                else:
                    new_temp_state = "normal"
                
                # Nem durumunu güncelle
                if humidity < self.humidity_thresholds["dry"]:
                    new_humidity_state = "dry"
                elif humidity > self.humidity_thresholds["humid"]:
                    new_humidity_state = "humid"
                else:
                    new_humidity_state = "normal"
                
                # Sıcaklık değişikliği kontrolü
                if new_temp_state != self.environmental_reactions["temperature"]:
                    self.environmental_reactions["temperature"] = new_temp_state
                    self.on_environment_change("temperature", new_temp_state, temperature)
                
                # Nem değişikliği kontrolü
                if new_humidity_state != self.environmental_reactions["humidity"]:
                    self.environmental_reactions["humidity"] = new_humidity_state
                    self.on_environment_change("humidity", new_humidity_state, humidity)
            else:
                # Simülasyon modu: Gerçekçi sıcaklık ve nem değerleri üret
                month = time.localtime().tm_mon
                hour = time.localtime().tm_hour
                
                # Mevsimsel sıcaklık simülasyonu (Kuzey Yarımküre)
                if 3 <= month <= 5:  # İlkbahar
                    base_temp = random.uniform(15, 25)
                elif 6 <= month <= 8:  # Yaz
                    base_temp = random.uniform(22, 32)
                elif 9 <= month <= 11:  # Sonbahar
                    base_temp = random.uniform(10, 20)
                else:  # Kış
                    base_temp = random.uniform(0, 10)
                
                # Gün içi değişimler
                if 0 <= hour < 6:  # Gece yarısı - sabah
                    temp_offset = -3
                elif 6 <= hour < 10:  # Sabah
                    temp_offset = -1
                elif 10 <= hour < 16:  # Öğlen
                    temp_offset = 3
                elif 16 <= hour < 20:  # Akşam
                    temp_offset = 1
                else:  # Gece
                    temp_offset = -2
                
                # Küçük rastgele değişimler
                temperature = base_temp + temp_offset + random.uniform(-1, 1)
                
                # Nem simülasyonu (sıcaklıkla ters orantılı, basit bir yaklaşım)
                base_humidity = 80 - temperature
                humidity = base_humidity + random.uniform(-10, 10)
                humidity = max(10, min(95, humidity))  # 10% ile 95% arasında sınırla
                
                self.environment_data["temperature"] = temperature
                self.environment_data["humidity"] = humidity
            
            return temperature, humidity
            
        except Exception as e:
            logger.error(f"Sıcaklık ve nem değerleri okunurken hata: {e}")
            return self.environment_data["temperature"], self.environment_data["humidity"]
    
    def read_touch_sensors(self) -> bool:
        """
        Dokunmatik sensörleri okur
        
        Returns:
            bool: Dokunma algılandıysa True, değilse False
        """
        touch_detected = False
        
        try:
            if GPIO_AVAILABLE and self.touch_sensor_pins:
                # Gerçek GPIO pinlerinden oku
                for pin in self.touch_sensor_pins:
                    pin_state = GPIO.input(pin)
                    
                    # Dokunma algılandı (HIGH sinyali)
                    if pin_state == GPIO.HIGH:
                        touch_detected = True
                        break
            else:
                # Simülasyon modu: Düşük olasılıkla rastgele dokunma simülasyonu
                touch_detected = random.random() < 0.001  # %0.1 olasılık
            
            # Durum değişikliği varsa güncelle
            if touch_detected != self.environment_data["touch_detected"]:
                self.environment_data["touch_detected"] = touch_detected
                
                if touch_detected:
                    self.environmental_reactions["touch"] = "detected"
                    self.on_environment_change("touch", "detected", 1)
                else:
                    self.environmental_reactions["touch"] = None
            
            return touch_detected
            
        except Exception as e:
            logger.error(f"Dokunmatik sensörler okunurken hata: {e}")
            return self.environment_data["touch_detected"]
    
    def read_motion_sensor(self) -> bool:
        """
        Hareket sensörünü okur
        
        Returns:
            bool: Hareket algılandıysa True, değilse False
        """
        motion_detected = False
        
        try:
            if GPIO_AVAILABLE and self.motion_sensor_pin is not None:
                # Gerçek GPIO pininden oku
                pin_state = GPIO.input(self.motion_sensor_pin)
                
                # Hareket algılandı (HIGH sinyali)
                if pin_state == GPIO.HIGH:
                    motion_detected = True
            else:
                # Simülasyon modu: Düşük olasılıkla rastgele hareket simülasyonu
                motion_detected = random.random() < 0.005  # %0.5 olasılık
            
            # Durum değişikliği varsa güncelle
            if motion_detected != self.environment_data["motion_detected"]:
                self.environment_data["motion_detected"] = motion_detected
                
                if motion_detected:
                    self.environmental_reactions["motion"] = "detected"
                    self.on_environment_change("motion", "detected", 1)
                else:
                    self.environmental_reactions["motion"] = None
            
            return motion_detected
            
        except Exception as e:
            logger.error(f"Hareket sensörü okunurken hata: {e}")
            return self.environment_data["motion_detected"]
    
    def process_environmental_reactions(self) -> None:
        """
        Çevresel faktörlere göre tepkiler oluşturur
        Bu metod alt sınıflar tarafından override edilebilir
        """
        # Aktif tepkileri kontrol et
        active_reactions = []
        for factor, state in self.environmental_reactions.items():
            if state is not None:
                active_reactions.append((factor, state))
        
        if not active_reactions:
            return
        
        # Tepki öncelikleri (önemli olandan önemsiz olana doğru)
        priority_order = ["touch", "motion", "temperature", "light", "humidity"]
        
        # Öncelik sırasına göre tepkileri sırala
        sorted_reactions = sorted(
            active_reactions,
            key=lambda x: priority_order.index(x[0]) if x[0] in priority_order else 999
        )
        
        # En öncelikli tepkiyi seç
        if sorted_reactions:
            highest_priority = sorted_reactions[0]
            factor, state = highest_priority
            
            # Eğer OLED kontrolcü ve duygu motoru tanımlıysa uygun tepkileri göster
            if hasattr(self, 'oled_controller') and self.oled_controller is not None:
                if hasattr(self.oled_controller, 'show_environmental_reaction'):
                    # Örnek: show_environmental_reaction("light", "dark") gibi
                    self.oled_controller.show_environmental_reaction(factor, state)
            
            if hasattr(self, 'emotion_engine') and self.emotion_engine is not None:
                if hasattr(self.emotion_engine, 'react_to_environment'):
                    self.emotion_engine.react_to_environment(factor, state)
    
    def on_environment_change(self, factor: str, state: str, value: float) -> None:
        """
        Çevresel faktör değişikliklerini işler
        
        Args:
            factor (str): Değişen çevresel faktör ("light", "temperature", "humidity", "motion", "touch")
            state (str): Yeni durum ("dark", "bright", "cold", "hot", "dry", "humid", "detected", vb.)
            value (float): Ölçülen değer
        """
        # Önceki değerden farklı ise loglama yap
        if abs(self.last_environment_values.get(factor, 0) - value) > 0.001:  # Küçük değişimleri engelle
            logger.info(f"Çevresel değişiklik: {factor}={state} (değer: {value})")
            self.last_environment_values[factor] = value
        
        # Geri çağırma işlevlerini çağır
        for callback in self.environment_callbacks:
            try:
                callback(factor, state, value)
            except Exception as e:
                logger.error(f"Çevresel değişiklik geri çağırma hatası: {e}")
                
        # Özel durumlar için özel tepkiler
        self._handle_special_environmental_cases(factor, state, value)
    
    def _handle_special_environmental_cases(self, factor: str, state: str, value: float) -> None:
        """
        Özel çevresel durumlara tepki verir (özel kullanım durumları için)
        
        Args:
            factor (str): Çevresel faktör
            state (str): Durum
            value (float): Değer
        """
        # Işık sensörü için özel durumlar
        if factor == "light":
            # Karanlık ortamda göz parlaklığını azalt
            if state == "dark" and hasattr(self, 'oled_controller'):
                if hasattr(self.oled_controller, 'set_brightness'):
                    logger.debug("Karanlık ortam algılandı: Göz parlaklığı azaltılıyor")
                    self.oled_controller.set_brightness(0.3)  # Düşük parlaklık
            
            # Parlak ortamda göz parlaklığını artır
            elif state == "bright" and hasattr(self, 'oled_controller'):
                if hasattr(self.oled_controller, 'set_brightness'):
                    logger.debug("Parlak ortam algılandı: Göz parlaklığı artırılıyor")
                    self.oled_controller.set_brightness(1.0)  # Tam parlaklık
        
        # Dokunma için özel durumlar
        elif factor == "touch" and state == "detected":
            # Dokunma algılandığında bir animasyon oynat
            if hasattr(self, 'animation_engine'):
                if hasattr(self.animation_engine, 'play_animation'):
                    logger.debug("Dokunma algılandı: 'touch_reaction' animasyonu oynatılıyor")
                    self.animation_engine.play_animation("touch_reaction")
        
        # Hareket için özel durumlar
        elif factor == "motion" and state == "detected":
            # Hareket algılandığında robotu aktifleştir (güç tasarrufundan çık)
            if hasattr(self, 'oled_controller'):
                if hasattr(self.oled_controller, 'reset_activity_timer'):
                    logger.debug("Hareket algılandı: Aktivite zamanlayıcısı sıfırlanıyor")
                    self.oled_controller.reset_activity_timer()
    
    def register_environment_callback(self, callback) -> None:
        """
        Çevresel faktör değişiklikleri için geri çağırma işlevi kaydeder
        
        Args:
            callback: (factor: str, state: str, value: float) parametrelerini alan fonksiyon
        """
        if callback not in self.environment_callbacks:
            self.environment_callbacks.append(callback)
    
    def unregister_environment_callback(self, callback) -> None:
        """
        Çevresel faktör geri çağırma işlevini kaldırır
        
        Args:
            callback: Kaldırılacak geri çağırma işlevi
        """
        if callback in self.environment_callbacks:
            self.environment_callbacks.remove(callback)
    
    def get_environment_data(self) -> Dict:
        """
        Güncel çevresel faktör verilerini döndürür
        
        Returns:
            Dict: Çevresel faktör verileri
        """
        return self.environment_data.copy()
    
    def cleanup_environment_resources(self) -> None:
        """
        Çevresel faktör kaynaklarını temizler (program sonlandırılırken)
        """
        # İzleme döngüsünü durdur
        self.stop_environment_monitoring()
        
        # GPIO kaynaklarını temizle
        if GPIO_AVAILABLE:
            try:
                # Sadece GPIO pinleri yapılandırıldıysa temizle
                if hasattr(self, 'touch_sensor_pins') and self.touch_sensor_pins or \
                   hasattr(self, 'motion_sensor_pin') and self.motion_sensor_pin is not None:
                    GPIO.cleanup()
                    logger.info("GPIO kaynakları temizlendi")
            except Exception as e:
                logger.warning(f"GPIO temizleme sırasında hata: {e}")
        
        # Sensör kaynaklarını temizle
        self.light_sensor = None
        self.temp_sensor = None
        
        logger.info("Çevresel faktör kaynakları temizlendi")