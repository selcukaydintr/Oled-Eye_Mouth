#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: emotion_engine_memory.py
# Açıklama: Duygu motoru hafıza ve istatistik yönetimi.
# Bağımlılıklar: logging, time
# Bağlı Dosyalar: emotion_states.py, emotion_engine_base.py, emotion_engine.py

# Versiyon: 0.5.0
# Değişiklikler:
# - [0.5.0] Hafıza yönetimi iyileştirildi, bellek kullanımı optimize edildi
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
from typing import Dict, List, Tuple, Optional
from collections import deque

# Duygu durumlarını içe aktaralım
from src.modules.emotion_states import EmotionState

# Logger yapılandırması
logger = logging.getLogger("EmotionEngine")


class EmotionMemoryMixin:
    """
    Duygu hafızası mixin sınıfı
    
    Bu sınıf, duygu hafızası ve istatistiklerini yönetme yöntemlerini sağlar.
    EmotionEngine tarafından mixin olarak kullanılır.
    """
    
    def __init_memory(self):
        """
        Duygu hafıza ve istatistik değişkenlerini başlatır.
        Bu metot, ana sınıfın __init__ metodundan çağrılmalıdır.
        """
        # Duygu hafızası (geçmiş duygular) - daha verimli bellek kullanımı için deque kullanılıyor
        self.emotion_memory = deque(maxlen=100)  # Son duygular listesi [(zaman, duygu, yoğunluk), ...]
        self.memory_capacity = 100  # Hafıza kapasitesi
        
        # Duygu istatistikleri
        self.emotion_stats = {emotion.value: {
            "occurrence_count": 0,
            "total_duration": 0.0,
            "avg_intensity": 0.0,
            "last_occurrence": 0.0,
            "peak_intensity": 0.0
        } for emotion in EmotionState}
        
        # Duygu hafıza grupları - farklı zaman dilimlerine göre gruplandırılmış duygular
        self.short_term_memory = []  # Son 5 dakikalık duygular
        self.medium_term_memory = []  # Son 1 saatlik duygular
        self.long_term_memory = []  # Son 24 saatlik duygular
        
        # Yapılandırmadan değerler (eğer mevcutsa)
        try:
            emotion_config = getattr(self, 'emotion_config', {})
            # Duygu azalma süresi - saniye cinsinden
            self.emotion_decay_time = emotion_config.get("decay_time", 60.0)
            # Hafıza ölçeklendirme faktörü
            self.memory_scale_factor = emotion_config.get("memory_scale", 1.0)
        except AttributeError:
            # Varsayılan değerler
            self.emotion_decay_time = 60.0
            self.memory_scale_factor = 1.0
        
        logger.info(f"Duygu hafıza sistemi başlatıldı. Azalma süresi: {self.emotion_decay_time}s")
    
    def _update_emotion_stats(self, emotion: str, intensity: float) -> None:
        """
        Duygu istatistiklerini günceller
        
        Args:
            emotion (str): Duygu durumu
            intensity (float): Duygu yoğunluğu
        """
        stats = self.emotion_stats.get(emotion)
        if stats is None:
            return
            
        current_time = time.time()
        last_occurrence = stats["last_occurrence"]
        
        # İstatistikleri güncelle
        stats["occurrence_count"] += 1
        
        # Son oluşumdan bu yana geçen süreyi hesapla ve toplam süreye ekle
        if last_occurrence > 0:
            elapsed = current_time - last_occurrence
            stats["total_duration"] += elapsed
        
        stats["last_occurrence"] = current_time
        stats["avg_intensity"] = ((stats["avg_intensity"] * (stats["occurrence_count"] - 1)) + intensity) / stats["occurrence_count"]
        stats["peak_intensity"] = max(stats["peak_intensity"], intensity)
    
    def _update_memory_tiers(self) -> None:
        """
        Hafıza katmanlarını günceller - kısa, orta ve uzun vadeli hafızalar
        """
        current_time = time.time()
        
        # Zaman eşiklerini hesapla
        short_term_threshold = current_time - (300 * self.memory_scale_factor)  # 5 dakika
        medium_term_threshold = current_time - (3600 * self.memory_scale_factor)  # 1 saat
        long_term_threshold = current_time - (86400 * self.memory_scale_factor)  # 24 saat
        
        # Mevcut hafızadan uygun katmanları oluştur
        self.short_term_memory = [item for item in self.emotion_memory if item[0] >= short_term_threshold]
        self.medium_term_memory = [item for item in self.emotion_memory if item[0] >= medium_term_threshold]
        self.long_term_memory = [item for item in self.emotion_memory if item[0] >= long_term_threshold]
        
        # Bellek kullanımını optimize etmek için eski kayıtları temizle
        # Sınırlı sayıda örnek tut
        max_long_term_samples = 100
        if len(self.long_term_memory) > max_long_term_samples:
            # Eşit aralıklarla örnekler al
            step = len(self.long_term_memory) // max_long_term_samples
            self.long_term_memory = self.long_term_memory[::step][:max_long_term_samples]
    
    def _update_emotion_memory(self) -> None:
        """
        Duygu hafızasını günceller
        
        Mevcut duygu durumunu hafızaya ekler ve istatistikleri günceller.
        """
        # Mevcut duygu durumunu al
        try:
            current_emotion = self.get_current_emotion()
            emotion = current_emotion["state"]
            intensity = current_emotion["intensity"]
            
            # Yeni duyguyu hafızaya ekle
            current_time = time.time()
            self.emotion_memory.append((current_time, emotion, intensity))
            
            # İstatistikleri güncelle
            self._update_emotion_stats(emotion, intensity)
            
        except (AttributeError, KeyError) as e:
            logger.warning(f"Duygu hafızası güncellenemedi: {e}")
    
    def get_emotion_memory(self, timeframe: str = "all") -> List:
        """
        Duygu hafızasını döndürür
        
        Args:
            timeframe (str): Zaman dilimi ("short", "medium", "long", "all")
            
        Returns:
            List: Duygu hafızası kayıtları
        """
        if timeframe == "short":
            return list(self.short_term_memory)
        elif timeframe == "medium":
            return list(self.medium_term_memory)
        elif timeframe == "long":
            return list(self.long_term_memory)
        else:
            return list(self.emotion_memory)
    
    def get_dominant_emotion(self, timeframe: str = "short") -> Dict:
        """
        Belirli bir zaman diliminde baskın duyguyu döndürür
        
        Args:
            timeframe (str): Zaman dilimi ("short", "medium", "long")
            
        Returns:
            Dict: Baskın duygu bilgisi
        """
        # Zaman dilimine göre hafıza seç
        if timeframe == "medium":
            memory = self.medium_term_memory
        elif timeframe == "long":
            memory = self.long_term_memory
        else:  # varsayılan: kısa
            memory = self.short_term_memory
            
        if not memory:
            return {
                "state": EmotionState.NEUTRAL.value,
                "intensity": 0.5,
                "confidence": 0.0
            }
            
        # Duyguların sıklıklarını ve ortalama yoğunluklarını hesapla
        emotion_counts = {}
        emotion_total_intensity = {}
        
        for _, emotion, intensity in memory:
            if emotion not in emotion_counts:
                emotion_counts[emotion] = 0
                emotion_total_intensity[emotion] = 0.0
            
            emotion_counts[emotion] += 1
            emotion_total_intensity[emotion] += intensity
        
        # En çok tekrarlanan duyguyu bul
        if not emotion_counts:
            return {
                "state": EmotionState.NEUTRAL.value,
                "intensity": 0.5,
                "confidence": 0.0
            }
            
        dominant_emotion = max(emotion_counts, key=emotion_counts.get)
        dominant_count = emotion_counts[dominant_emotion]
        
        # Güven seviyesi (ne kadar baskın)
        total_entries = sum(emotion_counts.values())
        confidence = dominant_count / total_entries if total_entries > 0 else 0.0
        
        # Ortalama yoğunluk
        avg_intensity = (
            emotion_total_intensity[dominant_emotion] / dominant_count 
            if dominant_count > 0 else 0.5
        )
        
        return {
            "state": dominant_emotion,
            "intensity": avg_intensity,
            "confidence": confidence,
            "occurrence_count": dominant_count,
            "total_entries": total_entries
        }
    
    def get_emotion_trend(self) -> Dict:
        """
        Duygu trendini hesaplar ve döndürür
        
        Returns:
            Dict: Duygu trendi bilgisi (artış/azalma eğilimleri)
        """
        if len(self.short_term_memory) < 2:
            return {"trend": "stable", "confidence": 0.0}
            
        # Trend hesaplama için kısa dönem hafızayı kullan
        # Hafızayı zaman sırasına göre sırala
        sorted_memory = sorted(self.short_term_memory, key=lambda x: x[0])
        
        # Hafızayı iki eşit parçaya böl
        mid_point = len(sorted_memory) // 2
        first_half = sorted_memory[:mid_point]
        second_half = sorted_memory[mid_point:]
        
        # Her yarıda duygu dağılımını hesapla
        first_distribution = {}
        second_distribution = {}
        
        for _, emotion, intensity in first_half:
            if emotion not in first_distribution:
                first_distribution[emotion] = {"count": 0, "total_intensity": 0.0}
            first_distribution[emotion]["count"] += 1
            first_distribution[emotion]["total_intensity"] += intensity
            
        for _, emotion, intensity in second_half:
            if emotion not in second_distribution:
                second_distribution[emotion] = {"count": 0, "total_intensity": 0.0}
            second_distribution[emotion]["count"] += 1
            second_distribution[emotion]["total_intensity"] += intensity
        
        # Her duygudaki değişimi hesapla
        trends = {}
        confidence_sum = 0.0
        
        all_emotions = set(list(first_distribution.keys()) + list(second_distribution.keys()))
        for emotion in all_emotions:
            first_count = first_distribution.get(emotion, {"count": 0})["count"]
            second_count = second_distribution.get(emotion, {"count": 0})["count"]
            
            if first_count == 0 and second_count == 0:
                continue
                
            # Değişim oranı
            if first_count == 0:
                change = 1.0  # Yeni duygu (sonsuz artış yerine 1.0)
            elif second_count == 0:
                change = -1.0  # Kaybolmuş duygu
            else:
                change = (second_count - first_count) / first_count
                
            # Güven değeri - örnek sayısının karekökü ile orantılı
            confidence = ((first_count + second_count) ** 0.5) / (len(first_half) + len(second_half)) ** 0.5
                
            trends[emotion] = {
                "change": change,
                "confidence": confidence,
                "first_count": first_count,
                "second_count": second_count
            }
            
            confidence_sum += confidence
            
        # En belirgin trend
        if not trends:
            return {"trend": "stable", "confidence": 0.0}
            
        # En belirgin duygu değişimini bul (güven ile ağırlıklandırılmış)
        significant_emotion = max(trends, key=lambda e: abs(trends[e]["change"]) * trends[e]["confidence"])
        
        change = trends[significant_emotion]["change"]
        confidence = trends[significant_emotion]["confidence"] / confidence_sum if confidence_sum > 0 else 0.0
        
        # Trend yönünü belirle
        if change > 0.2:
            trend = "increasing"
        elif change < -0.2:
            trend = "decreasing"
        else:
            trend = "stable"
            
        return {
            "trend": trend,
            "emotion": significant_emotion,
            "change": change,
            "confidence": confidence
        }
    
    def _calculate_stability(self) -> float:
        """
        Duygu dengesini hesaplar (0.0-1.0)
        0: Çok değişken duygular
        1: Çok dengeli duygular
        
        Returns:
            float: Duygu denge puanı
        """
        if len(self.short_term_memory) < 3:
            return 0.5  # Yeterli veri yok
            
        # Son duyguları al ve sırala
        sorted_memory = sorted(self.short_term_memory, key=lambda x: x[0])
        
        # Ardışık duygu değişimlerini hesapla
        changes = []
        for i in range(1, len(sorted_memory)):
            prev_emotion = sorted_memory[i-1][1]
            curr_emotion = sorted_memory[i][1]
            prev_intensity = sorted_memory[i-1][2]
            curr_intensity = sorted_memory[i][2]
            
            # Duygu değişimi
            emotion_change = 0 if prev_emotion == curr_emotion else 1
            
            # Yoğunluk değişimi
            intensity_change = abs(curr_intensity - prev_intensity)
            
            # Toplam değişim
            total_change = emotion_change + intensity_change
            changes.append(total_change)
        
        # Değişim ortalaması
        avg_change = sum(changes) / len(changes) if changes else 0
        
        # 0-1 arasında dengeyi döndür (değişim arttıkça denge azalır)
        stability = max(0.0, min(1.0, 1.0 - avg_change))
        return stability
        
    def generate_emotional_summary(self) -> Dict:
        """
        Duygu durumunun özet bilgisini oluşturur
        
        Returns:
            Dict: Duygu özeti
        """
        try:
            current = self.get_current_emotion()
            dominant_short = self.get_dominant_emotion("short")
            dominant_medium = self.get_dominant_emotion("medium")
            trend = self.get_emotion_trend()
            stability = self._calculate_stability()
            
            # Duygusal karmaşıklık - belirli bir süre içinde kaç farklı duygu yaşandığı
            unique_emotions_short = len({emotion for _, emotion, _ in self.short_term_memory})
            unique_emotions_medium = len({emotion for _, emotion, _ in self.medium_term_memory})
            
            # Özet bilgi
            summary = {
                "current_state": current["state"],
                "current_intensity": current["intensity"],
                "short_term_dominant": dominant_short["state"],
                "short_term_confidence": dominant_short["confidence"],
                "medium_term_dominant": dominant_medium["state"],
                "medium_term_confidence": dominant_medium["confidence"],
                "trend": trend["trend"],
                "trend_emotion": trend.get("emotion"),
                "trend_confidence": trend["confidence"],
                "emotional_stability": stability,
                "emotional_complexity_short": unique_emotions_short,
                "emotional_complexity_medium": unique_emotions_medium,
                "memory_entries": len(self.emotion_memory)
            }
            
            return summary
            
        except Exception as e:
            logger.error(f"Duygu özeti oluşturulurken hata: {e}")
            return {"error": str(e)}