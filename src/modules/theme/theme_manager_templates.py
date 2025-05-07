#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: theme_manager_templates.py
# Açıklama: Tema yöneticisi için tema şablonları ve mixin sınıfı
# Bağımlılıklar: logging, os, json
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

Bu modül, tema yöneticisi için tema şablonları sağlayan mixin sınıfını tanımlar.
Önceden tanımlanmış tema şablonları (varsayılan, minimal, pixel, gerçekçi) oluşturma
işlevlerini içerir.
"""

import os
import json
import logging
from typing import Dict

# Logger yapılandırması
logger = logging.getLogger("ThemeManager")

class ThemeTemplatesMixin:
    """
    Tema şablonları için mixin sınıfı.
    Bu sınıf, önceden tanımlanmış tema şablonları oluşturmak için gerekli işlevselliği sağlar.
    """
    
    def _create_default_theme_file(self, theme_dir: str) -> None:
        """
        Varsayılan tema tanımlama dosyasını oluşturur
        
        Args:
            theme_dir (str): Tema dizini
        """
        default_theme = {
            "name": "Default",
            "description": "Standard cartoon-style expressions",
            "author": "FACE1 Team",
            "version": "1.0",
            "eyes": {
                "happy": {
                    "style": "cartoon",
                    "pupil_size": 0.3,
                    "iris_color": [0, 0, 0],
                    "animation": "blink",
                    "blink_rate": 5.0
                },
                "sad": {
                    "style": "cartoon",
                    "pupil_size": 0.3,
                    "iris_color": [0, 0, 0],
                    "animation": "blink_slow",
                    "blink_rate": 3.0
                },
                "angry": {
                    "style": "cartoon",
                    "pupil_size": 0.25,
                    "iris_color": [0, 0, 0],
                    "animation": "squint",
                    "blink_rate": 8.0
                },
                "surprised": {
                    "style": "cartoon",
                    "pupil_size": 0.5,
                    "iris_color": [0, 0, 0],
                    "animation": "wide",
                    "blink_rate": 2.0
                },
                "neutral": {
                    "style": "cartoon",
                    "pupil_size": 0.35,
                    "iris_color": [0, 0, 0],
                    "animation": "blink",
                    "blink_rate": 5.0
                },
                "calm": {
                    "style": "cartoon",
                    "pupil_size": 0.4,
                    "iris_color": [0, 0, 0],
                    "animation": "blink_slow",
                    "blink_rate": 4.0
                },
                "fearful": {
                    "style": "cartoon",
                    "pupil_size": 0.5,
                    "iris_color": [0, 0, 0],
                    "animation": "look_around",
                    "blink_rate": 8.0
                },
                "disgusted": {
                    "style": "cartoon",
                    "pupil_size": 0.3,
                    "iris_color": [0, 0, 0],
                    "animation": "squint",
                    "blink_rate": 6.0
                }
            },
            "mouth": {
                "happy": {
                    "style": "smile",
                    "width": 0.7,
                    "height": 0.4
                },
                "sad": {
                    "style": "frown",
                    "width": 0.6,
                    "height": 0.3
                },
                "angry": {
                    "style": "flat",
                    "width": 0.5,
                    "height": 0.1
                },
                "surprised": {
                    "style": "o",
                    "width": 0.5,
                    "height": 0.5
                },
                "neutral": {
                    "style": "slight_smile",
                    "width": 0.6,
                    "height": 0.2
                },
                "calm": {
                    "style": "slight_smile",
                    "width": 0.7,
                    "height": 0.2
                },
                "fearful": {
                    "style": "o_small",
                    "width": 0.4,
                    "height": 0.3
                },
                "disgusted": {
                    "style": "grimace",
                    "width": 0.6,
                    "height": 0.25
                }
            },
            "led": {
                "happy": {
                    "color": [255, 255, 0],  # Sarı
                    "pattern": "pulse",
                    "speed": 50
                },
                "sad": {
                    "color": [0, 0, 255],  # Mavi
                    "pattern": "breathe",
                    "speed": 80
                },
                "angry": {
                    "color": [255, 0, 0],  # Kırmızı
                    "pattern": "wipe",
                    "speed": 30
                },
                "surprised": {
                    "color": [255, 0, 255],  # Mor
                    "pattern": "sparkle",
                    "speed": 40
                },
                "neutral": {
                    "color": [255, 255, 255],  # Beyaz
                    "pattern": "static",
                    "speed": 0
                },
                "calm": {
                    "color": [0, 255, 255],  # Cyan
                    "pattern": "breathe",
                    "speed": 100
                },
                "fearful": {
                    "color": [128, 0, 128],  # Koyu mor
                    "pattern": "pulse",
                    "speed": 30
                },
                "disgusted": {
                    "color": [0, 128, 0],  # Koyu yeşil
                    "pattern": "wipe",
                    "speed": 60
                }
            }
        }
        
        # JSON dosyasına kaydet
        theme_file = os.path.join(theme_dir, "theme.json")
        with open(theme_file, 'w') as f:
            json.dump(default_theme, f, indent=2)
        
        logger.info(f"Varsayılan tema dosyası oluşturuldu: {theme_file}")
    
    def _create_minimal_theme_file(self, theme_dir: str) -> None:
        """
        Minimal tema tanımlama dosyasını oluşturur
        
        Args:
            theme_dir (str): Tema dizini
        """
        minimal_theme = {
            "name": "Minimal",
            "description": "Simplified line-art style expressions",
            "author": "FACE1 Team",
            "version": "1.0",
            "eyes": {
                "happy": {
                    "style": "minimal",
                    "pupil_size": 0.2,
                    "iris_color": [0, 0, 0],
                    "animation": "blink",
                    "blink_rate": 5.0
                },
                "sad": {
                    "style": "minimal",
                    "pupil_size": 0.2,
                    "iris_color": [0, 0, 0],
                    "animation": "blink_slow",
                    "blink_rate": 3.0
                },
                "angry": {
                    "style": "minimal",
                    "pupil_size": 0.15,
                    "iris_color": [0, 0, 0],
                    "animation": "squint",
                    "blink_rate": 8.0
                },
                "surprised": {
                    "style": "minimal",
                    "pupil_size": 0.3,
                    "iris_color": [0, 0, 0],
                    "animation": "wide",
                    "blink_rate": 2.0
                },
                "neutral": {
                    "style": "minimal",
                    "pupil_size": 0.25,
                    "iris_color": [0, 0, 0],
                    "animation": "blink",
                    "blink_rate": 5.0
                },
                "calm": {
                    "style": "minimal",
                    "pupil_size": 0.3,
                    "iris_color": [0, 0, 0],
                    "animation": "blink_slow",
                    "blink_rate": 4.0
                },
                "fearful": {
                    "style": "minimal",
                    "pupil_size": 0.35,
                    "iris_color": [0, 0, 0],
                    "animation": "look_around",
                    "blink_rate": 8.0
                },
                "disgusted": {
                    "style": "minimal",
                    "pupil_size": 0.2,
                    "iris_color": [0, 0, 0],
                    "animation": "squint",
                    "blink_rate": 6.0
                }
            },
            "mouth": {
                "happy": {
                    "style": "line_smile",
                    "width": 0.6,
                    "height": 0.2
                },
                "sad": {
                    "style": "line_frown",
                    "width": 0.5,
                    "height": 0.2
                },
                "angry": {
                    "style": "line_flat",
                    "width": 0.5,
                    "height": 0.0
                },
                "surprised": {
                    "style": "line_o",
                    "width": 0.4,
                    "height": 0.4
                },
                "neutral": {
                    "style": "line",
                    "width": 0.5,
                    "height": 0.1
                },
                "calm": {
                    "style": "line_smile",
                    "width": 0.6,
                    "height": 0.1
                },
                "fearful": {
                    "style": "line_o_small",
                    "width": 0.3,
                    "height": 0.3
                },
                "disgusted": {
                    "style": "line_grimace",
                    "width": 0.5,
                    "height": 0.15
                }
            },
            "led": {
                "happy": {
                    "color": [255, 255, 0],  # Sarı
                    "pattern": "static",
                    "speed": 0
                },
                "sad": {
                    "color": [0, 0, 255],  # Mavi
                    "pattern": "static",
                    "speed": 0
                },
                "angry": {
                    "color": [255, 0, 0],  # Kırmızı
                    "pattern": "static",
                    "speed": 0
                },
                "surprised": {
                    "color": [255, 0, 255],  # Mor
                    "pattern": "static",
                    "speed": 0
                },
                "neutral": {
                    "color": [255, 255, 255],  # Beyaz
                    "pattern": "static",
                    "speed": 0
                },
                "calm": {
                    "color": [0, 255, 255],  # Cyan
                    "pattern": "static",
                    "speed": 0
                },
                "fearful": {
                    "color": [128, 0, 128],  # Koyu mor
                    "pattern": "static",
                    "speed": 0
                },
                "disgusted": {
                    "color": [0, 128, 0],  # Koyu yeşil
                    "pattern": "static",
                    "speed": 0
                }
            }
        }
        
        # JSON dosyasına kaydet
        theme_file = os.path.join(theme_dir, "theme.json")
        with open(theme_file, 'w') as f:
            json.dump(minimal_theme, f, indent=2)
        
        logger.info(f"Minimal tema dosyası oluşturuldu: {theme_file}")
    
    def _create_pixel_theme_file(self, theme_dir: str) -> None:
        """
        Pixel tema dosyası oluşturur
        
        Args:
            theme_dir (str): Tema dizini yolu
        """
        theme_file = os.path.join(theme_dir, "theme.json")
        
        # Pixel tema şablonu
        theme_data = {
            "name": "Pixel",
            "theme_name": "pixel",
            "theme_type": "pixel",
            "display_name": "Pixel",
            "version": "1.0.0",
            "author": "FACE1 Project",
            "default_emotion": "neutral",
            "eyes": {
                "style": "pixel",
                "resolution": "low",
                "blink_speed": 0.2
            },
            "mouth": {
                "style": "pixel",
                "resolution": "low",
                "animation_speed": 0.3
            },
            "led": {
                "brightness": 0.8,
                "color_harmony": "analogous",
                "animation_speed": 0.5,
                "color_multiplier": 1.0
            },
            "emotions": {
                "happy": {
                    "eyes": {
                        "shape": "pixel_happy",
                        "style": "8bit"
                    },
                    "mouth": {
                        "shape": "pixel_smile",
                        "style": "8bit"
                    },
                    "led": {
                        "color": [255, 255, 0],
                        "pattern": "pulse"
                    }
                },
                "sad": {
                    "eyes": {
                        "shape": "pixel_sad",
                        "style": "8bit"
                    },
                    "mouth": {
                        "shape": "pixel_frown",
                        "style": "8bit"
                    },
                    "led": {
                        "color": [0, 0, 255],
                        "pattern": "fade"
                    }
                },
                "angry": {
                    "eyes": {
                        "shape": "pixel_angry",
                        "style": "8bit"
                    },
                    "mouth": {
                        "shape": "pixel_grimace",
                        "style": "8bit"
                    },
                    "led": {
                        "color": [255, 0, 0],
                        "pattern": "scan"
                    }
                },
                "surprised": {
                    "eyes": {
                        "shape": "pixel_wide",
                        "style": "8bit"
                    },
                    "mouth": {
                        "shape": "pixel_o_shape",
                        "style": "8bit"
                    },
                    "led": {
                        "color": [255, 0, 255],
                        "pattern": "sparkle"
                    }
                },
                "disgusted": {
                    "eyes": {
                        "shape": "pixel_disgusted",
                        "style": "8bit"
                    },
                    "mouth": {
                        "shape": "pixel_grimace",
                        "style": "8bit"
                    },
                    "led": {
                        "color": [0, 128, 0],
                        "pattern": "wave"
                    }
                },
                "fearful": {
                    "eyes": {
                        "shape": "pixel_wide",
                        "style": "8bit"
                    },
                    "mouth": {
                        "shape": "pixel_small_o",
                        "style": "8bit"
                    },
                    "led": {
                        "color": [128, 0, 128],
                        "pattern": "chase"
                    }
                },
                "neutral": {
                    "eyes": {
                        "shape": "pixel_neutral",
                        "style": "8bit"
                    },
                    "mouth": {
                        "shape": "pixel_straight",
                        "style": "8bit"
                    },
                    "led": {
                        "color": [255, 255, 255],
                        "pattern": "static"
                    }
                },
                "calm": {
                    "eyes": {
                        "shape": "pixel_calm",
                        "style": "8bit"
                    },
                    "mouth": {
                        "shape": "pixel_small_smile",
                        "style": "8bit"
                    },
                    "led": {
                        "color": [0, 255, 255],
                        "pattern": "breathe"
                    }
                }
            }
        }
        
        # Temayı JSON dosyasına kaydet
        with open(theme_file, 'w') as f:
            json.dump(theme_data, f, indent=4)
            
        logger.info(f"Pixel tema dosyası oluşturuldu: {theme_file}")
    
    def _create_realistic_theme_file(self, theme_dir: str) -> None:
        """
        Gerçekçi tema dosyasını oluşturur
        
        Args:
            theme_dir (str): Tema dizini
        """
        theme_data = {
            "theme_name": "realistic",
            "display_name": "Gerçekçi Stil",
            "description": "İnsan gözüne benzeyen gerçekçi robot yüzü",
            "version": "0.1.0",
            "author": "FACE1 Team",
            "default_emotion": "neutral",
            "style": "realistic",
            "eyes": {
                "happy": {
                    "style": "realistic_human",
                    "pupil_size": 8,
                    "iris_color": [100, 150, 220],
                    "sclera_color": [240, 240, 240],
                    "reflection": True,
                    "animation_speed": 1.0,
                    "blink_frequency": 0.9
                },
                "sad": {
                    "style": "realistic_human",
                    "pupil_size": 10,
                    "iris_color": [80, 100, 180],
                    "sclera_color": [230, 230, 240],
                    "reflection": True,
                    "animation_speed": 0.6,
                    "blink_frequency": 0.6
                },
                "angry": {
                    "style": "realistic_human",
                    "pupil_size": 12,
                    "iris_color": [150, 60, 50],
                    "sclera_color": [240, 220, 220],
                    "reflection": True,
                    "animation_speed": 1.4,
                    "blink_frequency": 0.4
                },
                "surprised": {
                    "style": "realistic_human",
                    "pupil_size": 14,
                    "iris_color": [100, 180, 200],
                    "sclera_color": [250, 250, 250],
                    "reflection": True,
                    "animation_speed": 1.5,
                    "blink_frequency": 0.3
                },
                "calm": {
                    "style": "realistic_human",
                    "pupil_size": 9,
                    "iris_color": [90, 130, 180],
                    "sclera_color": [245, 245, 245],
                    "reflection": True,
                    "animation_speed": 0.7,
                    "blink_frequency": 1.2
                },
                "default": {
                    "style": "realistic_human",
                    "pupil_size": 10,
                    "iris_color": [100, 140, 200],
                    "sclera_color": [245, 245, 245],
                    "reflection": True,
                    "animation_speed": 1.0,
                    "blink_frequency": 0.8
                }
            },
            "mouth": {
                "happy": {
                    "style": "realistic_smile",
                    "size": 1.0,
                    "teeth_visible": True,
                    "lip_color": [220, 150, 150],
                    "animation_speed": 1.0
                },
                "sad": {
                    "style": "realistic_frown",
                    "size": 0.9,
                    "teeth_visible": False,
                    "lip_color": [200, 140, 140],
                    "animation_speed": 0.6
                },
                "angry": {
                    "style": "realistic_grimace",
                    "size": 0.9,
                    "teeth_visible": True,
                    "lip_color": [210, 120, 120],
                    "animation_speed": 1.3
                },
                "surprised": {
                    "style": "realistic_o",
                    "size": 1.1,
                    "teeth_visible": True,
                    "lip_color": [220, 160, 160],
                    "animation_speed": 1.2
                },
                "calm": {
                    "style": "realistic_soft_smile",
                    "size": 0.9,
                    "teeth_visible": False,
                    "lip_color": [210, 150, 150],
                    "animation_speed": 0.7
                },
                "default": {
                    "style": "realistic_neutral",
                    "size": 0.9,
                    "teeth_visible": False,
                    "lip_color": [210, 150, 150],
                    "animation_speed": 0.9
                }
            },
            "led": {
                "color_harmony": "analogous",
                "brightness": 0.7,
                "pattern": "pulse",
                "animation_speed": 50
            }
        }
        
        # JSON dosyasını oluştur
        theme_file = os.path.join(theme_dir, "theme.json")
        with open(theme_file, "w") as f:
            json.dump(theme_data, f, indent=4)
            
        logger.info(f"Gerçekçi tema dosyası oluşturuldu: {theme_file}")