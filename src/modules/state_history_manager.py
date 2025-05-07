#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FACE1 Durum Tarihçesi Yöneticisi
Bu modül, sistem genelindeki durum değişikliklerini takip eder, kaydeder ve sorgular.
"""

import time
import logging
import json
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta
from collections import deque
import threading
import os.path

# Modül seviyesinde logger
logger = logging.getLogger(__name__)

class StateHistoryManager:
    """
    FACE1 durum tarihçesi yönetim sınıfı.
    Bu sınıf, sistem durumlarını, duygu değişikliklerini, hataları ve diğer önemli olayları kaydeder.
    """
    
    def __init__(self, max_history_size: int = 500, storage_path: Optional[str] = None):
        """
        StateHistoryManager sınıfını başlatır
        
        Args:
            max_history_size: Bellekte saklanacak maksimum giriş sayısı
            storage_path: Tarihçe kayıtlarının saklanacağı dosya yolu (None ise depolama yapılmaz)
        """
        self.max_history_size = max_history_size
        self.storage_path = storage_path
        
        # Tarihçe verileri için thread-safe deque
        self._history = deque(maxlen=max_history_size)
        
        # Durum değişiklikleri için istatistikler
        self._stats = {
            "system": {},
            "emotion": {},
            "speaking": {},
            "animation": {},
            "error": {}
        }
        
        # Erişim için kilit mekanizması
        self._lock = threading.RLock()
        
        # Tarihsel verileri yükle (eğer bir depolama yolu belirtilmişse)
        self._load_history()
        
        logger.info(f"StateHistoryManager başlatıldı: max_size={max_history_size}, storage={storage_path}")

    def add_entry(self, entry_type: str, message: str, metadata: Optional[Dict] = None) -> None:
        """
        Tarihçeye yeni bir giriş ekler
        
        Args:
            entry_type: Giriş tipi ('system', 'emotion', 'speaking', 'animation', 'error')
            message: Giriş mesajı
            metadata: Giriş ile ilgili ek veri
        """
        with self._lock:
            timestamp = datetime.now()
            
            entry = {
                "type": entry_type,
                "message": message,
                "timestamp": timestamp,
                "metadata": metadata or {}
            }
            
            self._history.append(entry)
            self._update_stats(entry_type, message, timestamp)
            
            # Depolama etkinleştirilmişse tarihçeyi kaydet
            if self.storage_path:
                self._save_entry_to_storage(entry)
            
            logger.debug(f"Tarihçe girişi eklendi: {entry_type} - {message}")
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Tarihçe girişlerini döndürür
        
        Args:
            limit: Döndürülecek maksimum giriş sayısı (None ise tümü döndürülür)
            
        Returns:
            Tarihçe girişleri listesi (en yeniden en eskiye doğru)
        """
        with self._lock:
            if limit is None or limit >= len(self._history):
                return list(self._history)
            else:
                return list(self._history)[-limit:]
    
    def get_entries_by_type(self, entry_type: str, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Belirli bir türdeki tarihçe girişlerini döndürür
        
        Args:
            entry_type: İstenilen giriş tipi
            limit: Döndürülecek maksimum giriş sayısı
            
        Returns:
            Belirtilen türdeki tarihçe girişleri listesi
        """
        with self._lock:
            entries = [entry for entry in self._history if entry["type"] == entry_type]
            
            if limit is None or limit >= len(entries):
                return entries
            else:
                return entries[-limit:]
    
    def get_events_since(self, since_time: datetime) -> List[Dict[str, Any]]:
        """
        Belirli bir zamandan sonraki tüm girişleri döndürür
        
        Args:
            since_time: Başlangıç zamanı
            
        Returns:
            Belirtilen zamandan sonraki girişlerin listesi
        """
        with self._lock:
            return [entry for entry in self._history if entry["timestamp"] > since_time]
    
    def get_stats(self, entry_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Tarihçe istatistiklerini döndürür
        
        Args:
            entry_type: İstenilen giriş tipi (None ise tüm tipler için istatistikler döndürülür)
            
        Returns:
            Tarihçe istatistikleri
        """
        with self._lock:
            if entry_type:
                return self._stats.get(entry_type, {}).copy()
            else:
                return {k: v.copy() for k, v in self._stats.items()}
    
    def clear_history(self) -> None:
        """Tüm tarihçeyi temizler"""
        with self._lock:
            self._history.clear()
            
            # İstatistikleri sıfırla
            for stat_type in self._stats:
                self._stats[stat_type] = {}
            
            logger.info("Tarihçe temizlendi")
    
    def get_last_entry(self, entry_type: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Son tarihçe girişini döndürür
        
        Args:
            entry_type: İstenilen giriş tipi (None ise herhangi bir türdeki son giriş döndürülür)
            
        Returns:
            Son tarihçe girişi veya None
        """
        with self._lock:
            if not self._history:
                return None
                
            if entry_type is None:
                return self._history[-1]
            
            # Belirli tipte son girişi bul
            for entry in reversed(self._history):
                if entry["type"] == entry_type:
                    return entry
            
            return None
    
    def get_frequency(self, entry_type: str, time_period: timedelta) -> int:
        """
        Belirli bir zaman diliminde belirli tipte kaç giriş olduğunu hesaplar
        
        Args:
            entry_type: Giriş tipi
            time_period: Zaman dilimi
            
        Returns:
            Belirtilen zaman dilimindeki giriş sayısı
        """
        with self._lock:
            since_time = datetime.now() - time_period
            return sum(1 for entry in self._history 
                      if entry["type"] == entry_type and entry["timestamp"] > since_time)
    
    def _update_stats(self, entry_type: str, message: str, timestamp: datetime) -> None:
        """
        Belirli bir giriş tipi için istatistikleri günceller
        
        Args:
            entry_type: Giriş tipi
            message: Giriş mesajı
            timestamp: Giriş zaman damgası
        """
        if entry_type not in self._stats:
            self._stats[entry_type] = {}
        
        # Toplam sayımı artır
        self._stats[entry_type]["total_count"] = self._stats[entry_type].get("total_count", 0) + 1
        
        # Son olay bilgisini güncelle
        self._stats[entry_type]["last_message"] = message
        self._stats[entry_type]["last_timestamp"] = timestamp
        
        # Zaman aralıklarını hesapla
        if "last_timestamp" in self._stats[entry_type]:
            prev_timestamp = self._stats[entry_type]["last_timestamp"]
            
            # Ortalama aralık süresini güncelle
            if "avg_interval" in self._stats[entry_type]:
                prev_avg = self._stats[entry_type]["avg_interval"]
                count = self._stats[entry_type]["total_count"]
                new_interval = (timestamp - prev_timestamp).total_seconds()
                self._stats[entry_type]["avg_interval"] = (prev_avg * (count - 1) + new_interval) / count
            else:
                self._stats[entry_type]["avg_interval"] = 0
    
    def _save_entry_to_storage(self, entry: Dict[str, Any]) -> None:
        """
        Bir girişi depoya kaydeder
        
        Args:
            entry: Kaydedilecek giriş
        """
        if not self.storage_path:
            return
            
        try:
            # timestamp değerini string'e çevir
            entry_copy = entry.copy()
            entry_copy["timestamp"] = entry_copy["timestamp"].isoformat()
            
            with open(self.storage_path, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry_copy) + "\n")
        except Exception as e:
            logger.error(f"Tarihçe girişi depoya kaydedilirken hata: {e}")
    
    def _load_history(self) -> None:
        """Depodan tarihçe verilerini yükler"""
        if not self.storage_path or not os.path.exists(self.storage_path):
            return
            
        try:
            with open(self.storage_path, 'r', encoding='utf-8') as f:
                for line in f:
                    try:
                        entry = json.loads(line.strip())
                        
                        # timestamp string'i datetime'a çevir
                        if "timestamp" in entry and isinstance(entry["timestamp"], str):
                            entry["timestamp"] = datetime.fromisoformat(entry["timestamp"])
                            
                        self._history.append(entry)
                        self._update_stats(
                            entry["type"], 
                            entry["message"], 
                            entry["timestamp"]
                        )
                    except json.JSONDecodeError:
                        logger.warning(f"Geçersiz tarihçe girişi atlanıyor: {line}")
                        continue
                        
            logger.info(f"{len(self._history)} tarihçe girişi yüklendi")
        except Exception as e:
            logger.error(f"Tarihçe verileri yüklenirken hata: {e}")
    
    def set_storage_path(self, storage_path: str) -> None:
        """
        Tarihçe depolama yolunu değiştirir
        
        Args:
            storage_path: Yeni depolama yolu
        """
        with self._lock:
            self.storage_path = storage_path
            
            # Mevcut tarihçeyi yeni depoya kaydet
            if storage_path:
                try:
                    for entry in self._history:
                        self._save_entry_to_storage(entry)
                except Exception as e:
                    logger.error(f"Tarihçe yeni depoya kaydedilirken hata: {e}")