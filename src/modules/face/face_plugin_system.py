#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: face_plugin_system.py
# Açıklama: FacePlugin sınıfının sistem işlevleri, başlatma, durdurma, yeniden başlatma, watchdog
# Bağımlılıklar: logging, threading, time
# Bağlı Dosyalar: face_plugin.py, face_plugin_base.py, face_plugin_lifecycle.py

# Versiyon: 0.5.0
# Değişiklikler:
# - [0.5.0] Ses işleme modülü (sound_processor.py) entegrasyonu eklendi
# - [0.4.1] Gelişmiş yaşam döngüsü yönetimi sistemiyle uyumlu hale getirildi
# - [0.4.0] FacePlugin modülerleştirildi, sistem işlevleri ayrı dosyaya taşındı
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-04
===========================================================
"""

import logging
import threading
import time
import os
from typing import Dict, List, Optional, Union

from .face_plugin_lifecycle import PluginState

# Loglama yapılandırması
logger = logging.getLogger("FacePluginSystem")

class FacePluginSystem:
    """
    FacePlugin sistem sınıfı
    
    Bu sınıf FacePlugin sınıfı için sistem işlevlerini içerir:
    - Başlatma ve durdurma
    - Watchdog işlevleri
    - Durum yönetimi
    """
    
    def initialize(self) -> bool:
        """
        Yüz eklentisini ve tüm modüllerini başlatır
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        if self.is_initialized:
            logger.warning("Yüz eklentisi zaten başlatılmış.")
            return True
        
        # Durum geçişi yapılıyor mu kontrol et
        if not self.transition_to(PluginState.INITIALIZING):
            logger.error("Başlatma durumuna geçilemiyor.")
            return False
        
        try:
            logger.info("Yüz eklentisi başlatılıyor...")
            
            # Başlangıç gecikmesi (sistem komponenetlerinin başlaması için)
            startup_delay = self.config.get("system", {}).get("startup_delay", 1.0)
            if startup_delay > 0:
                logger.debug(f"Başlangıç gecikmesi: {startup_delay} saniye")
                time.sleep(startup_delay)
                
            # Tema yöneticisini başlat
            logger.info("Tema yöneticisi başlatılıyor...")
            from src.modules.theme_manager import ThemeManager
            self.theme_manager = ThemeManager(self.config)
            if not self.theme_manager.start():
                logger.error("Tema yöneticisi başlatılamadı.")
                self.transition_to(PluginState.ERROR)
                return False
                
            # Tema değişikliği için geri çağırma fonksiyonunu kaydet
            self.theme_manager.register_change_callback(self._on_theme_changed)
            
            # LED kontrolcüyü başlat
            logger.info("LED kontrolcü başlatılıyor...")
            from src.modules.led_controller import LEDController
            self.led_controller = LEDController(self.config)
            if not self.led_controller.start():
                logger.error("LED kontrolcü başlatılamadı.")
                self.transition_to(PluginState.ERROR)
                return False
                
            # OLED kontrolcüyü başlat
            logger.info("OLED kontrolcü başlatılıyor...")
            from src.modules.oled_controller import OLEDController
            self.oled_controller = OLEDController(self.config)
            if not self.oled_controller.start():
                logger.error("OLED kontrolcü başlatılamadı.")
                self.transition_to(PluginState.ERROR)
                return False
            
            # Duygu motorunu başlat
            logger.info("Duygu motoru başlatılıyor...")
            from src.modules.emotion_engine import EmotionEngine
            self.emotion_engine = EmotionEngine(self.config)
            
            # Geri çağrıları kaydet
            self._register_callbacks()
            
            # Duygu motorunu başlat
            if not self.emotion_engine.start():
                logger.error("Duygu motoru başlatılamadı.")
                self.transition_to(PluginState.ERROR)
                return False
            
            # Animasyon motorunu başlat
            logger.info("Animasyon motoru başlatılıyor...")
            from src.modules.animation_engine import AnimationEngine
            self.animation_engine = AnimationEngine(self.config)
            if not self.animation_engine.start():
                logger.error("Animasyon motoru başlatılamadı.")
                self.transition_to(PluginState.ERROR)
                return False
            
            # Ses işleme modülünü başlat
            logger.info("Ses işleme modülü başlatılıyor...")
            from src.modules.sound_processor import SoundProcessor
            self.sound_processor = SoundProcessor(self.config.get("sound", {}))
            
            # Ses işleme geri çağrı fonksiyonlarını kaydet
            if self.emotion_engine:
                self.sound_processor.register_emotion_callback(self.emotion_engine.set_emotion_suggestion)
            
            if self.oled_controller:
                self.sound_processor.register_speaking_callback(self.oled_controller.animate_mouth_speaking)
            
            # Ses işleme modülünü başlat
            if not self.sound_processor.start():
                logger.warning("Ses işleme modülü başlatılamadı, ses reaktif özellikler devre dışı.")
                # Bu modül olmadan da çalışabileceği için hata vermeyelim
            
            # Performans optimize ediciyi başlat (Faz 4 - Performans Optimizasyonu)
            logger.info("Performans optimize edici başlatılıyor...")
            from src.modules.performance_optimizer import PerformanceOptimizer
            self.performance_optimizer = PerformanceOptimizer(self.config)
            
            # Controller referanslarını ayarla
            self.performance_optimizer.set_controllers(
                oled_controller=self.oled_controller,
                led_controller=self.led_controller,
                sound_processor=self.sound_processor
            )
            
            # Performans optimize ediciyi başlat
            if not self.performance_optimizer.start():
                logger.warning("Performans optimize edici başlatılamadı, performans optimizasyonu devre dışı.")
                # Bu modül olmadan da çalışabileceği için hata vermeyelim
            
            # Varsayılan duyguyu ayarla
            default_emotion = self.config.get("emotions", {}).get("default_emotion", "neutral")
            self.emotion_engine.set_emotion(default_emotion, 0.7)
            
            # Başlangıç animasyonu
            self._run_startup_sequence()
            
            # Bakım döngüsünü başlat
            maintenance_interval = self.config.get("system", {}).get("maintenance_interval", 3600.0)  # 1 saat
            self.start_maintenance_cycle(maintenance_interval)
            
            # Watchdog zamanlayıcısını başlat
            if self.config.get("system", {}).get("watchdog_enabled", True):
                self._start_watchdog()
            
            # API'yi başlat (isteğe bağlı)
            if self.config.get("api", {}).get("enabled", True):
                self._setup_api()
            
            # İşlem başarılı, durumu başlatıldı olarak ayarla
            self.transition_to(PluginState.INITIALIZED)
            logger.info("Yüz eklentisi başlatıldı.")
            return True
            
        except Exception as e:
            logger.error(f"Yüz eklentisi başlatılırken hata: {e}")
            import traceback
            logger.error(traceback.format_exc())
            self.transition_to(PluginState.ERROR)
            return False
    
    def _start_watchdog(self) -> None:
        """
        Watchdog zamanlayıcısını başlatır
        """
        try:
            watchdog_timeout = self.config.get("system", {}).get("watchdog_timeout", 10.0)
            
            def watchdog_check():
                while not self.shutdown_requested:
                    # Son kalp atışından bu yana geçen süre
                    elapsed = time.time() - self.last_heartbeat
                    
                    # Eğer zaman aşımını geçerse sistemi yeniden başlat
                    if elapsed > watchdog_timeout:
                        logger.warning(f"Watchdog zaman aşımı: {elapsed:.1f}s > {watchdog_timeout:.1f}s")
                        if self.config.get("system", {}).get("auto_restart", True):
                            logger.warning("Sistem yeniden başlatılıyor...")
                            self.restart()
                        else:
                            logger.warning("Otomatik yeniden başlatma devre dışı, sistemin manuel müdahaleye ihtiyacı var.")
                    
                    # Her 1 saniye kontrol et
                    time.sleep(1.0)
            
            # Watchdog iş parçacığını başlat
            self.watchdog_timer = threading.Thread(target=watchdog_check, daemon=True)
            self.watchdog_timer.start()
            logger.debug("Watchdog zamanlayıcısı başlatıldı.")
            
        except Exception as e:
            logger.error(f"Watchdog zamanlayıcısı başlatılırken hata: {e}")
    
    def heartbeat(self) -> None:
        """
        Watchdog kalp atışını günceller
        """
        self.last_heartbeat = time.time()
    
    def start(self) -> bool:
        """
        Yüz eklentisini çalıştırmaya başlar
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        if self.is_running:
            logger.warning("Yüz eklentisi zaten çalışıyor.")
            return True
        
        try:
            # İlk başlatma
            if not self.is_initialized and not self.initialize():
                logger.error("Yüz eklentisi başlatılamadı.")
                return False
            
            # Not: Durum geçişlerini üst sınıf yapacak, burada yapmayalım
            # Bu sayede "starting -> starting" hatası olmayacak
            
            # Burada gerekli başlatma işlemleri yapılabilir
            # ...
            
            # Çalışır durumuna geçiş üst sınıf tarafından yapılacak
            # Bu sınıfın kendi değişkenlerini güncelle
            self.is_running = True
                
            logger.info("Yüz eklentisi çalışıyor.")
            return True
            
        except Exception as e:
            logger.error(f"Yüz eklentisi başlatılırken hata: {e}")
            # Hata durumunu bildir, ama durum geçişini üst sınıfa bırak
            return False
    
    def stop(self) -> None:
        """
        Yüz eklentisini durdurur
        """
        if not self.is_running:
            logger.warning("Yüz eklentisi zaten durdurulmuş.")
            return
        
        try:
            logger.info("Yüz eklentisi durduruluyor...")
            self.shutdown_requested = True
            
            # Durdurma durumuna geçiş
            if not self.transition_to(PluginState.STOPPING):
                logger.error("Durdurma durumuna geçilemiyor.")
                return
            
            # API sunucusunu durdur
            if self.is_api_running:
                self._stop_api()
            
            # Duygu motorunu durdur
            if self.emotion_engine:
                logger.debug("Duygu motoru durduruluyor...")
                self.emotion_engine.stop()
            
            # LED kontrolcüyü durdur
            if self.led_controller:
                logger.debug("LED kontrolcü durduruluyor...")
                self.led_controller.stop()
            
            # OLED kontrolcüyü durdur
            if self.oled_controller:
                logger.debug("OLED kontrolcü durduruluyor...")
                self.oled_controller.stop()
                
            # Tema yöneticisini durdur
            if self.theme_manager:
                logger.debug("Tema yöneticisi durduruluyor...")
                self.theme_manager.stop()
            
            # Animasyon motorunu durdur
            if self.animation_engine:
                logger.debug("Animasyon motoru durduruluyor...")
                self.animation_engine.stop()
            
            # Performans optimize ediciyi durdur
            if self.performance_optimizer:
                logger.debug("Performans optimize edici durduruluyor...")
                self.performance_optimizer.stop()
            
            # Ses işleme modülünü durdur
            if self.sound_processor:
                logger.debug("Ses işleme modülü durduruluyor...")
                self.sound_processor.stop()
            
            # Bakım döngüsünü durdur
            self.stop_maintenance_cycle()
            
            # Grace period
            grace_period = self.config.get("system", {}).get("shutdown_grace_period", 2.0)
            if grace_period > 0:
                logger.debug(f"Kapanış bekleme süresi: {grace_period} saniye")
                time.sleep(grace_period)
            
            # Durmuş durumuna geçiş
            self.transition_to(PluginState.STOPPED)
            logger.info("Yüz eklentisi durduruldu.")
            
        except Exception as e:
            logger.error(f"Yüz eklentisi durdurulurken hata: {e}")
            self.transition_to(PluginState.ERROR)
    
    def restart(self) -> bool:
        """
        Yüz eklentisini yeniden başlatır
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            logger.info("Yüz eklentisi yeniden başlatılıyor...")
            self.stop()
            time.sleep(1.0)  # Tamamen durması için bekle
            
            # Yapılandırmayı yeniden yükle
            self.config = self._load_config()
            
            # Durumu sıfırla
            self.is_initialized = False
            self.is_running = False
            self.shutdown_requested = False
            
            # Yeniden başlatma için önce başlatılıyor durumuna geçiş
            self.transition_to(PluginState.INITIALIZING)
            
            # Yeniden başlat
            return self.start()
        
        except Exception as e:
            logger.error(f"Yüz eklentisi yeniden başlatılırken hata: {e}")
            self.transition_to(PluginState.ERROR)
            return False
            
    def save_state(self) -> bool:
        """
        Eklenti durumunu kaydeder
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            if not self.emotion_engine:
                logger.warning("Duygu motoru başlatılmamış, durum kaydedilemiyor.")
                return False
            
            # Durum dosya yolu
            import os
            state_dir = os.path.join(str(PROJECT_DIR), "config")
            os.makedirs(state_dir, exist_ok=True)
            state_path = os.path.join(state_dir, "face_state.json")
            
            # Durum dosyasını kaydet
            success = self.emotion_engine.save_state(state_path)
            
            # Durum raporunu oluştur ve ekle
            if success:
                try:
                    with open(state_path, 'r') as f:
                        state_data = json.load(f)
                    
                    # Yaşam döngüsü durumu ekle
                    state_data['lifecycle'] = self.get_status_report()
                    
                    # Güncellenmiş durumu kaydet
                    with open(state_path, 'w') as f:
                        json.dump(state_data, f, indent=4)
                        
                except Exception as e:
                    logger.error(f"Durum raporunu eklerken hata: {e}")
            
            return success
            
        except Exception as e:
            logger.error(f"Eklenti durumu kaydedilirken hata: {e}")
            return False
    
    def load_state(self) -> bool:
        """
        Eklenti durumunu yükler
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            if not self.emotion_engine:
                logger.warning("Duygu motoru başlatılmamış, durum yüklenemiyor.")
                return False
            
            # Durum dosya yolu
            import os
            state_path = os.path.join(str(PROJECT_DIR), "config", "face_state.json")
            
            # Durum dosyası var mı?
            if not os.path.exists(state_path):
                logger.warning(f"Durum dosyası bulunamadı: {state_path}")
                return False
            
            # Durum dosyasını yükle
            return self.emotion_engine.load_state(state_path)
            
        except Exception as e:
            logger.error(f"Eklenti durumu yüklenirken hata: {e}")
            return False
            
    # FacePluginLifecycle sınıfı için özel metodlar
    
    def perform_maintenance(self) -> None:
        """
        Bakım işlemlerini gerçekleştirir - FacePluginLifecycle'dan override edildi
        """
        try:
            logger.info("Bakım işlemleri gerçekleştiriliyor...")
            
            # Mevcut durum
            current_state = self.state
            
            # Eğer zaten bakım modundaysa veya durdurulmuşsa işlem yapma
            if current_state in [PluginState.MAINTENANCE, PluginState.SHUTDOWN, PluginState.STOPPED]:
                return
                
            # Eğer çalışma durumundaysa ve bakım gerekiyorsa
            if (current_state == PluginState.RUNNING and self.should_enter_maintenance()):
                logger.info("Bakım modu gerektiren koşullar tespit edildi.")
                
                # Durum kaydını al
                self.save_state()
                
                # Tema önbelleğini temizle
                if self.theme_manager:
                    logger.debug("Tema önbelleği temizleniyor...")
                    self.theme_manager.clear_cache()
                
                # Bellek temizliği
                import gc
                gc.collect()
                
                logger.info("Rutin bakım tamamlandı.")
            
        except Exception as e:
            logger.error(f"Bakım işlemleri gerçekleştirilirken hata: {e}")
            
    def notify_state_change(self, old_state: PluginState, new_state: PluginState) -> None:
        """
        Durum değişikliğini istemcilere bildirir
        
        Args:
            old_state (PluginState): Önceki durum
            new_state (PluginState): Yeni durum
        """
        try:
            # API mevcutsa WebSocket üzerinden bildir
            if hasattr(self, '_notify_websocket_clients') and callable(getattr(self, '_notify_websocket_clients')):
                self._notify_websocket_clients({
                    'type': 'state_change',
                    'old_state': old_state.value,
                    'new_state': new_state.value,
                    'timestamp': time.time(),
                    'uptime': self.get_uptime(),
                    'error_count': self._error_count
                })
        except Exception as e:
            logger.error(f"Durum değişikliği bildirimi gönderilemedi: {e}")
            
    def _run_startup_sequence(self) -> None:
        """
        Başlangıç animasyon sekansını çalıştırır
        """
        # Başlangıç animasyonu etkinleştirilmiş mi?
        if not self.config.get("animation", {}).get("startup_animation_enabled", True):
            logger.info("Başlangıç animasyonu devre dışı bırakıldı.")
            return
            
        try:
            logger.info("Başlangıç animasyon sekansı çalıştırılıyor...")
            
            # Animasyon motoru başlatıldı mı?
            if self.animation_engine:
                # startup_animation.json dosyasını çalıştır
                animation_name = "startup_animation"
                if self.animation_engine.play_animation(animation_name):
                    logger.info(f"Başlangıç animasyonu başlatıldı: {animation_name}")
                else:
                    logger.warning(f"Başlangıç animasyonu başlatılamadı: {animation_name}")
            else:
                logger.warning("Animasyon motoru başlatılmadı, başlangıç animasyonu çalıştırılamıyor.")
                
        except Exception as e:
            logger.error(f"Başlangıç sekansı çalıştırılırken hata: {e}")