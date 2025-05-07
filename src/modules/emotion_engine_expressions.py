#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: emotion_engine_expressions.py
# Açıklama: Duygu motoru ifadeleri ve mikro ifade yönetimini içerir.
# Bağımlılıklar: logging, time, random
# Bağlı Dosyalar: emotion_states.py, emotion_engine_base.py, emotion_engine.py

# Versiyon: 0.5.0
# Değişiklikler:
# - [0.5.0] Mikro ifade yönetimi geliştirildi, bellek kullanımı optimize edildi
# - [0.4.0] emotion_engine.py dosyasından bölündü (modüler mimari)
# - [0.3.0] Duygu ifadeleri doğal görüntü için geliştirildi (30.04.2025)
# - [0.2.0] Mikro ifade sistemi eklendi (30.04.2025)
# - [0.1.0] Temel duygu motoru sınıfı oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-02
===========================================================
"""

import time
import logging
import random
from typing import Dict, List, Optional, Tuple, Any

from src.modules.emotion_states import EmotionState, get_emotion_subtype
from src.modules.emotion_states import get_intensity_label, is_valid_emotion

# Logger yapılandırması
logger = logging.getLogger("EmotionEngine")

class EmotionExpressionsMixin:
    """
    Duygu ifadeleri mixin sınıfı
    
    Bu sınıf, duygu ifadeleri ve mikro ifadelerle ilgili işlevler sağlar.
    EmotionEngine tarafından mixin olarak kullanılır.
    """
    
    def __init_expressions(self) -> None:
        """
        Duygu ifade değişkenlerini başlatır.
        Bu metot, ana sınıfın __init__ metodundan çağrılmalıdır.
        """
        try:
            emotion_config = getattr(self, 'emotion_config', {})
            # Varsayılan duygu durumu
            default_emotion = emotion_config.get("default_emotion", "NEUTRAL")
            # Duygu azalma süresi
            self.emotion_decay_time = emotion_config.get("emotion_decay_time", 60.0)
            # Mikro ifadeler etkin mi?
            self.micro_expressions_enabled = emotion_config.get("micro_expressions_enabled", True)
        except AttributeError:
            # Varsayılan değerler
            default_emotion = "NEUTRAL"
            self.emotion_decay_time = 60.0
            self.micro_expressions_enabled = True
        
        # Mevcut duygu durumu
        self.current_emotion = {
            "state": default_emotion,
            "intensity": 0.7,
            "start_time": time.time(),
            "target": None,
            "subtype": None
        }
        
        # Mikro ifadeler listesi
        self.micro_expressions = []
        
        # Şu anda aktif mikro ifade
        self.active_micro_expression = None
        
        # Son duygu değişim zamanı
        self.last_emotion_change_time = time.time()
        
        # Spontane mikro ifadeler etkin mi?
        self.spontaneous_micro_expressions = emotion_config.get("spontaneous_micro_expressions", True)
        
        # Spontane mikro ifade parametreleri
        self.spontaneous_interval_min = emotion_config.get("spontaneous_interval_min", 30.0)
        self.spontaneous_interval_max = emotion_config.get("spontaneous_interval_max", 120.0)
        
        # Sonraki spontane mikro ifade zamanı
        self.next_spontaneous_micro_time = time.time() + random.uniform(
            self.spontaneous_interval_min, 
            self.spontaneous_interval_max
        )
        
        logger.info(f"Duygu ifadeleri modülü başlatıldı. Varsayılan duygu: {default_emotion}, " + 
                    f"Mikro ifadeler: {'Etkin' if self.micro_expressions_enabled else 'Devre Dışı'}")
    
    def get_current_emotion(self) -> Dict:
        """
        Mevcut duygu durumunu döndürür

        Returns:
            Dict: Duygu durumu, yoğunluğu ve alt tipi içeren sözlük
                  {"state": "HAPPY", "intensity": 0.8, "subtype": "JOYFUL"}
        """
        # Mevcut durumu al
        current = self.current_emotion.copy()
        
        # Aktif bir mikro ifade varsa, o anki görünümü etkiler
        if self.active_micro_expression:
            # Mikro ifadeden etkilenme seviyesi (zaman bazlı)
            time_now = time.time()
            micro = self.active_micro_expression
            
            if time_now < micro["end_time"]:
                # Mikro ifadenin etkisini hesapla
                total_duration = micro["end_time"] - micro["start_time"]
                elapsed_time = time_now - micro["start_time"]
                progress = elapsed_time / total_duration
                
                # Mikro ifadenin kuvvetini hesapla (0-1 arasında bell eğrisi)
                # Başlangıçta ve sonunda zayıf, ortada güçlü
                influence = 4 * progress * (1 - progress)
                influence = min(1.0, influence * 1.5)
                
                # Ana duyguyu ve mikro ifadeyi karıştır
                blended_state = micro["state"]
                blended_intensity = (current["intensity"] + 
                                   (micro["intensity"] - current["intensity"]) * influence)
                
                # Anlık ifadenin temeli olarak ana duyguyu koru ama mikro ifade ile karıştır
                return {
                    "state": blended_state,
                    "intensity": blended_intensity,
                    "subtype": get_emotion_subtype(blended_state, blended_intensity),
                    "base_state": current["state"],
                    "is_micro_expression": True,
                    "micro_progress": progress,
                    "micro_influence": influence
                }
        
        # Alt tip özelliğini güncelle
        if "subtype" not in current or current["subtype"] is None:
            current["subtype"] = get_emotion_subtype(current["state"], current["intensity"])
            
        return current
    
    def set_emotion(self, emotion: str, intensity: float = 1.0, 
                   transition_time: Optional[float] = None) -> bool:
        """
        Duygu durumunu ayarlar

        Args:
            emotion (str): Duygu durumu (EmotionState değerleri)
            intensity (float, optional): Duygu yoğunluğu (0.0-1.0)
            transition_time (float, optional): Geçiş süresi. Belirtilmezse otomatik hesaplanır.

        Returns:
            bool: Başarılı ise True, değilse False
        """
        # Duygu geçişini yönet
        if hasattr(self, 'transition_to'):
            return self.transition_to(emotion, transition_time, intensity)
        
        # Durum geçişi yoksa doğrudan ayarla
        # Duygu geçerliliğini kontrol et
        if not is_valid_emotion(emotion):
            logger.warning(f"Geçersiz duygu: {emotion}")
            return False
        
        # Yoğunluğu sınırla
        intensity = max(0.0, min(1.0, intensity))
        
        # Duyguyu ayarla
        self.current_emotion["state"] = emotion
        self.current_emotion["intensity"] = intensity
        self.current_emotion["start_time"] = time.time()
        self.current_emotion["subtype"] = get_emotion_subtype(emotion, intensity)
        self.current_emotion["target"] = None
        
        # Duygu değişim zamanını güncelle
        self.last_emotion_change_time = time.time()
        
        # Geri çağrıları tetikle
        self._trigger_callbacks("emotion_changed", self.get_current_emotion())
        
        logger.info(f"Duygu ayarlandı: {emotion}, yoğunluk: {intensity:.2f}, alt tip: {self.current_emotion['subtype']}")
        return True
    
    def _process_emotion_decay(self) -> None:
        """
        Duygu yoğunluğu zamanla azalma işlemini gerçekleştirir
        """
        # Duygu geçişi sırasında azalma işleme
        if self.current_emotion.get("target"):
            return
        
        # Mevcut durum nötr ise azalma işleme
        if self.current_emotion["state"] == EmotionState.NEUTRAL.value:
            return
        
        # Azalma süresi sıfır veya negatifse azalma yapma
        if self.emotion_decay_time <= 0:
            return
        
        # Geçen süreyi hesapla
        time_now = time.time()
        elapsed = time_now - self.current_emotion["start_time"]
        
        # Azalma hesaplaması
        if elapsed < self.emotion_decay_time:
            # Azalma için kalan süre var
            current_intensity = self.current_emotion["intensity"]
            time_ratio = elapsed / self.emotion_decay_time
            
            # Üstel azalma: başlangıçta hızlı, sonra yavaş
            decay_factor = 1.0 - (1.0 - time_ratio) ** 0.7
            new_intensity = current_intensity - (current_intensity - 0.3) * decay_factor
            
            # Yoğunluk değişimi çok azsa, daha fazla azaltmaya gerek yok
            if abs(new_intensity - current_intensity) > 0.01:
                self.current_emotion["intensity"] = new_intensity
                
                # Alt tipi güncelle
                self.current_emotion["subtype"] = get_emotion_subtype(
                    self.current_emotion["state"], 
                    self.current_emotion["intensity"]
                )
        else:
            # Azalma süresi doldu, nötre geçiş yap
            if hasattr(self, 'transition_to'):
                self.transition_to(EmotionState.NEUTRAL.value, 2.0, 0.7)
            else:
                self.current_emotion["state"] = EmotionState.NEUTRAL.value
                self.current_emotion["intensity"] = 0.7
                self.current_emotion["subtype"] = get_emotion_subtype(
                    EmotionState.NEUTRAL.value, 0.7)
                self.current_emotion["start_time"] = time_now
                
                # Geri çağrıları tetikle
                self._trigger_callbacks("emotion_changed", self.get_current_emotion())
                
                logger.debug("Duygu nötre döndü (azalma süresi doldu)")
    
    def add_micro_expression(self, emotion: str, intensity: float = 0.8, 
                            duration: float = 1.0, delay: float = 0.0) -> bool:
        """
        Bir mikro ifade ekler

        Args:
            emotion (str): Mikro ifade duygu durumu
            intensity (float): Duygu yoğunluğu (0.0-1.0)
            duration (float): Mikro ifade süresi (saniye)
            delay (float): Başlangıç gecikmesi (saniye)

        Returns:
            bool: Başarılı ise True, değilse False
        """
        # Mikro ifadeler devredışı ise işleme
        if not self.micro_expressions_enabled:
            return False
        
        # Duygu geçerliliğini kontrol et
        if not is_valid_emotion(emotion):
            logger.warning(f"Geçersiz mikro ifade: {emotion}")
            return False
        
        # Süre kontrolü
        if duration <= 0:
            logger.warning("Mikro ifade süresi pozitif olmalıdır")
            return False
        
        # Şimdiki zaman
        time_now = time.time()
        
        # Mikro ifade bilgisi
        micro_expression = {
            "state": emotion,
            "intensity": max(0.0, min(1.0, intensity)),
            "start_time": time_now + delay,
            "end_time": time_now + delay + duration,
            "priority": 1  # Standart öncelik
        }
        
        # Mikro ifadeyi listeye ekle ve süre sırasına göre sırala
        self.micro_expressions.append(micro_expression)
        self.micro_expressions.sort(key=lambda x: x["start_time"])
        
        logger.debug(f"Mikro ifade eklendi: {emotion}, yoğunluk: {intensity:.2f}, " +
                    f"süre: {duration:.1f}s" + (f", gecikme: {delay:.1f}s" if delay > 0 else ""))
        return True
    
    def _clean_expired_micro_expressions(self) -> None:
        """
        Süresi dolmuş mikro ifadeleri temizler
        """
        time_now = time.time()
        expired_indices = []
        
        # Sona ermiş mikro ifadeleri bul
        for i, micro in enumerate(self.micro_expressions):
            if time_now > micro["end_time"]:
                expired_indices.append(i)
        
        # Sondan başlayarak sil (indekslerin değişmemesi için)
        for idx in sorted(expired_indices, reverse=True):
            micro = self.micro_expressions.pop(idx)
            logger.debug(f"Mikro ifade süresi doldu: {micro['state']}")
    
    def _process_micro_expressions(self) -> None:
        """
        Mikro ifadeleri işler
        """
        # Mikro ifadeler kapalıysa işleme
        if not self.micro_expressions_enabled:
            if self.active_micro_expression:
                self.active_micro_expression = None
            return
        
        time_now = time.time()
        
        # Spontane mikro ifadeleri kontrol et
        if (self.spontaneous_micro_expressions and 
            time_now >= self.next_spontaneous_micro_time):
            self._generate_spontaneous_micro_expression()
            
            # Bir sonraki spontane mikro ifade için zaman belirle
            self.next_spontaneous_micro_time = time_now + random.uniform(
                self.spontaneous_interval_min, 
                self.spontaneous_interval_max
            )
        
        # Süresi dolmuş mikro ifadeleri temizle
        self._clean_expired_micro_expressions()
        
        # Aktif mikro ifadeyi kontrol et
        if self.active_micro_expression:
            if time_now > self.active_micro_expression["end_time"]:
                # Aktif mikro ifade süresi doldu
                logger.debug(f"Aktif mikro ifade bitti: {self.active_micro_expression['state']}")
                self.active_micro_expression = None
            else:
                # Aktif mikro ifade devam ediyor
                return
        
        # Yeni bir mikro ifade işleme alınabilir mi?
        if not self.micro_expressions:
            return
            
        # Listedeki ilk mikro ifadeyi kontrol et
        next_micro = self.micro_expressions[0]
        
        # Zamanı geldi mi?
        if time_now >= next_micro["start_time"]:
            # Mikro ifadeyi aktifleştir
            self.active_micro_expression = self.micro_expressions.pop(0)
            
            # Geri çağrıları tetikle
            self._trigger_callbacks("micro_expression", {
                "state": self.active_micro_expression["state"],
                "intensity": self.active_micro_expression["intensity"],
                "duration": self.active_micro_expression["end_time"] - self.active_micro_expression["start_time"]
            })
            
            logger.debug(f"Mikro ifade başladı: {self.active_micro_expression['state']}, " +
                        f"yoğunluk: {self.active_micro_expression['intensity']:.2f}")
    
    def _generate_spontaneous_micro_expression(self) -> None:
        """
        Rastgele bir spontane mikro ifade oluşturur
        """
        # Mevcut duruma göre uyumlu mikro ifadeler
        current_state = self.current_emotion["state"]
        micro_options = []
        
        # Her duygu durumuna uyumlu mikro ifadeleri belirle
        emotion_micro_map = {
            EmotionState.HAPPY.value: [
                (EmotionState.SURPRISED.value, 0.5, 0.3),  # Küçük şaşırma
                (EmotionState.CURIOUS.value, 0.6, 0.5)     # Merak
            ],
            EmotionState.SAD.value: [
                (EmotionState.WORRIED.value, 0.7, 0.5),    # Endişe
                (EmotionState.FEARFUL.value, 0.3, 0.4)     # Hafif korku
            ],
            EmotionState.ANGRY.value: [
                (EmotionState.SURPRISED.value, 0.7, 0.3),  # Şaşkınlık
                (EmotionState.DISGUSTED.value, 0.6, 0.5)   # İğrenme
            ],
            EmotionState.SURPRISED.value: [
                (EmotionState.FEARFUL.value, 0.4, 0.3),    # Hafif korku
                (EmotionState.CURIOUS.value, 0.8, 0.6)     # Güçlü merak
            ],
            EmotionState.FEARFUL.value: [
                (EmotionState.WORRIED.value, 0.8, 0.6),    # Endişe
                (EmotionState.SURPRISED.value, 0.7, 0.4)   # Şaşırma
            ],
            EmotionState.DISGUSTED.value: [
                (EmotionState.ANGRY.value, 0.5, 0.4),      # Hafif kızgınlık
                (EmotionState.SURPRISED.value, 0.6, 0.3)   # Şaşırma
            ],
            EmotionState.NEUTRAL.value: [
                (EmotionState.CURIOUS.value, 0.6, 0.5),    # Merak
                (EmotionState.HAPPY.value, 0.3, 0.4),      # Hafif mutluluk
                (EmotionState.WORRIED.value, 0.4, 0.4),    # Hafif endişe
                (EmotionState.SURPRISED.value, 0.5, 0.3)   # Hafif şaşkınlık
            ]
        }
        
        # Mevcut duygu için mikro ifadeleri al
        micro_options = emotion_micro_map.get(current_state, [])
        
        # Mikro ifade seçenekleri yoksa genel seçenekleri kullan
        if not micro_options:
            micro_options = [
                (EmotionState.SURPRISED.value, 0.5, 0.3),  # Hafif şaşırma
                (EmotionState.CURIOUS.value, 0.6, 0.5),    # Merak
                (EmotionState.WORRIED.value, 0.4, 0.4)     # Hafif endişe
            ]
        
        # Rastgele bir mikro ifade seç
        if random.random() < 0.7:  # %70 olasılıkla özel listeden seç
            micro_emotion, micro_intensity, micro_duration = random.choice(micro_options)
        else:  # %30 olasılıkla tamamen rastgele seç
            available_emotions = [e for e in EmotionState if e.value != current_state]
            micro_emotion = random.choice(available_emotions).value
            micro_intensity = random.uniform(0.3, 0.7)
            micro_duration = random.uniform(0.3, 1.0)
        
        # Mikro ifadeyi ekle (0-1 saniyelik gecikmeyle)
        delay = random.uniform(0.0, 1.0)
        self.add_micro_expression(micro_emotion, micro_intensity, micro_duration, delay)
    
    def get_emotional_description(self) -> str:
        """
        Mevcut duygu durumunun metin açıklamasını oluşturur

        Returns:
            str: Duygu durumunun metin açıklaması
        """
        emotion = self.get_current_emotion()
        state = emotion["state"]
        intensity = emotion["intensity"]
        subtype = emotion["subtype"] if "subtype" in emotion else get_emotion_subtype(state, intensity)
        
        # Yoğunluk etiketi
        intensity_label = get_intensity_label(intensity)
        
        # Duygu durumu cümlesini oluştur
        description = f"{intensity_label} derecede {subtype}"
        
        # Mikro ifade varsa onu da ekle
        if emotion.get("is_micro_expression", False):
            base_state = emotion.get("base_state", "")
            if base_state:
                base_subtype = get_emotion_subtype(base_state, intensity)
                description += f" (temel duygu: {base_subtype})"
        
        return description