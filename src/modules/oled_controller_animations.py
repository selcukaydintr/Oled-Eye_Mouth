#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: oled_controller_animations.py
# Açıklama: OLED ekranları için animasyon ve duygu geçişlerini içeren modül.
# Bağımlılıklar: PIL, threading, time
# Bağlı Dosyalar: hardware_defines.py, oled_controller_base.py

# Versiyon: 0.3.2
# Değişiklikler:
# - [0.3.2] Çevresel faktörlere tepki veren ifadeler için fonksiyonlar eklendi
# - [0.3.1] Modül 3'e bölündü, animasyon fonksiyonları bu modüle taşındı
# - [0.3.0] Duygu geçişleri daha akıcı hale getirildi
# - [0.2.0] Mikro ifadeler eklendi ve enerji tasarrufu modu geliştirildi
# 
# Yazar: GitHub Copilot
# Tarih: 2025-04-30
===========================================================
"""

import logging
import time
import random
from typing import Dict, List, Tuple, Optional, Union

# Logger yapılandırması
logger = logging.getLogger("OLEDController")

class OLEDAnimationsMixin:
    """
    OLED ekranlar için animasyon ve duygu geçiş işlevlerini içeren mixin sınıfı.
    OLEDController sınıfı ile birlikte kullanılmak üzere tasarlanmıştır.
    """

    # Çevresel faktörlere göre ifadeler için eşik değerleri
    LIGHT_THRESHOLD_BRIGHT = 1000  # lux
    LIGHT_THRESHOLD_DARK = 10      # lux
    TEMP_THRESHOLD_HOT = 28        # °C
    TEMP_THRESHOLD_COLD = 15       # °C
    HUMIDITY_THRESHOLD_DRY = 30    # %
    HUMIDITY_THRESHOLD_HUMID = 70  # %
    NOISE_THRESHOLD_LOUD = 70      # dB
    
    # Çevresel faktörlere tepki gecikme süreleri
    ENVIRONMENTAL_REACTION_COOLDOWN = 60  # saniye

    def set_emotion(self, emotion: str, intensity: float = 1.0) -> None:
        """
        Ekranları belirtilen duygu durumuna göre günceller
        
        Args:
            emotion (str): Duygu durumu (örn. "happy", "sad", "angry" vb.)
            intensity (float, optional): Duygu yoğunluğu (0.0-1.0 arası). Varsayılan: 1.0
        """
        # Duygu durumunu yapılandırmaya kaydet
        if "emotions" not in self.config:
            self.config["emotions"] = {}
        self.config["emotions"]["default_emotion"] = emotion
        
        # Aktivite zamanını güncelle (güç tasarrufu kontrolü için)
        self.last_activity_time = time.time()
        
        # Güç modu kapalıysa açık moda geç
        if self.power_mode == "off" or self.power_mode == "dim":
            self.set_power_mode("on")
        
        # Doğrudan çizim yapmak yerine bir sonraki animasyon çerçevesinde güncellenecektir
        logger.info(f"Duygu durumu ayarlandı: {emotion}, yoğunluk: {intensity:.2f}")
    
    def show_micro_expression(self, emotion: str, duration: float = 0.5, intensity: float = 1.0) -> None:
        """
        Kısa süreli mikro ifade gösterir
        
        Args:
            emotion (str): Duygu durumu (örn. "happy", "sad", "angry" vb.)
            duration (float, optional): İfade süresi (saniye). Varsayılan: 0.5
            intensity (float, optional): Duygu yoğunluğu (0.0-1.0 arası). Varsayılan: 1.0
        """
        # Süreyi sınırla
        duration = max(self.MIN_MICRO_EXPRESSION_DURATION, 
                      min(self.MAX_MICRO_EXPRESSION_DURATION, duration))
        
        # Yoğunluğu sınırla
        intensity = max(0.0, min(1.0, intensity))
        
        # Mikro ifadeyi ayarla
        self.micro_expression = emotion
        self.micro_expression_end_time = time.time() + duration
        self.micro_expression_intensity = intensity
        
        # Aktivite zamanını güncelle (güç tasarrufu kontrolü için)
        self.last_activity_time = time.time()
        
        # Güç modu kapalıysa açık moda geç
        if self.power_mode == "off" or self.power_mode == "dim":
            self.set_power_mode("on")
        
        logger.info(f"Mikro ifade gösteriliyor: {emotion}, süre: {duration:.2f}s, yoğunluk: {intensity:.2f}")
    
    def look_at(self, x: float, y: float, speed: float = 0.2) -> None:
        """
        Göz bebeklerinin belirli bir noktaya bakmasını sağlar
        
        Args:
            x (float): X koordinatı (-1.0 - 1.0 arası, -1.0: sol, 1.0: sağ)
            y (float): Y koordinatı (-1.0 - 1.0 arası, -1.0: yukarı, 1.0: aşağı)
            speed (float, optional): Göz hareket hızı (0.0-1.0 arası). Varsayılan: 0.2
        """
        # Koordinatları sınırla
        x = max(-1.0, min(1.0, x))
        y = max(-1.0, min(1.0, y))
        
        # Hızı sınırla
        speed = max(0.01, min(1.0, speed))
        
        # Göz hedef pozisyonunu ayarla
        self.target_eye_position = (x, y)
        self.eye_move_speed = speed
        
        # Otomatik göz hareketini devre dışı bırak
        self.random_eye_move = False
        
        # Aktivite zamanını güncelle (güç tasarrufu kontrolü için)
        self.last_activity_time = time.time()
        
        # Güç modu kapalıysa açık moda geç
        if self.power_mode == "off" or self.power_mode == "dim":
            self.set_power_mode("on")
        
        logger.debug(f"Göz bakışı ayarlandı: x={x:.2f}, y={y:.2f}, hız={speed:.2f}")
    
    def enable_random_eye_movement(self, enabled: bool = True) -> None:
        """
        Rastgele göz hareketlerini etkinleştirir veya devre dışı bırakır
        
        Args:
            enabled (bool, optional): Etkinleştirme durumu. Varsayılan: True
        """
        self.random_eye_move = enabled
        
        if enabled:
            # Sonraki göz hareket zamanını ayarla
            self.next_eye_move_time = time.time() + random.uniform(0.5, 1.5)
            logger.debug("Rastgele göz hareketleri etkinleştirildi")
        else:
            logger.debug("Rastgele göz hareketleri devre dışı bırakıldı")
    
    def blend_emotions(self, emotion1: str, emotion2: str, ratio: float) -> str:
        """
        İki duygu arasında yumuşak geçiş sağlar. 
        Verilen orana göre iki duygudaki göz ve ağız pozisyonlarını karıştırır.
        
        Args:
            emotion1 (str): Başlangıç duygu durumu
            emotion2 (str): Hedef duygu durumu
            ratio (float): Karıştırma oranı (0.0: tamamen emotion1, 1.0: tamamen emotion2)
            
        Returns:
            str: Görsel temsil için kullanılacak etkili duygu
        """
        # Performans optimizasyonu: Önbelleğe alınmış sonuçları kullan
        cache_key = f"{emotion1}_{emotion2}_{ratio:.2f}"
        if hasattr(self, "_emotion_blend_cache") and cache_key in self._emotion_blend_cache:
            return self._emotion_blend_cache[cache_key]
        
        # Önbellek yoksa oluştur
        if not hasattr(self, "_emotion_blend_cache"):
            self._emotion_blend_cache = {}
            
        # Maksimum önbellek boyutunu kontrol et (bellek optimizasyonu)
        if hasattr(self, "_emotion_blend_cache") and len(self._emotion_blend_cache) > 100:
            self._emotion_blend_cache.clear()
        
        # Geçiş oranını sınırla (0.0-1.0 arası)
        ratio = max(0.0, min(1.0, ratio))
        
        # Eğer geçiş henüz başlamamışsa veya tamamlanmışsa, doğrudan duygulardan birini döndür
        if ratio <= 0.01:
            result = emotion1
            self._emotion_blend_cache[cache_key] = result
            return result
        elif ratio >= 0.99:
            result = emotion2
            self._emotion_blend_cache[cache_key] = result
            return result
            
        # Performans optimizasyonu: Duygu çiftlerini önceden tanımla ve hızlı erişim için sözlük kullan
        emotion_pair = f"{emotion1}_{emotion2}"
        transition_map = {
            "happy_sad": "neutral" if abs(ratio - 0.5) < 0.2 else (emotion1 if ratio < 0.5 else emotion2),
            "sad_happy": "neutral" if abs(ratio - 0.5) < 0.2 else (emotion1 if ratio < 0.5 else emotion2),
            "angry_happy": emotion1 if ratio < 0.33 else ("surprised" if ratio < 0.66 else emotion2),
            "happy_angry": emotion1 if ratio < 0.33 else ("surprised" if ratio < 0.66 else emotion2),
            "fearful_angry": emotion1 if ratio < 0.33 else ("surprised" if ratio < 0.66 else emotion2),
            "angry_fearful": emotion1 if ratio < 0.33 else ("surprised" if ratio < 0.66 else emotion2),
            "sad_calm": emotion1 if ratio < 0.5 else emotion2,
            "calm_sad": emotion1 if ratio < 0.5 else emotion2
        }
        
        # Duygu çiftine göre uygun geçiş uygula
        if emotion_pair in transition_map:
            result = transition_map[emotion_pair]
        else:
            # Diğer durumlarda sadece oran kontrolü yap
            result = emotion2 if ratio > 0.5 else emotion1
        
        # Sonucu önbelleğe al
        self._emotion_blend_cache[cache_key] = result
        return result
    
    def start_emotion_transition(self, target_emotion: str, duration: float = 2.0) -> None:
        """
        Bir duygu durumundan diğerine yumuşak geçiş başlatır
        
        Args:
            target_emotion (str): Hedef duygu durumu
            duration (float, optional): Geçiş süresi (saniye). Varsayılan: 2.0
        """
        if "emotions" not in self.config:
            self.config["emotions"] = {}
        
        # Mevcut duyguyu kaynağa kaydet
        source_emotion = self.config["emotions"].get("default_emotion", "neutral")
        self.config["emotions"]["source"] = source_emotion
        
        # Hedef duyguyu ve geçiş bilgilerini ayarla
        self.config["emotions"]["target"] = {
            "state": target_emotion,
            "start_time": time.time(),
            "duration": max(0.5, duration),
            "progress": 0.0
        }
        
        # Aktivite zamanını güncelle (güç tasarrufu kontrolü için)
        self.last_activity_time = time.time()
        
        # Güç modu kapalıysa açık moda geç
        if self.power_mode == "off" or self.power_mode == "dim":
            self.set_power_mode("on")
        
        logger.info(f"Duygu geçişi başlatıldı: {source_emotion} -> {target_emotion}, süre: {duration:.1f}s")
    
    def update_emotion_transition(self) -> None:
        """
        Duygu geçiş durumunu günceller
        """
        # Performans optimizasyonu: Gereksiz kontrolleri minimuma indir
        if not hasattr(self, "config") or "emotions" not in self.config:
            return
            
        emotions = self.config["emotions"]
        if "target" not in emotions or emotions["target"] is None:
            return
            
        target = emotions["target"]
        
        # Zaman hesaplamaları için önceden alınmış değişkenler
        current_time = time.time()
        start_time = target.get("start_time", current_time)
        duration = target.get("duration", 2.0)
        
        # Eğer süre 0 veya negatifse, hemen tamamla
        if duration <= 0:
            emotions["default_emotion"] = target["state"]
            emotions["target"] = None
            logger.debug(f"Duygu geçişi anında tamamlandı, yeni durum: {target['state']}")
            return
        
        # İlerleme oranını hesapla (0.0 - 1.0)
        elapsed = current_time - start_time
        progress = min(1.0, elapsed / duration)
        
        # Son değeri önbelleğe almak için önceki değeri kontrol et
        prev_progress = target.get("progress", 0.0)
        
        # Önemli bir değişiklik olduğunda veya tamamlandığında güncelle - performans için
        if abs(progress - prev_progress) >= 0.01 or progress >= 1.0:
            # İlerleme durumunu güncelle
            target["progress"] = progress
            
            # Geçiş tamamlandıysa, hedef durumu ana duygu olarak ayarla ve hedefi temizle
            if progress >= 1.0:
                emotions["default_emotion"] = target["state"]
                emotions["target"] = None
                logger.debug(f"Duygu geçişi tamamlandı, yeni durum: {target['state']}")
                
                # Bellek temizliği - eski geçiş verilerini temizle
                if hasattr(self, "_emotion_blend_cache"):
                    self._emotion_blend_cache.clear()
    
    def animate_blink(self, immediate: bool = False) -> None:
        """
        Göz kırpma animasyonu başlatır
        
        Args:
            immediate (bool, optional): True ise hemen göz kırp, False ise normal zamanlamayı kullan. Varsayılan: False
        """
        if immediate:
            # Hemen göz kırp
            self.blink_state = False
            self.next_blink_time = time.time() + 0.15  # Göz kapalı kalma süresi
        elif random.random() < 0.2:  # %20 olasılıkla göz kırpma zamanını değiştir
            # Rastgele bir zamanlamada göz kırp
            self.next_blink_time = time.time() + random.uniform(0.1, 0.5)

    def react_to_environmental_factors(self) -> None:
        """
        Çevresel faktörlere göre ifadeyi ayarlar.
        Işık, sıcaklık, nem gibi çevresel faktörlere göre otomatik tepkiler oluşturur.
        """
        # Performans optimizasyonu: Zaman kontrollerini hızlı yap
        current_time = time.time()
        last_reaction_time = getattr(self, "last_environmental_reaction_time", 0)
        
        # Çok sık çevresel tepki vermesini önlemek için zaman kontrolü
        if current_time - last_reaction_time < self.ENVIRONMENTAL_REACTION_COOLDOWN:
            return
        
        # Performans optimizasyonu: Erken çıkış kontrolü - güç tasarrufu modunda çevresel tepki verme
        if self.power_mode == "off" or self.power_mode == "dim":
            return
        
        # Bellek optimizasyonu: Tek seferlik tepki yapılacak, bu yüzden sensör verilerini önbelleğe al
        sensor_data = {}
        
        # Sıcaklık ve nem tepkisi
        if hasattr(self, "temp_sensor") and self.temp_sensor is not None:
            try:
                # Sensör verilerini tek seferde topla
                sensor_data["temperature"] = self.temp_sensor.temperature
                sensor_data["humidity"] = self.temp_sensor.relative_humidity
                
                # Sıcaklık tepkileri - öncelik yüksek
                if sensor_data["temperature"] > self.TEMP_THRESHOLD_HOT:
                    self.show_environmental_reaction("hot", sensor_data["temperature"])
                    return
                elif sensor_data["temperature"] < self.TEMP_THRESHOLD_COLD:
                    self.show_environmental_reaction("cold", sensor_data["temperature"])
                    return
                
                # Nem tepkileri - öncelik daha düşük
                if sensor_data["humidity"] > self.HUMIDITY_THRESHOLD_HUMID:
                    self.show_environmental_reaction("humid", sensor_data["humidity"])
                    return
                elif sensor_data["humidity"] < self.HUMIDITY_THRESHOLD_DRY:
                    self.show_environmental_reaction("dry", sensor_data["humidity"])
                    return
                    
            except Exception as e:
                # Hata durumunda diğer sensörleri kontrol etmeye devam et
                logger.error(f"Sıcaklık sensörü okunurken hata: {e}")
        
        # Işık tepkisi
        if hasattr(self, "light_sensor") and self.light_sensor is not None:
            try:
                light_level = self.light_sensor.lux
                sensor_data["light"] = light_level
                
                # Işık tepkileri
                if light_level > self.LIGHT_THRESHOLD_BRIGHT:
                    self.show_environmental_reaction("bright", light_level)
                    return
                elif light_level < self.LIGHT_THRESHOLD_DARK:
                    self.show_environmental_reaction("dark", light_level)
                    return
                    
            except Exception as e:
                logger.error(f"Işık sensörü okunurken hata: {e}")
        
        # Performans optimizasyonu: Rastgele sayı üretimi ve zaman kontrollerini en aza indir
        
        # Günün saati ve olasılık kontrolünü birleştir
        hour_of_day = time.localtime().tm_hour
        rand_value = random.random()
        
        # Gece (22:00-06:00) - %5 olasılıkla uykulu davranış
        if (22 <= hour_of_day or hour_of_day < 6) and rand_value < 0.05:
            self.show_environmental_reaction("sleepy", hour_of_day)
        
        # Sabah (06:00-09:00) - %5 olasılıkla uyanık/enerjik davranış  
        elif 6 <= hour_of_day < 9 and rand_value < 0.05:
            self.show_environmental_reaction("energetic", hour_of_day)

    def show_environmental_reaction(self, reaction_type: str, value: float) -> None:
        """
        Çevresel faktörlere göre tepki gösterir
        
        Args:
            reaction_type (str): Tepki türü ("hot", "cold", "humid", "dry", "bright", "dark", "sleepy", "energetic")
            value (float): Çevresel değer (sıcaklık, nem, ışık seviyesi vb.)
        """
        # Çevresel tepki zamanını kaydet
        self.last_environmental_reaction_time = time.time()
        
        # Performans optimizasyonu: Tepki türlerine göre önceden tanımlanmış tepki planlarını kullan
        reaction_plan = self._get_optimized_reaction_plan(reaction_type, value)
        
        # Tepki planını uygula
        for action in reaction_plan:
            action_type, params = action
            
            if action_type == "micro_expression":
                self.show_micro_expression(params["emotion"], params.get("duration", 0.8), params.get("intensity", 1.0))
            elif action_type == "blink":
                self.animate_blink(params.get("immediate", True))
            elif action_type == "look_at":
                self.look_at(params.get("x", 0), params.get("y", 0), params.get("speed", 0.1))
            elif action_type == "wait":
                time.sleep(params.get("duration", 0.1))
            elif action_type == "log":
                logger.info(params["message"])
        
        # Rastgele göz hareketlerini yeniden etkinleştir - son adım
        self.enable_random_eye_movement(True)
    
    def _get_optimized_reaction_plan(self, reaction_type: str, value: float) -> list:
        """
        Çevresel tepki türüne göre optimize edilmiş tepki planı döndürür
        
        Args:
            reaction_type (str): Tepki türü
            value (float): Çevresel değer
            
        Returns:
            list: Eylem ve parametrelerin listesi
        """
        # Tepki planları önbelleği - bellek ve işlemci optimizasyonu
        if not hasattr(self, "_reaction_plans_cache"):
            self._reaction_plans_cache = {}
        
        # Önbellekten yükle
        cache_key = f"{reaction_type}_{int(value)}"
        if cache_key in self._reaction_plans_cache:
            return self._reaction_plans_cache[cache_key]
            
        plan = []
        
        if reaction_type == "hot":
            # Sıcak hava tepkisi
            plan = [
                ("micro_expression", {"emotion": "surprised", "duration": 0.7}),
                ("wait", {"duration": 0.3}),
                ("blink", {"immediate": True}),
                ("look_at", {"x": 0, "y": -0.7, "speed": 0.1}),
            ]
            
            # Mevcut duyguya bağlı olarak farklı mikro ifadeler ekle
            current_emotion = self.config.get("emotions", {}).get("default_emotion", "neutral")
            if current_emotion in ["happy", "excited", "calm"]:
                plan.append(("micro_expression", {"emotion": "surprised", "duration": 1.0}))
                plan.append(("log", {"message": f"Sıcaklık tepkisi: Şaşkın ({value:.1f}°C)"}))
            else:
                plan.append(("micro_expression", {"emotion": "annoyed", "duration": 1.0}))
                plan.append(("log", {"message": f"Sıcaklık tepkisi: Rahatsız ({value:.1f}°C)"}))
                
        elif reaction_type == "cold":
            # Soğuk hava tepkisi
            plan = [
                ("look_at", {"x": 0, "y": 0, "speed": 0.1}),
                ("blink", {"immediate": True}),
                ("micro_expression", {"emotion": "nervous", "duration": 0.8}),
                ("log", {"message": f"Sıcaklık tepkisi: Üşümüş ({value:.1f}°C)"})
            ]
            
        elif reaction_type == "humid":
            # Nemli hava tepkisi
            plan = [
                ("look_at", {"x": 0, "y": -0.5, "speed": 0.1}),
                ("blink", {"immediate": True}),
                ("micro_expression", {"emotion": "disapproval", "duration": 0.8}),
                ("log", {"message": f"Nem tepkisi: Rahatsız (Nem: {value:.1f}%)"})
            ]
            
        elif reaction_type == "dry":
            # Kuru hava tepkisi
            plan = [
                ("look_at", {"x": 0, "y": 0.3, "speed": 0.1}),
                ("micro_expression", {"emotion": "sad", "duration": 0.8}),
                ("log", {"message": f"Nem tepkisi: Mutsuz (Nem: {value:.1f}%)"})
            ]
            
        elif reaction_type == "bright":
            # Parlak ışık tepkisi
            plan = [
                ("blink", {"immediate": True}),
                ("look_at", {"x": 0, "y": 0.8, "speed": 0.3}),
                ("micro_expression", {"emotion": "anxious", "duration": 0.5}),
                ("log", {"message": f"Işık tepkisi: Gözlerini kısmış ({value:.1f} lux)"})
            ]
            
        elif reaction_type == "dark":
            # Karanlık tepkisi
            rand_x = random.uniform(-0.5, 0.5) 
            rand_y = random.uniform(-0.5, 0.5)
            plan = [
                ("look_at", {"x": rand_x, "y": rand_y, "speed": 0.05}),
                ("micro_expression", {"emotion": "fearful", "duration": 0.8}),
                ("log", {"message": f"Işık tepkisi: Endişeli ({value:.1f} lux)"})
            ]
            
        elif reaction_type == "sleepy":
            # Uykulu tepkisi
            plan = [
                ("blink", {"immediate": True}),
                ("wait", {"duration": 0.3}),
                ("blink", {"immediate": True}),
                ("look_at", {"x": 0, "y": 0.5, "speed": 0.05}),
                ("micro_expression", {"emotion": "sleepy", "duration": 1.5}),
                ("log", {"message": "Zaman tepkisi: Uykulu"})
            ]
            
        elif reaction_type == "energetic":
            # Enerjik tepkisi
            rand_x = random.uniform(-0.8, 0.8)
            rand_y = random.uniform(-0.8, 0.8)
            plan = [
                ("look_at", {"x": rand_x, "y": rand_y, "speed": 0.2}),
                ("micro_expression", {"emotion": "excited", "duration": 0.8}),
                ("log", {"message": "Zaman tepkisi: Enerjik"})
            ]
            
        else:
            # Bilinmeyen tepki türü - minimum plan
            plan = [
                ("log", {"message": f"Bilinmeyen çevresel tepki türü: {reaction_type}"})
            ]
        
        # Tepki planını önbelleğe al (sadece performans kritik tepkiler için)
        if reaction_type in ["hot", "cold", "humid", "dry", "bright", "dark"]:
            self._reaction_plans_cache[cache_key] = plan
            
            # Önbellek boyutu kontrolü
            if len(self._reaction_plans_cache) > 20:
                self._reaction_plans_cache.clear()
        
        return plan

# OLEDController sınıfını OLEDAnimationsMixin ile bağla
try:
    from .oled_controller_base import OLEDController
    # Mixin sınıfını OLEDController ile birleştir - Bu adım normalde oled_controller.py'de yapılacak
except ImportError:
    logger.warning("OLEDController sınıfı içe aktarılamadı, bağımsız olarak çalışıyor.")

if __name__ == "__main__":
    # Test kodu buraya gelecek, ancak modüller bölündüğü için main kodu oled_controller.py'ye taşınacak
    pass