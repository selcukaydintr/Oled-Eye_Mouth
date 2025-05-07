#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: face_plugin_base.py
# Açıklama: FacePlugin sınıfının temel işlevleri, yapılandırma yükleme ve oluşturma
# Bağımlılıklar: logging, os, json
# Bağlı Dosyalar: face_plugin.py, face_plugin_callbacks.py, face_plugin_api.py, face_plugin_system.py

# Versiyon: 0.5.0
# Değişiklikler:
# - [0.5.0] Ses işleme modülü (sound_processor) desteği eklendi
# - [0.4.1] Genişletilmiş durum yönetimi için FacePluginLifecycle sınıfıyla entegre edildi
# - [0.4.0] FacePlugin modülerleştirildi, temel sınıf oluşturuldu
# - [0.3.3] Animasyon motoru entegrasyonu ve JSON formatı desteği eklendi
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-04
===========================================================
"""

import os
import json
import logging
import threading
import time
from typing import Dict, List, Optional
from pathlib import Path

from .face_plugin_lifecycle import FacePluginLifecycle, PluginState

# Proje dizinini al
PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))

# Loglama yapılandırması
logger = logging.getLogger("FacePluginBase")

class FacePluginBase(FacePluginLifecycle):
    """
    FacePlugin temel sınıfı
    
    Bu sınıf FacePlugin sınıfı için temel işlevleri içerir:
    - Yapılandırma yükleme ve oluşturma
    - Loglama yapılandırması
    - Temel durum değişkenleri
    """
    
    def __init__(self, config_path: str = None):
        """
        FacePluginBase sınıfını başlatır
        
        Args:
            config_path (str, optional): Yapılandırma dosyasının yolu. 
                                      None ise varsayılan yol kullanılır.
        """
        # Yaşam döngüsü yöneticisini başlat
        super().__init__()
        
        logger.info("FACE1 Yüz Eklentisi Temel Sınıfı başlatılıyor...")
        
        # Yapılandırma dosyasını yükle
        self.config_path = config_path or os.path.join(PROJECT_DIR, "config", "config.json")
        self.config = self._load_config()
        
        # Durum değişkenleri
        self.is_running = False
        self.is_initialized = False
        self.is_api_running = False
        self.shutdown_requested = False
        
        # Modül nesneleri
        self.oled_controller = None
        self.led_controller = None
        self.emotion_engine = None
        self.theme_manager = None
        self.animation_engine = None
        self.performance_optimizer = None
        self.sound_processor = None  # Ses işleme modülü
        
        # API nesnesi
        self.api = None
        self.api_server = None
        self.api_thread = None
        
        # Watchdog zamanlayıcısı
        self.watchdog_timer = None
        self.last_heartbeat = time.time()
        
        # Senkronizasyon nesneleri
        self.lock = threading.RLock()
        
        # Durum değişikliği callback'ini kaydet
        self.register_state_change_callback(self._on_state_changed)
        
        logger.info("FACE1 Yüz Eklentisi Temel Sınıfı başlatıldı.")
        
    def _on_state_changed(self, old_state: PluginState, new_state: PluginState) -> None:
        """
        Durum değişikliği olaylarını işler
        
        Args:
            old_state (PluginState): Önceki durum
            new_state (PluginState): Yeni durum
        """
        logger.info(f"Plugin durumu değişti: {old_state.value} -> {new_state.value}")
        
        # Durum değişikliğine göre bazı değişkenleri güncelle
        if new_state == PluginState.RUNNING:
            self.is_running = True
        elif new_state == PluginState.INITIALIZED:
            self.is_initialized = True
        elif new_state in [PluginState.STOPPED, PluginState.ERROR, PluginState.SHUTDOWN]:
            self.is_running = False
            
        # Durum değişikliğini istemcilere bildir (API üzerinden)
        if hasattr(self, 'notify_state_change') and callable(getattr(self, 'notify_state_change')):
            try:
                self.notify_state_change(old_state, new_state)
            except Exception as e:
                logger.error(f"Durum değişikliği bildirimi gönderilemedi: {e}")
    
    def _load_config(self) -> Dict:
        """
        Yapılandırma dosyasını yükler
        
        Returns:
            Dict: Yapılandırma ayarları
        """
        try:
            if not os.path.exists(self.config_path):
                logger.warning(f"Yapılandırma dosyası bulunamadı: {self.config_path}")
                return self._create_default_config()
            
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            logger.info(f"Yapılandırma dosyası yüklendi: {self.config_path}")
            return config
            
        except Exception as e:
            logger.error(f"Yapılandırma dosyası yüklenirken hata: {e}")
            return self._create_default_config()
    
    def _create_default_config(self) -> Dict:
        """
        Varsayılan yapılandırma ayarlarını oluşturur
        
        Returns:
            Dict: Varsayılan yapılandırma ayarları
        """
        # Temel varsayılan ayarlar
        default_config = {
            "hardware": {
                "platform": "auto",
                "oled_displays": {
                    "left_eye": {
                        "i2c_address": "0x3C",
                        "width": 128,
                        "height": 64,
                        "channel": 0
                    },
                    "right_eye": {
                        "i2c_address": "0x3D",
                        "width": 128,
                        "height": 64,
                        "channel": 1
                    },
                    "mouth": {
                        "i2c_address": "0x3E",
                        "width": 128,
                        "height": 64,
                        "channel": 2
                    }
                },
                "use_multiplexer": True,
                "multiplexer_address": "0x70",
                "led_strip": {
                    "pin": 18,
                    "count": 30,
                    "brightness": 0.5
                },
                "i2c_bus": 1,
                "debug_mode": False
            },
            "emotions": {
                "default_emotion": "neutral",
                "transition_speed": 0.5
            },
            "animation": {
                "fps": 30,
                "blink_interval_min": 2.0,
                "blink_interval_max": 8.0,
                "idle_animations": True
            },
            "logging": {
                "level": "INFO",
                "file": "logs/face_plugin.log",
                "console_output": True
            },
            "system": {
                "startup_delay": 1.0,
                "watchdog_enabled": True,
                "watchdog_timeout": 10.0,
                "shutdown_grace_period": 2.0,
                "auto_restart": True
            },
            "performance": {
                "enabled": True,
                "check_interval": 5.0,
                "cpu_threshold": 70,
                "memory_threshold": 80,
                "temperature_threshold": 70,
                "auto_adjust_fps": True,
                "auto_adjust_brightness": True,
                "battery_saver_enabled": False,
                "battery_threshold": 20,
                "performance_tiers": [
                    [80, 15, 0.5],  # Yüksek yük: Düşük FPS, orta parlaklık
                    [60, 20, 0.7],  # Orta yük: Orta FPS, yüksek parlaklık
                    [30, 30, 0.9],  # Düşük yük: Yüksek FPS, tam parlaklığa yakın
                    [0, 60, 1.0]    # Boşta: Maksimum FPS, tam parlaklık
                ]
            },
            "api": {
                "enabled": True,
                "port": 8000,
                "host": "0.0.0.0",
                "debug": False
            },
            "sound": {
                "enabled": True,
                "sample_rate": 16000,
                "chunk_size": 1024,
                "channels": 1,
                "format": 8,  # PyAudio.paInt16
                "device_index": None,
                "volume_threshold": 0.1,
                "emotion_sensitivity": 0.7,
                "speaking_animation_enabled": True,
                "sound_reactive_expression": True
            }
        }
        
        # Yapılandırma dosyasını kaydet
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            logger.info(f"Varsayılan yapılandırma dosyası oluşturuldu: {self.config_path}")
        except Exception as e:
            logger.error(f"Varsayılan yapılandırma dosyası oluşturulurken hata: {e}")
        
        return default_config
    
    def _setup_logging(self) -> None:
        """
        Loglama yapılandırmasını ayarlar
        """
        try:
            logging_config = self.config.get("logging", {})
            log_level_str = logging_config.get("level", "INFO")
            log_levels = {
                "DEBUG": logging.DEBUG,
                "INFO": logging.INFO,
                "WARNING": logging.WARNING,
                "ERROR": logging.ERROR,
                "CRITICAL": logging.CRITICAL
            }
            log_level = log_levels.get(log_level_str, logging.INFO)
            
            # Log dosya yolu
            log_file = logging_config.get("file", "logs/face_plugin.log")
            log_file_path = os.path.join(PROJECT_DIR, log_file)
            os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
            
            # Dönen dosya loglayıcısı
            max_size = logging_config.get("max_size", 5 * 1024 * 1024)  # 5MB
            backup_count = logging_config.get("backup_count", 3)
            
            # Loglama formatı
            log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            formatter = logging.Formatter(log_format)
            
            # Kök logger yapılandırması
            root_logger = logging.getLogger()
            root_logger.setLevel(log_level)
            
            # Mevcut işleyicileri temizle
            for handler in root_logger.handlers[:]:
                root_logger.removeHandler(handler)
            
            # Dosya işleyicisi
            from logging.handlers import RotatingFileHandler
            file_handler = RotatingFileHandler(
                log_file_path, 
                maxBytes=max_size, 
                backupCount=backup_count
            )
            file_handler.setFormatter(formatter)
            root_logger.addHandler(file_handler)
            
            # Konsol işleyicisi (isteğe bağlı)
            if logging_config.get("console_output", True):
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                root_logger.addHandler(console_handler)
            
            logger.debug("Loglama yapılandırması ayarlandı.")
            
        except Exception as e:
            print(f"Loglama yapılandırması ayarlanırken hata: {e}")
            # Hata durumunda basit yapılandırma
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
    
    def update_config(self, new_config: Dict) -> bool:
        """
        Yeni yapılandırmayı uygular ve yapılandırma dosyasına kaydeder
        
        Args:
            new_config (Dict): Yeni yapılandırma ayarları
            
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            logger.info("Yapılandırma güncelleniyor...")
            
            # Mevcut yapılandırmayı yedekle
            old_config = self.config.copy()
            
            # Yeni yapılandırmayı ayarla
            self.config = new_config
            
            # Yapılandırma dosyasına kaydet
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            
            logger.info(f"Yapılandırma dosyası güncellendi: {self.config_path}")
            
            # Değişiklikleri modüllere bildir
            try:
                # OLED kontrolcü ayarlarını güncelle
                if self.oled_controller and "oled" in new_config:
                    logger.debug("OLED kontrolcü ayarları güncelleniyor...")
                    self.oled_controller.update_config(new_config)
                
                # LED kontrolcü ayarlarını güncelle
                if self.led_controller and "led" in new_config:
                    logger.debug("LED kontrolcü ayarları güncelleniyor...")
                    self.led_controller.update_config(new_config)
                
                # Duygu motoru ayarlarını güncelle
                if self.emotion_engine and "emotion_engine" in new_config:
                    logger.debug("Duygu motoru ayarları güncelleniyor...")
                    self.emotion_engine.update_config(new_config)
                
                # Tema yöneticisi ayarlarını güncelle
                if self.theme_manager and "theme" in new_config:
                    logger.debug("Tema yöneticisi ayarları güncelleniyor...")
                    self.theme_manager.update_config(new_config)
                    
                # Animasyon motoru ayarlarını güncelle
                if self.animation_engine and "animation" in new_config:
                    logger.debug("Animasyon motoru ayarları güncelleniyor...")
                    self.animation_engine.update_config(new_config)
                
                # Loglama yapılandırmasını güncelle
                if "logging" in new_config:
                    logger.debug("Loglama yapılandırması güncelleniyor...")
                    self._setup_logging()
                
            except Exception as module_error:
                logger.error(f"Modül yapılandırmaları güncellenirken hata: {module_error}")
                # Hata durumunda eski yapılandırmaya geri dön
                self.config = old_config
                with open(self.config_path, 'w') as f:
                    json.dump(old_config, f, indent=4)
                return False
            
            logger.info("Yapılandırma başarıyla güncellendi.")
            return True
            
        except Exception as e:
            logger.error(f"Yapılandırma güncellenirken hata: {e}")
            return False