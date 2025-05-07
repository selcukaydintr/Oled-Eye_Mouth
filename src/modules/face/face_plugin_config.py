#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: face_plugin_config.py
# Açıklama: FacePlugin yapılandırma yönetimi işlevleri
# Bağımlılıklar: logging, os, json
# Bağlı Dosyalar: face_plugin_base.py, face_plugin_system.py

# Versiyon: 0.4.4
# Değişiklikler:
# - [0.4.4] Yapılandırma yönetimi işlevleri modülerleştirildi
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-04
===========================================================
"""

import os
import json
import logging
import copy
from typing import Dict, Any, Optional

# Loglama yapılandırması
logger = logging.getLogger("FacePluginConfig")

class FacePluginConfigMixin:
    """
    FacePlugin yapılandırma yönetimi mixin sınıfı
    
    Bu sınıf FacePlugin için yapılandırma yönetimi işlevlerini içerir:
    - Yapılandırma dosyası yükleme/kaydetme
    - Yapılandırma doğrulama
    - Varsayılan yapılandırma oluşturma
    - Yapılandırma değişikliklerini takip etme
    """
    
    def _create_default_config(self) -> Dict:
        """
        Varsayılan yapılandırmayı oluşturur
        
        Returns:
            Dict: Varsayılan yapılandırma
        """
        default_config = {
            "system": {
                "log_level": "INFO",
                "watchdog_enabled": True,
                "watchdog_timeout": 10,  # saniye
                "power_save_enabled": True,
                "debug_mode": False
            },
            "oled": {
                "brightness": 128,
                "power_save": True,
                "power_save_timeout": 300,  # saniye
                "random_eye_movement": True,
                "blink_frequency": 4.5  # saniye
            },
            "leds": {
                "brightness": 128,
                "enabled": True,
                "animate_emotions": True
            },
            "emotions": {
                "default_emotion": "neutral",
                "emotion_decay_time": 300,  # saniye
                "micro_expressions_enabled": True,
                "personality_profile": "balanced"
            },
            "animation": {
                "startup_animation_enabled": True,
                "fps": 30,
                "transition_speed": 1.0
            },
            "theme": {
                "default_theme": "default",
                "cache_enabled": True,
                "cache_size": 10
            },
            "api": {
                "port": 8000,
                "enabled": True,
                "access_control_enabled": False,
                "api_key": ""
            },
            "performance": {
                "enabled": True,
                "check_interval": 5,
                "cpu_threshold": 70,
                "memory_threshold": 80,
                "temperature_threshold": 70,
                "auto_adjust_fps": True,
                "auto_adjust_brightness": True,
                "battery_saver_enabled": False,
                "battery_threshold": 20
            }
        }
        
        logger.info("Varsayılan yapılandırma oluşturuldu")
        return default_config
    
    def _load_config(self) -> Dict:
        """
        Yapılandırma dosyasını yükler
        
        Returns:
            Dict: Yapılandırma ayarları
        """
        try:
            if not hasattr(self, 'config_path') or self.config_path is None or not os.path.exists(self.config_path):
                if hasattr(self, 'config_path'):
                    logger.warning(f"Yapılandırma dosyası bulunamadı: {self.config_path}")
                else:
                    logger.warning("Yapılandırma dosya yolu belirtilmemiş")
                return self._create_default_config()
            
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            logger.info(f"Yapılandırma dosyası yüklendi: {self.config_path}")
            return config
            
        except Exception as e:
            logger.error(f"Yapılandırma dosyası yüklenirken hata: {e}")
            return self._create_default_config()
    
    def _save_config(self) -> bool:
        """
        Yapılandırmayı dosyaya kaydeder
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            if not hasattr(self, 'config_path') or self.config_path is None:
                logger.error("Yapılandırma dosya yolu belirtilmemiş")
                return False
                
            # Yapılandırma dizininin var olduğundan emin ol
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            # Yapılandırmayı kaydet
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=4)
            
            logger.info(f"Yapılandırma dosyaya kaydedildi: {self.config_path}")
            return True
            
        except Exception as e:
            logger.error(f"Yapılandırma kaydedilirken hata: {e}")
            return False
    
    def update_config(self, new_config: Dict, save: bool = True) -> bool:
        """
        Yeni yapılandırmayı uygular ve isteğe bağlı olarak dosyaya kaydeder
        
        Args:
            new_config (Dict): Yeni yapılandırma ayarları
            save (bool, optional): Yapılandırmayı dosyaya kaydet. Varsayılan: True
            
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            if not hasattr(self, 'config'):
                logger.warning("Mevcut yapılandırma bulunamadı, yeni yapılandırma doğrudan uygulanıyor")
                self.config = new_config
            else:
                logger.info("Yapılandırma güncelleniyor...")
                
                # Mevcut yapılandırmayı yedekle
                old_config = copy.deepcopy(self.config)
                
                # Yeni yapılandırmayı ayarla
                self.config = new_config
                
                # Değişiklikleri kaydet
                if hasattr(self, 'track_config_changes'):
                    self.track_config_changes(old_config, new_config)
            
            # Modüllere yapılandırma değişikliğini bildir
            if hasattr(self, 'notify_config_changed'):
                self.notify_config_changed()
            
            # Yapılandırmayı dosyaya kaydet
            if save:
                return self._save_config()
            
            return True
            
        except Exception as e:
            logger.error(f"Yapılandırma güncellenirken hata: {e}")
            return False
    
    def reset_config(self) -> bool:
        """
        Yapılandırmayı varsayılan değerlere sıfırlar
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            # Varsayılan yapılandırmayı oluştur
            default_config = self._create_default_config()
            
            # Yapılandırmayı güncelle ve kaydet
            return self.update_config(default_config, save=True)
            
        except Exception as e:
            logger.error(f"Yapılandırma sıfırlanırken hata: {e}")
            return False
    
    def get_config_value(self, path: str, default: Any = None) -> Any:
        """
        Yapılandırmadan değer alır (nokta ayrılmış yol ile)
        
        Args:
            path (str): Nokta ayrılmış yapılandırma yolu (örn: "system.log_level")
            default (Any, optional): Değer bulunamazsa döndürülecek varsayılan değer
            
        Returns:
            Any: İstenen yapılandırma değeri veya varsayılan değer
        """
        if not hasattr(self, 'config'):
            return default
            
        try:
            parts = path.split('.')
            current = self.config
            
            for part in parts:
                if part not in current:
                    return default
                current = current[part]
            
            return current
            
        except Exception:
            return default
    
    def set_config_value(self, path: str, value: Any, save: bool = True) -> bool:
        """
        Yapılandırmada değer ayarlar (nokta ayrılmış yol ile)
        
        Args:
            path (str): Nokta ayrılmış yapılandırma yolu (örn: "system.log_level")
            value (Any): Ayarlanacak değer
            save (bool, optional): Değişiklikten sonra yapılandırmayı dosyaya kaydet. Varsayılan: True
            
        Returns:
            bool: Başarılı ise True, değilse False
        """
        if not hasattr(self, 'config'):
            logger.error("Yapılandırma bulunamadı, değer ayarlanamıyor")
            return False
            
        try:
            # Yapılandırmayı kopyala
            new_config = copy.deepcopy(self.config)
            
            parts = path.split('.')
            current = new_config
            
            # Son parçaya kadar ilerle
            for i, part in enumerate(parts[:-1]):
                if part not in current:
                    # Yeni dal oluştur
                    current[part] = {}
                current = current[part]
                
                if not isinstance(current, dict):
                    logger.error(f"Yapılandırma yolu geçersiz: {path} ('{part}' bir sözlük değil)")
                    return False
            
            # Son parçayı ayarla
            current[parts[-1]] = value
            
            # Yapılandırmayı güncelle
            return self.update_config(new_config, save=save)
            
        except Exception as e:
            logger.error(f"Yapılandırma değeri ayarlanırken hata: {path}={value}, hata: {e}")
            return False
    
    def track_config_changes(self, old_config: Dict, new_config: Dict) -> None:
        """
        Yapılandırma değişikliklerini takip eder ve loglar
        
        Args:
            old_config (Dict): Önceki yapılandırma
            new_config (Dict): Yeni yapılandırma
        """
        changed_paths = []
        
        def traverse_and_compare(old: Dict, new: Dict, path=""):
            if isinstance(old, dict) and isinstance(new, dict):
                # Tüm anahtarları kontrol et
                all_keys = set(list(old.keys()) + list(new.keys()))
                
                for key in all_keys:
                    # Yeni anahtar
                    if key not in old:
                        changed_paths.append(f"{path}{key}")
                    # Silinen anahtar
                    elif key not in new:
                        changed_paths.append(f"{path}{key}")
                    # Değişen değer
                    elif old[key] != new[key]:
                        # Eğer iki değer de sözlükse, karşılaştırmaya devam et
                        if isinstance(old[key], dict) and isinstance(new[key], dict):
                            traverse_and_compare(old[key], new[key], f"{path}{key}.")
                        else:
                            changed_paths.append(f"{path}{key}")
        
        # Yapılandırmaları karşılaştır
        traverse_and_compare(old_config, new_config)
        
        if changed_paths:
            logger.info(f"Yapılandırma değişiklikleri: {', '.join(changed_paths)}")
    
    def notify_config_changed(self) -> None:
        """
        Modülleri yapılandırma değişikliğinden haberdar eder
        """
        try:
            # OLED kontrolcü ayarlarını güncelle
            if hasattr(self, 'oled_controller') and self.oled_controller is not None:
                logger.debug("OLED kontrolcü ayarları güncelleniyor...")
                self.oled_controller.update_config(self.config)
            
            # LED kontrolcü ayarlarını güncelle
            if hasattr(self, 'led_controller') and self.led_controller is not None:
                logger.debug("LED kontrolcü ayarları güncelleniyor...")
                self.led_controller.update_config(self.config)
            
            # Duygu motoru ayarlarını güncelle
            if hasattr(self, 'emotion_engine') and self.emotion_engine is not None:
                logger.debug("Duygu motoru ayarları güncelleniyor...")
                self.emotion_engine.update_config(self.config)
            
            # Tema yöneticisi ayarlarını güncelle
            if hasattr(self, 'theme_manager') and self.theme_manager is not None:
                logger.debug("Tema yöneticisi ayarları güncelleniyor...")
                self.theme_manager.update_config(self.config)
            
            # Animasyon motoru ayarlarını güncelle
            if hasattr(self, 'animation_engine') and self.animation_engine is not None:
                logger.debug("Animasyon motoru ayarları güncelleniyor...")
                self.animation_engine.update_config(self.config)
            
            # Performans optimize edici ayarlarını güncelle
            if hasattr(self, 'performance_optimizer') and self.performance_optimizer is not None:
                logger.debug("Performans optimize edici ayarları güncelleniyor...")
                self.performance_optimizer.update_config(self.config)
                
            # Dashboard server ayarlarını güncelle
            if hasattr(self, 'dashboard_server') and self.dashboard_server is not None:
                logger.debug("Dashboard server ayarları güncelleniyor...")
                self.dashboard_server.update_config(self.config)
            
            logger.info("Tüm modüller yapılandırma değişikliğinden haberdar edildi")
            
        except Exception as e:
            logger.error(f"Yapılandırma değişikliği bildirilirken hata: {e}")