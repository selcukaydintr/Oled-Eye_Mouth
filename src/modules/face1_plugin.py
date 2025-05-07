#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: face1_plugin.py
# Açıklama: Ana yüz eklentisi kontrolcüsü. Modüler mimariden gelen sınıfları birleştirir.
# Bağımlılıklar: fastapi, uvicorn, logging, threading, time, json
# Bağlı Dosyalar: 
#   - modules/face/face_plugin_base.py
#   - modules/face/face_plugin_callbacks.py
#   - modules/face/face_plugin_system.py
#   - modules/face/face_plugin_api.py
#   - modules/face/face_plugin_config.py
#   - modules/face/face_plugin_metrics.py
#   - modules/face/face_plugin_environment.py
#   - modules/face/face_plugin_lifecycle.py
#   - plugins/plugin_isolation.py
#   - plugins/config_standardizer.py
#   - modules/sound_processor.py

# Versiyon: 0.5.0
# Değişiklikler:
# - [0.5.0] Ses tepkimeli ifade sistemi entegre edildi
# - [0.4.4] Tüm işlevler modüler mixin sınıflarına bölündü
# - [0.4.3] Üst proje entegrasyonu için plugin izolasyon ve yapılandırma standardizasyon modülleri entegre edildi
# - [0.4.0] FacePlugin modülerleştirildi, mixin mimarisi uygulandı
# - [0.3.3] Animasyon motoru entegrasyonu ve JSON formatı desteği eklendi
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-05
===========================================================
"""

import os
import sys
import time
import json
import signal
import logging
import threading
import traceback
import random
from typing import Dict, List, Tuple, Optional, Any, Union
from pathlib import Path
import asyncio

# Proje dizinini Python yoluna ekle
PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(str(PROJECT_DIR))

# Modüler sınıfları içe aktar
from src.modules.face.face_plugin_base import FacePluginBase
from src.modules.face.face_plugin_callbacks import FacePluginCallbacks
from src.modules.face.face_plugin_system import FacePluginSystem
from src.modules.face.face_plugin_api import FacePluginAPI
from src.modules.face.face_plugin_lifecycle import PluginState

# Yeni modüler bileşenleri içe aktar
from src.modules.face.face_plugin_config import FacePluginConfigMixin
from src.modules.face.face_plugin_metrics import FacePluginMetricsMixin
from src.modules.face.face_plugin_environment import FacePluginEnvironmentMixin

# Üst proje entegrasyonu için plugin modüllerini içe aktar
from src.plugins.plugin_isolation import PluginIsolation
from src.plugins.config_standardizer import ConfigStandardizer

# Ses tepkimeli ifade sistemi için ses işleme modülü
from src.modules.sound_processor import SoundProcessor

# Loglama yapılandırması
logger = logging.getLogger("FacePlugin")

class FacePlugin(FacePluginBase, FacePluginCallbacks, FacePluginSystem, FacePluginAPI,
               FacePluginConfigMixin, FacePluginMetricsMixin, FacePluginEnvironmentMixin):
    """
    FACE1 yüz eklentisi ana sınıf
    
    Bu sınıf, modüler mimarideki tüm sınıfları bir araya getirir ve
    tam işlevli bir FacePlugin sağlar.
    
    Sınıf, şu ana işlevleri sunar:
    - Yüz eklentisinin başlatılması ve durdurulması
    - Duygu durumu kontrolü ve animasyonlar
    - Tema yönetimi
    - API ve HTTP sunucu
    - Watchdog ve sistem durumu izleme
    - Plugin izolasyon ve kaynak yönetimi
    - Üst proje yapılandırma entegrasyonu
    - Çevresel faktör ve sensör izleme (v0.4.4+)
    - Performans metrik toplama ve raporlama (v0.4.4+)
    - Yapılandırma yönetimi ve izleme (v0.4.4+)
    - Ses tepkimeli ifade sistemi (v0.5.0+)
    """
    
    def __init__(self, config_path: str = None):
        """
        FACE1 yüz eklentisini başlatır
        
        Args:
            config_path (str, optional): Yapılandırma dosyasının yolu. 
                                      None ise varsayılan yol kullanılır.
        """
        # Durum değişkeni (doğrudan _state olarak ayarla)
        self._state = PluginState.UNINITIALIZED
        
        # Yapılandırma standardizasyonu
        self.config_standardizer = ConfigStandardizer(config_path)
        standardized_config = self.config_standardizer.config
        
        # Plugin izolasyon katmanı
        self.plugin_isolation = PluginIsolation(standardized_config)
        
        # Temel sınıfı başlat (FacePluginBase) - standardize edilmiş yapılandırma ile
        FacePluginBase.__init__(self, config_path)
        self.config = standardized_config  # Yapılandırma ayarını doğrudan ayarla
        
        # Yeni modülleri başlat
        self.__init_metrics__()  # Performans metrik sistemi
        self.__init_environment__()  # Çevresel faktör sistemi
        
        # Ses işleme modülünü başlat
        self.sound_processor = None  # Başlangıçta None olarak ayarla
        
        # Loglama yapılandırmasını ayarla
        self._setup_logging()
        
        # Durum dosyasının yolu
        self.status_file_path = os.path.join(PROJECT_DIR, "face_plugin_status.json")
        
        # Durum güncelleme
        self.state = PluginState.INITIALIZED
        
        logger.info("FACE1 Yüz Eklentisi başlatıldı.")
    
    def _init_modules(self) -> None:
        """
        Tüm modülleri başlatır
        """
        # Ana modülleri başlat
        self._init_oled_controller()
        self._init_led_controller()
        self._init_theme_manager()
        self._init_emotion_engine()
        self._init_animation_engine()
        self._init_sound_processor()
        
        # Modüller başlatıldı
        logger.info("Tüm modüller başlatıldı")
    
    def _init_oled_controller(self) -> None:
        """
        OLED kontrolcü modülünü başlatır
        """
        try:
            from src.modules.oled_controller import OLEDController
            self.oled_controller = OLEDController(self.config)
            logger.info("OLED kontrolcü başlatıldı")
        except Exception as e:
            logger.error(f"OLED kontrolcü başlatılırken hata: {e}")
            self.oled_controller = None
    
    def _init_led_controller(self) -> None:
        """
        LED kontrolcü modülünü başlatır
        """
        try:
            from src.modules.led_controller import LEDController
            self.led_controller = LEDController(self.config)
            logger.info("LED kontrolcü başlatıldı")
        except Exception as e:
            logger.error(f"LED kontrolcü başlatılırken hata: {e}")
            self.led_controller = None
    
    def _init_theme_manager(self) -> None:
        """
        Tema yöneticisi modülünü başlatır
        """
        try:
            from src.modules.theme_manager import ThemeManager
            self.theme_manager = ThemeManager(self.config)
            logger.info("Tema yöneticisi başlatıldı")
        except Exception as e:
            logger.error(f"Tema yöneticisi başlatılırken hata: {e}")
            self.theme_manager = None
    
    def _init_emotion_engine(self) -> None:
        """
        Duygu motoru modülünü başlatır
        """
        try:
            from src.modules.emotion_engine import EmotionEngine
            self.emotion_engine = EmotionEngine(self.config)
            logger.info("Duygu motoru başlatıldı")
        except Exception as e:
            logger.error(f"Duygu motoru başlatılırken hata: {e}")
            self.emotion_engine = None
    
    def _init_animation_engine(self) -> None:
        """
        Animasyon motoru modülünü başlatır
        """
        try:
            from src.modules.animation_engine import AnimationEngine
            self.animation_engine = AnimationEngine(self.config)
            logger.info("Animasyon motoru başlatıldı")
        except Exception as e:
            logger.error(f"Animasyon motoru başlatılırken hata: {e}")
            self.animation_engine = None
    
    def _init_sound_processor(self) -> None:
        """
        Ses işleme modülünü başlatır
        """
        try:
            from src.modules.sound_processor import SoundProcessor
            self.sound_processor = SoundProcessor(self.config)
            logger.info("Ses işleme modülü başlatıldı")
        except Exception as e:
            logger.error(f"Ses işleme modülü başlatılırken hata: {e}")
            self.sound_processor = None
    
    def initialize_modules(self) -> None:
        """
        Tüm modülleri başlatır ve aralarındaki bağlantıları kurar
        """
        try:
            # Modülleri başlat
            self._init_modules()
            
            # Tema değişikliği için callback'leri kaydet
            if self.theme_manager and self.oled_controller and self.led_controller:
                # Tema değiştiğinde OLED ve LED kontrolcüleri güncelle
                self.theme_manager.register_theme_callback(self.oled_controller.apply_theme)
                self.theme_manager.register_theme_callback(self.led_controller.apply_theme)
                
                # Başlangıç temasını uygula
                theme_name = self.config.get("theme", {}).get("default_theme", "default")
                self.theme_manager.set_active_theme(theme_name)
            
            # Duygu motoru için tema ve kontrolcü bağlantıları
            if self.emotion_engine:
                if self.theme_manager:
                    self.emotion_engine.set_theme_manager(self.theme_manager)
                if self.oled_controller:
                    self.emotion_engine.set_oled_controller(self.oled_controller)
                if self.led_controller:
                    self.emotion_engine.set_led_controller(self.led_controller)
            
            # Animasyon motoru için bağlantılar
            if self.animation_engine:
                if self.oled_controller:
                    self.animation_engine.set_oled_controller(self.oled_controller)
                if self.led_controller:
                    self.animation_engine.set_led_controller(self.led_controller)
                if self.emotion_engine:
                    self.animation_engine.set_emotion_engine(self.emotion_engine)
            
            # Ses işleme modülü için bağlantılar
            if self.sound_processor:
                if self.emotion_engine:
                    # Duygu motoru önerileri için callback kaydı
                    self.sound_processor.register_emotion_callback(
                        lambda emotion, intensity: self.emotion_engine.suggest_emotion(emotion, intensity)
                    )
                
                if self.oled_controller and hasattr(self.oled_controller, 'set_speaking_state'):
                    # Konuşma durumuna göre ağız animasyonu için callback kaydı
                    self.sound_processor.register_speaking_callback(self.oled_controller.set_speaking_state)
            
            logger.info("Modüller başarıyla başlatıldı ve yapılandırıldı")
            return True
            
        except Exception as e:
            logger.error(f"Modüller başlatılırken hata: {e}")
            return False
    
    def start(self) -> bool:
        """
        Yüz eklentisini başlatır
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        # Durum kontrolü
        if self.state != PluginState.INITIALIZED and self.state != PluginState.PAUSED:
            logger.error(f"Geçersiz durum: {self.state}. Yüz eklentisi başlatılamıyor.")
            return False
        
        try:
            # Durum güncelleme - burada sadece bir kez STARTING durumuna geçiriyoruz
            if not self.transition_to(PluginState.STARTING):
                logger.error("Başlatma durumuna geçilemiyor.")
                return False
            
            # Plugin izolasyonu başlat
            if not self.plugin_isolation.start():
                logger.error("Plugin izolasyon katmanı başlatılamadı")
                return False
            
            # İzole edilmiş çağrı olarak temel başlatma işlemi - burada super().start() çağrısı durum değiştirmeye çalışmayacak
            success = self.plugin_isolation.wrap_call(super().start)
            
            if not success:
                # İzolasyonu durdur
                self.plugin_isolation.stop()
                # Hata durumunda INITIALIZED durumuna geri dön
                self.transition_to(PluginState.INITIALIZED)
                return False
            
            # Metrik toplama sistemini başlat
            self.start_metric_collection()
            
            # Çevresel sensörleri yapılandır
            self.setup_environment_sensors()
            
            # Çevresel faktör izleme sistemini başlat
            self.start_environment_monitoring()
            
            # Ses işleme modülünü başlat
            if self.sound_processor:
                self.sound_processor.start()
            
            # Başarılı başlatma sonrası RUNNING durumuna geç
            if not self.transition_to(PluginState.RUNNING):
                logger.error("Çalışma durumuna geçilemiyor.")
                # Hata durumunda temizlik yap
                self.plugin_isolation.stop()
                self.transition_to(PluginState.INITIALIZED)
                return False
            
            # Durum dosyasını güncelle
            self._update_status_file("running")
                
            return True
            
        except Exception as e:
            logger.error(f"Yüz eklentisi başlatılırken hata: {e}")
            # Hata durumunda izolasyonu durdur ve durumu sıfırla
            if hasattr(self, 'plugin_isolation'):
                self.plugin_isolation.stop()
            # Durumu INITIALIZED'a geri çevir
            self.transition_to(PluginState.INITIALIZED)
            return False
    
    def stop(self) -> None:
        """
        Yüz eklentisini durdurur
        """
        # Durum kontrolü ve güncelleme
        if self.state == PluginState.UNINITIALIZED:
            logger.warning("Yüz eklentisi henüz başlatılmamış.")
            return
            
        # Çevresel faktör izleme sistemini durdur
        if hasattr(self, 'stop_environment_monitoring'):
            self.stop_environment_monitoring()
            
        # Çevresel sensör kaynaklarını temizle
        if hasattr(self, 'cleanup_environment_resources'):
            self.cleanup_environment_resources()
        
        # Metrik toplama sistemini durdur
        if hasattr(self, 'stop_metric_collection'):
            self.stop_metric_collection()
        
        # Ses işleme modülünü durdur
        if hasattr(self, 'sound_processor') and self.sound_processor is not None:
            self.sound_processor.stop()
        
        # Önce temel durdurmayı çağır
        super().stop()
        
        # Son olarak izolasyon katmanını durdur
        self.plugin_isolation.stop()
        
        # Durum dosyasını güncelle
        self._update_status_file("stopped")
        
        # Düzgün durum geçişleri
        # STOPPED durumundan doğrudan INITIALIZED durumuna geçiş yerine
        # Önce INITIALIZING durumuna geçiş yapılır
        if self.state == PluginState.STOPPED:
            if self.transition_to(PluginState.INITIALIZING):
                self.transition_to(PluginState.INITIALIZED)
        
        logger.info("Yüz eklentisi ve izolasyon katmanı durduruldu")
    
    def pause(self) -> bool:
        """
        Yüz eklentisini duraklatır (ancak durdurma yerine kısmi işlevsellik sürdürür)
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        # Durum kontrolü
        if self.state != PluginState.RUNNING:
            logger.warning(f"Geçersiz durum: {self.state}. Yüz eklentisi duraklatılamıyor.")
            return False
        
        try:
            # Durum güncelleme
            self.state = PluginState.PAUSING
            
            # Çevresel faktör izlemesini askıya al
            self.stop_environment_monitoring()
            
            # Metrik toplamayı durdur
            self.stop_metric_collection()
            
            # Ses işleme modülünü duraklat
            self.sound_processor.pause()
            
            # Ekranlarda güç tasarrufu modunu etkinleştir
            if hasattr(self, 'oled_controller') and self.oled_controller is not None:
                if hasattr(self.oled_controller, 'set_power_mode'):
                    self.oled_controller.set_power_mode("dim")
            
            # LED'leri kapat
            if hasattr(self, 'led_controller') and self.led_controller is not None:
                if hasattr(self.led_controller, 'clear'):
                    self.led_controller.clear()
            
            # Durum dosyasını güncelle
            self._update_status_file("paused")
            
            # Durum güncelleme
            self.state = PluginState.PAUSED
            
            logger.info("Yüz eklentisi duraklatıldı")
            return True
            
        except Exception as e:
            logger.error(f"Yüz eklentisi duraklatılırken hata: {e}")
            # Hata durumunda durumu tekrar running yap
            self.state = PluginState.RUNNING
            return False
    
    def resume(self) -> bool:
        """
        Duraklatılmış yüz eklentisini devam ettirir
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        # Durum kontrolü
        if self.state != PluginState.PAUSED:
            logger.warning(f"Geçersiz durum: {self.state}. Yüz eklentisi devam ettirilemiyor.")
            return False
        
        try:
            # Durum güncelleme
            self.state = PluginState.STARTING
            
            # Metrik toplama sistemini başlat
            self.start_metric_collection()
            
            # Çevresel faktör izleme sistemini başlat
            self.start_environment_monitoring()
            
            # Ses işleme modülünü devam ettir
            self.sound_processor.resume()
            
            # Ekranlarda tam güç modunu etkinleştir
            if hasattr(self, 'oled_controller') and self.oled_controller is not None:
                if hasattr(self.oled_controller, 'set_power_mode'):
                    self.oled_controller.set_power_mode("on")
                    
                # Aktivite zamanlayıcısını sıfırla
                if hasattr(self.oled_controller, 'reset_activity_timer'):
                    self.oled_controller.reset_activity_timer()
            
            # Durum dosyasını güncelle
            self._update_status_file("running")
            
            # Durum güncelleme
            self.state = PluginState.RUNNING
            
            logger.info("Yüz eklentisi devam ediyor")
            return True
            
        except Exception as e:
            logger.error(f"Yüz eklentisi devam ettirilirken hata: {e}")
            # Hata durumunda durumu tekrar paused yap
            self.state = PluginState.PAUSED
            return False
    
    def set_emotion(self, emotion: str, intensity: float = 1.0) -> bool:
        """
        Duygu durumunu ayarlar
        
        Args:
            emotion (str): Duygu durumu
            intensity (float, optional): Duygu yoğunluğu (0.0-1.0). Varsayılan: 1.0
            
        Returns:
            bool: Başarılı ise True, değilse False
        """
        if self.state != PluginState.RUNNING or not self.emotion_engine:
            logger.warning(f"Yüz eklentisi çalışmıyor (durum: {self.state}), duygu ayarlanamıyor.")
            return False
        
        try:
            # Watchdog kalp atışını güncelle
            self.heartbeat()
            
            # İzole edilmiş çağrı
            return self.plugin_isolation.wrap_call(
                self.emotion_engine.set_emotion, emotion, intensity
            )
            
        except Exception as e:
            logger.error(f"Duygu ayarlanırken hata: {e}")
            return False
    
    def transition_to_emotion(self, emotion: str, transition_time: float = None) -> bool:
        """
        Belirli bir duyguya yumuşak geçiş yapar
        
        Args:
            emotion (str): Hedef duygu durumu
            transition_time (float, optional): Geçiş süresi (saniye). None ise otomatik hesaplanır.
            
        Returns:
            bool: Başarılı ise True, değilse False
        """
        if self.state != PluginState.RUNNING or not self.emotion_engine:
            logger.warning(f"Yüz eklentisi çalışmıyor (durum: {self.state}), duygu geçişi yapılamıyor.")
            return False
        
        try:
            # Watchdog kalp atışını güncelle
            self.heartbeat()
            
            # İzole edilmiş çağrı
            return self.plugin_isolation.wrap_call(
                self.emotion_engine.transition_to, emotion, transition_time
            )
            
        except Exception as e:
            logger.error(f"Duygu geçişi yapılırken hata: {e}")
            return False
    
    def get_current_emotion(self) -> Dict:
        """
        Mevcut duygu durumu bilgisini döndürür
        
        Returns:
            Dict: Duygu durumu bilgisi
        """
        if not self.is_running or not self.emotion_engine:
            logger.warning("Yüz eklentisi çalışmıyor, duygu bilgisi alınamıyor.")
            return {"state": "unknown", "intensity": 0.0}
        
        try:
            # Watchdog kalp atışını güncelle
            self.heartbeat()
            
            # İzole edilmiş çağrı
            return self.plugin_isolation.wrap_call(
                self.emotion_engine.get_current_emotion
            ) or {"state": "unknown", "intensity": 0.0}
            
        except Exception as e:
            logger.error(f"Duygu bilgisi alınırken hata: {e}")
            return {"state": "unknown", "intensity": 0.0}
    
    def get_plugin_status(self) -> Dict:
        """
        Plugin durumunu döndürür
        
        Returns:
            Dict: Plugin durumu
        """
        status = {
            "state": self.state.value,
            "running": self.state == PluginState.RUNNING,
            "version": "0.5.0",
            "uptime": time.time() - self.start_time if hasattr(self, 'start_time') else 0,
            "health": self.get_health_status() if hasattr(self, 'get_health_status') else {"status": "unknown"}
        }
        return status
    
    def get_metrics(self) -> Dict:
        """
        Plugin metriklerini döndürür
        
        Returns:
            Dict: Metrikler
        """
        # FacePluginMetricsMixin'den get_metrics metodunu çağır
        if hasattr(super(), 'get_metrics'):
            base_metrics = super().get_metrics()
        else:
            base_metrics = {}
            
        # Ek plugin izolasyon metriklerini ekle
        metrics = {
            **base_metrics,
            "plugin_isolation": self.plugin_isolation.get_metrics() if hasattr(self.plugin_isolation, 'get_metrics') else {},
            "state": self.state.value,
            "uptime": time.time() - self.start_time if hasattr(self, 'start_time') else 0
        }
        return metrics
        
    def migrate_parent_config(self, parent_config: Dict) -> Dict:
        """
        Üst proje yapılandırmasını FACE1'e uygun formata dönüştürür
        
        Args:
            parent_config (Dict): Üst proje yapılandırması
            
        Returns:
            Dict: FACE1 uyumlu yapılandırma
        """
        return self.config_standardizer.migrate_from_parent_config(parent_config)
    
    def export_to_parent_config(self) -> Dict:
        """
        FACE1 yapılandırmasını üst proje formatına dönüştürür
        
        Returns:
            Dict: Üst proje formatı yapılandırma
        """
        return self.config_standardizer.export_to_parent_format()
    
    def handle_environment_change(self, factor: str, state: str, value: float) -> None:
        """
        Çevresel faktör değişikliklerini işler ve websocket üzerinden istemcilere bildirir
        
        Args:
            factor (str): Çevresel faktör (temperature, light, humidity, motion, touch)
            state (str): Yeni durum
            value (float): Ölçülen değer
        """
        # Temel sınıfın işleyicisini çağırmayı atla - sonsuz döngüye neden olur!
        # super().on_environment_change içinden yine bu fonksiyon çağrılıyordu
        
        # Doğrudan websocket üzerinden istemcilere bildir
        if hasattr(self, 'dashboard_server') and self.dashboard_server is not None:
            if hasattr(self.dashboard_server, 'broadcast_event'):
                event_data = {
                    "factor": factor,
                    "state": state,
                    "value": value,
                    "timestamp": time.time()
                }
                self.dashboard_server.broadcast_event("environment_change", event_data)
                
    def run_forever(self) -> None:
        """
        Eklentiyi başlatır ve sonsuza kadar çalıştırır
        """
        # SIGINT (Ctrl+C) ve SIGTERM sinyallerini yakala
        def signal_handler(sig, frame):
            logger.info("Sinyal alındı: kapanıyor...")
            self.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Çevresel faktör değişikliklerini işleyici fonksiyonu kaydet
        self.register_environment_callback(self.handle_environment_change)
        
        # Eklentiyi başlat
        if not self.start():
            logger.error("Yüz eklentisi başlatılamadı. Çıkılıyor...")
            return
        
        try:
            logger.info("Yüz eklentisi çalışıyor. Durdurmak için Ctrl+C'ye basın...")
            
            # Ana döngü
            while self.is_running and not self.shutdown_requested:
                # Watchdog kalp atışını güncelle
                self.heartbeat()
                
                # Durum dosyasını düzenli olarak güncelle
                if hasattr(self, 'is_running') and self.is_running:
                    self._update_status_file("running")
                
                # Bir süre bekle
                time.sleep(1.0)
                
                # İzolasyon metrikleri
                if hasattr(self, 'debug_mode') and self.debug_mode:
                    metrics = self.plugin_isolation.get_metrics()
                    logger.debug(f"Plugin izolasyon metrikleri: {metrics}")
                
        except KeyboardInterrupt:
            logger.info("Klavye kesintisi alındı. Kapanıyor...")
        finally:
            self.stop()
    
    def _update_status_file(self, status: str) -> None:
        """
        Yüz eklentisi durum dosyasını günceller. Bu dosya, ayrı süreçlerde çalışan
        dashboard sunucusu ile iletişim için kullanılır.
        
        Args:
            status (str): Durum metni ('running', 'stopped', 'paused', vb.)
        """
        try:
            status_data = {
                "status": status,
                "timestamp": time.time(),
                "version": "0.5.1",  # Versiyon numarası
                "pid": os.getpid(),  # Süreç ID'si
                "plugin_module": "src.modules.face1_plugin",  # FacePlugin sınıfının modülü
                "plugin_class": "FacePlugin"  # FacePlugin sınıfının adı
            }
            
            # Eğer çalışıyorsa, daha fazla bilgi ekle
            if status == "running":
                status_data.update({
                    "uptime": time.time() - self.start_time if hasattr(self, 'start_time') else 0,
                    "theme": self.theme_manager.get_current_theme() if hasattr(self, 'theme_manager') and self.theme_manager else "default",
                })
            
            with open(self.status_file_path, 'w') as f:
                json.dump(status_data, f)
                
            logger.debug(f"Durum dosyası güncellendi: {self.status_file_path}")
                
        except Exception as e:
            logger.error(f"Durum dosyası güncellenirken hata: {e}")


def main():
    """
    Ana fonksiyon
    """
    try:
        # Loglama yapılandırması
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Alt modüllerin log seviyelerini ayarla
        logging.getLogger("PluginIsolation").setLevel(logging.INFO)
        logging.getLogger("ConfigStandardizer").setLevel(logging.INFO)
        logging.getLogger("FacePluginMetrics").setLevel(logging.INFO)
        logging.getLogger("FacePluginEnvironment").setLevel(logging.INFO)
        logging.getLogger("FacePluginConfig").setLevel(logging.INFO)
        
        # Yüz eklentisini oluştur
        config_path = os.path.join(PROJECT_DIR, "config", "config.json")
        face_plugin = FacePlugin(config_path)
        
        # Sonsuza kadar çalıştır
        face_plugin.run_forever()
        
    except Exception as e:
        logger.critical(f"Kritik hata: {e}")
        logger.critical(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()