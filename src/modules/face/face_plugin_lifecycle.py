#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: face_plugin_lifecycle.py
# Açıklama: FacePlugin yaşam döngüsü ve durum yönetimi işlevleri
# Bağımlılıklar: logging, threading, time
# Bağlı Dosyalar: face_plugin_base.py, face_plugin_system.py

# Versiyon: 0.4.1
# Değişiklikler:
# - [0.4.1] Gelişmiş yaşam döngüsü ve durum yönetimi fonksiyonları eklendi
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-03
===========================================================
"""

import logging
import threading
import time
import os
import json
import enum
from typing import Dict, List, Optional, Union, Callable

# Loglama yapılandırması
logger = logging.getLogger("FacePluginLifecycle")

# Plugin durumlarını tanımlama
class PluginState(enum.Enum):
    """
    Plugin durumlarını tanımlayan enum sınıfı
    """
    UNINITIALIZED = "uninitialized"
    INITIALIZING = "initializing" 
    INITIALIZED = "initialized"
    STARTING = "starting"
    RUNNING = "running"
    PAUSING = "pausing"
    PAUSED = "paused"
    RESUMING = "resuming"
    STOPPING = "stopping"
    STOPPED = "stopped"
    ERROR = "error"
    SHUTDOWN = "shutdown"
    MAINTENANCE = "maintenance"

# Durum geçiş izinlerini tanımlama (hangi durumdan hangi duruma geçilebilir)
STATE_TRANSITIONS = {
    PluginState.UNINITIALIZED: [PluginState.INITIALIZING, PluginState.INITIALIZED],
    PluginState.INITIALIZING: [PluginState.INITIALIZED, PluginState.ERROR],
    PluginState.INITIALIZED: [PluginState.STARTING, PluginState.STOPPING, PluginState.MAINTENANCE],
    PluginState.STARTING: [PluginState.RUNNING, PluginState.ERROR],
    PluginState.RUNNING: [PluginState.PAUSING, PluginState.STOPPING, PluginState.ERROR, PluginState.MAINTENANCE],
    PluginState.PAUSING: [PluginState.PAUSED, PluginState.ERROR],
    PluginState.PAUSED: [PluginState.RESUMING, PluginState.STOPPING, PluginState.MAINTENANCE],
    PluginState.RESUMING: [PluginState.RUNNING, PluginState.ERROR],
    PluginState.STOPPING: [PluginState.STOPPED, PluginState.ERROR],
    PluginState.STOPPED: [PluginState.INITIALIZING, PluginState.SHUTDOWN],
    PluginState.ERROR: [PluginState.INITIALIZING, PluginState.STOPPED, PluginState.SHUTDOWN],
    PluginState.SHUTDOWN: [],  # Son durum
    PluginState.MAINTENANCE: [PluginState.INITIALIZING, PluginState.STOPPED]
}

class FacePluginLifecycle:
    """
    FacePlugin yaşam döngüsü sınıfı
    
    Bu sınıf FacePlugin sınıfı için yaşam döngüsü ve durum yönetimi işlevlerini içerir:
    - Genişletilmiş durum yönetimi
    - Durumlar arası geçiş kontrolü
    - Durum değişikliği olayları
    - Periyodik bakım ve kontroller
    """
    
    def __init__(self):
        """
        FacePluginLifecycle sınıfını başlatır
        """
        # Durum yönetimi
        self._state = PluginState.UNINITIALIZED
        self._state_lock = threading.RLock()
        self._state_change_callbacks = []
        
        # Durum değişiklik zamanları
        self._state_history = []
        self._state_timestamps = {state: None for state in PluginState}
        self._state_durations = {state: 0 for state in PluginState}
        
        # Periyodik görevler
        self._maintenance_thread = None
        self._maintenance_interval = 60.0  # saniye
        self._maintenance_running = False
        
        # Hata yönetimi
        self._error_count = 0
        self._error_threshold = 5
        self._consecutive_errors = 0
        self._last_error = None
        self._error_timestamps = []
        
        logger.debug("FacePluginLifecycle sınıfı başlatıldı")
    
    @property
    def state(self) -> PluginState:
        """
        Plugin'in mevcut durumunu döndürür
        
        Returns:
            PluginState: Plugin durumu
        """
        with self._state_lock:
            return self._state
    
    @state.setter
    def state(self, value: PluginState) -> None:
        """
        Plugin'in durumunu ayarlar (durum geçişi yapar)
        
        Args:
            value (PluginState): Yeni durum
        """
        if not isinstance(value, PluginState):
            logger.error(f"Geçersiz durum değeri: {value}")
            return
        
        # transition_to metodu üzerinden durum değişikliği yap
        self.transition_to(value)
    
    @property
    def state_name(self) -> str:
        """
        Plugin'in mevcut durum adını döndürür
        
        Returns:
            str: Durum adı
        """
        return self.state.value
    
    def can_transition_to(self, target_state: PluginState) -> bool:
        """
        Belirtilen duruma geçişin mümkün olup olmadığını kontrol eder
        
        Args:
            target_state (PluginState): Hedef durum
            
        Returns:
            bool: Geçiş yapılabilirse True, değilse False
        """
        with self._state_lock:
            current_state = self._state
            return target_state in STATE_TRANSITIONS.get(current_state, [])
    
    def transition_to(self, target_state: PluginState) -> bool:
        """
        Belirtilen duruma geçiş yapar
        
        Args:
            target_state (PluginState): Hedef durum
            
        Returns:
            bool: Geçiş başarılı olduysa True, değilse False
        """
        with self._state_lock:
            current_state = self._state
            
            # Geçiş yapılabilir mi?
            if not self.can_transition_to(target_state):
                logger.warning(f"Geçersiz durum geçişi: {current_state.value} -> {target_state.value}")
                return False
            
            # Önceki durum
            old_state = self._state
            
            # Durum değişimi
            self._state = target_state
            now = time.time()
            
            # Durum tarihçesini güncelle
            self._state_history.append((old_state, target_state, now))
            
            # Başlangıç zamanını güncelle
            self._state_timestamps[target_state] = now
            
            # Bitiş zamanını ve süreyi güncelle
            if self._state_timestamps[old_state] is not None:
                duration = now - self._state_timestamps[old_state]
                self._state_durations[old_state] += duration
            
            # Hata sayacını güncelle
            if target_state == PluginState.ERROR:
                self._error_count += 1
                self._consecutive_errors += 1
                self._error_timestamps.append(now)
            else:
                self._consecutive_errors = 0
            
            # Durum değişikliği bildirimlerini gönder
            self._notify_state_changed(old_state, target_state)
            
            logger.info(f"Durum değişti: {old_state.value} -> {target_state.value}")
            return True
    
    def register_state_change_callback(self, callback: Callable[[PluginState, PluginState], None]) -> None:
        """
        Durum değişikliği olayları için callback kaydeder
        
        Args:
            callback (Callable): İki parametre alan (old_state, new_state) fonksiyon
        """
        if callback not in self._state_change_callbacks:
            self._state_change_callbacks.append(callback)
    
    def unregister_state_change_callback(self, callback: Callable) -> None:
        """
        Durum değişikliği callback'ini kaldırır
        
        Args:
            callback (Callable): Kaldırılacak callback fonksiyonu
        """
        if callback in self._state_change_callbacks:
            self._state_change_callbacks.remove(callback)
    
    def _notify_state_changed(self, old_state: PluginState, new_state: PluginState) -> None:
        """
        Durum değişikliği bildirimlerini gönderir
        
        Args:
            old_state (PluginState): Önceki durum
            new_state (PluginState): Yeni durum
        """
        for callback in self._state_change_callbacks[:]:  # Kopya üzerinde işlem yap
            try:
                callback(old_state, new_state)
            except Exception as e:
                logger.error(f"Durum değişikliği bildirimi gönderilirken hata: {e}")
    
    def start_maintenance_cycle(self, interval: float = 60.0) -> None:
        """
        Periyodik bakım döngüsünü başlatır
        
        Args:
            interval (float): Bakım aralığı (saniye)
        """
        if self._maintenance_thread and self._maintenance_thread.is_alive():
            logger.warning("Bakım döngüsü zaten çalışıyor.")
            return
        
        self._maintenance_interval = interval
        self._maintenance_running = True
        
        def maintenance_loop():
            while self._maintenance_running:
                try:
                    # Bakım işlemi
                    if self.state != PluginState.ERROR and self.state != PluginState.SHUTDOWN:
                        self.perform_maintenance()
                    
                    # Bekleme
                    time.sleep(self._maintenance_interval)
                except Exception as e:
                    logger.error(f"Bakım döngüsünde hata: {e}")
                    time.sleep(5)  # Hata durumunda kısa bir bekleme
        
        self._maintenance_thread = threading.Thread(target=maintenance_loop, daemon=True)
        self._maintenance_thread.start()
        logger.debug(f"Bakım döngüsü başlatıldı ({interval}s aralıklarla)")
    
    def stop_maintenance_cycle(self) -> None:
        """
        Periyodik bakım döngüsünü durdurur
        """
        self._maintenance_running = False
        if self._maintenance_thread and self._maintenance_thread.is_alive():
            self._maintenance_thread.join(timeout=2.0)
            logger.debug("Bakım döngüsü durduruldu")
    
    def perform_maintenance(self) -> None:
        """
        Bakım işlemlerini gerçekleştirir
        Bu metod alt sınıflar tarafından override edilebilir
        """
        # Durum değişikliğini kontrol et
        if self.state == PluginState.RUNNING:
            # Çalışma durumunda bellek kullanımını, performansı kontrol et
            # Örnek: Bellek temizliği, önbellek optimizasyonu, vb.
            pass
        elif self.state == PluginState.MAINTENANCE:
            # Bakım durumunda daha kapsamlı işlemler
            # Örnek: Dosya sistemi kontrolü, veritabanı bakımı, vb.
            pass
    
    def get_state_history(self) -> List[tuple]:
        """
        Durum geçiş tarihçesini döndürür
        
        Returns:
            List[tuple]: (eski_durum, yeni_durum, zaman) içeren liste
        """
        return self._state_history.copy()
    
    def get_state_duration(self, state: PluginState) -> float:
        """
        Belirli bir durumda toplam geçirilen süreyi döndürür
        
        Args:
            state (PluginState): Durum
            
        Returns:
            float: Saniye cinsinden süre
        """
        return self._state_durations.get(state, 0)
    
    def get_uptime(self) -> float:
        """
        Plugin'in toplam çalışma süresini döndürür
        
        Returns:
            float: Saniye cinsinden çalışma süresi
        """
        running_time = self.get_state_duration(PluginState.RUNNING)
        paused_time = self.get_state_duration(PluginState.PAUSED)
        return running_time + paused_time
    
    def get_error_rate(self) -> float:
        """
        Hata oranını döndürür
        
        Returns:
            float: Hata oranı (0.0-1.0 arası)
        """
        total_state_changes = len(self._state_history)
        if total_state_changes == 0:
            return 0.0
        return self._error_count / total_state_changes
    
    def should_enter_maintenance(self) -> bool:
        """
        Bakım moduna geçilmesi gerekip gerekmediğini kontrol eder
        
        Returns:
            bool: Bakım gerekliyse True, değilse False
        """
        # Kriterlere göre bakım ihtiyacını belirle
        # Örnek: Belirli süre çalıştıktan sonra, hata sayısı belirli eşiği geçince, vb.
        
        # Ardışık hata sayısı eşik değerini aştıysa
        if self._consecutive_errors >= self._error_threshold:
            return True
        
        # Son 1 saat içinde çok fazla hata olduysa
        recent_errors = 0
        now = time.time()
        one_hour_ago = now - 3600
        
        for timestamp in self._error_timestamps:
            if timestamp >= one_hour_ago:
                recent_errors += 1
        
        if recent_errors >= self._error_threshold * 2:
            return True
        
        # Uzun süredir çalışıyorsa (örn: 24 saat)
        uptime = self.get_uptime()
        if uptime > 24 * 3600:  # 24 saat
            return True
        
        return False
    
    def get_status_report(self) -> Dict:
        """
        Plugin durumunun detaylı raporunu döndürür
        
        Returns:
            Dict: Durum raporu
        """
        now = time.time()
        
        # Mevcut durum için geçen süre
        current_state_time = 0
        if self._state_timestamps[self._state] is not None:
            current_state_time = now - self._state_timestamps[self._state]
        
        return {
            "state": self.state_name,
            "uptime": self.get_uptime(),
            "current_state_time": current_state_time,
            "error_count": self._error_count,
            "consecutive_errors": self._consecutive_errors,
            "error_rate": self.get_error_rate(),
            "last_maintenance": self._state_timestamps.get(PluginState.MAINTENANCE),
            "state_history": [
                {
                    "from": old.value,
                    "to": new.value,
                    "timestamp": ts
                }
                for old, new, ts in self._state_history[-10:]  # Son 10 değişiklik
            ]
        }
    
    def pause(self) -> bool:
        """
        Plugin'i duraklatır
        
        Returns:
            bool: Başarılı olduysa True, değilse False
        """
        if self.state != PluginState.RUNNING:
            logger.warning(f"Plugin duraklatılamıyor: mevcut durum {self.state_name}")
            return False
        
        # Önce duraklatma sürecine geçiş yap
        if not self.transition_to(PluginState.PAUSING):
            return False
        
        # Duraklatma işlemi burada yapılır
        # Alt sınıflar bu işlemi override edebilir
        
        # Duraklatıldı durumuna geçiş
        return self.transition_to(PluginState.PAUSED)
    
    def resume(self) -> bool:
        """
        Duraklatılmış plugin'i devam ettirir
        
        Returns:
            bool: Başarılı olduysa True, değilse False
        """
        if self.state != PluginState.PAUSED:
            logger.warning(f"Plugin devam ettirilemiyor: mevcut durum {self.state_name}")
            return False
        
        # Önce devam ettirme sürecine geçiş yap
        if not self.transition_to(PluginState.RESUMING):
            return False
        
        # Devam ettirme işlemi burada yapılır
        # Alt sınıflar bu işlemi override edebilir
        
        # Çalışıyor durumuna geçiş
        return self.transition_to(PluginState.RUNNING)
    
    def shutdown(self) -> bool:
        """
        Plugin'i tamamen kapatır (shutdown)
        
        Returns:
            bool: Başarılı olduysa True, değilse False
        """
        # Önce durdur
        if self.state not in [PluginState.STOPPED, PluginState.ERROR]:
            if not self.transition_to(PluginState.STOPPING):
                logger.error("Plugin durdurulamadı, kapanış işlemi yapılamıyor")
                return False
            
            # Durdurma işlemleri burada yapılır...
            
            if not self.transition_to(PluginState.STOPPED):
                logger.error("Plugin durdurulamadı, kapanış işlemi yapılamıyor")
                return False
        
        # Bakım döngüsünü durdur
        self.stop_maintenance_cycle()
        
        # Kapanış durumuna geçiş
        return self.transition_to(PluginState.SHUTDOWN)
    
    def enter_maintenance_mode(self) -> bool:
        """
        Plugin'i bakım moduna alır
        
        Returns:
            bool: Başarılı olduysa True, değilse False
        """
        # Sadece belirli durumlardan bakım moduna geçilebilir
        if not self.can_transition_to(PluginState.MAINTENANCE):
            logger.warning(f"Plugin bakım moduna alınamıyor: mevcut durum {self.state_name}")
            return False
        
        # Bakım moduna geçiş
        return self.transition_to(PluginState.MAINTENANCE)
    
    def exit_maintenance_mode(self) -> bool:
        """
        Plugin'i bakım modundan çıkarır
        
        Returns:
            bool: Başarılı olduysa True, değilse False
        """
        if self.state != PluginState.MAINTENANCE:
            logger.warning(f"Plugin bakım modundan çıkamıyor: mevcut durum {self.state_name}")
            return False
        
        # Bakım tamamlandıktan sonra genellikle yeniden başlatılır
        return self.transition_to(PluginState.INITIALIZING)