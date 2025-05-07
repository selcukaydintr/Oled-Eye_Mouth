#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: emotion_engine_transitions.py
# Açıklama: Duygu motoru geçiş yönetimi ve mantığını içerir.
# Bağımlılıklar: logging, time, math
# Bağlı Dosyalar: emotion_states.py, emotion_engine_base.py, emotion_engine.py

# Versiyon: 0.5.0
# Değişiklikler:
# - [0.5.0] Duygu geçişleri iyileştirildi, easing fonksiyonları eklendi, bellek kullanımı optimize edildi
# - [0.4.0] emotion_engine.py dosyasından bölündü (modüler mimari)
# - [0.3.0] Duygu geçişlerini daha akıcı hale getirme ve alt tipler için gelişmiş destekler eklendi
# - [0.2.0] Duygu hafıza sistemi ve duygu tepki eğrileri geliştirildi
# - [0.1.0] Temel duygu motoru sınıfı oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-02
===========================================================
"""

import time
import logging
import random
import math
from typing import Dict, Tuple, List, Callable, Optional, Union

# Duygu durumlarını içe aktaralım
from src.modules.emotion_states import EmotionState, EMOTION_TRANSITION_MATRIX, EMOTION_RESPONSE_CURVES

# Logger yapılandırması
logger = logging.getLogger("EmotionEngine")


class EmotionTransitionsMixin:
    """
    Duygu geçişleri mixin sınıfı
    
    Bu sınıf, duygular arasında geçişleri yönetme yöntemlerini sağlar.
    EmotionEngine tarafından mixin olarak kullanılır.
    """
    
    def __init_transitions(self):
        """
        Duygu geçiş değişkenlerini başlatır.
        Bu metot, ana sınıfın __init__ metodundan çağrılmalıdır.
        """
        # Geçiş özellikleri
        try:
            emotion_config = getattr(self, 'emotion_config', {})
            # Geçiş hızı çarpanı
            self.transition_speed = emotion_config.get("transition_speed", 1.0)
            # Geçiş easing fonksiyonu
            self.transition_easing = emotion_config.get("transition_easing", "easeInOutCubic")
            # Mikro ifade geçiş olasılığı
            self.micro_expression_transition_probability = emotion_config.get("micro_expression_prob", 0.3)
        except AttributeError:
            # Varsayılan değerler
            self.transition_speed = 1.0
            self.transition_easing = "easeInOutCubic"
            self.micro_expression_transition_probability = 0.3
        
        # Easing fonksiyonları sözlüğü
        self.easing_functions = {
            "linear": lambda x: x,
            "easeInQuad": lambda x: x * x,
            "easeOutQuad": lambda x: 1 - (1 - x) * (1 - x),
            "easeInOutQuad": lambda x: 2 * x * x if x < 0.5 else 1 - pow(-2 * x + 2, 2) / 2,
            "easeInCubic": lambda x: x * x * x,
            "easeOutCubic": lambda x: 1 - pow(1 - x, 3),
            "easeInOutCubic": lambda x: 4 * x * x * x if x < 0.5 else 1 - pow(-2 * x + 2, 3) / 2,
            "easeInExpo": lambda x: 0 if x == 0 else pow(2, 10 * x - 10),
            "easeOutExpo": lambda x: 1 if x == 1 else 1 - pow(2, -10 * x),
            "easeInOutExpo": lambda x: (
                0 if x == 0 else 
                1 if x == 1 else 
                pow(2, 10 * x - 10) / 2 if x < 0.5 else 
                (2 - pow(2, -10 * x - 10)) / 2
            )
        }
        
        # Aktif geçiş listesi - birden çok geçişi desteklemek için
        self.active_transitions = []
        
        logger.info(f"Duygu geçiş modülü başlatıldı. Geçiş hızı: {self.transition_speed}, Easing: {self.transition_easing}")
    
    def _update_emotion_transition(self) -> None:
        """
        Duygu geçiş durumunu günceller
        """
        # Ana geçişi kontrol et
        target = getattr(self.current_emotion, "target", None)
        if target and target.get("progress", 1.0) < 1.0:
            self._process_single_transition(target)
            return
            
        # Aktif geçişleri kontrol et ve yönet
        if not self.active_transitions:
            return
            
        completed_transitions = []
        for idx, transition in enumerate(self.active_transitions):
            if transition["progress"] >= 1.0:
                completed_transitions.append(idx)
                continue
                
            # Geçişi işle
            self._process_single_transition(transition)
            
            # Geçiş tamamlandı mı?
            if transition["progress"] >= 1.0:
                completed_transitions.append(idx)
                
                # Ana duygu geçişiyse mevcut duygu durumunu güncelle
                if transition.get("is_main_transition", False):
                    self._complete_main_transition(transition)
        
        # Tamamlanan geçişleri kaldır
        for idx in sorted(completed_transitions, reverse=True):
            self.active_transitions.pop(idx)
    
    def _process_single_transition(self, transition: Dict) -> None:
        """
        Tek bir duygu geçişini işler
        
        Args:
            transition (Dict): Geçiş bilgisi
        """
        # Geçiş ilerleme hızını hesapla
        current_state = self.current_emotion["state"]
        target_state = transition["state"]
        
        # Geçiş matrisinden kolaylık faktörünü al
        transition_ease = EMOTION_TRANSITION_MATRIX.get(
            current_state, {}).get(target_state, 0.5)
        
        # Temel hız, yapılandırmadan ve hız faktöründen gelir
        base_speed = 0.05 * self.transition_speed  # Her döngüde yaklaşık %5 ilerleme
        
        # İlerlemeyi güncelle
        transition["progress"] += base_speed * transition_ease
        transition["progress"] = min(1.0, transition["progress"])
        
        # Easing fonksiyonunu uygula
        easing_func = self.easing_functions.get(
            self.transition_easing, self.easing_functions["easeInOutCubic"])
        eased_progress = easing_func(transition["progress"])
        
        # OLED Controller için geçiş bilgilerini gönder
        transition_data = {
            "source": current_state,
            "state": target_state,
            "raw_progress": transition["progress"],
            "eased_progress": eased_progress,
            "intensity": transition["intensity"],
            "is_main_transition": transition.get("is_main_transition", False)
        }
        
        # Geri çağrıları tetikle
        self._trigger_callbacks("emotion_transition", transition_data)
    
    def _complete_main_transition(self, transition: Dict) -> None:
        """
        Ana duygu geçişini tamamlar
        
        Args:
            transition (Dict): Geçiş bilgisi
        """
        # Geçişi tamamla
        self.current_emotion["state"] = transition["state"]
        self.current_emotion["intensity"] = transition["intensity"]
        self.current_emotion["start_time"] = time.time()
        
        logger.debug(f"Duygu geçişi tamamlandı: {transition['state']}, yoğunluk: {transition['intensity']:.2f}")
        
        # Geri çağrıları tetikle
        self._trigger_callbacks("emotion_changed", self.get_current_emotion())
        
        # Duygu hafızasını güncelle - 
        # Eğer _update_emotion_memory metodunda parametre yoksa 
        try:
            self._update_emotion_memory()
        except (TypeError, AttributeError):
            # Eski sürüm _update_emotion_memory metodunu kullan
            try:
                self._update_emotion_memory(transition["state"], transition["intensity"])
            except (TypeError, AttributeError) as e:
                logger.warning(f"Duygu hafızası güncellenemedi: {e}")
    
    def _get_response_curve_value(self, emotion: str, time_ratio: float) -> float:
        """
        Bir duygu için tepki eğrisindeki değeri hesaplar (zamanın bir fonksiyonu olarak)
        
        Args:
            emotion (str): Duygu durumu
            time_ratio (float): Zaman oranı (0.0-1.0)
        
        Returns:
            float: Tepki eğrisi değeri (0.0-1.0)
        """
        # Tepki eğrisini al
        curve = EMOTION_RESPONSE_CURVES.get(emotion, [])
        if not curve:
            # Eğri yoksa doğrusal değişim
            return time_ratio
        
        # Zamanı ilgili aralığa yerleştir
        for i in range(len(curve) - 1):
            x1, y1 = curve[i]
            x2, y2 = curve[i + 1]
            
            if x1 <= time_ratio <= x2:
                # Doğrusal interpolasyon
                if x2 == x1:  # Bölme sıfıra önleme
                    return y1
                ratio = (time_ratio - x1) / (x2 - x1)
                value = y1 + ratio * (y2 - y1)
                return value
        
        # Eğrinin dışındaysa, eğrinin başı veya sonu
        if time_ratio < curve[0][0]:
            return curve[0][1]
        else:
            return curve[-1][1]
        
    def transition_to(self, target_emotion: str, transition_time: float = None, 
                      intensity: float = 1.0, delay: float = 0.0,
                      add_micro_expressions: bool = True) -> bool:
        """
        Belirtilen duyguya geçiş yapar
        
        Args:
            target_emotion (str): Hedef duygu durumu
            transition_time (float, optional): Geçiş süresi (saniye). 
                                             None ise otomatik hesaplanır.
            intensity (float): Hedef duygu yoğunluğu (0.0-1.0)
            delay (float): Geçiş başlamadan önce beklenecek süre (saniye)
            add_micro_expressions (bool): Geçiş sırasında mikro ifadeler eklenecek mi?
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        # Duygu geçerliliğini kontrol et
        try:
            emotion_state = EmotionState(target_emotion)
            target_emotion = emotion_state.value
        except ValueError:
            logger.warning(f"Geçersiz hedef duygu: {target_emotion}")
            return False
        
        # Eğer şu anki duygu hedef duygunun aynısıysa ve yoğunluk da aynıysa hiçbir şey yapma
        try:
            current_state = self.current_emotion["state"]
            current_intensity = self.current_emotion["intensity"]
            if current_state == target_emotion and abs(current_intensity - intensity) < 0.05:
                logger.debug(f"Duygu zaten {target_emotion}, yoğunluk: {intensity:.2f}")
                return True
        except (KeyError, AttributeError):
            pass
        
        # Geçiş süresini hesapla
        if transition_time is None:
            # Geçiş faktörüne göre otomatik hesapla
            current_state = self.current_emotion["state"]
            transition_ease = EMOTION_TRANSITION_MATRIX.get(
                current_state, {}).get(target_emotion, 0.5)
            
            # Kişilik faktörünü de dikkate al
            try:
                personality_factor = getattr(self, 'personality_factor', 1.0)
            except AttributeError:
                personality_factor = 1.0
            
            # Geçiş süresi: 0.5 - 5 saniye arası, kişiliğe ve duygu geçiş kolaylığına bağlı
            transition_time = max(0.5, min(5.0, 3.0 * (1.0 - transition_ease) * personality_factor))
        
        # Hedef duygu geçiş verisi
        transition_data = {
            "state": target_emotion,
            "intensity": intensity,
            "progress": 0.0,
            "start_time": time.time() + delay,
            "duration": transition_time,
            "is_main_transition": True
        }
        
        # Gecikmeli başlangıç yoksa
        if delay <= 0:
            # Ana geçiş olarak ayarla
            self.current_emotion["target"] = transition_data
        else:
            # Aktif geçişler listesine ekle
            self.active_transitions.append(transition_data)
        
        # Mikro ifade geçişleri
        if add_micro_expressions and random.random() < self.micro_expression_transition_probability:
            self._add_transition_micro_expressions(current_state, target_emotion, 
                                                  transition_time, delay)
        
        logger.info(f"Duygu geçişi başlatıldı: {current_state} -> {target_emotion}, " +
                   f"yoğunluk: {intensity:.2f}, süre: {transition_time:.1f}s" +
                   (f", gecikme: {delay:.1f}s" if delay > 0 else ""))
        return True
    
    def _add_transition_micro_expressions(self, current_state: str, target_state: str, 
                                         transition_time: float, delay: float) -> None:
        """
        Duygu geçişine uygun mikro ifadeler ekler
        
        Args:
            current_state (str): Mevcut duygu
            target_state (str): Hedef duygu
            transition_time (float): Geçiş süresi
            delay (float): Başlangıç gecikmesi
        """
        # Duygu geçişi sırasında ara mikro ifadeler
        transition_map = {
            # Mutludan kızgına geçiş: Önce şaşkınlık mikro ifadesi
            (EmotionState.HAPPY.value, EmotionState.ANGRY.value): 
                [(EmotionState.SURPRISED.value, 0.7, 0.3)],
                
            # Üzgünden mutluya geçiş: Sakin geçiş sonra endişe
            (EmotionState.SAD.value, EmotionState.HAPPY.value): 
                [(EmotionState.CALM.value, 0.6, 0.2), (EmotionState.WORRIED.value, 0.4, 0.5)],
                
            # Korkudan kızgına geçiş: Şaşkınlık ve ardından endişe
            (EmotionState.FEARFUL.value, EmotionState.ANGRY.value): 
                [(EmotionState.SURPRISED.value, 0.8, 0.2), (EmotionState.WORRIED.value, 0.6, 0.5)],
                
            # Sakin durumdan korkuya geçiş: Endişe
            (EmotionState.CALM.value, EmotionState.FEARFUL.value):
                [(EmotionState.WORRIED.value, 0.7, 0.4)],
                
            # Şaşkınlıktan mutluluğa: Kısa bir sakinlik
            (EmotionState.SURPRISED.value, EmotionState.HAPPY.value):
                [(EmotionState.CALM.value, 0.5, 0.3)]
                
            # Diğer geçişler için buraya eklemeler yapılabilir
        }
        
        # Geçiş için özel mikro ifadeler var mı?
        transition_key = (current_state, target_state)
        if transition_key in transition_map:
            micro_expressions = transition_map[transition_key]
            
            for micro_emotion, micro_intensity, micro_timing in micro_expressions:
                micro_delay = delay + (transition_time * micro_timing)
                micro_duration = transition_time * 0.2  # Geçiş süresinin %20'si kadar sür
                
                try:
                    self.add_micro_expression(micro_emotion, micro_intensity, micro_duration, micro_delay)
                except Exception as e:
                    logger.warning(f"Mikro ifade eklenemedi: {e}")
        else:
            # Genel mikro ifadeler - rastgele
            # Özel geçiş tanımlanmamışsa ve duygular çok farklıysa, rastgele bir ara mikro ifade
            emotion_distance = abs(
                list(EmotionState).index(EmotionState(current_state)) - 
                list(EmotionState).index(EmotionState(target_state))
            )
            
            if emotion_distance > 2:  # Duygular arasındaki mesafe büyükse
                # Rastgele bir ara duygu seç (şaşkınlık veya endişe)
                micro_options = [EmotionState.SURPRISED, EmotionState.WORRIED]
                micro_emotion = random.choice(micro_options).value
                micro_intensity = random.uniform(0.5, 0.8)
                micro_timing = random.uniform(0.2, 0.5)
                
                micro_delay = delay + (transition_time * micro_timing)
                micro_duration = transition_time * 0.15
                
                try:
                    self.add_micro_expression(micro_emotion, micro_intensity, micro_duration, micro_delay)
                except Exception as e:
                    logger.warning(f"Rastgele mikro ifade eklenemedi: {e}")