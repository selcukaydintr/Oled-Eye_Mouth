#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: theme_manager_base.py
# Açıklama: Tema yöneticisi temel sınıfı ve çekirdek işlevler
# Bağımlılıklar: logging, os, pathlib, json
# Bağlı Dosyalar: oled_controller.py, face_plugin.py

# Versiyon: 0.3.4
# Değişiklikler:
# - [0.1.0] Temel tema yöneticisi sınıfı oluşturuldu
# - [0.2.0] Tema önizleme özelliği, Pixel ve Gerçekçi tema şablonları eklendi
# - [0.3.0] Tema düzenleme, kopyalama ve önizleme özellikleri geliştirildi  
# - [0.3.3] Tema önbellek sistemi geliştirildi
# - [0.3.4] Tema varlıkları için iyileştirme ve önbellek performans optimizasyonu eklendi
#
# Son Güncelleme: 2025-05-02
# Yazar: GitHub Copilot
# Tarih: 2025-05-02
===========================================================

Bu modül, tema yöneticisi için temel sınıf ve gerekli çekirdek işlevleri içerir.
Tema yönetimi için gerekli temel yapıyı sağlar.
"""

import os
import sys
import json
import shutil
import logging
import threading
import re
import copy
import time
from typing import Dict, List, Optional, Union
from pathlib import Path

# Proje dizinini ve include dizinini Python yoluna ekle
PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.append(str(PROJECT_DIR))

# Logger yapılandırması
logger = logging.getLogger("ThemeManager")


class BaseThemeManager:
    """
    Tema yöneticisi temel sınıfı
    
    Bu sınıf, robot yüzü için farklı görsel temaları yönetmek için
    gerekli temel işlevselliği sağlar.
    """
    
    # Tema stilleri
    THEME_STYLES = ["cartoon", "minimal", "pixel", "realistic"]
    
    def __init__(self, config):
        """
        Tema yöneticisi temel sınıfını başlatır
        
        Args:
            config (dict): Yapılandırma ayarları
        """
        logger.info("Tema Yöneticisi temel sınıfı başlatılıyor...")
        self.config = config
        
        # Tema dizini
        self.theme_base_dir = os.path.join(PROJECT_DIR, "themes")
        
        # Mevcut tema
        self.active_theme = config.get("theme", {}).get("default_theme", "default")
        
        # Tema önbelleği
        self.theme_cache = {}
        
        # Tema önizleme verileri (önbellek)
        self.preview_cache = {}
        
        # Alt tip varlıkları önbelleği
        self.subtype_asset_cache = {}
        
        # Varlık maksimum önbellek boyutu (tema sayısı)
        self.max_cache_size = config.get("theme", {}).get("max_cache_size", 5)
        
        # Son erişilen tema önbelleği (LRU - En az kullanılanı önce çıkar)
        self.lru_cache = []
        
        # Önbellek süre aşımı (saniye)
        self.cache_timeout = config.get("theme", {}).get("cache_timeout", 300)  # 5 dakika
        
        # Önbellek zaman damgaları
        self.cache_timestamps = {}
        
        # İlk yükleme işlemi için kilit
        self.load_lock = threading.RLock()
        
        # Tema değiştirme için geri çağırma listesi
        self.change_callbacks = []
        
        # Tema listesi önbelleği
        self.themes_list_cache = []
        self.themes_list_cache_timestamp = 0
        self.themes_list_cache_timeout = config.get("theme", {}).get("themes_list_cache_timeout", 60)  # 1 dakika
        
        logger.info("Tema Yöneticisi temel sınıfı başlatıldı.")
    
    def start(self) -> bool:
        """
        Tema yöneticisini başlatır
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            # Tema dizinlerini kontrol et
            if not os.path.exists(self.theme_base_dir):
                os.makedirs(self.theme_base_dir, exist_ok=True)
                logger.info(f"Temalar dizini oluşturuldu: {self.theme_base_dir}")
            
            # Varsayılan tema dizinini kontrol et
            default_theme_dir = os.path.join(self.theme_base_dir, "default")
            if not os.path.exists(default_theme_dir):
                os.makedirs(default_theme_dir, exist_ok=True)
                logger.info(f"Varsayılan tema dizini oluşturuldu: {default_theme_dir}")
                
                # Alt dizinleri oluştur
                os.makedirs(os.path.join(default_theme_dir, "eyes"), exist_ok=True)
                os.makedirs(os.path.join(default_theme_dir, "mouth"), exist_ok=True)
                
                # Varsayılan tema dosyasını oluştur
                self._create_default_theme_file(default_theme_dir)
            
            # Minimal tema dizinini kontrol et
            minimal_theme_dir = os.path.join(self.theme_base_dir, "minimal")
            if not os.path.exists(minimal_theme_dir):
                os.makedirs(minimal_theme_dir, exist_ok=True)
                logger.info(f"Minimal tema dizini oluşturuldu: {minimal_theme_dir}")
                
                # Alt dizinleri oluştur
                os.makedirs(os.path.join(minimal_theme_dir, "eyes"), exist_ok=True)
                os.makedirs(os.path.join(minimal_theme_dir, "mouth"), exist_ok=True)
                
                # Minimal tema dosyasını oluştur
                self._create_minimal_theme_file(minimal_theme_dir)
            
            # Pixel tema dizinini kontrol et
            pixel_theme_dir = os.path.join(self.theme_base_dir, "pixel")
            if not os.path.exists(pixel_theme_dir):
                os.makedirs(pixel_theme_dir, exist_ok=True)
                logger.info(f"Pixel tema dizini oluşturuldu: {pixel_theme_dir}")
                
                # Alt dizinleri oluştur
                os.makedirs(os.path.join(pixel_theme_dir, "eyes"), exist_ok=True)
                os.makedirs(os.path.join(pixel_theme_dir, "mouth"), exist_ok=True)
                
                # Pixel tema dosyasını oluştur
                self._create_pixel_theme_file(pixel_theme_dir)
            
            # Gerçekçi tema dizinini kontrol et
            realistic_theme_dir = os.path.join(self.theme_base_dir, "realistic")
            if not os.path.exists(realistic_theme_dir):
                os.makedirs(realistic_theme_dir, exist_ok=True)
                logger.info(f"Gerçekçi tema dizini oluşturuldu: {realistic_theme_dir}")
                
                # Alt dizinleri oluştur
                os.makedirs(os.path.join(realistic_theme_dir, "eyes"), exist_ok=True)
                os.makedirs(os.path.join(realistic_theme_dir, "mouth"), exist_ok=True)
                
                # Gerçekçi tema dosyasını oluştur
                self._create_realistic_theme_file(realistic_theme_dir)
            
            # Mevcut temayı yükle
            if not self.load_theme(self.active_theme):
                logger.warning(f"'{self.active_theme}' teması yüklenemedi, varsayılana geçiliyor.")
                self.active_theme = "default"
                if not self.load_theme(self.active_theme):
                    logger.error("Varsayılan tema da yüklenemedi!")
                    return False
            
            logger.info(f"Tema yöneticisi başlatıldı. Mevcut tema: {self.active_theme}")
            return True
            
        except Exception as e:
            logger.error(f"Tema yöneticisi başlatılırken hata: {e}")
            return False
    
    def stop(self) -> None:
        """
        Tema yöneticisini durdurur
        """
        # Önbelleği temizle
        self.theme_cache.clear()
        logger.info("Tema yöneticisi durduruldu.")
    
    def set_theme(self, theme_name: str) -> bool:
        """
        Temayı değiştirir
        
        Args:
            theme_name (str): Tema adı
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        # Tema geçerliliğini kontrol et
        theme_dir = os.path.join(self.theme_base_dir, theme_name)
        if not os.path.exists(theme_dir) or not os.path.isdir(theme_dir):
            logger.error(f"Tema bulunamadı: {theme_name}")
            return False
        
        # Tema verilerini yükle
        theme_data = self.load_theme(theme_name)
        if not theme_data:
            logger.error(f"Tema verileri yüklenemedi: {theme_name}")
            return False
        
        # Önceki tema
        prev_theme = self.active_theme
        
        # Mevcut temayı güncelle
        self.active_theme = theme_name
        
        # Geri çağırma fonksiyonlarını tetikle
        for callback in self.change_callbacks:
            try:
                # Dict formatında tema değişim bilgileri gönder
                callback({
                    "new_theme": theme_name,
                    "old_theme": prev_theme
                })
            except Exception as e:
                logger.error(f"Tema değiştirme geri çağrıma hatası: {e}")
        
        logger.info(f"Tema değiştirildi: {prev_theme} -> {theme_name}")
        return True
    
    def get_current_theme(self) -> str:
        """
        Mevcut tema adını döndürür
        
        Returns:
            str: Mevcut tema adı
        """
        return self.active_theme
    
    def load_theme(self, theme_name: str) -> Optional[Dict]:
        """
        Bir temayı yükler
        
        Args:
            theme_name (str): Tema adı
        
        Returns:
            Optional[Dict]: Tema verileri veya başarısız olursa None
        """
        with self.load_lock:
            # Önbellekte kontrol et
            if theme_name in self.theme_cache:
                return self.theme_cache[theme_name]
            
            # Tema dizini kontrolü
            theme_dir = os.path.join(self.theme_base_dir, theme_name)
            theme_file = os.path.join(theme_dir, "theme.json")
            
            if not os.path.exists(theme_file):
                logger.error(f"Tema dosyası bulunamadı: {theme_file}")
                return None
            
            try:
                # Tema dosyasını yükle
                with open(theme_file, 'r') as f:
                    theme_data = json.load(f)
                
                # Temel doğrulamaları yap
                required_fields = ["name", "eyes", "mouth", "led"]
                for field in required_fields:
                    if field not in theme_data:
                        logger.error(f"Tema dosyası geçersiz, gerekli alan eksik: {field}")
                        return None
                
                # Önbelleğe al
                self.theme_cache[theme_name] = theme_data
                logger.info(f"Tema yüklendi: {theme_name}")
                return theme_data
                
            except json.JSONDecodeError as e:
                logger.error(f"Tema dosyası geçersiz JSON formatı: {e}")
                return None
            except Exception as e:
                logger.error(f"Tema yüklenirken hata: {e}")
                return None
    
    def get_theme_list(self) -> List[str]:
        """
        Mevcut temaların listesini döndürür
        
        Returns:
            List[str]: Tema adları listesi
        """
        # Zamanı kontrol et ve gerektiğinde önbelleği güncelle
        current_time = time.time()
        
        # Önbelleklenmiş tema listesi varsa ve zaman aşımına uğramamışsa kullan
        if self.themes_list_cache and (current_time - self.themes_list_cache_timestamp) < self.themes_list_cache_timeout:
            return self.themes_list_cache
        
        themes = []
        
        try:
            for item in os.listdir(self.theme_base_dir):
                theme_dir = os.path.join(self.theme_base_dir, item)
                theme_file = os.path.join(theme_dir, "theme.json")
                
                if os.path.isdir(theme_dir) and os.path.exists(theme_file):
                    themes.append(item)
                    
            # Tema listesini önbelleğe al
            self.themes_list_cache = themes
            self.themes_list_cache_timestamp = current_time
            
        except Exception as e:
            logger.error(f"Tema listesi alınırken hata: {e}")
            
            # Hata durumunda önbellek varsa onu kullan
            if self.themes_list_cache:
                return self.themes_list_cache
        
        return themes
    
    def register_change_callback(self, callback) -> None:
        """
        Tema değişikliği için geri çağrı fonksiyonu kaydeder
        
        Args:
            callback: Geri çağrı fonksiyonu (yeni_tema, eski_tema)
        """
        if callback not in self.change_callbacks:
            self.change_callbacks.append(callback)
    
    def unregister_change_callback(self, callback) -> None:
        """
        Tema değişikliği için geri çağrı fonksiyonu kaydını siler
        
        Args:
            callback: Geri çağrı fonksiyonu
        """
        if callback in self.change_callbacks:
            self.change_callbacks.remove(callback)
    
    def _deep_merge_dict(self, base_dict: Dict, update_dict: Dict) -> Dict:
        """
        İki sözlüğü derin birleştirir, iç içe yapıları korur
        
        Args:
            base_dict (Dict): Temel sözlük
            update_dict (Dict): Güncelleme sözlüğü
        
        Returns:
            Dict: Birleştirilmiş sözlük
        """
        # Temel sözlüğün bir kopyasını oluştur
        result = copy.deepcopy(base_dict)
        
        # Güncelleme sözlüğündeki her öğe için
        for key, value in update_dict.items():
            # Eğer iki sözlükte de aynı anahtar var ve her ikisi de sözlük ise
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # İç içe sözlükleri derin birleştir
                result[key] = self._deep_merge_dict(result[key], value)
            else:
                # Değilse üzerine yaz
                result[key] = copy.deepcopy(value)
                
        return result