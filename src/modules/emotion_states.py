#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: emotion_states.py
# Açıklama: Duygu durumları ve ilgili sabit tanımlamaları.
# Bağımlılıklar: enum
# Bağlı Dosyalar: emotion_engine.py

# Versiyon: 0.4.0
# Değişiklikler:
# - [0.4.0] emotion_engine.py dosyasından bölündü (modüler mimari)
# - [0.3.0] Duygu geçişlerini daha akıcı hale getirme ve alt tipler için gelişmiş destekler eklendi
# - [0.2.0] Duygu hafıza sistemi ve duygu tepki eğrileri geliştirildi
# - [0.1.0] Temel duygu motoru sınıfı oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-02
===========================================================
"""

from enum import Enum


class EmotionState(Enum):
    """Duygu durumları için enum"""
    HAPPY = "happy"           # Mutlu
    SAD = "sad"               # Üzgün
    ANGRY = "angry"           # Kızgın
    SURPRISED = "surprised"   # Şaşkın
    FEARFUL = "fearful"       # Korkmuş
    DISGUSTED = "disgusted"   # İğrenmiş
    CALM = "calm"             # Sakin
    NEUTRAL = "neutral"       # Nötr


# Duygu geçiş matrisi - bir duygudan diğerine geçiş kolaylığı (0.0-1.0)
# Yüksek değer = kolay geçiş, düşük değer = zor geçiş
EMOTION_TRANSITION_MATRIX = {
    EmotionState.HAPPY.value: {
        EmotionState.HAPPY.value: 1.0,
        EmotionState.SAD.value: 0.3,
        EmotionState.ANGRY.value: 0.2,
        EmotionState.SURPRISED.value: 0.8,
        EmotionState.FEARFUL.value: 0.3,
        EmotionState.DISGUSTED.value: 0.4,
        EmotionState.CALM.value: 0.7,
        EmotionState.NEUTRAL.value: 0.9
    },
    EmotionState.SAD.value: {
        EmotionState.HAPPY.value: 0.3,
        EmotionState.SAD.value: 1.0,
        EmotionState.ANGRY.value: 0.6,
        EmotionState.SURPRISED.value: 0.5,
        EmotionState.FEARFUL.value: 0.7,
        EmotionState.DISGUSTED.value: 0.6,
        EmotionState.CALM.value: 0.5,
        EmotionState.NEUTRAL.value: 0.7
    },
    EmotionState.ANGRY.value: {
        EmotionState.HAPPY.value: 0.1,
        EmotionState.SAD.value: 0.6,
        EmotionState.ANGRY.value: 1.0,
        EmotionState.SURPRISED.value: 0.7,
        EmotionState.FEARFUL.value: 0.5,
        EmotionState.DISGUSTED.value: 0.8,
        EmotionState.CALM.value: 0.2,
        EmotionState.NEUTRAL.value: 0.4
    },
    EmotionState.SURPRISED.value: {
        EmotionState.HAPPY.value: 0.7,
        EmotionState.SAD.value: 0.5,
        EmotionState.ANGRY.value: 0.6,
        EmotionState.SURPRISED.value: 1.0,
        EmotionState.FEARFUL.value: 0.8,
        EmotionState.DISGUSTED.value: 0.6,
        EmotionState.CALM.value: 0.5,
        EmotionState.NEUTRAL.value: 0.7
    },
    EmotionState.FEARFUL.value: {
        EmotionState.HAPPY.value: 0.2,
        EmotionState.SAD.value: 0.6,
        EmotionState.ANGRY.value: 0.4,
        EmotionState.SURPRISED.value: 0.8,
        EmotionState.FEARFUL.value: 1.0,
        EmotionState.DISGUSTED.value: 0.5,
        EmotionState.CALM.value: 0.3,
        EmotionState.NEUTRAL.value: 0.5
    },
    EmotionState.DISGUSTED.value: {
        EmotionState.HAPPY.value: 0.2,
        EmotionState.SAD.value: 0.6,
        EmotionState.ANGRY.value: 0.8,
        EmotionState.SURPRISED.value: 0.6,
        EmotionState.FEARFUL.value: 0.5,
        EmotionState.DISGUSTED.value: 1.0,
        EmotionState.CALM.value: 0.3,
        EmotionState.NEUTRAL.value: 0.5
    },
    EmotionState.CALM.value: {
        EmotionState.HAPPY.value: 0.8,
        EmotionState.SAD.value: 0.5,
        EmotionState.ANGRY.value: 0.2,
        EmotionState.SURPRISED.value: 0.6,
        EmotionState.FEARFUL.value: 0.4,
        EmotionState.DISGUSTED.value: 0.3,
        EmotionState.CALM.value: 1.0,
        EmotionState.NEUTRAL.value: 0.9
    },
    EmotionState.NEUTRAL.value: {
        EmotionState.HAPPY.value: 0.8,
        EmotionState.SAD.value: 0.6,
        EmotionState.ANGRY.value: 0.3,
        EmotionState.SURPRISED.value: 0.7,
        EmotionState.FEARFUL.value: 0.5,
        EmotionState.DISGUSTED.value: 0.4,
        EmotionState.CALM.value: 0.9,
        EmotionState.NEUTRAL.value: 1.0
    }
}

# Duygu tepki eğrileri - bir duygu uyarıcısına karşı zamanla verilen tepkiler
EMOTION_RESPONSE_CURVES = {
    # Mutluluk tepkisi - hızlı yükselir, yavaş düşer
    EmotionState.HAPPY.value: [(0.0, 0.0), (0.1, 0.5), (0.3, 0.9), (0.5, 1.0), (0.7, 0.9), (0.9, 0.7), (1.0, 0.6)],
    
    # Üzüntü tepkisi - yavaş yükselir, çok yavaş düşer
    EmotionState.SAD.value: [(0.0, 0.0), (0.2, 0.3), (0.4, 0.7), (0.6, 0.9), (0.8, 1.0), (0.9, 0.95), (1.0, 0.9)],
    
    # Kızgınlık tepkisi - çok hızlı yükselir, orta hızda düşer
    EmotionState.ANGRY.value: [(0.0, 0.0), (0.05, 0.6), (0.1, 0.9), (0.2, 1.0), (0.5, 0.8), (0.7, 0.6), (1.0, 0.3)],
    
    # Şaşkınlık tepkisi - ani yükseliş, hızlı düşüş
    EmotionState.SURPRISED.value: [(0.0, 0.0), (0.05, 0.9), (0.1, 1.0), (0.3, 0.7), (0.5, 0.4), (0.7, 0.2), (1.0, 0.0)],
    
    # Korku tepkisi - ani yükseliş, orta düşüş
    EmotionState.FEARFUL.value: [(0.0, 0.0), (0.05, 0.8), (0.1, 1.0), (0.3, 0.9), (0.5, 0.7), (0.8, 0.4), (1.0, 0.2)],
    
    # İğrenme tepkisi - orta yükseliş, yavaş düşüş
    EmotionState.DISGUSTED.value: [(0.0, 0.0), (0.1, 0.4), (0.2, 0.8), (0.3, 1.0), (0.6, 0.8), (0.8, 0.6), (1.0, 0.4)],
    
    # Sakinlik tepkisi - yavaş yükseliş, çok yavaş düşüş
    EmotionState.CALM.value: [(0.0, 0.0), (0.2, 0.3), (0.4, 0.6), (0.6, 0.8), (0.8, 0.9), (0.9, 1.0), (1.0, 1.0)],
    
    # Nötr tepkisi - orta yükseliş, orta düşüş
    EmotionState.NEUTRAL.value: [(0.0, 0.0), (0.2, 0.5), (0.5, 1.0), (0.8, 0.5), (1.0, 0.0)]
}

# Gelişmiş duygu türleri - temel duyguların alt türleri
EMOTION_SUBTYPES = {
    EmotionState.HAPPY.value: ["joy", "content", "excited", "amused", "proud"],
    EmotionState.SAD.value: ["disappointed", "lonely", "depressed", "miserable", "guilty"],
    EmotionState.ANGRY.value: ["frustrated", "irritated", "enraged", "annoyed", "bitter"],
    EmotionState.SURPRISED.value: ["amazed", "astonished", "shocked", "startled", "confused"],
    EmotionState.FEARFUL.value: ["anxious", "terrified", "nervous", "worried", "scared"],
    EmotionState.DISGUSTED.value: ["disapproval", "revolted", "judgmental", "avoidant", "loathing"],
    EmotionState.CALM.value: ["relaxed", "peaceful", "serene", "tranquil", "composed"],
    EmotionState.NEUTRAL.value: ["indifferent", "objective", "detached", "unconcerned", "balanced"]
}

# Duygu yoğunluk seviyeleri - alt duygular için tanımlayıcı
EMOTION_INTENSITY_LABELS = {
    (0.0, 0.2): "slightly",
    (0.2, 0.4): "somewhat",
    (0.4, 0.6): "moderately",
    (0.6, 0.8): "quite",
    (0.8, 1.0): "extremely"
}


def get_emotion_state(emotion_name: str) -> EmotionState:
    """
    Duygu adından EmotionState nesnesini döndürür
    
    Args:
        emotion_name (str): Duygu adı
        
    Returns:
        EmotionState: Duygu durumu. Geçersiz ise None.
    """
    try:
        return EmotionState(emotion_name)
    except ValueError:
        return None


def is_valid_emotion(emotion_name: str) -> bool:
    """
    Duygu adının geçerli olup olmadığını kontrol eder
    
    Args:
        emotion_name (str): Duygu adı
        
    Returns:
        bool: Geçerli ise True, değilse False
    """
    try:
        EmotionState(emotion_name)
        return True
    except ValueError:
        return False


def get_all_emotions() -> list:
    """
    Tüm duygu durumlarını liste olarak döndürür
    
    Returns:
        list: Tüm duygu durumlarının string listesi
    """
    return [e.value for e in EmotionState]


def get_emotion_subtype(emotion_name: str, intensity: float) -> str:
    """
    Belirli bir duygu ve yoğunluğa göre alt tür seçer
    
    Args:
        emotion_name (str): Duygu adı
        intensity (float): Duygu yoğunluğu (0.0-1.0)
    
    Returns:
        str: Alt tür adı. Eğer geçersiz duygu veya alt tür yoksa None.
    """
    if not is_valid_emotion(emotion_name):
        return None
        
    subtypes = EMOTION_SUBTYPES.get(emotion_name, [])
    if not subtypes:
        return None
    
    # Yoğunluğa göre alt tür seç
    subtype_index = min(int(intensity * len(subtypes)), len(subtypes) - 1)
    return subtypes[subtype_index]


def get_intensity_label(intensity: float) -> str:
    """
    Belirli bir yoğunluk için etiket döndürür
    
    Args:
        intensity (float): Duygu yoğunluğu (0.0-1.0)
    
    Returns:
        str: Yoğunluk etiketi
    """
    for intensity_range, label in EMOTION_INTENSITY_LABELS.items():
        if intensity_range[0] <= intensity < intensity_range[1]:
            return label
    
    return "extremely"  # Varsayılan