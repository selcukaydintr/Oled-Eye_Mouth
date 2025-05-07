#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: emotion_engine_base.py
# Açıklama: Duygu motoru temel sınıfı ve yaşam döngüsü işlevlerini içerir.
# Bağımlılıklar: logging, threading, time
# Bağlı Dosyalar: emotion_states.py, emotion_engine.py

# Versiyon: 0.4.0
# Değişiklikler:
# - [0.4.0] emotion_engine.py dosyasından bölündü (modüler mimari)
# - [0.3.0] Duygu geçişlerini daha akıcı hale getirme ve alt tipler için gelişmiş destekler eklendi
# - [0.2.0] Duygu hafıza sistemi ve duygu tepki eğrileri geliştirildi
# - [0.1.0] Temel duygu motoru sınıfı oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-02
===========================================================
"""

import os
import sys
import time
import logging
import threading
from typing import Dict, List, Tuple, Optional, Union, Callable
from pathlib import Path

# Projemizin kök dizinini ekleyelim
PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(str(PROJECT_DIR))

# Duygu durumlarını içe aktaralım
from src.modules.emotion_states import EmotionState

# Logger yapılandırması
logger = logging.getLogger("EmotionEngine")


class EmotionEngineBase:
    """
    Duygu motoru temel sınıfı
    
    Bu sınıf, duygu motorunun temel yapısını ve yaşam döngüsü işlevlerini içerir.
    """
    
    def __init__(self, config: Dict):
        """
        Duygu motoru temel sınıfını başlatır
        
        Args:
            config (Dict): Yapılandırma ayarları
        """
        logger.info("Duygu Motoru başlatılıyor...")
        self.config = config
        
        # Duygu yapılandırması
        self.emotion_config = config.get("emotions", {})
        self.default_emotion = self.emotion_config.get("default_emotion", EmotionState.NEUTRAL.value)
        self.transition_speed = self.emotion_config.get("transition_speed", 0.5)  # 0.0-1.0
        
        # Mevcut duygu ve ilgili değişkenler
        self.current_emotion = {
            "state": self.default_emotion,    # Duygu durumu
            "intensity": 0.5,                 # 0.0-1.0 arası duygu yoğunluğu
            "start_time": time.time(),        # Duygunun başlama zamanı
            "target": {                       # Hedef duygu (geçiş sırasında)
                "state": self.default_emotion,
                "intensity": 0.5,
                "progress": 1.0               # Geçiş tamamlanma yüzdesi (0.0-1.0)
            }
        }
        
        # Olaylar ve geri çağrılar
        self.event_callbacks = {}
        
        # Döngü değişkenleri
        self.is_running = False
        self.update_thread = None
        self.update_interval = 0.1  # Saniye
        
    def start(self) -> bool:
        """
        Duygu motorunu başlatır
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        if self.is_running:
            logger.warning("Duygu motoru zaten çalışıyor.")
            return True
        
        try:
            # Durumu başlatılıyor olarak işaretle
            self.is_running = True
            
            # Güncelleme döngüsünü ayrı bir iş parçacığında başlat
            self.update_thread = threading.Thread(target=self._update_loop)
            self.update_thread.daemon = True
            self.update_thread.start()
            
            logger.info("Duygu motoru başlatıldı.")
            return True
            
        except Exception as e:
            logger.error(f"Duygu motoru başlatılırken hata: {e}")
            self.is_running = False
            return False
    
    def stop(self) -> None:
        """
        Duygu motorunu durdurur
        """
        if not self.is_running:
            return
        
        self.is_running = False
        
        if self.update_thread:
            try:
                self.update_thread.join(timeout=1.0)
            except Exception:
                pass
        
        logger.info("Duygu motoru durduruldu.")
    
    def _update_loop(self) -> None:
        """
        Duygu güncelleme döngüsü - alt sınıflar tarafından uygulanacak
        """
        raise NotImplementedError("Bu metod alt sınıflar tarafından uygulanmalıdır")
        
    def register_callback(self, event_type: str, callback: Callable) -> None:
        """
        Olay geri çağrısı kaydeder
        
        Args:
            event_type (str): Olay tipi ("emotion_changed", "emotion_update", "micro_expression")
            callback (Callable): Geri çağrı fonksiyonu
        """
        if event_type not in self.event_callbacks:
            self.event_callbacks[event_type] = []
        
        if callback not in self.event_callbacks[event_type]:
            self.event_callbacks[event_type].append(callback)
            logger.debug(f"Geri çağrı kaydedildi: {event_type}")
    
    def unregister_callback(self, event_type: str, callback: Callable) -> None:
        """
        Olay geri çağrısı kaydını siler
        
        Args:
            event_type (str): Olay tipi
            callback (Callable): Geri çağrı fonksiyonu
        """
        if event_type in self.event_callbacks and callback in self.event_callbacks[event_type]:
            self.event_callbacks[event_type].remove(callback)
            logger.debug(f"Geri çağrı kaydı silindi: {event_type}")
    
    def _trigger_callbacks(self, event_type: str, data: Dict) -> None:
        """
        Belirtilen olay tipindeki tüm geri çağrıları tetikler
        
        Args:
            event_type (str): Olay tipi
            data (Dict): Olay verileri
        """
        if event_type in self.event_callbacks:
            for callback in self.event_callbacks[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Geri çağrı hatası ({event_type}): {e}")