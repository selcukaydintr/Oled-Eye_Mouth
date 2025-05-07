#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: animation_engine.py
# Açıklama: Animasyon sekanslarını yöneten ve çalıştıran modül
# Bağımlılıklar: json, threading, logging, time
# Bağlı Dosyalar: oled_controller.py, led_controller.py

# Versiyon: 0.3.3
# Değişiklikler:
# - [0.3.3] Animasyon motoru ve JSON formatı desteği eklendi
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-01
===========================================================
"""
import os
import sys
import json
import time
import logging
import threading
from typing import Dict, List, Tuple, Optional, Union, Any, Callable
from pathlib import Path

# Proje dizinini Python yoluna ekle
PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(str(PROJECT_DIR))

# Logger yapılandırması
logger = logging.getLogger("AnimationEngine")

class AnimationEngine:
    """
    Animasyon sekanslarını yöneten ve oynatmaya yarayan motor sınıfı
    """
    
    def __init__(self, config: Dict, oled_controller=None, led_controller=None):
        """
        Animasyon motorunu başlatır
        
        Args:
            config (Dict): Yapılandırma ayarları
            oled_controller: OLED kontrolcü referansı
            led_controller: LED kontrolcü referansı
        """
        self.config = config
        self.oled_controller = oled_controller
        self.led_controller = led_controller
        
        # Animasyon dizinleri
        self.animation_dir = os.path.join(PROJECT_DIR, "animation")
        self.standard_dir = os.path.join(self.animation_dir, "standard")
        self.custom_dir = os.path.join(self.animation_dir, "custom")
        
        # Animasyon çalıştırma değişkenleri
        self.current_animation = None
        self.animation_running = False
        self.animation_thread = None
        self.stop_animation = threading.Event()
        self.is_running = False
        
        # Kullanılabilir animasyonların listesi
        self.animations = {}
        
        # Animasyon eylemlerinin işlevi haritası
        self.eye_actions = {
            "clear": self._action_eyes_clear,
            "growing_circle": self._action_eyes_growing_circle,
            "blink": self._action_eyes_blink,
            "look_around": self._action_eyes_look_around,
        }
        
        self.mouth_actions = {
            "clear": self._action_mouth_clear,
            "smile": self._action_mouth_smile,
            "speak": self._action_mouth_speak,
        }
        
        self.led_actions = {
            "off": self._action_leds_off,
            "pulse": self._action_leds_pulse,
            "rainbow": self._action_leds_rainbow,
        }
        
        self.emotion_actions = {
            "set_emotion": self._action_set_emotion,
        }
        
        # Animasyonları yükle
        self.load_animations()
    
    def start(self) -> bool:
        """
        Animasyon motorunu başlatır
        
        Returns:
            bool: Başlatma başarılı ise True
        """
        try:
            logger.info("Animasyon motoru başlatılıyor...")
            
            # Animasyonları yüklediğimizden emin olalım
            if not self.animations:
                self.load_animations()
            
            # Kontrolcüleri ayarla
            from src.face_plugin import FacePlugin
            face_plugin = None
            # Eğer üst sınıf referansı var ise kontrolcüleri ondan alabiliriz
            if hasattr(sys.modules.get('__main__', None), 'face_plugin'):
                face_plugin = sys.modules['__main__'].face_plugin
                
            if face_plugin is not None:
                if self.oled_controller is None and hasattr(face_plugin, 'oled_controller'):
                    self.oled_controller = face_plugin.oled_controller
                    
                if self.led_controller is None and hasattr(face_plugin, 'led_controller'):
                    self.led_controller = face_plugin.led_controller
            
            self.is_running = True
            logger.info(f"Animasyon motoru başlatıldı. Yüklü animasyon sayısı: {len(self.animations)}")
            return True
            
        except Exception as e:
            logger.error(f"Animasyon motoru başlatılırken hata: {e}")
            return False
    
    def stop(self) -> None:
        """
        Animasyon motorunu durdurur
        """
        try:
            logger.info("Animasyon motoru durduruluyor...")
            
            # Çalışan animasyonu durdur
            self.stop_current_animation()
            
            # Motoru durdur
            self.is_running = False
            logger.info("Animasyon motoru durduruldu.")
            
        except Exception as e:
            logger.error(f"Animasyon motoru durdurulurken hata: {e}")
    
    def set_theme(self, theme_name: str) -> bool:
        """
        Temayı değiştirir
        
        Args:
            theme_name (str): Tema adı
            
        Returns:
            bool: Başarılı ise True
        """
        try:
            logger.info(f"Tema değiştiriliyor: {theme_name}")
            # Burada tema özelleştirmeleri yapılabilir
            return True
            
        except Exception as e:
            logger.error(f"Tema değiştirilirken hata: {e}")
            return False
    
    def set_emotion(self, emotion: str, intensity: float = 1.0) -> bool:
        """
        Duygu durumunu ayarlar
        
        Args:
            emotion (str): Duygu adı
            intensity (float): Yoğunluk (0.0-1.0)
            
        Returns:
            bool: Başarılı ise True
        """
        try:
            logger.debug(f"Duygu durumu ayarlanıyor: {emotion}, yoğunluk: {intensity}")
            # Gerçek uygulamada burada duygu durumuna göre animasyonları seçebiliriz
            return True
            
        except Exception as e:
            logger.error(f"Duygu durumu ayarlanırken hata: {e}")
            return False
            
    def show_micro_expression(self, emotion: str, intensity: float = 1.0, duration: float = 0.5) -> bool:
        """
        Mikro ifade gösterir
        
        Args:
            emotion (str): Duygu adı
            intensity (float): Yoğunluk (0.0-1.0)
            duration (float): Süre (saniye)
            
        Returns:
            bool: Başarılı ise True
        """
        try:
            logger.debug(f"Mikro ifade gösteriliyor: {emotion}, yoğunluk: {intensity}, süre: {duration}")
            # Gerçek uygulamada burada kısa süreli animasyon oynatılabilir
            return True
            
        except Exception as e:
            logger.error(f"Mikro ifade gösterilirken hata: {e}")
            return False
    
    def show_startup_animation(self) -> bool:
        """
        Başlangıç animasyonunu oynatır
        
        Returns:
            bool: Başarılı ise True
        """
        try:
            # Startup animasyonunu bul ve oynat
            startup_animations = ["startup", "boot", "welcome"]
            
            for anim_name in startup_animations:
                if anim_name in self.animations:
                    logger.info(f"Başlangıç animasyonu oynatılıyor: {anim_name}")
                    return self.play_animation(anim_name)
            
            logger.warning("Başlangıç animasyonu bulunamadı.")
            return False
            
        except Exception as e:
            logger.error(f"Başlangıç animasyonu oynatılırken hata: {e}")
            return False
            
    def transition_emotion(self, source_state: str, target_state: str, progress: float, intensity: float) -> bool:
        """
        İki duygu arasında geçiş için animasyon yapar
        
        Args:
            source_state (str): Kaynak duygu durumu
            target_state (str): Hedef duygu durumu
            progress (float): Geçiş ilerlemesi (0.0-1.0)
            intensity (float): Duygu yoğunluğu (0.0-1.0)
            
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            # Başlangıçta event trigger yaparak geçişin başladığını bildir
            if not hasattr(self, '_transition_reported'):
                self._transition_reported = {}
            
            transition_key = f"{source_state}_{target_state}"
            if transition_key not in self._transition_reported:
                self._transition_reported[transition_key] = set()
            
            # Parametreleri doğrula
            if not 0.0 <= progress <= 1.0:
                logger.warning(f"Geçersiz geçiş ilerlemesi: {progress}, sınırlar [0.0-1.0] içinde değer bekleniyor")
                progress = max(0.0, min(1.0, progress))  # Aralık içine sabitle
            
            if not 0.0 <= intensity <= 1.0:
                logger.warning(f"Geçersiz yoğunluk değeri: {intensity}, sınırlar [0.0-1.0] içinde değer bekleniyor")
                intensity = max(0.0, min(1.0, intensity))  # Aralık içine sabitle
            
            # Geçişi yumuşatmak için spesifik bir easing fonksiyonu uygula
            eased_progress = self._ease_transition(progress)
            
            # İlerleme durumu bildirimleri için %10'luk dönüm noktaları (performans için)
            for progress_point in [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]:
                if abs(progress - progress_point) < 0.05 and progress_point not in self._transition_reported[transition_key]:
                    # Bu dönüm noktası daha önce bildirilmediyse, bildir
                    self._transition_reported[transition_key].add(progress_point)
                    
                    # Önemli bir dönüm noktasına ulaşıldığında callback ile bildir
                    event_data = {
                        "source": source_state,
                        "state": target_state,
                        "raw_progress": progress,
                        "eased_progress": eased_progress,
                        "intensity": intensity,
                        "milestone": True,
                        "milestone_value": progress_point
                    }
                    self._trigger_animation_event("emotion_transition", event_data)
                    
                    # Dönüm noktalarında özel LED efektleri
                    if progress_point in [0.25, 0.5, 0.75]:
                        threading.Thread(
                            target=self._transition_led_effect,
                            args=(source_state, target_state, eased_progress),
                            daemon=True
                        ).start()
            
            # Geçiş için özel bir animasyon bul ve oynat
            transition_animation = f"{source_state}_to_{target_state}"
            fallback_animation = "emotion_transition"
            
            # İleri seviye kullanım: Eğer tam geçiş animasyonu varsa, oynat
            if progress == 0.5 and transition_animation in self.animations:
                # Direkt animasyonu çağırmak yerine geçiş bilgisini ilet (recursive çağrıyı önle)
                return self._play_transition_animation(transition_animation, source_state, target_state, intensity)
            
            # Veya varsayılan geçiş animasyonu kullan (emotion_transition.json)
            elif progress == 0.5 and fallback_animation in self.animations:
                return self._play_transition_animation(fallback_animation, source_state, target_state, intensity)
                
            # OLED kontrolcü ile duygu ifadelerini güncelle
            if self.oled_controller:
                # İki duygu durumu arasındaki karışımı hesapla ve uygula
                self._update_emotion_blend(source_state, target_state, eased_progress, intensity)
            
            # Geçiş tamamlandı mı kontrolü
            if progress >= 1.0:
                # Geçiş tamamlandığında bildir ve temizle
                if transition_key in self._transition_reported:
                    del self._transition_reported[transition_key]
                    
                # Tamamlanma olayını tetikle
                self._trigger_animation_event("emotion_transition_completed", {
                    "source": source_state,
                    "state": target_state,
                    "intensity": intensity
                })
                
                logger.debug(f"Duygu geçişi tamamlandı: {source_state} -> {target_state}")
            
            return True
            
        except Exception as e:
            logger.error(f"Duygu geçişi animasyonu sırasında hata: {e}")
            logger.debug("Hata ayrıntıları:", exc_info=True)
            
            # Hata bildirimini gönder - dashboard'a hata göstermesi için
            self._trigger_animation_event("animation_error", {
                "animation": f"transition_{source_state}_to_{target_state}",
                "error": str(e),
                "code": 1001,  # Geçiş hatası kodu
                "recoverable": True,  # Genellikle bu tür hatalar giderilebilir
                "source_state": source_state,
                "target_state": target_state,
                "progress": progress
            })
            
            # Başarısız geçiş durumunda kurtarma mekanizması
            try:
                # Ağzı ve gözleri normal duruma getir (oluşabilecek garip ifadeleri temizle)
                if self.oled_controller:
                    self.oled_controller.set_emotion("neutral", intensity)
                
                # LEDleri sabit bir renge getir
                if self.led_controller:
                    self.led_controller.clear()
                    
            except Exception as recovery_error:
                logger.error(f"Geçiş hatası sonrası kurtarma başarısız: {recovery_error}")
            
            return False
    
    def _ease_transition(self, progress: float) -> float:
        """
        Geçiş ilerlemesini yumuşatmak için easing fonksiyonu uygular
        
        Args:
            progress (float): Ham ilerleme (0.0-1.0)
            
        Returns:
            float: Yumuşatılmış ilerleme (0.0-1.0)
        """
        # Cubic easing fonksiyonu (yavaş başla, hızlan, yavaş bitir)
        if progress < 0.5:
            return 4 * (progress ** 3)
        else:
            return 1 - (4 * ((1 - progress) ** 3))
    
    def _play_transition_animation(self, animation_name: str, source_state: str, target_state: str, intensity: float) -> bool:
        """
        Geçiş animasyonunu oynatır
        
        Args:
            animation_name (str): Oynatılacak animasyon adı
            source_state (str): Kaynak duygu durumu
            target_state (str): Hedef duygu durumu
            intensity (float): Duygu yoğunluğu
            
        Returns:
            bool: Başarılı ise True
        """
        try:
            # Çalışan bir geçiş animasyonu var mı kontrol et
            if hasattr(self, '_transition_animation_running') and self._transition_animation_running:
                # İki geçiş animasyonunu üst üste bindirmek istemiyoruz
                logger.debug(f"Zaten bir geçiş animasyonu çalışıyor, yeni istek iptal edildi")
                return False
            
            # Bu geçiş için özel olarak düzenlenecek animasyon verilerini kopyala
            animation_data = self.animations[animation_name].copy()
            
            # Animasyon meta verilerini geçişe göre güncelle
            animation_data["metadata"] = animation_data.get("metadata", {}).copy()
            animation_data["metadata"]["source_state"] = source_state
            animation_data["metadata"]["target_state"] = target_state
            animation_data["metadata"]["intensity"] = intensity
            
            # Geçiş durumunu işaretle
            self._transition_animation_running = True
            
            # Animasyonu yeni bir thread'de çalıştır
            threading.Thread(
                target=self._run_transition_animation,
                args=(animation_data,),
                daemon=True
            ).start()
            
            return True
            
        except Exception as e:
            logger.error(f"Geçiş animasyonu başlatılırken hata: {e}")
            self._transition_animation_running = False
            return False
    
    def _run_transition_animation(self, animation_data: Dict) -> None:
        """
        Geçiş animasyonunu çalıştırır ve tamamlandığında temizlik yapar
        
        Args:
            animation_data (Dict): Animasyon verileri
        """
        try:
            # Animasyonu normal şekilde çalıştır (mevcut metodu kullan)
            self._run_animation(animation_data)
        except Exception as e:
            logger.error(f"Geçiş animasyonu çalıştırılırken hata: {e}")
        finally:
            # Geçiş durumunu temizle
            self._transition_animation_running = False
    
    def _update_emotion_blend(self, source_state: str, target_state: str, progress: float, intensity: float) -> None:
        """
        İki duygu durumu arasında karışım uygula
        
        Args:
            source_state (str): Kaynak duygu durumu
            target_state (str): Hedef duygu durumu
            progress (float): Geçiş ilerlemesi (0.0-1.0)
            intensity (float): Duygu yoğunluğu (0.0-1.0)
        """
        if not self.oled_controller:
            return
            
        try:
            # OLED kontrolcü ile duygu ifadelerini güncelle
            if hasattr(self.oled_controller, 'blend_emotions'):
                # Yüksek seviye API - oled_controller'da blend_emotions metodu varsa kullan
                self.oled_controller.blend_emotions(source_state, target_state, progress, intensity)
            else:
                # Düşük seviye API - manuel olarak duygular arasında geçiş yap
                if progress < 0.5:
                    # İlk yarıda kaynak duygu baskın
                    effective_intensity = intensity * (1 - progress * 2)
                    self.oled_controller.set_emotion(source_state, effective_intensity)
                else:
                    # İkinci yarıda hedef duygu baskın
                    effective_intensity = intensity * ((progress - 0.5) * 2)
                    self.oled_controller.set_emotion(target_state, effective_intensity)
                    
        except Exception as e:
            logger.error(f"Duygu karışımı güncellenirken hata: {e}")
    
    def _transition_led_effect(self, source_state: str, target_state: str, progress: float) -> None:
        """
        Geçiş anında LED efekti uygular
        
        Args:
            source_state (str): Kaynak duygu durumu
            target_state (str): Hedef duygu durumu
            progress (float): Geçiş ilerlemesi (0.0-1.0)
        """
        if not self.led_controller:
            return
            
        try:
            # Duygu durumlarına göre farklı LED efektleri seç
            if progress < 0.3:
                # Başlangıç efekti
                self.led_controller.pulse([0, 0, 255], 30)
            elif 0.3 <= progress < 0.7:
                # Orta nokta efekti
                self.led_controller.fade([255, 255, 255], 40)
            else:
                # Bitiş efekti
                self.led_controller.pulse([0, 255, 0], 30)
                
        except Exception as e:
            logger.debug(f"LED geçiş efekti uygulanırken hata: {e}")
    
    def _trigger_animation_event(self, event_type: str, event_data: Dict) -> None:
        """
        Animasyon olayını tetikler ve callback'leri çağırır
        
        Args:
            event_type (str): Olay tipi
            event_data (Dict): Olay verileri
        """
        try:
            # Callback sistemi - callback var mı kontrol et
            if hasattr(self, 'callbacks') and isinstance(self.callbacks, dict):
                if event_type in self.callbacks:
                    for callback in self.callbacks[event_type]:
                        try:
                            callback(event_data)
                        except Exception as e:
                            logger.error(f"Callback çalıştırılırken hata: {e}")
        except Exception as e:
            logger.error(f"Olay tetiklenirken hata: {e}")
    
    def load_animations(self) -> None:
        """
        Tüm animasyon dosyalarını yükler
        """
        logger.info("Animasyonlar yükleniyor...")
        
        # Öncelikle standart animasyonlar
        self._load_animations_from_dir(self.standard_dir)
        
        # Sonra özel animasyonlar (aynı isimli olanlar standart olanları geçersiz kılar)
        self._load_animations_from_dir(self.custom_dir)
        
        logger.info(f"Toplam {len(self.animations)} animasyon yüklendi")
    
    def _load_animations_from_dir(self, directory: str) -> None:
        """
        Belirtilen dizindeki tüm JSON animasyonlarını yükler
        
        Args:
            directory (str): Animasyonların bulunduğu dizin
        """
        if not os.path.exists(directory):
            logger.warning(f"Dizin bulunamadı: {directory}")
            return
            
        for filename in os.listdir(directory):
            if not filename.endswith(".json"):
                continue
                
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r') as f:
                    animation_data = json.load(f)
                
                # Animasyon adını dosya adından al (uzantısız)
                anim_name = os.path.splitext(filename)[0]
                
                # Animasyon verilerini doğrula
                if not self._validate_animation(animation_data):
                    logger.error(f"Geçersiz animasyon formatı: {filepath}")
                    continue
                
                # Animasyonu koleksiyona ekle
                self.animations[anim_name] = animation_data
                logger.debug(f"Animasyon yüklendi: {anim_name}")
                
            except Exception as e:
                logger.error(f"Animasyon dosyası yüklenirken hata: {filepath} - {e}")
    
    def _validate_animation(self, animation_data: Dict) -> bool:
        """
        Animasyon verilerini doğrular
        
        Args:
            animation_data (Dict): Animasyon verileri
            
        Returns:
            bool: Doğrulama başarılı ise True
        """
        # Temel animasyon yapısını kontrol et
        if not isinstance(animation_data, dict):
            return False
        
        # Metadata alanını kontrol et
        if "metadata" not in animation_data or not isinstance(animation_data["metadata"], dict):
            return False
        
        # Adım sırasını kontrol et
        if "sequence" not in animation_data or not isinstance(animation_data["sequence"], list):
            return False
        
        # Tüm değil, ama basit kontroller yeterlidir
        return True
    
    def get_animation_names(self) -> List[str]:
        """
        Mevcut animasyon adlarını döndürür
        
        Returns:
            List[str]: Animasyon adları listesi
        """
        return list(self.animations.keys())
    
    def get_animation_info(self, name: str) -> Optional[Dict]:
        """
        Animasyon meta bilgilerini döndürür
        
        Args:
            name (str): Animasyon adı
            
        Returns:
            Optional[Dict]: Animasyon bilgileri veya bulunamazsa None
        """
        if name not in self.animations:
            return None
        
        animation_data = self.animations[name]
        
        # Metadata bilgilerinden bir kopya döndür
        return animation_data.get("metadata", {})
    
    def get_animation_details(self, name: str) -> Optional[Dict]:
        """
        Animasyon detaylarını döndürür (tam içerik)
        
        Args:
            name (str): Animasyon adı
            
        Returns:
            Optional[Dict]: Animasyon detayları veya bulunamazsa None
        """
        if name not in self.animations:
            return None
        
        return self.animations[name]
    
    def save_animation(self, name: str, animation_data: Dict) -> bool:
        """
        Animasyonu dosyaya kaydeder
        
        Args:
            name (str): Animasyon adı (dosya adı)
            animation_data (Dict): Animasyon verileri
            
        Returns:
            bool: Başarılı ise True
        """
        try:
            # Animasyon formatını doğrula
            if not self._validate_animation(animation_data):
                logger.error(f"Geçersiz animasyon formatı: {name}")
                return False
            
            # Dosya adını oluştur
            filename = f"{name}.json"
            if not filename.endswith(".json"):
                filename += ".json"
            
            # Özel animasyonlar dizinine kaydet
            filepath = os.path.join(self.custom_dir, filename)
            
            # Özel animasyonlar dizininin varlığını kontrol et
            if not os.path.exists(self.custom_dir):
                os.makedirs(self.custom_dir)
            
            # Dosyaya yaz
            with open(filepath, 'w') as f:
                json.dump(animation_data, f, indent=2)
            
            # Animasyonu koleksiyona ekle veya güncelle
            self.animations[name] = animation_data
            
            logger.info(f"Animasyon kaydedildi: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Animasyon kaydedilirken hata: {name} - {e}")
            return False
    
    def delete_animation(self, name: str) -> bool:
        """
        Animasyonu siler
        
        Args:
            name (str): Animasyon adı
            
        Returns:
            bool: Başarılı ise True
        """
        try:
            # Standart animasyonların silinmesini engelle (sadece özel animasyonlar silinebilir)
            standard_filepath = os.path.join(self.standard_dir, f"{name}.json")
            if os.path.exists(standard_filepath):
                logger.warning(f"Standart animasyonlar silinemez: {name}")
                return False
            
            # Özel animasyon dosyasını kontrol et
            custom_filepath = os.path.join(self.custom_dir, f"{name}.json")
            if not os.path.exists(custom_filepath):
                logger.warning(f"Animasyon bulunamadı: {name}")
                return False
            
            # Dosyayı sil
            os.remove(custom_filepath)
            
            # Animasyonu koleksiyondan kaldır
            if name in self.animations:
                del self.animations[name]
            
            logger.info(f"Animasyon silindi: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Animasyon silinirken hata: {name} - {e}")
            return False
    
    def play_animation(self, name: str) -> bool:
        """
        Belirtilen animasyonu oynatır
        
        Args:
            name (str): Oynatılacak animasyon adı
            
        Returns:
            bool: Başarılı ise True
        """
        if name not in self.animations:
            logger.warning(f"Animasyon bulunamadı: {name}")
            return False
        
        # Zaten çalışan bir animasyon varsa durdur
        self.stop_current_animation()
        
        try:
            # Animasyon verilerini al
            animation_data = self.animations[name]
            
            # Mevcut animasyonu ayarla
            self.current_animation = name
            
            # Animasyon iş parçacığını başlat
            self.animation_thread = threading.Thread(target=self._run_animation, args=(animation_data,))
            self.animation_thread.daemon = True
            self.animation_thread.start()
            
            self.animation_running = True
            
            logger.info(f"Animasyon oynatılıyor: {name}")
            return True
            
        except Exception as e:
            logger.error(f"Animasyon oynatılırken hata: {name} - {e}")
            self.animation_running = False
            self.current_animation = None
            return False
    
    def stop_current_animation(self) -> None:
        """
        Çalışan animasyonu durdurur
        """
        if not self.animation_running:
            return
        
        # Durdurma sinyali gönder
        self.stop_animation.set()
        
        # İş parçacığının tamamlanmasını bekle
        if self.animation_thread and self.animation_thread.is_alive():
            self.animation_thread.join(timeout=1.0)
        
        self.animation_running = False
        self.current_animation = None
        self.stop_animation.clear()
        
        logger.info("Animasyon durduruldu")
    
    def _run_animation(self, animation_data: Dict) -> None:
        """
        Animasyon sekansını çalıştırır
        
        Args:
            animation_data (Dict): Animasyon verileri
        """
        if not animation_data or "sequence" not in animation_data:
            logger.error("Geçersiz animasyon verileri")
            return
        
        sequence = animation_data["sequence"]
        
        try:
            # Adımları zamana göre sırala ve sadece bir kez sırala
            sorted_steps = sorted(sequence, key=lambda x: x.get("time", 0))
            
            # Animasyon başlangıç zamanını kaydet
            self.animation_start_time = time.time()
            start_time = self.animation_start_time
            
            # Adımları önceden işlenecek gruplara ayır - performans optimizasyonu
            max_time = 0
            if sorted_steps:
                max_time = sorted_steps[-1].get("time", 0)
            
            # Her adım için, zaman gelince eylemleri gerçekleştir
            step_index = 0
            step_count = len(sorted_steps)
            
            while step_index < step_count:
                # Durdurma sinyali kontrol et
                if self.stop_animation.is_set():
                    break
                
                current_time = time.time() - start_time
                
                # Şu anki zamanda çalıştırılması gereken tüm adımları bul ve çalıştır
                steps_to_execute = []
                
                # Mevcut zamanda yürütülmesi gereken adımları topla
                while step_index < step_count:
                    step = sorted_steps[step_index]
                    step_time = step.get("time", 0)
                    
                    if step_time <= current_time:
                        steps_to_execute.append(step)
                        step_index += 1
                    else:
                        break
                
                # Toplanmış adımları yürüt
                for step in steps_to_execute:
                    self._execute_step(step)
                
                # Adımlar arasında CPU'yu rahatlatmak için kısa bir bekleme
                if not steps_to_execute and step_index < step_count:
                    next_step = sorted_steps[step_index]
                    next_time = next_step.get("time", 0)
                    wait_time = max(0.001, min(next_time - current_time, 0.05))  # En fazla 50ms bekle
                    
                    if self.stop_animation.wait(timeout=wait_time):
                        break
                
                # Animasyon süresi doldu mu kontrol et
                if max_time > 0 and current_time > max_time + 0.5:  # 0.5 saniye tolerans
                    break
            
        except Exception as e:
            logger.error(f"Animasyon çalıştırılırken hata: {e}")
        finally:
            # Animasyonu temizle
            self.animation_running = False
            self.current_animation = None
    
    def _execute_step(self, step: Dict) -> None:
        """
        Animasyon adımını yürütür
        
        Args:
            step (Dict): Animasyon adımı
        """
        try:
            # Performans optimizasyonu: Eylemleri önbelleğe alarak tekrar tekrar getattr çağırmayı engelle
            if not hasattr(self, '_action_cache'):
                # Eylem fonksiyonlarını bir kere önbelleğe al
                self._action_cache = {}
            
            # Eylemi önbellekten al veya önbelleğe ekle
            def get_action_func(component, action):
                cache_key = f"{component}_{action}"
                if cache_key not in self._action_cache:
                    action_name = f"_action_{component}_{action}"
                    if hasattr(self, action_name):
                        self._action_cache[cache_key] = getattr(self, action_name)
                    else:
                        logger.warning(f"Eylem bulunamadı: {action_name}")
                        self._action_cache[cache_key] = None
                return self._action_cache[cache_key]
            
            # Performans optimizasyonu: Animasyon adımlarını önceliğe göre sırala 
            # (Ses olayları önce, görsel efektler sonra)
            all_actions = []
            
            # Öncelik 1 - Ses ve duygu ayarları
            if "sound" in step:
                all_actions.append(("sound", step["sound"]))
            if "emotion" in step:
                all_actions.append(("emotion", step["emotion"]))
            
            # Öncelik 2 - LED efektleri
            if "leds" in step:
                all_actions.append(("leds", step["leds"]))
            
            # Öncelik 3 - Ekran efektleri
            if "eyes" in step:
                all_actions.append(("eyes", step["eyes"]))
            if "mouth" in step:
                all_actions.append(("mouth", step["mouth"]))
            
            # Performans optimizasyonu: Hafıza kullanımını azaltmak için
            # eylemleri tek seferde işle
            for component, action_data in all_actions:
                if not action_data.get("action"):
                    continue
                
                action_name = action_data.get("action", "")
                params = action_data.get("params", {})
                
                # Bellek optimizasyonu: Büyük parametreleri kontrol et
                if params and isinstance(params, dict):
                    # Büyük veri yapılarını optimize et (örn. büyük listeler)
                    for key, value in params.items():
                        # Eğer liste uzunsa ve azaltılabilirse
                        if isinstance(value, list) and len(value) > 100:
                            # Örnek: Çok fazla nokta içeren koordinat listeleri 
                            # gibi büyük listeleri örnekleyerek küçült
                            params[key] = value[::2]  # Her ikinci değeri al
                
                # Eylem fonksiyonunu al
                action_func = get_action_func(component, action_name)
                
                # Eylemi yürüt
                if action_func:
                    # Performans takibi
                    action_start = time.perf_counter()
                    action_func(params)
                    action_time = time.perf_counter() - action_start
                    
                    # Performans uyarısı - yavaş eylemler için log
                    if action_time > 0.1:  # 100ms'den uzun süren eylemler
                        logger.debug(f"Performans uyarısı: {component}_{action_name} eylemi {action_time:.3f} sn sürdü")
                        
        except Exception as e:
            logger.error(f"Adım yürütülürken hata: {e}")
            logger.error(f"Adım verisi: {step}")
    
    # Eylem fonksiyonları
    def _action_eyes_clear(self, params: Dict) -> None:
        """Gözleri temizler"""
        if self.oled_controller:
            self.oled_controller.clear_eyes()
    
    def _action_eyes_blink(self, params: Dict) -> None:
        """Göz kırpma"""
        duration = params.get("duration", 0.2)
        if self.oled_controller:
            self.oled_controller.blink(duration)
    
    def _action_eyes_look_around(self, params: Dict) -> None:
        """Etrafı izleme"""
        duration = params.get("duration", 1.0)
        points = params.get("points", [[-0.5, 0], [0.5, 0], [0, 0]])
        if self.oled_controller:
            self.oled_controller.look_at_points(points, duration)
    
    def _action_eyes_growing_circle(self, params: Dict) -> None:
        """Büyüyen çember"""
        duration = params.get("duration", 1.0)
        if self.oled_controller:
            self.oled_controller.show_growing_circle(duration)
    
    def _action_mouth_clear(self, params: Dict) -> None:
        """Ağzı temizler"""
        if self.oled_controller:
            self.oled_controller.clear_mouth()
    
    def _action_mouth_smile(self, params: Dict) -> None:
        """Gülümseme"""
        emotion = params.get("emotion", "happy")
        intensity = params.get("intensity", 0.7)
        if self.oled_controller:
            self.oled_controller.set_mouth_expression(emotion, intensity)
    
    def _action_mouth_speak(self, params: Dict) -> None:
        """Konuşma animasyonu"""
        duration = params.get("duration", 1.0)
        pattern = params.get("pattern", "default")
        if self.oled_controller:
            self.oled_controller.animate_speaking(duration, pattern)
    
    def _action_leds_off(self, params: Dict) -> None:
        """LED'leri kapatır"""
        if self.led_controller:
            self.led_controller.clear()
    
    def _action_leds_pulse(self, params: Dict) -> None:
        """LED'leri yanıp söndürür"""
        speed = params.get("speed", 50)
        color = params.get("color", [0, 0, 255])  # Varsayılan mavi
        if self.led_controller:
            self.led_controller.pulse(color, speed)
    
    def _action_leds_rainbow(self, params: Dict) -> None:
        """LED'lerde gökkuşağı efekti"""
        speed = params.get("speed", 30)
        if self.led_controller:
            self.led_controller.rainbow(speed)
    
    def _action_set_emotion(self, params: Dict) -> None:
        """Duygu durumunu ayarlar"""
        emotion = params.get("emotion", "neutral")
        intensity = params.get("intensity", 0.7)
        transition = params.get("transition", 0.5)
        
        if hasattr(sys.modules.get('__main__', None), 'face_plugin'):
            face_plugin = sys.modules['__main__'].face_plugin
            if face_plugin and hasattr(face_plugin, 'set_emotion'):
                face_plugin.set_emotion(emotion, intensity, transition)
    
    def get_animation_status(self) -> Dict:
        """
        Mevcut animasyon durumunu döndürür
        
        Returns:
            Dict: Animasyon durum bilgileri
        """
        status = {
            "playing": self.animation_running,
            "current_animation": self.current_animation,
            "progress": 0.0
        }
        
        # İlerleme bilgisini hesapla
        if self.animation_running and self.current_animation in self.animations:
            animation_data = self.animations[self.current_animation]
            duration = animation_data.get("metadata", {}).get("duration", 0)
            
            if duration > 0:
                # Mevcut zamanı al
                current_time = time.time()
                
                # Animasyon başlangıç zamanını tahmin et
                if hasattr(self, 'animation_start_time'):
                    elapsed = current_time - self.animation_start_time
                    progress = min(elapsed / duration, 1.0)
                    status["progress"] = progress
        
        return status

# Animasyon motoru test kodu
if __name__ == "__main__":
    # Logging yapılandırması
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test yapılandırması
    test_config = {
        "animation": {
            "base_dir": "animation"
        }
    }
    
    print("Animasyon Motoru Testi")
    print("----------------------")
    
    # Animasyon motoru örneği oluştur
    engine = AnimationEngine(test_config)
    
    # Mevcut animasyonları listele
    animations = engine.get_animation_names()
    print(f"Yüklenen Animasyonlar ({len(animations)}): {animations}")
    
    # Her bir animasyon hakkında bilgiler
    for anim_name in animations:
        info = engine.get_animation_info(anim_name)
        if info:
            print(f"\nAnimasyon: {anim_name}")
            print(f"  İsim: {info['name']}")
            print(f"  Açıklama: {info['description']}")
            print(f"  Süre: {info['duration']} saniye")
    
    # Kontrolcü yokken animasyonları test edelim - sadece yükleme kontrolü
    if animations:
        anim_to_test = animations[0]  # İlk animasyonu test et
        print(f"\nAnimasyon testi: {anim_to_test}")
        print("Not: Kontrolcü olmadan test edildiği için eylemler uygulanmayacaktır")
        
        result = engine.play_animation(anim_to_test)
        print(f"Animasyon başlatma sonucu: {'Başarılı' if result else 'Başarısız'}")
        
        # Animasyonun tamamlanması için bekle
        if result:
            info = engine.get_animation_info(anim_to_test)
            duration = info.get("duration", 5.0)
            print(f"{anim_to_test} animasyonu çalışıyor ({duration} saniye)...")
            time.sleep(duration + 1)
    
    print("\nTest tamamlandı")
