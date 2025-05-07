#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: theme_manager_operations.py
# Açıklama: Tema yöneticisi için tema işlemleri ve mixin sınıfı
# Bağımlılıklar: logging, os, shutil, re, json
# Bağlı Dosyalar: theme_manager_base.py, theme_manager_cache.py

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

Bu modül, tema yöneticisi için tema işlemlerini (oluşturma, düzenleme, silme, kopyalama)
içeren mixin sınıfını tanımlar. Tema dosyaları ve varlıkları üzerinde çeşitli işlemler
gerçekleştiren yöntemleri sağlar.
"""

import os
import re
import json
import shutil
import logging
import copy
from typing import Dict, List, Optional, Any

# Logger yapılandırması
logger = logging.getLogger("ThemeManager")

class ThemeOperationsMixin:
    """
    Tema işlemleri için mixin sınıfı.
    Bu sınıf, tema oluşturma, düzenleme, silme ve kopyalama gibi işlemleri gerçekleştirmek
    için gerekli işlevselliği sağlar.
    """
    
    def create_theme(self, theme_name: str, theme_data: Dict) -> bool:
        """
        Yeni bir tema oluşturur
        
        Args:
            theme_name (str): Tema adı
            theme_data (Dict): Tema verileri
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        # Özel karakterler ve boşlukları temizle
        theme_name = theme_name.strip().lower().replace(" ", "_")
        if not theme_name:
            logger.error("Geçersiz tema adı.")
            return False
        
        # Tema adı geçerliliğini kontrol et
        if not self._is_valid_theme_name(theme_name):
            logger.error(f"Geçersiz tema adı: {theme_name}")
            return False
        
        # Tema dizini oluştur
        theme_dir = os.path.join(self.theme_base_dir, theme_name)
        if os.path.exists(theme_dir):
            logger.error(f"Bu isimde bir tema zaten var: {theme_name}")
            return False
        
        try:
            # Dizinleri oluştur
            os.makedirs(theme_dir, exist_ok=True)
            os.makedirs(os.path.join(theme_dir, "eyes"), exist_ok=True)
            os.makedirs(os.path.join(theme_dir, "mouth"), exist_ok=True)
            
            # Tema verisini kontrol et
            required_fields = ["name", "description", "eyes", "mouth", "led"]
            for field in required_fields:
                if field not in theme_data:
                    logger.error(f"Tema verileri eksik alan içeriyor: {field}")
                    return False
            
            # JSON dosyasına kaydet
            theme_file = os.path.join(theme_dir, "theme.json")
            with open(theme_file, 'w') as f:
                json.dump(theme_data, f, indent=2)
            
            # Önbelleği güncelle
            self.theme_cache[theme_name] = theme_data
            
            logger.info(f"Yeni tema oluşturuldu: {theme_name}")
            return True
            
        except Exception as e:
            logger.error(f"Tema oluşturulurken hata: {e}")
            # Hata durumunda temizlik
            if os.path.exists(theme_dir):
                shutil.rmtree(theme_dir, ignore_errors=True)
            return False
    
    def delete_theme(self, theme_name: str) -> bool:
        """
        Bir temayı siler
        
        Args:
            theme_name (str): Tema adı
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        # Varsayılan temaları koruma
        protected_themes = ["default", "minimal", "pixel", "realistic"]
        if theme_name in protected_themes:
            logger.error(f"Varsayılan tema silinemez: {theme_name}")
            return False
        
        # Mevcut temayı silmeye çalışıyorsa kontrol et
        if theme_name == self.active_theme:
            logger.error(f"Mevcut tema silinemez. Önce başka bir temaya geçiş yapın: {theme_name}")
            return False
        
        theme_dir = os.path.join(self.theme_base_dir, theme_name)
        if not os.path.exists(theme_dir) or not os.path.isdir(theme_dir):
            logger.error(f"Tema bulunamadı: {theme_name}")
            return False
        
        try:
            # Tema dizinini sil
            shutil.rmtree(theme_dir)
            
            # Önbellekten kaldır
            if theme_name in self.theme_cache:
                del self.theme_cache[theme_name]
            
            # Önizleme önbelleğinden kaldır
            if theme_name in self.preview_cache:
                del self.preview_cache[theme_name]
                
            # LRU listesinden kaldır
            if theme_name in self.lru_cache:
                self.lru_cache.remove(theme_name)
            
            # Zaman damgalarını temizle
            if theme_name in self.cache_timestamps:
                del self.cache_timestamps[theme_name]
            
            logger.info(f"Tema silindi: {theme_name}")
            return True
            
        except Exception as e:
            logger.error(f"Tema silinirken hata: {e}")
            return False
    
    def copy_theme(self, source_theme: str, target_theme: str) -> bool:
        """
        Bir temayı başka bir isimle kopyalar
        
        Args:
            source_theme (str): Kaynak tema adı
            target_theme (str): Hedef tema adı
            
        Returns:
            bool: İşlem başarılı ise True, değilse False
        """
        # Kaynak temanın varlığını kontrol et
        if source_theme not in self.get_theme_list():
            logger.error(f"Kaynak tema bulunamadı: {source_theme}")
            return False
        
        # Hedef temanın zaten var olup olmadığını kontrol et
        if target_theme in self.get_theme_list():
            logger.error(f"Hedef tema zaten var: {target_theme}")
            return False
        
        # Tema adının geçerli olup olmadığını kontrol et
        if not self._is_valid_theme_name(target_theme):
            logger.error(f"Geçersiz tema adı: {target_theme}")
            return False
            
        try:
            # Kaynak tema verilerini yükle
            source_data = self._load_theme_file(source_theme)
            if not source_data:
                logger.error(f"Kaynak tema verileri yüklenemedi: {source_theme}")
                return False
                
            # Hedef tema verilerini oluştur (derin kopya)
            target_data = copy.deepcopy(source_data)
            
            # Tema adını ve açıklamasını güncelle
            target_data["name"] = target_theme
            target_data["description"] = f"{target_data.get('description', 'Tema')} (Kopya)"
            
            # Kaynak tema dizini
            source_dir = os.path.join(self.theme_base_dir, source_theme)
            
            # Hedef tema dizini oluştur
            target_dir = os.path.join(self.theme_base_dir, target_theme)
            os.makedirs(target_dir, exist_ok=True)
            
            # Alt dizinleri oluştur
            os.makedirs(os.path.join(target_dir, "eyes"), exist_ok=True)
            os.makedirs(os.path.join(target_dir, "mouth"), exist_ok=True)
            
            # Tema dosyasını kaydet
            theme_file = os.path.join(target_dir, "theme.json")
            with open(theme_file, 'w') as f:
                json.dump(target_data, f, indent=2)
                
            # Resim dosyalarını kopyala
            self._copy_theme_assets(source_dir, target_dir)
            
            # Önbelleğe al
            self.theme_cache[target_theme] = target_data
            
            logger.info(f"Tema kopyalandı: {source_theme} -> {target_theme}")
            return True
            
        except Exception as e:
            logger.error(f"Tema kopyalanırken hata: {e}")
            # Hata durumunda oluşturulmuş dizinleri temizle
            target_dir = os.path.join(self.theme_base_dir, target_theme)
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir, ignore_errors=True)
            return False
            
    def _copy_theme_assets(self, source_dir: str, target_dir: str) -> None:
        """
        Tema varlıklarını bir dizinden diğerine kopyalar
        
        Args:
            source_dir (str): Kaynak dizin
            target_dir (str): Hedef dizin
        """
        try:
            # Gözler dizini
            source_eyes = os.path.join(source_dir, "eyes")
            target_eyes = os.path.join(target_dir, "eyes")
            
            # Ağız dizini
            source_mouth = os.path.join(source_dir, "mouth")
            target_mouth = os.path.join(target_dir, "mouth")
            
            # Göz resimlerini kopyala
            if os.path.exists(source_eyes):
                for file_name in os.listdir(source_eyes):
                    if file_name.endswith((".png", ".jpg", ".jpeg", ".gif")):
                        shutil.copy2(
                            os.path.join(source_eyes, file_name),
                            os.path.join(target_eyes, file_name)
                        )
            
            # Ağız resimlerini kopyala
            if os.path.exists(source_mouth):
                for file_name in os.listdir(source_mouth):
                    if file_name.endswith((".png", ".jpg", ".jpeg", ".gif")):
                        shutil.copy2(
                            os.path.join(source_mouth, file_name),
                            os.path.join(target_mouth, file_name)
                        )
            
            # Thumbnail ve diğer dosyaları kopyala
            for file_name in os.listdir(source_dir):
                if file_name.endswith((".png", ".jpg", ".jpeg", ".gif")) and os.path.isfile(os.path.join(source_dir, file_name)):
                    shutil.copy2(
                        os.path.join(source_dir, file_name),
                        os.path.join(target_dir, file_name)
                    )
                        
        except Exception as e:
            logger.error(f"Tema varlıkları kopyalanırken hata: {e}")
            
    def _is_valid_theme_name(self, theme_name: str) -> bool:
        """
        Tema adının geçerli olup olmadığını kontrol eder
        
        Args:
            theme_name (str): Kontrol edilecek tema adı
            
        Returns:
            bool: Geçerli ise True, değilse False
        """
        # Tema adı en az 3 karakter olmalı
        if len(theme_name) < 3:
            return False
            
        # Sadece harfler, rakamlar, tire ve alt çizgi içermeli
        if not re.match(r'^[a-zA-Z0-9_-]+$', theme_name):
            return False
            
        # Rezerve edilmiş isimler
        reserved_names = ["themes", "assets", "temp", "tmp", "cache", "system"]
        if theme_name.lower() in reserved_names:
            return False
            
        return True
    
    def edit_theme(self, theme_name: str, theme_data: Dict) -> bool:
        """
        Mevcut bir temayı düzenler
        
        Args:
            theme_name (str): Tema adı
            theme_data (Dict): Yeni tema verileri
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        # Temanın varlığını kontrol et
        if theme_name not in self.get_theme_list():
            logger.error(f"Tema bulunamadı: {theme_name}")
            return False
        
        # Varsayılan temaları koruma
        protected_themes = ["default", "minimal", "pixel", "realistic"]
        if theme_name in protected_themes and not self.config.get("allow_default_theme_edit", False):
            logger.error(f"Varsayılan tema düzenlenemez: {theme_name}")
            return False
            
        try:
            # Mevcut tema verilerini yükle
            current_data = self.load_theme(theme_name)
            if not current_data:
                logger.error(f"Mevcut tema verileri yüklenemedi: {theme_name}")
                return False
                
            # Tema adını değiştirilmesini engelle
            if "name" in theme_data and theme_data["name"] != current_data.get("name"):
                logger.warning(f"Tema adı değiştirilemez. Bunun için copy_theme() kullanın.")
                theme_data["name"] = current_data.get("name")
            
            # Tema verilerini güncelle (derin birleştirme)
            updated_data = self._deep_merge_dict(current_data, theme_data)
            
            # JSON dosyasına kaydet
            theme_dir = os.path.join(self.theme_base_dir, theme_name)
            theme_file = os.path.join(theme_dir, "theme.json")
            
            with open(theme_file, 'w') as f:
                json.dump(updated_data, f, indent=2)
            
            # Önbelleği güncelle
            self.theme_cache[theme_name] = updated_data
            
            # Bu temayı kullananlar için değişikliği bildir
            if theme_name == self.active_theme:
                # Geri çağırma fonksiyonlarını tetikle
                for callback in self.change_callbacks:
                    try:
                        callback({
                            "theme_updated": theme_name,
                            "theme_data": updated_data
                        })
                    except Exception as e:
                        logger.error(f"Tema güncelleme geri çağrıma hatası: {e}")
            
            logger.info(f"Tema güncellendi: {theme_name}")
            return True
            
        except Exception as e:
            logger.error(f"Tema düzenlenirken hata: {e}")
            return False
    
    def get_theme_details(self, theme_name: str) -> Optional[Dict]:
        """
        Bir tema hakkında detaylı bilgi döndürür
        
        Args:
            theme_name (str): Tema adı
        
        Returns:
            Optional[Dict]: Tema detayları veya başarısız olursa None
        """
        theme_data = self.load_theme(theme_name)
        if not theme_data:
            return None
        
        # Dosya bilgilerini ekle
        theme_dir = os.path.join(self.theme_base_dir, theme_name)
        theme_file = os.path.join(theme_dir, "theme.json")
        
        try:
            file_time = os.path.getmtime(theme_file)
            file_size = os.path.getsize(theme_file)
            
            # Dosya bilgilerini ekle
            theme_data["_file_info"] = {
                "modified": file_time,
                "size": file_size,
                "path": theme_file
            }
            
            return theme_data
        except Exception as e:
            logger.error(f"Tema detayları alınırken hata: {e}")
            return theme_data  # En azından tema verisini döndür
    
    def get_theme_preview(self, theme_name: str) -> Dict:
        """
        Tema önizleme verileri oluşturur
        
        Args:
            theme_name (str): Tema adı
            
        Returns:
            Dict: Tema önizleme verileri
        """
        # Önbellekten kontrol et
        cached_preview = self._get_cached_theme_preview(theme_name)
        if cached_preview:
            return cached_preview
        
        if theme_name not in self.get_theme_list():
            logger.error(f"Tema bulunamadı: {theme_name}")
            return {}
        
        try:
            theme_data = self.load_theme(theme_name)
            if not theme_data:
                logger.error(f"Tema verileri yüklenemedi: {theme_name}")
                return {}
                
            preview_data = {
                "name": theme_name,
                "display_name": theme_data.get("display_name", theme_data.get("name", theme_name)),
                "description": theme_data.get("description", ""),
                "thumbnail": os.path.join("themes", theme_name, "thumbnail.png"),
                "emotions": {}
            }
            
            # Tema yapısına göre duygu verilerini ek
            emotions_data = {}
            
            # Eski format kontrolü
            if "emotions" in theme_data:
                # Yeni format
                emotions_data = theme_data["emotions"]
                
                # Temel duyguları ekle
                for emotion, data in emotions_data.items():
                    preview_data["emotions"][emotion] = {
                        "eyes": data.get("eyes", {}),
                        "mouth": data.get("mouth", {}),
                        "led": data.get("led", {})
                    }
            else:
                # Eski format - her duygu tipi ayrı sözlükte
                for emotion_type in ["happy", "sad", "angry", "surprised", "neutral", "calm", "fearful", "disgusted"]:
                    # Göz ve ağız verilerini al
                    eyes_data = theme_data.get("eyes", {}).get(emotion_type, {})
                    mouth_data = theme_data.get("mouth", {}).get(emotion_type, {})
                    led_data = theme_data.get("led", {}).get(emotion_type, {})
                    
                    preview_data["emotions"][emotion_type] = {
                        "eyes": eyes_data,
                        "mouth": mouth_data,
                        "led": led_data
                    }
            
            # Önbelleğe al
            self._cache_theme_preview(theme_name, preview_data)
            
            return preview_data
            
        except Exception as e:
            logger.error(f"Tema önizleme oluşturulurken hata: {e}")
            return {}