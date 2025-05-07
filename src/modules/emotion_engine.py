#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: emotion_engine.py
# Açıklama: Duygu motoru modülü. Duygu durumlarını işler ve yönetir.
# Bağımlılıklar: logging, threading, time
# Bağlı Dosyalar: oled_controller.py, led_controller.py

# Versiyon: 0.5.0
# Değişiklikler:
# - [0.5.0] Tam modüler yapıya dönüştürüldü, sınıf yapısı iyileştirildi
# - [0.4.0] Modüler mimari - dosya parçalandı ve yeniden yapılandırıldı
# - [0.3.0] Duygu geçişlerini daha akıcı hale getirme ve alt tipler için gelişmiş destekler eklendi
# - [0.2.0] Duygu hafıza sistemi ve duygu tepki eğrileri geliştirildi
# - [0.1.0] Temel duygu motoru sınıfı oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-02
===========================================================
"""

import os
import sys
import time
import json
import logging
from typing import Dict, List, Tuple, Optional, Union, Callable
from pathlib import Path

# Proje dizinini ve include dizinini Python yoluna ekle
PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(str(PROJECT_DIR))

# Alt modülleri içe aktar
from src.modules.emotion_states import EmotionState, is_valid_emotion
from src.modules.emotion_engine_base import EmotionEngineBase
from src.modules.emotion_engine_transitions import EmotionTransitionsMixin
from src.modules.emotion_engine_memory import EmotionMemoryMixin
from src.modules.emotion_engine_expressions import EmotionExpressionsMixin

# Logger yapılandırması
logger = logging.getLogger("EmotionEngine")


class EmotionEngine(EmotionEngineBase, EmotionTransitionsMixin, EmotionMemoryMixin, EmotionExpressionsMixin):
    """
    Duygu motoru ana sınıfı
    
    Bu sınıf, robotun duygu durumlarını yönetir ve işler.
    Duygu geçişleri, duygu ifadeleri ve duygu hafızası gibi özellikler sağlar.
    
    Mixin sınıfların davranışlarını birleştirir:
    - EmotionEngineBase: Temel davranışlar, yaşam döngüsü ve geri çağrılar
    - EmotionTransitionsMixin: Duygu geçişleri işlevselliği
    - EmotionMemoryMixin: Duygu hafızası işlevselliği
    - EmotionExpressionsMixin: Duygu ifadeleri işlevselliği
    """
    
    def __init__(self, config: Dict):
        """
        Duygu motoru sınıfını başlatır
        
        Args:
            config (dict): Yapılandırma ayarları
        """
        # Temel sınıf başlatma
        EmotionEngineBase.__init__(self, config)
        
        # Kişilik matrisi ayarları
        self.personality_matrix = self._load_personality()
        
        # Alt mixin modüllerinin başlatma metotlarını çağır
        self.__init_memory()
        self.__init_expressions()
        
        logger.info("Duygu Motoru başlatıldı.")
    
    def _load_personality(self) -> Dict:
        """
        Kişilik matrisini yükler
        
        Returns:
            Dict: Kişilik matrisi
        """
        # Varsayılan kişilik
        default_personality = {
            "baseline_emotions": {
                EmotionState.HAPPY.value: 0.6,
                EmotionState.SAD.value: 0.3,
                EmotionState.ANGRY.value: 0.2,
                EmotionState.SURPRISED.value: 0.5,
                EmotionState.FEARFUL.value: 0.3,
                EmotionState.DISGUSTED.value: 0.2,
                EmotionState.CALM.value: 0.7,
                EmotionState.NEUTRAL.value: 0.8
            },
            "response_intensity": {
                EmotionState.HAPPY.value: 0.8,
                EmotionState.SAD.value: 0.6,
                EmotionState.ANGRY.value: 0.4,
                EmotionState.SURPRISED.value: 0.9,
                EmotionState.FEARFUL.value: 0.5,
                EmotionState.DISGUSTED.value: 0.3,
                EmotionState.CALM.value: 0.7,
                EmotionState.NEUTRAL.value: 0.6
            },
            "emotion_duration": {
                EmotionState.HAPPY.value: 1.2,  # Çarpan (1.0 = normal süre)
                EmotionState.SAD.value: 1.5,
                EmotionState.ANGRY.value: 0.8,
                EmotionState.SURPRISED.value: 0.5,
                EmotionState.FEARFUL.value: 0.7,
                EmotionState.DISGUSTED.value: 0.9,
                EmotionState.CALM.value: 1.5,
                EmotionState.NEUTRAL.value: 1.0
            }
        }
        
        # Yapılandırmadan kişilik profilini al
        profile_name = self.emotion_config.get("personality_profile", "balanced")
        
        # Farklı kişilik profilleri için önceden tanımlanmış ayarlar
        if profile_name == "cheerful":
            # Neşeli profil: Mutluluk yüksek, üzüntü düşük
            default_personality["baseline_emotions"][EmotionState.HAPPY.value] = 0.8
            default_personality["baseline_emotions"][EmotionState.SAD.value] = 0.2
            default_personality["response_intensity"][EmotionState.HAPPY.value] = 0.9
        elif profile_name == "serious":
            # Ciddi profil: Sakinlik yüksek, sürpriz düşük
            default_personality["baseline_emotions"][EmotionState.CALM.value] = 0.9
            default_personality["baseline_emotions"][EmotionState.SURPRISED.value] = 0.3
        elif profile_name == "reactive":
            # Tepkisel profil: Duygu geçişleri hızlı
            for emotion in EmotionState:
                default_personality["emotion_duration"][emotion.value] = 0.7
        elif profile_name == "calm":
            # Sakin profil: Duygu geçişleri yavaş
            for emotion in EmotionState:
                default_personality["emotion_duration"][emotion.value] = 1.5
        
        # Yapılandırmadan kişilik ayarlarını al
        custom_personality = self.emotion_config.get("personality", {})
        
        # Varsayılan kişiliği özel ayarlarla güncelle
        personality = default_personality.copy()
        for category, values in custom_personality.items():
            if category in personality:
                personality[category].update(values)
        
        return personality
    
    def _update_loop(self) -> None:
        """
        Duygu güncelleme döngüsü
        """
        logger.info("Duygu güncelleme döngüsü başladı.")
        
        while self.is_running:
            try:
                # Geçiş ilerleme durumunu güncelle
                self._update_emotion_transition()
                
                # Mikro ifadeleri kontrol et ve işle
                self._process_micro_expressions()
                
                # Duygu durumunu güncelle (zaman bazlı azalma)
                self._process_emotion_decay()
                
                # Duygu hafıza sistemini güncelle
                self._update_emotion_memory()
                
                # Hafıza katmanlarını güncelle
                self._update_memory_tiers()
                
                # Her güncelleme sonrası geri çağrıları çalıştır
                self._trigger_callbacks("emotion_update", self.get_current_emotion())
                
            except Exception as e:
                logger.error(f"Duygu güncelleme döngüsünde hata: {e}")
            
            # Güncelleme aralığı kadar bekle
            time.sleep(self.update_interval)
        
        logger.info("Duygu güncelleme döngüsü sonlandı.")
    
    def save_state(self, filepath: str) -> bool:
        """
        Duygu motoru durumunu dosyaya kaydeder
        
        Args:
            filepath (str): Kayıt dosyasının yolu
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            state = {
                "current_emotion": self.current_emotion,
                "emotion_memory": self.emotion_memory,
                "micro_expressions": self.micro_expressions,
                "personality_matrix": self.personality_matrix
            }
            
            with open(filepath, 'w') as f:
                json.dump(state, f, indent=2)
            
            logger.info(f"Duygu motoru durumu kaydedildi: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Durum kaydedilirken hata: {e}")
            return False
    
    def load_state(self, filepath: str) -> bool:
        """
        Duygu motoru durumunu dosyadan yükler
        
        Args:
            filepath (str): Kayıt dosyasının yolu
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            if not os.path.exists(filepath):
                logger.warning(f"Durum dosyası bulunamadı: {filepath}")
                return False
            
            with open(filepath, 'r') as f:
                state = json.load(f)
            
            self.current_emotion = state["current_emotion"]
            self.emotion_memory = state["emotion_memory"]
            self.micro_expressions = state["micro_expressions"]
            self.personality_matrix = state["personality_matrix"]
            
            logger.info(f"Duygu motoru durumu yüklendi: {filepath}")
            
            # Geri çağrıyı tetikle
            self._trigger_callbacks("emotion_changed", self.get_current_emotion())
            
            return True
            
        except Exception as e:
            logger.error(f"Durum yüklenirken hata: {e}")
            return False


# Test kodu
if __name__ == "__main__":
    # Logging yapılandırması
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Varsayılan yapılandırma
    test_config = {
        "emotions": {
            "default_emotion": "calm",
            "transition_speed": 0.5,
            "personality_profile": "cheerful",
            "personality": {
                "baseline_emotions": {
                    "happy": 0.7,
                    "angry": 0.3
                }
            }
        }
    }
    
    print("Duygu Motoru Test")
    print("----------------")
    
    # Duygu motoru örneğini oluştur
    emotion_engine = EmotionEngine(test_config)
    
    # Geri çağrıları tanımla
    def on_emotion_changed(data):
        print(f"Duygu değişti: {data['state']}, yoğunluk: {data['intensity']:.2f}")
    
    def on_emotion_update(data):
        if data["transition_progress"] < 1.0:
            print(f"Duygu geçiş durumu: {data['transition_progress']:.2f}")
    
    # Geri çağrıları kaydet
    emotion_engine.register_callback("emotion_changed", on_emotion_changed)
    emotion_engine.register_callback("emotion_update", on_emotion_update)
    
    # Duygu motorunu başlat
    if emotion_engine.start():
        print("Duygu motoru başlatıldı")
        
        # Test senaryosu
        print("\n--- Duygu Testleri ---")
        
        # Mevcut duyguyu görüntüle
        current = emotion_engine.get_current_emotion()
        print(f"Başlangıç duygusu: {current['state']}, yoğunluk: {current['intensity']:.2f}")
        
        # Duygu değişikliği testi
        print("\nMutlu duygusuna geçiş...")
        emotion_engine.set_emotion("happy", 0.8)
        time.sleep(2)
        
        print("\nŞaşkın duygusuna hızlı geçiş...")
        emotion_engine.set_emotion("surprised", 1.0)
        time.sleep(2)
        
        print("\nSakin duygusuna yavaş geçiş...")
        emotion_engine.transition_to("calm", 3.0)
        time.sleep(3)
        
        # Mikro ifade testi
        print("\nMikro ifade testi...")
        emotion_engine.add_micro_expression("angry", 0.7, 0.5, 0.2)
        time.sleep(1)
        
        # Duygu hafızası testi
        print("\nDuygu hafızası:")
        memory = emotion_engine.get_emotion_memory()
        for time_stamp, emotion, intensity in memory:
            print(f"  - {emotion}: {intensity:.2f}")
        
        # Özet bilgi testi
        print("\nDuygu özeti:")
        summary = emotion_engine.generate_emotional_summary()
        for key, value in summary.items():
            print(f"  - {key}: {value}")
        
        # Durdur
        emotion_engine.stop()
        print("\nDuygu motoru durduruldu.")
    else:
        print("Duygu motoru başlatılamadı!")
    
    print("\nTest tamamlandı.")