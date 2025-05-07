#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: theme_manager.py
# Açıklama: Tema yöneticisi modülü. Farklı yüz temalarını yönetir.
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
"""

import os
import sys
import logging
from pathlib import Path

# Proje dizinini ve include dizinini Python yoluna ekle
PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(str(PROJECT_DIR))

# Tema yöneticisi bileşenleri
from .theme.theme_manager_base import BaseThemeManager
from .theme.theme_manager_templates import ThemeTemplatesMixin
from .theme.theme_manager_operations import ThemeOperationsMixin
from .theme.theme_manager_assets import ThemeAssetsMixin
from .theme.theme_manager_cache import ThemeCacheMixin

# Logger yapılandırması
logger = logging.getLogger("ThemeManager")


class ThemeManager(BaseThemeManager, ThemeTemplatesMixin, 
                  ThemeOperationsMixin, ThemeAssetsMixin,
                  ThemeCacheMixin):
    """
    Tema yöneticisi kompozit sınıfı
    
    Bu sınıf, robot yüzü için farklı görsel temaları yönetir.
    Temalar, göz ve ağız tasarımları için farklı görünümler sağlar.
    
    Bu sınıf çeşitli mixin'leri (ThemeTemplatesMixin, ThemeOperationsMixin, vb.)
    kullanarak modüler bir yapı oluşturur. Her mixin, belirli bir işlevsellik
    alanını yönetir.
    """
    
    # Tema stilleri
    THEME_STYLES = ["cartoon", "minimal", "pixel", "realistic"]


# Test kodu
if __name__ == "__main__":
    # Logging yapılandırması
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Varsayılan yapılandırma
    test_config = {
        "theme": {
            "default_theme": "default"
        }
    }
    
    print("Tema Yöneticisi Test")
    print("-------------------")
    
    # Tema yöneticisi örneği oluştur
    theme_manager = ThemeManager(test_config)
    
    if theme_manager.start():
        print("Tema yöneticisi başlatıldı")
        
        # Tema listesini görüntüle
        themes = theme_manager.get_theme_list()
        print(f"Mevcut temalar: {themes}")
        
        # Mevcut temayı görüntüle
        current = theme_manager.get_current_theme()
        print(f"Mevcut tema: {current}")
        
        # Bir temayı yükle ve duygu varlıklarını al
        for theme_name in themes:
            theme_data = theme_manager.load_theme(theme_name)
            if theme_data:
                print(f"\nTema: {theme_data.get('name')} ({theme_name})")
                print(f"Açıklama: {theme_data.get('description', 'Açıklama yok')}")
                
                # Happy duygusu için varlıkları görüntüle
                if theme_manager.set_theme(theme_name):
                    happy_assets = theme_manager.get_emotion_assets("happy")
                    print("Mutlu duygusu varlıkları:")
                    print(f"  Göz stili: {happy_assets['eyes'].get('style', 'yok')}")
                    print(f"  Ağız stili: {happy_assets['mouth'].get('style', 'yok')}")
                    print(f"  LED rengi: {happy_assets['led'].get('color', 'yok')}")
        
        # Temayı varsayılana geri al
        theme_manager.set_theme("default")
        
        # Tema yöneticisini durdur
        theme_manager.stop()
        print("\nTema yöneticisi durduruldu.")
    else:
        print("Tema yöneticisi başlatılamadı!")
    
    print("\nTest tamamlandı.")