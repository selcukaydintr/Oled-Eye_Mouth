#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: config_standardizer.py
# Açıklama: Plugin yapılandırma standardizasyonu, FACE1'in üst proje ile uyumlu yapılandırma yönetimi
# Bağımlılıklar: logging, json, jsonschema, os, sys
# Bağlı Dosyalar: 
#   - src/modules/face1_plugin.py
#   - src/plugins/plugin_isolation.py

# Versiyon: 0.4.3
# Değişiklikler:
# - [0.4.3] Plugin yapılandırma standardizasyonu modülü oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-04
===========================================================
"""

import os
import sys
import json
import logging
import copy
from typing import Dict, List, Optional, Any, Union
from pathlib import Path
from datetime import datetime

try:
    import jsonschema
    JSONSCHEMA_AVAILABLE = True
except ImportError:
    JSONSCHEMA_AVAILABLE = False

# Proje dizinini Python yoluna ekle
PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(str(PROJECT_DIR))

# Logger yapılandırması
logger = logging.getLogger("ConfigStandardizer")


class ConfigStandardizer:
    """
    Plugin Yapılandırma Standardizasyonu
    
    Bu sınıf, FACE1 plugin'inin yapılandırmasını üst proje ile uyumlu hale getirir:
    - Yapılandırma şema doğrulaması
    - Yapılandırma dönüşümü ve uyumluluk sağlama
    - Default değerleri sağlama
    - Yapılandırma geçmişi ve geri alma
    - Yapılandırma migrasyonu
    """
    
    # FACE1 yapılandırma şeması - modülün doğrudan bir parçası olarak tanımlanmıştır
    FACE1_CONFIG_SCHEMA = {
        "type": "object",
        "properties": {
            "system": {
                "type": "object",
                "properties": {
                    "log_level": {"type": "string", "enum": ["DEBUG", "INFO", "WARNING", "ERROR"]},
                    "watchdog_enabled": {"type": "boolean"},
                    "watchdog_timeout": {"type": "number", "minimum": 1}
                }
            },
            "oled": {
                "type": "object",
                "properties": {
                    "brightness": {"type": "integer", "minimum": 0, "maximum": 255},
                    "power_save": {"type": "boolean"},
                    "power_save_timeout": {"type": "number", "minimum": 10},
                    "random_eye_movement": {"type": "boolean"},
                    "blink_frequency": {"type": "number", "minimum": 0.1}
                }
            },
            "leds": {
                "type": "object",
                "properties": {
                    "brightness": {"type": "integer", "minimum": 0, "maximum": 255},
                    "enabled": {"type": "boolean"},
                    "animate_emotions": {"type": "boolean"}
                }
            },
            "emotions": {
                "type": "object",
                "properties": {
                    "default_emotion": {"type": "string"},
                    "emotion_decay_time": {"type": "number", "minimum": 0},
                    "micro_expressions_enabled": {"type": "boolean"},
                    "personality_profile": {"type": "string"}
                }
            },
            "animation": {
                "type": "object",
                "properties": {
                    "startup_animation_enabled": {"type": "boolean"},
                    "fps": {"type": "number", "minimum": 1, "maximum": 60},
                    "transition_speed": {"type": "number", "minimum": 0.1, "maximum": 5.0}
                }
            },
            "theme": {
                "type": "object",
                "properties": {
                    "default_theme": {"type": "string"},
                    "cache_enabled": {"type": "boolean"},
                    "cache_size": {"type": "integer", "minimum": 1}
                }
            },
            "api": {
                "type": "object",
                "properties": {
                    "port": {"type": "integer", "minimum": 1024, "maximum": 65535},
                    "enabled": {"type": "boolean"},
                    "access_control_enabled": {"type": "boolean"},
                    "api_key": {"type": "string"}
                }
            },
            "performance": {
                "type": "object",
                "properties": {
                    "enabled": {"type": "boolean"},
                    "check_interval": {"type": "number", "minimum": 1},
                    "cpu_threshold": {"type": "number", "minimum": 0, "maximum": 100},
                    "memory_threshold": {"type": "number", "minimum": 0, "maximum": 100},
                    "auto_adjust_fps": {"type": "boolean"},
                    "auto_adjust_brightness": {"type": "boolean"},
                    "battery_saver_enabled": {"type": "boolean"},
                    "battery_threshold": {"type": "number", "minimum": 0, "maximum": 100}
                }
            },
            "plugin_isolation": {
                "type": "object",
                "properties": {
                    "enabled": {"type": "boolean"},
                    "resource_limits": {
                        "type": "object",
                        "properties": {
                            "cpu_limit": {"type": "number", "minimum": 0, "maximum": 100},
                            "memory_limit": {"type": "number", "minimum": 10},
                            "file_descriptors_limit": {"type": "integer", "minimum": 100}
                        }
                    },
                    "error_recovery": {"type": "boolean"},
                    "max_recovery_attempts": {"type": "integer", "minimum": 1}
                }
            }
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Yapılandırma standardizasyonu başlatır
        
        Args:
            config_path: Yapılandırma dosyasının yolu (None ise varsayılanı kullan)
        """
        self.config_path = config_path or os.path.join(PROJECT_DIR, "config", "config.json")
        self.backup_dir = os.path.join(PROJECT_DIR, "config", "backups")
        self.config_history = []
        
        # Yedekleme dizinini oluştur
        os.makedirs(self.backup_dir, exist_ok=True)
        
        # Varsayılan yapılandırma
        self.default_config = self._get_default_config()
        
        # Mevcut yapılandırmayı yükle
        self.config = self._load_config()
        
        logger.info("Yapılandırma standardizasyonu başlatıldı")
    
    def standardize(self, config: Dict = None) -> Dict:
        """
        Yapılandırmayı standardize eder ve şema uygunluğunu doğrular
        
        Args:
            config: Standardize edilecek yapılandırma (None ise yüklenmiş yapılandırma kullanılır)
            
        Returns:
            Dict: Standardize edilmiş yapılandırma
        """
        # Yapılandırmayı kopyala (None ise mevcut yapılandırmayı kullan)
        working_config = copy.deepcopy(config if config is not None else self.config)
        
        # Default değerleri ekle (eksik değerler için)
        standardized_config = self._merge_with_defaults(working_config)
        
        # Değerleri standartlaştır (tip dönüşümleri ve uyumluluk)
        standardized_config = self._normalize_values(standardized_config)
        
        # Şema doğrulaması yap
        if self._validate_schema(standardized_config):
            logger.info("Yapılandırma standardize edildi ve doğrulandı")
        else:
            logger.warning("Yapılandırma şema doğrulaması başarısız, varsayılan değerler kullanılacak")
            # Şema doğrulaması başarısız olursa, varsayılan yapılandırmayı kullan
            standardized_config = copy.deepcopy(self.default_config)
        
        return standardized_config
    
    def migrate_from_parent_config(self, parent_config: Dict) -> Dict:
        """
        Üst projenin yapılandırmasından FACE1'e uygun yapılandırma oluşturur
        
        Args:
            parent_config: Üst projenin yapılandırması
            
        Returns:
            Dict: FACE1 uyumlu yapılandırma
        """
        # Üst projeden alınacak yapılandırma eşleştirmeleri
        # Üst proje yapılandırma anahtarı -> FACE1 yapılandırma yolu
        mapping = {
            "robot.face.log_level": "system.log_level",
            "robot.face.display.brightness": "oled.brightness",
            "robot.face.display.power_save": "oled.power_save",
            "robot.face.leds.enabled": "leds.enabled",
            "robot.face.leds.brightness": "leds.brightness",
            "robot.face.emotion.default": "emotions.default_emotion",
            "robot.face.theme": "theme.default_theme",
            "robot.api.port": "api.port",
            "robot.api.key": "api.api_key"
        }
        
        # Varsayılan FACE1 yapılandırması
        face_config = copy.deepcopy(self.default_config)
        
        # Eşleştirme mapini kullanarak değerleri kopyala
        for parent_path, face_path in mapping.items():
            # Üst projeden değer al
            value = self._get_nested_value(parent_config, parent_path.split('.'))
            
            # Değer varsa FACE1 yapılandırmasına ayarla
            if value is not None:
                self._set_nested_value(face_config, face_path.split('.'), value)
        
        # Standardizasyon uygula
        return self.standardize(face_config)
    
    def export_to_parent_format(self, face_config: Dict = None) -> Dict:
        """
        FACE1 yapılandırmasını üst proje formatına dönüştürür
        
        Args:
            face_config: FACE1 yapılandırması (None ise mevcut yapılandırma kullanılır)
            
        Returns:
            Dict: Üst proje formatında yapılandırma
        """
        # Yapılandırmayı kopyala (None ise mevcut yapılandırmayı kullan)
        config = copy.deepcopy(face_config if face_config is not None else self.config)
        
        # FACE1'den üst projeye yapılandırma eşleştirmeleri
        # FACE1 yapılandırma yolu -> Üst proje yapılandırma anahtarı
        mapping = {
            "system.log_level": "robot.face.log_level",
            "oled.brightness": "robot.face.display.brightness",
            "oled.power_save": "robot.face.display.power_save",
            "leds.enabled": "robot.face.leds.enabled",
            "leds.brightness": "robot.face.leds.brightness",
            "emotions.default_emotion": "robot.face.emotion.default",
            "theme.default_theme": "robot.face.theme",
            "api.port": "robot.api.port",
            "api.api_key": "robot.api.key"
        }
        
        # Üst proje yapılandırması için boş başla
        parent_config = {}
        
        # Eşleştirme mapini kullanarak değerleri kopyala
        for face_path, parent_path in mapping.items():
            # FACE1 yapılandırmasından değer al
            value = self._get_nested_value(config, face_path.split('.'))
            
            # Değer varsa üst proje yapılandırmasına ayarla
            if value is not None:
                self._set_nested_value(parent_config, parent_path.split('.'), value)
        
        return parent_config
    
    def save_config(self, config: Dict = None, create_backup: bool = True) -> bool:
        """
        Yapılandırmayı kaydeder
        
        Args:
            config: Kaydedilecek yapılandırma (None ise mevcut yapılandırma kullanılır)
            create_backup: Yedek oluşturulup oluşturulmayacağı
            
        Returns:
            bool: Kaydetme başarılı mı
        """
        # Yapılandırmayı kopyala (None ise mevcut yapılandırmayı kullan)
        working_config = copy.deepcopy(config if config is not None else self.config)
        
        try:
            # Mevcut yapılandırmayı yedekle
            if create_backup and os.path.exists(self.config_path):
                self._create_backup()
            
            # Yapılandırmayı kaydet
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(working_config, f, indent=2, ensure_ascii=False)
            
            # Yapılandırmayı güncelle
            self.config = working_config
            
            # Yapılandırma geçmişine ekle
            self._add_to_history(working_config)
            
            logger.info("Yapılandırma başarıyla kaydedildi")
            return True
        except Exception as e:
            logger.error(f"Yapılandırma kaydedilemedi: {e}")
            return False
    
    def restore_backup(self, backup_index: int = -1) -> Optional[Dict]:
        """
        Yedekten yapılandırmayı geri yükler
        
        Args:
            backup_index: Geri yüklenecek yedeğin indeksi (-1 en son yedek)
            
        Returns:
            Dict: Geri yüklenen yapılandırma veya None
        """
        try:
            # Yedek dosyalarını listele
            backup_files = [f for f in os.listdir(self.backup_dir) if f.endswith('.json')]
            backup_files.sort()  # Tarih/saat sırasına göre sırala
            
            if not backup_files:
                logger.warning("Geri yüklenecek yedek bulunamadı")
                return None
            
            # Belirtilen indeksteki yedeği seç
            try:
                backup_file = backup_files[backup_index]
            except IndexError:
                backup_file = backup_files[-1]  # Son yedeği kullan
            
            backup_path = os.path.join(self.backup_dir, backup_file)
            
            # Yedeği oku
            with open(backup_path, 'r', encoding='utf-8') as f:
                backup_config = json.load(f)
            
            # Mevcut yapılandırmayı yedekle
            self._create_backup()
            
            # Yedeği mevcut yapılandırma olarak kaydet
            self.config = backup_config
            self.save_config(backup_config, create_backup=False)
            
            logger.info(f"Yapılandırma {backup_file} yedeğinden geri yüklendi")
            return backup_config
        except Exception as e:
            logger.error(f"Yedek geri yüklenirken hata: {e}")
            return None
    
    def _load_config(self) -> Dict:
        """
        Yapılandırma dosyasını yükler
        
        Returns:
            Dict: Yüklenen yapılandırma
        """
        try:
            # Yapılandırma dosyası var mı kontrol et
            if not os.path.exists(self.config_path):
                logger.warning(f"Yapılandırma dosyası bulunamadı: {self.config_path}, varsayılanlar kullanılacak")
                return self.default_config
                
            # Dosyadan yapılandırmayı oku
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                
            # Geçmiş bilgisine ekle
            self._add_to_history(config)
                
            # Standardize et ve döndür
            return self.standardize(config)
        except Exception as e:
            logger.error(f"Yapılandırma yüklenirken hata: {e}, varsayılanlar kullanılacak")
            return self.default_config
    
    def _get_default_config(self) -> Dict:
        """
        Varsayılan yapılandırmayı döndürür
        
        Returns:
            Dict: Varsayılan yapılandırma
        """
        return {
            "system": {
                "log_level": "INFO",
                "watchdog_enabled": True,
                "watchdog_timeout": 10
            },
            "oled": {
                "brightness": 128,
                "power_save": True,
                "power_save_timeout": 300,
                "random_eye_movement": True,
                "blink_frequency": 4.5
            },
            "leds": {
                "brightness": 128,
                "enabled": True,
                "animate_emotions": True
            },
            "emotions": {
                "default_emotion": "neutral",
                "emotion_decay_time": 300,
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
                "check_interval": 10,
                "cpu_threshold": 80,
                "memory_threshold": 80,
                "auto_adjust_fps": True,
                "auto_adjust_brightness": True,
                "battery_saver_enabled": True,
                "battery_threshold": 20
            },
            "plugin_isolation": {
                "enabled": True,
                "resource_limits": {
                    "cpu_limit": 80,
                    "memory_limit": 500,
                    "file_descriptors_limit": 1000
                },
                "error_recovery": True,
                "max_recovery_attempts": 3
            }
        }
    
    def _merge_with_defaults(self, config: Dict) -> Dict:
        """
        Yapılandırmayı varsayılanlar ile birleştirir
        
        Args:
            config: Birleştirilecek yapılandırma
            
        Returns:
            Dict: Birleştirilmiş yapılandırma
        """
        # Derin birleştirme
        def deep_merge(default: Dict, custom: Dict) -> Dict:
            result = copy.deepcopy(default)
            
            for key, value in custom.items():
                # Eğer değer bir sözlük ise ve varsayılanlarda da varsa, alt sözlükleri birleştir
                if isinstance(value, dict) and key in result and isinstance(result[key], dict):
                    result[key] = deep_merge(result[key], value)
                # Değilse, değeri doğrudan kopyala
                else:
                    result[key] = copy.deepcopy(value)
                    
            return result
        
        # Varsayılanlar ile birleştir
        return deep_merge(self.default_config, config)
    
    def _normalize_values(self, config: Dict) -> Dict:
        """
        Yapılandırma değerlerini normalleştirir
        
        Args:
            config: Normalleştirilecek yapılandırma
            
        Returns:
            Dict: Normalleştirilmiş yapılandırma
        """
        # Derin normalleştirme
        def normalize(cfg: Dict, path: str = "") -> Dict:
            result = {}
            
            for key, value in cfg.items():
                current_path = f"{path}.{key}" if path else key
                
                # Eğer değer bir sözlük ise, alt sözlükleri normalleştir
                if isinstance(value, dict):
                    result[key] = normalize(value, current_path)
                # Değilse, değeri normalleştir
                else:
                    # Boolean değerleri normalleştir
                    if current_path in [
                        "system.watchdog_enabled", "oled.power_save", "oled.random_eye_movement",
                        "leds.enabled", "leds.animate_emotions", "emotions.micro_expressions_enabled",
                        "animation.startup_animation_enabled", "theme.cache_enabled",
                        "api.enabled", "api.access_control_enabled", "performance.enabled",
                        "performance.auto_adjust_fps", "performance.auto_adjust_brightness",
                        "performance.battery_saver_enabled", "plugin_isolation.enabled",
                        "plugin_isolation.error_recovery"
                    ]:
                        # Çeşitli boolean temsilleri için normalleştirme
                        if isinstance(value, str):
                            result[key] = value.lower() in ["true", "yes", "1", "on", "evet", "doğru"]
                        else:
                            result[key] = bool(value)
                    # Sayısal değerleri normalleştir
                    elif current_path in [
                        "oled.brightness", "leds.brightness", "api.port",
                        "theme.cache_size", "plugin_isolation.max_recovery_attempts"
                    ]:
                        try:
                            result[key] = int(value)
                        except (ValueError, TypeError):
                            # Dönüştürme başarısız olursa varsayılana geç
                            default_value = self._get_nested_value(
                                self.default_config, current_path.split('.')
                            )
                            result[key] = default_value
                    # Float değerleri normalleştir
                    elif current_path in [
                        "system.watchdog_timeout", "oled.power_save_timeout",
                        "oled.blink_frequency", "emotions.emotion_decay_time",
                        "animation.fps", "animation.transition_speed",
                        "performance.check_interval", "performance.cpu_threshold",
                        "performance.memory_threshold", "performance.battery_threshold",
                        "plugin_isolation.resource_limits.cpu_limit",
                        "plugin_isolation.resource_limits.memory_limit"
                    ]:
                        try:
                            result[key] = float(value)
                        except (ValueError, TypeError):
                            # Dönüştürme başarısız olursa varsayılana geç
                            default_value = self._get_nested_value(
                                self.default_config, current_path.split('.')
                            )
                            result[key] = default_value
                    # Diğer değerleri olduğu gibi al
                    else:
                        result[key] = value
                
            return result
        
        # Yapılandırmayı normalleştir
        return normalize(config)
    
    def _validate_schema(self, config: Dict) -> bool:
        """
        Yapılandırmanın şema uygunluğunu doğrular
        
        Args:
            config: Doğrulanacak yapılandırma
            
        Returns:
            bool: Doğrulama başarılı mı
        """
        if not JSONSCHEMA_AVAILABLE:
            logger.warning("jsonschema kütüphanesi kurulu değil, şema doğrulaması atlanıyor")
            return True
        
        try:
            jsonschema.validate(config, self.FACE1_CONFIG_SCHEMA)
            return True
        except jsonschema.exceptions.ValidationError as e:
            logger.error(f"Yapılandırma şema doğrulaması başarısız: {e}")
            return False
    
    def _create_backup(self) -> str:
        """
        Mevcut yapılandırmanın yedeğini oluşturur
        
        Returns:
            str: Yedek dosyasının yolu
        """
        try:
            # Tarih/saat eklenmiş yedek dosya adı
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_path = os.path.join(self.backup_dir, f"config_{timestamp}.json")
            
            # Mevcut yapılandırmayı yeni dosyaya kopyala
            with open(self.config_path, 'r', encoding='utf-8') as src, \
                 open(backup_path, 'w', encoding='utf-8') as dst:
                dst.write(src.read())
            
            logger.info(f"Yapılandırma yedeği oluşturuldu: {backup_path}")
            
            # Eski yedekleri temizle (son 10 taneyi tut)
            backup_files = [f for f in os.listdir(self.backup_dir) if f.endswith('.json')]
            backup_files.sort()  # Tarih/saat sırasına göre sırala
            
            # 10'dan fazla yedek varsa, eski olanları sil
            if len(backup_files) > 10:
                for old_backup in backup_files[:-10]:  # Son 10 hariç hepsini sil
                    os.remove(os.path.join(self.backup_dir, old_backup))
                logger.info(f"{len(backup_files) - 10} eski yedek temizlendi")
            
            return backup_path
        except Exception as e:
            logger.error(f"Yedek oluşturulamadı: {e}")
            return ""
    
    def _add_to_history(self, config: Dict) -> None:
        """
        Yapılandırmayı geçmiş bilgisine ekler
        
        Args:
            config: Eklenecek yapılandırma
        """
        # En fazla 5 yapılandırmayı geçmişte tut
        if len(self.config_history) >= 5:
            self.config_history.pop(0)
        
        # Yapılandırmanın derin kopyasını ekle
        self.config_history.append({
            "timestamp": datetime.now().isoformat(),
            "config": copy.deepcopy(config)
        })
    
    def _get_nested_value(self, d: Dict, keys: List[str]) -> Any:
        """
        İç içe sözlükten değer alır
        
        Args:
            d: Sözlük
            keys: Anahtar listesi
            
        Returns:
            Any: Bulunan değer veya None
        """
        for key in keys:
            if isinstance(d, dict) and key in d:
                d = d[key]
            else:
                return None
        return d
    
    def _set_nested_value(self, d: Dict, keys: List[str], value: Any) -> None:
        """
        İç içe sözlükte değer ayarlar
        
        Args:
            d: Sözlük
            keys: Anahtar listesi
            value: Ayarlanacak değer
        """
        for key in keys[:-1]:
            if key not in d:
                d[key] = {}
            d = d[key]
        d[keys[-1]] = value


# Test kodu
if __name__ == "__main__":
    # Logging yapılandırması
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Geçici bir test yapılandırma dosyası yolu oluştur
    import tempfile
    test_dir = tempfile.mkdtemp()
    test_config_path = os.path.join(test_dir, "test_config.json")
    
    # Test yapılandırması
    test_config = {
        "system": {
            "log_level": "DEBUG"
        },
        "oled": {
            "brightness": "200",  # String olarak bir sayı
            "power_save": "yes"   # String olarak boolean
        },
        "animation": {
            "fps": 45
        }
    }
    
    # Yapılandırma değerlerini dosyaya yaz
    with open(test_config_path, 'w', encoding='utf-8') as f:
        json.dump(test_config, f)
    
    print("=== Yapılandırma Standardizasyonu Testi ===")
    
    # ConfigStandardizer örneği oluştur
    standardizer = ConfigStandardizer(test_config_path)
    
    # Yapılandırmayı standardize et
    std_config = standardizer.standardize(test_config)
    print("\n1. Standardize Edilmiş Yapılandırma:")
    print(f"  - oled.brightness: {std_config['oled']['brightness']} ({type(std_config['oled']['brightness']).__name__})")
    print(f"  - oled.power_save: {std_config['oled']['power_save']} ({type(std_config['oled']['power_save']).__name__})")
    
    # Üst projeye dönüşüm testi
    parent_format = standardizer.export_to_parent_format(std_config)
    print("\n2. Üst Proje Formatında Yapılandırma:")
    print(f"  - robot.face.display.brightness: {parent_format.get('robot', {}).get('face', {}).get('display', {}).get('brightness')}")
    
    # Üst projeden dönüşüm testi
    parent_config = {
        "robot": {
            "face": {
                "log_level": "WARNING",
                "display": {
                    "brightness": 180
                },
                "leds": {
                    "enabled": False
                }
            }
        }
    }
    
    face_config = standardizer.migrate_from_parent_config(parent_config)
    print("\n3. Üst Projeden Dönüştürülmüş Yapılandırma:")
    print(f"  - system.log_level: {face_config['system']['log_level']}")
    print(f"  - oled.brightness: {face_config['oled']['brightness']}")
    print(f"  - leds.enabled: {face_config['leds']['enabled']}")
    
    # Temizlik
    import shutil
    shutil.rmtree(test_dir)
    
    print("\nYapılandırma standardizasyonu testi tamamlandı.")