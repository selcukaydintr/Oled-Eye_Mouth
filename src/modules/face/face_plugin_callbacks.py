#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: face_plugin_callbacks.py
# Açıklama: FacePlugin sınıfının callback işlevleri, duygu değişimi, tema değişimi vb.
# Bağımlılıklar: logging, random
# Bağlı Dosyalar: face_plugin.py, face_plugin_base.py

# Versiyon: 0.4.0
# Değişiklikler:
# - [0.4.0] FacePlugin modülerleştirildi, callback işlevleri ayrı dosyaya taşındı
# - [0.3.2] Çevresel faktörlere tepki veren ifadeler eklendi
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-02
===========================================================
"""

import logging
import random
from typing import Dict

# Loglama yapılandırması
logger = logging.getLogger("FacePluginCallbacks")

class FacePluginCallbacks:
    """
    FacePlugin callback sınıfı
    
    Bu sınıf FacePlugin sınıfı için callback işlevlerini içerir:
    - Duygu motoru için geri çağrılar
    - Tema değişimi için geri çağrılar
    - Mikro ifade geri çağrıları
    """
    
    def _register_callbacks(self) -> None:
        """
        Duygu motoru için geri çağrı fonksiyonlarını kaydeder
        """
        # Duygu değişikliği için geri çağrı
        self.emotion_engine.register_callback("emotion_changed", self._on_emotion_changed)
        
        # Duygu geçişleri için geri çağrı
        self.emotion_engine.register_callback("emotion_transition", self._on_emotion_transition)
        
        # Mikro ifadeler için geri çağrı
        self.emotion_engine.register_callback("micro_expression", self._on_micro_expression)
    
    def _on_emotion_changed(self, emotion_data: Dict) -> None:
        """
        Duygu değiştiğinde çağrılan fonksiyon
        
        Args:
            emotion_data (Dict): Duygu durumu verileri
        """
        try:
            emotion_state = emotion_data["state"]
            intensity = emotion_data["intensity"]
            
            logger.debug(f"Duygu değişti: {emotion_state}, yoğunluk: {intensity:.2f}")
            
            # OLED ekranları güncelle
            if self.oled_controller:
                self.oled_controller.set_emotion(emotion_state, intensity)
            
            # LED şeritlerini güncelle
            if self.led_controller:
                self.led_controller.animate_emotion(emotion_state, int(50 / (intensity + 0.1)))
            
            # Animasyon motorunu güncelle
            if self.animation_engine:
                self.animation_engine.set_emotion(emotion_state, intensity)
        
        except Exception as e:
            logger.error(f"Duygu değişimi işlenirken hata: {e}")
    
    def _on_emotion_transition(self, transition_data: Dict) -> None:
        """
        Duygu geçişi sürecinde çağrılan fonksiyon
        
        Args:
            transition_data (Dict): Geçiş verileri (kaynak, hedef, ilerleme, yoğunluk)
        """
        try:
            source_state = transition_data["source"]
            target_state = transition_data["state"]
            progress = transition_data["progress"]
            intensity = transition_data["intensity"]
            
            logger.debug(f"Duygu geçişi: {source_state} -> {target_state}, ilerleme: {progress:.2f}")
            
            # OLED ekranlar için yumuşak geçiş
            if self.oled_controller:
                # Kaynak ve hedef duyguyu karıştırarak yumuşak geçiş sağla
                self.oled_controller.blend_emotions(source_state, target_state, progress)
                
            # LED şeritler için geçiş animasyonu
            if self.led_controller and progress > 0.05 and progress < 0.95:
                # Geçiş ortasında özel bir animasyon seçilebilir
                if 0.4 < progress < 0.6:
                    # Geçiş animasyonu olarak 'sparkle' veya 'fade' kullanılabilir
                    animation_type = "sparkle" if random.random() > 0.5 else "fade"
                    self.led_controller.animate(animation_type, None, 30)
            
            # Animasyon motoru için geçiş
            if self.animation_engine:
                self.animation_engine.transition_emotion(source_state, target_state, progress, intensity)
        
        except Exception as e:
            logger.error(f"Duygu geçişi işlenirken hata: {e}")
    
    def _on_micro_expression(self, emotion_data: Dict) -> None:
        """
        Mikro ifade tetiklendiğinde çağrılan fonksiyon
        
        Args:
            emotion_data (Dict): Mikro ifade verileri
        """
        try:
            emotion_state = emotion_data["state"]
            intensity = emotion_data["intensity"]
            
            logger.debug(f"Mikro ifade: {emotion_state}, yoğunluk: {intensity:.2f}")
            
            # OLED ekranları güncelle (kısa süreli mikro ifade)
            if self.oled_controller:
                self.oled_controller.show_micro_expression(emotion_state, intensity, duration=0.5)
            
            # Animasyon motorunu güncelle
            if self.animation_engine:
                self.animation_engine.show_micro_expression(emotion_state, intensity, duration=0.5)
            
        except Exception as e:
            logger.error(f"Mikro ifade işlenirken hata: {e}")
            
    def _on_theme_changed(self, theme_data: Dict) -> None:
        """
        Tema değiştiğinde çağrılan fonksiyon
        
        Args:
            theme_data (Dict): Tema verileri (yeni tema adı, önceki tema adı)
        """
        try:
            new_theme = theme_data.get("new_theme", "")
            old_theme = theme_data.get("old_theme", "")
            
            logger.info(f"Tema değişti: {old_theme} -> {new_theme}")
            
            # Mevcut duygu durumunu al
            current_emotion = self.emotion_engine.get_current_emotion()
            emotion_state = current_emotion["state"]
            intensity = current_emotion["intensity"]
            
            # OLED ekranları güncelle
            if self.oled_controller:
                # Ekranları temizle ve yeni tema ile güncelle
                self.oled_controller.clear_displays()
                self.oled_controller.set_emotion(emotion_state, intensity)
                logger.debug(f"OLED ekranlar '{new_theme}' teması ile güncellendi")
            
            # LED şeritlerini güncelle
            if self.led_controller:
                # Önce temizle
                self.led_controller.clear()
                # Sonra yeni tema ile güncelle
                self.led_controller.animate_emotion(emotion_state, int(50 / (intensity + 0.1)))
                logger.debug(f"LED şeritler '{new_theme}' teması ile güncellendi")
            
            # Animasyon motorunu güncelle
            if self.animation_engine:
                self.animation_engine.set_theme(new_theme)
            
        except Exception as e:
            logger.error(f"Tema değişimi işlenirken hata: {e}")
    
    def _run_startup_sequence(self) -> None:
        """
        Başlangıç animasyon dizisini çalıştırır
        """
        try:
            logger.info("Başlangıç animasyon dizisi çalıştırılıyor...")
            
            # OLED kontrolcü ile başlangıç animasyonu
            if self.oled_controller:
                self.oled_controller.show_startup_animation()
            
            # LED kontrolcü ile başlangıç animasyonu
            if self.led_controller:
                self.led_controller.animate("rainbow", None, 30)
                import time
                time.sleep(2.0)  # Gökkuşağı animasyonu gösterildikten sonra
                self.led_controller.animate_emotion(
                    self.emotion_engine.current_emotion["state"], 
                    int(50 / (self.emotion_engine.current_emotion["intensity"] + 0.1))
                )
            
            # Animasyon motoru ile başlangıç animasyonu
            if self.animation_engine:
                self.animation_engine.show_startup_animation()
            
        except Exception as e:
            logger.error(f"Başlangıç animasyon dizisi çalıştırılırken hata: {e}")