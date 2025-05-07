#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: theme_manager_assets.py
# Açıklama: Tema yöneticisi varlıkları (assets) ile ilgili işlevler
# Bağımlılıklar: logging, os
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

Bu modül, tema varlıklarını (assets) yönetmek için gereken işlevleri içerir.
Tema varlıklarını (göz, ağız resimleri vb.) yönetme ve duygu durumları için
gerekli varlıkları döndürme işlevlerini sağlar.
"""

import os
import shutil
import logging
from typing import Dict, Optional

# Logger yapılandırması
logger = logging.getLogger("ThemeManager")

class ThemeAssetsMixin:
    """
    Tema varlıkları (assets) yönetimi için mixin sınıfı
    
    Tema varlıklarını yönetmek için gereken metotları içerir.
    Göz, ağız resimleri ve LED animasyonları gibi tema varlıklarını yönetir.
    """
    
    def get_emotion_assets(self, emotion: str) -> Dict:
        """
        Belirli bir duygu için tema varlıklarını döndürür
        
        Args:
            emotion (str): Duygu durumu
        
        Returns:
            Dict: Duygu ile ilgili tema varlıkları
        """
        result = {
            "eyes": {},
            "mouth": {},
            "led": {}
        }
        
        # Mevcut tema verilerini al
        theme_data = self.theme_cache.get(self.active_theme)
        if not theme_data:
            theme_data = self.load_theme(self.active_theme)
        
        if not theme_data:
            logger.error("Tema verileri yüklenemedi.")
            return result
        
        # Duygu verilerini topla
        for asset_type in ["eyes", "mouth", "led"]:
            # Duygu durumu için varlıkları al
            if asset_type in theme_data and emotion in theme_data[asset_type]:
                result[asset_type] = theme_data[asset_type][emotion]
            
            # Duygu durumu yoksa, nötr kullan
            elif asset_type in theme_data and "neutral" in theme_data[asset_type]:
                result[asset_type] = theme_data[asset_type]["neutral"]
            
            # Hiçbiri yoksa boş bırak
            else:
                result[asset_type] = {}
        
        return result
    
    def get_emotion_subtype_assets(self, emotion: str, subtype: str = None) -> Dict:
        """
        Duygu alt tipi için tema varlıklarını döndürür
        
        Args:
            emotion (str): Ana duygu durumu
            subtype (str, optional): Duygu alt tipi. Varsayılan None.
        
        Returns:
            Dict: Duygu alt tipi ile ilgili tema varlıkları
        """
        # Önbellekte kontrol et
        cache_key = f"{self.active_theme}_{emotion}_{subtype}"
        if cache_key in self.subtype_asset_cache:
            return self.subtype_asset_cache[cache_key]
        
        result = {
            "eyes": {},
            "mouth": {},
            "led": {},
            "effects": {}
        }
        
        # Mevcut tema verilerini al
        theme_data = self.theme_cache.get(self.active_theme)
        if not theme_data:
            theme_data = self.load_theme(self.active_theme)
        
        if not theme_data:
            logger.error("Tema verileri yüklenemedi.")
            return result
            
        # Ana duygu varlıklarını yükle
        emotion_assets = self.get_emotion_assets(emotion)
        result["eyes"] = emotion_assets["eyes"]
        result["mouth"] = emotion_assets["mouth"] 
        result["led"] = emotion_assets["led"]
        
        # Alt tip yoksa sadece ana duygu varlıklarını döndür
        if subtype is None:
            return result
        
        # Tema verilerinde alt tipler bölümü varsa
        subtypes = theme_data.get("emotion_subtypes", {})
        if not subtypes:
            logger.debug(f"Bu temada ({self.active_theme}) duygu alt tipleri tanımlanmamış.")
            return result
            
        # Belirli duygu için alt tipler
        emotion_subtypes = subtypes.get(emotion, {})
        if not emotion_subtypes:
            logger.debug(f"'{emotion}' duygusu için alt tipler tanımlanmamış.")
            return result
            
        # Belirli alt tip
        specific_subtype = emotion_subtypes.get(subtype, {})
        if not specific_subtype:
            logger.debug(f"'{emotion}' duygusu için '{subtype}' alt tipi tanımlanmamış.")
            return result
            
        # Alt tip özelleştirmelerini birleştir
        for asset_type in ["eyes", "mouth", "led", "effects"]:
            if asset_type in specific_subtype:
                if asset_type in result and isinstance(result[asset_type], dict):
                    # Derin birleştirme yap
                    result[asset_type] = self._deep_merge_dict(
                        result[asset_type], 
                        specific_subtype[asset_type]
                    )
                else:
                    # Doğrudan ata
                    result[asset_type] = specific_subtype[asset_type]
        
        # Önbelleğe al
        self.subtype_asset_cache[cache_key] = result
        
        return result
    
    def get_theme_preview(self, theme_name: str) -> Dict:
        """
        Tema önizleme verileri oluşturur
        
        Args:
            theme_name (str): Tema adı
            
        Returns:
            Dict: Tema önizleme verileri
        """
        # Önbellekte kontrol et
        if theme_name in self.preview_cache:
            return self.preview_cache[theme_name]
        
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
                "description": theme_data.get("description", ""),
                "thumbnail": os.path.join("themes", theme_name, "thumbnail.png"),
                "emotions": {}
            }
            
            # Temel duyguları ekle
            for emotion in ["happy", "sad", "angry", "surprised", "fearful", "disgusted", "calm", "neutral"]:
                if emotion in theme_data.get("emotions", {}):
                    # Duygu resimleri ve önizleme verileri
                    emotion_data = theme_data["emotions"][emotion]
                    
                    # Göz ve ağız resimlerinin yolları
                    left_eye_path = os.path.join("themes", theme_name, "eyes", emotion_data.get("eyes", {}).get("left_eye", ""))
                    right_eye_path = os.path.join("themes", theme_name, "eyes", emotion_data.get("eyes", {}).get("right_eye", ""))
                    mouth_path = os.path.join("themes", theme_name, "mouth", emotion_data.get("mouth", {}).get("shape", ""))
                    
                    # LED Renk bilgisi
                    led_color = emotion_data.get("led", {}).get("color", "#FFFFFF")
                    
                    # Yol bilgilerini kontrol et
                    base_dir = getattr(self, "config", {}).get("base_dir", "")
                    
                    preview_data["emotions"][emotion] = {
                        "left_eye": left_eye_path if os.path.exists(os.path.join(base_dir or "", left_eye_path)) else "",
                        "right_eye": right_eye_path if os.path.exists(os.path.join(base_dir or "", right_eye_path)) else "",
                        "mouth": mouth_path if os.path.exists(os.path.join(base_dir or "", mouth_path)) else "",
                        "led_color": led_color
                    }
                # Temel tema düzeninde ise
                elif "eyes" in theme_data and emotion in theme_data["eyes"] and "mouth" in theme_data and emotion in theme_data["mouth"]:
                    # Göz ve ağız stillerini al
                    eye_style = theme_data["eyes"][emotion].get("style", "cartoon")
                    mouth_style = theme_data["mouth"][emotion].get("style", "smile")
                    
                    # LED Renk bilgisi
                    led_color = theme_data.get("led", {}).get(emotion, {}).get("color", [255, 255, 255])
                    
                    preview_data["emotions"][emotion] = {
                        "eye_style": eye_style,
                        "mouth_style": mouth_style,
                        "led_color": led_color
                    }
            
            # Önbelleğe al
            self.preview_cache[theme_name] = preview_data
            
            return preview_data
        
        except Exception as e:
            logger.error(f"Tema önizleme oluşturulurken hata: {e}")
            return {}
    
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
            
    def _clear_asset_cache(self) -> None:
        """
        Tema varlıkları önbelleğini temizler
        """
        self.subtype_asset_cache.clear()
        self.preview_cache.clear()
        logger.debug("Tema varlıkları önbelleği temizlendi.")