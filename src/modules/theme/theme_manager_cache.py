#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: theme_manager_cache.py
# Açıklama: Tema yöneticisi için önbellek yönetim işlevleri ve mixin sınıfı
# Bağımlılıklar: logging, os, time, threading
# Bağlı Dosyalar: theme_manager_base.py

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

Bu modül, tema yöneticisi için önbellek yönetim işlevlerini içeren mixin sınıfını tanımlar.
Tema verileri önbellekleme, temizleme ve LRU (Least Recently Used) algoritmasını uygulayan
fonksiyonları sağlar.
"""

import os
import time
import json
import logging
import threading
from typing import Dict, List, Any, Optional

# Logger yapılandırması
logger = logging.getLogger("ThemeManager")

class ThemeCacheMixin:
    """
    Tema önbellek yönetimi için mixin sınıfı.
    Bu sınıf, tema verilerinin önbelleğe alınması ve yönetilmesi için
    gerekli işlevselliği sağlar.
    """
    
    def _load_theme_file(self, theme_name: str) -> Optional[Dict]:
        """
        Tema dosyasını disk üzerinden yükler
        
        Args:
            theme_name (str): Tema adı
        
        Returns:
            Optional[Dict]: Tema verileri veya başarısız olursa None
        """
        theme_file = os.path.join(self.theme_base_dir, theme_name, "theme.json")
        
        if not os.path.exists(theme_file):
            logger.error(f"Tema dosyası bulunamadı: {theme_file}")
            return None
            
        try:
            with open(theme_file, 'r') as f:
                theme_data = json.load(f)
                
            # Temel doğrulamaları yap
            if not theme_data or not isinstance(theme_data, dict):
                logger.error(f"Geçersiz tema verisi: {theme_file}")
                return None
                
            return theme_data
            
        except json.JSONDecodeError as e:
            logger.error(f"Tema dosyası geçersiz JSON formatı: {e}")
            return None
        except Exception as e:
            logger.error(f"Tema dosyası yüklenirken hata: {e}")
            return None
        
    def _save_theme_file(self, theme_name: str, theme_data: Dict) -> bool:
        """
        Tema verilerini dosyaya kaydeder
        
        Args:
            theme_name (str): Tema adı
            theme_data (Dict): Kaydedilecek tema verileri
            
        Returns:
            bool: Başarılı ise True, değilse False
        """
        theme_file = os.path.join(self.theme_base_dir, theme_name, "theme.json")
        
        try:
            with open(theme_file, 'w') as f:
                json.dump(theme_data, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Tema dosyası kaydedilirken hata: {e}")
            return False
    
    def _update_theme_cache(self) -> None:
        """
        Tema önbelleğini günceller
        """
        # Tüm tema dosyalarını yeniden yükle
        themes = self.get_theme_list()
        
        with self.load_lock:
            for theme_name in themes:
                # Tema dizini kontrolü
                theme_dir = os.path.join(self.theme_base_dir, theme_name)
                theme_file = os.path.join(theme_dir, "theme.json")
                
                if os.path.exists(theme_file):
                    try:
                        # Tema dosyasını yükle
                        with open(theme_file, 'r') as f:
                            theme_data = json.load(f)
                            
                        # Önbelleğe al
                        self.theme_cache[theme_name] = theme_data
                    except Exception as e:
                        logger.error(f"Tema dosyası yüklenirken hata: {theme_name} - {e}")
    
    def _update_cache_access(self, theme_name: str) -> None:
        """
        Tema erişim zamanını günceller (LRU için)
        
        Args:
            theme_name (str): Tema adı
        """
        with self.load_lock:
            # Zaman damgasını güncelle
            self.cache_timestamps[theme_name] = time.time()
            
            # LRU listesini güncelle
            if theme_name in self.lru_cache:
                self.lru_cache.remove(theme_name)
            
            # Listeye ekle (en son erişilen)
            self.lru_cache.append(theme_name)
            
            # Önbellek boyutu aşıldıysa, en az kullanılanı kaldır
            if len(self.lru_cache) > self.max_cache_size:
                least_used = self.lru_cache.pop(0)  # En az kullanılan
                
                # Aktif tema değilse sil
                if least_used != self.active_theme and least_used in self.theme_cache:
                    del self.theme_cache[least_used]
                    logger.debug(f"Önbellek boyutu aşımı, tema kaldırıldı: {least_used}")
    
    def _start_cache_cleanup_timer(self) -> None:
        """
        Önbellek temizleme zamanlayıcısını başlatır
        """
        cleanup_thread = threading.Thread(target=self._cache_cleanup_thread, daemon=True)
        cleanup_thread.start()
        logger.debug("Tema önbelleği temizleme zamanlayıcısı başlatıldı")
        
    def _cache_cleanup_thread(self) -> None:
        """
        Önbellek temizleme iş parçacığı
        """
        while True:
            try:
                # Her 60 saniyede bir kontrol et
                time.sleep(60)
                self._cleanup_expired_cache()
            except Exception as e:
                logger.error(f"Önbellek temizleme hatası: {e}")
    
    def _cleanup_expired_cache(self) -> None:
        """
        Süresi dolmuş önbellek öğelerini temizler
        """
        current_time = time.time()
        
        with self.load_lock:
            # Süresi dolmuş önbellek girdilerini belirle
            expired_entries = []
            for theme_name, timestamp in self.cache_timestamps.items():
                if current_time - timestamp > self.cache_timeout:
                    # Aktif tema değilse sil
                    if theme_name != self.active_theme:
                        expired_entries.append(theme_name)
            
            # Süresi dolmuş girdileri sil
            for theme_name in expired_entries:
                if theme_name in self.theme_cache:
                    del self.theme_cache[theme_name]
                if theme_name in self.cache_timestamps:
                    del self.cache_timestamps[theme_name]
                if theme_name in self.lru_cache:
                    self.lru_cache.remove(theme_name)
                
                logger.debug(f"Süresi dolmuş tema önbelleği temizlendi: {theme_name}")
                
    def _deep_merge_dict(self, base_dict: Dict, update_dict: Dict) -> Dict:
        """
        İki sözlüğü derin birleştirir, iç içe yapıları korur
        
        Args:
            base_dict (Dict): Temel sözlük
            update_dict (Dict): Güncelleme sözlüğü
        
        Returns:
            Dict: Birleştirilmiş sözlük
        """
        import copy
        
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

    def _cache_theme_preview(self, theme_name: str, preview_data: Dict[str, Any]) -> None:
        """
        Tema önizleme verilerini önbelleğe alır
        
        Args:
            theme_name (str): Tema adı
            preview_data (Dict[str, Any]): Önizleme verileri
        """
        with self.load_lock:
            self.preview_cache[theme_name] = preview_data
            self.cache_timestamps[f"preview_{theme_name}"] = time.time()

    def _get_cached_theme_preview(self, theme_name: str) -> Dict[str, Any]:
        """
        Önbelleğe alınmış tema önizleme verilerini döndürür
        
        Args:
            theme_name (str): Tema adı
            
        Returns:
            Dict[str, Any]: Önizleme verileri veya boş sözlük
        """
        if theme_name in self.preview_cache:
            # Erişim zamanını güncelle
            self.cache_timestamps[f"preview_{theme_name}"] = time.time()
            return self.preview_cache[theme_name]
            
        return {}
    
    def _cache_subtype_assets(self, emotion: str, subtype: str, assets: Dict[str, Any]) -> None:
        """
        Alt tip varlıklarını önbelleğe alır
        
        Args:
            emotion (str): Duygu durumu
            subtype (str): Alt tip
            assets (Dict[str, Any]): Varlık verileri
        """
        key = f"{emotion}_{subtype}"
        with self.load_lock:
            self.subtype_asset_cache[key] = assets
            self.cache_timestamps[f"subtype_{key}"] = time.time()
    
    def _get_cached_subtype_assets(self, emotion: str, subtype: str) -> Dict[str, Any]:
        """
        Önbelleğe alınmış alt tip varlıklarını döndürür
        
        Args:
            emotion (str): Duygu durumu
            subtype (str): Alt tip
            
        Returns:
            Dict[str, Any]: Varlık verileri veya boş sözlük
        """
        key = f"{emotion}_{subtype}"
        if key in self.subtype_asset_cache:
            # Erişim zamanını güncelle
            self.cache_timestamps[f"subtype_{key}"] = time.time()
            return self.subtype_asset_cache[key]
            
        return {}
    
    def clear_cache(self) -> None:
        """
        Tüm önbellek verilerini temizler
        """
        with self.load_lock:
            # Mevcut tema haricindeki tüm temaları temizle
            current_theme = self.active_theme
            active_theme_data = None
            
            # Aktif tema verisini geçici olarak kaydet
            if current_theme in self.theme_cache:
                active_theme_data = self.theme_cache[current_theme]
                
            # Tüm önbellekleri temizle
            self.theme_cache.clear()
            self.preview_cache.clear()
            self.subtype_asset_cache.clear()
            self.cache_timestamps.clear()
            self.lru_cache = []
            
            # Aktif temayı geri yükle
            if active_theme_data:
                self.theme_cache[current_theme] = active_theme_data
                self.cache_timestamps[current_theme] = time.time()
                self.lru_cache.append(current_theme)
                
            logger.info("Tema önbelleği temizlendi (aktif tema korundu)")