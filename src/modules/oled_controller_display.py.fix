#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: oled_controller_display.py
# Açıklama: OLED ekranları için çizim işlevlerini içeren modül.
# Bağımlılıklar: PIL, adafruit_ssd1306
# Bağlı Dosyalar: hardware_defines.py, oled_controller_base.py

# Versiyon: 0.3.1
# Değişiklikler:
# - [0.3.1] Modül 3'e bölündü, çizim fonksiyonları bu modüle taşındı
# - [0.3.0] Duygu alt tiplerinin görsel ifadeleri geliştirildi
# - [0.2.0] Göz takibi özelliği eklendi ve mikro ifadeler geliştirildi
#
# Yazar: GitHub Copilot
# Tarih: 2025-04-30
===========================================================
"""

import logging
import time
import math
import random
from typing import Dict, List, Tuple, Optional, Union

# Logger yapılandırması
logger = logging.getLogger("OLEDController")

class OLEDDisplayMixin:
    """
    OLED ekranlar için çizim işlevlerini içeren mixin sınıfı.
    OLEDController sınıfı ile birlikte kullanılmak üzere tasarlanmıştır.
    """

    def _draw_all_displays(self) -> None:
        """
        Tüm ekranlara mevcut duygu durumuna göre çizim yapar
        """
        # Kullanılacak duygu belirleme (mikro ifade varsa onu kullan)
        current_emotion = self.config.get("emotions", {}).get("default_emotion", "calm")
        
        # Eğer bir mikro ifade varsa, onu kullan
        if self.micro_expression:
            current_emotion = self.micro_expression
        # Eğer geçiş yapılıyorsa ve EmotionEngine'den bir geçiş hedefi alınmışsa
        elif "target" in self.config.get("emotions", {}) and self.config["emotions"].get("target") is not None:
            target = self.config["emotions"]["target"]
            source = self.config["emotions"].get("source", current_emotion)
            progress = target.get("progress", 0.0)
            
            # İki duygu arasında geçiş yaparken blend_emotions fonksiyonunu kullan
            if progress > 0.0 and progress < 1.0:
                # Duygu geçişini daha doğal bir eğri ile yumuşat (kübik easing fonksiyonu)
                # Bu fonksiyon başta yavaş, ortada hızlı, sonda tekrar yavaşlayan bir geçiş sağlar
                eased_progress = progress
                
                # Kübik easing fonksiyonu (daha doğal geçiş için)
                if progress < 0.5:
                    eased_progress = 4 * progress * progress * progress
                else:
                    p = progress - 1
                    eased_progress = 1 + 4 * p * p * p
                
                # Duygular arasında yumuşak geçiş için blend_emotions kullan
                current_emotion = self.blend_emotions(source, target["state"], eased_progress)
                
                # Göz pozisyonu ve kırpma durumunu duygu geçişine göre ayarla
                if 0.45 < progress < 0.55:
                    # Geçişin ortasında göz kırpma olasılığı artar
                    if random.random() < 0.2:
                        self.blink_state = not self.blink_state
                
                # "Concerned" ve "excited" gibi duygular için göz hareketi hızını ayarla
                if target["state"] in ["concerned", "nervous", "excited", "anxious"]:
                    self.eye_move_speed = min(0.3, self.eye_move_speed * 1.5)
                elif target["state"] in ["calm", "peaceful", "sleepy"]:
                    self.eye_move_speed = max(0.05, self.eye_move_speed * 0.7)
                
                # Eğer geçiş tamamlanmışsa, hedef duygusunu ayarla
                if progress >= 1.0:
                    self.config["emotions"]["default_emotion"] = target["state"]
        
        # Sol ve sağ gözleri çiz
        self.draw_eyes(current_emotion, self.blink_state)
        
        # Ağzı çiz
        self.draw_mouth(current_emotion)
    
    def draw_eyes(self, emotion: str, blink_state: bool) -> None:
        """
        Göz ekranlarına çizim yapar
        
        Args:
            emotion (str): Duygu durumu
            blink_state (bool): Göz kırpma durumu (True: açık, False: kapalı)
        """
        # Performans optimizasyonu: Duygu alt tiplerini önbellekleme
        if not hasattr(self, "_emotion_subtypes_map"):
            # Alt duygu tiplerini ana duygulara eşle - önbelleğe al
            self._emotion_subtypes_map = {
                # Happy alt tipleri
                "joy": "happy", "content": "happy", "excited": "excited",
                "amused": "happy", "proud": "happy",
                
                # Sad alt tipleri
                "disappointed": "sad", "lonely": "sad", "depressed": "sad",
                "miserable": "sad", "guilty": "sad",
                
                # Angry alt tipleri
                "frustrated": "angry", "irritated": "angry", "enraged": "angry",
                "annoyed": "angry", "bitter": "angry",
                
                # Surprised alt tipleri
                "amazed": "surprised", "astonished": "surprised", "shocked": "surprised",
                "startled": "surprised", "confused": "confused",
                
                # Fearful alt tipleri
                "anxious": "fearful", "terrified": "fearful", "nervous": "fearful", 
                "worried": "fearful", "scared": "fearful",
                
                # Disgusted alt tipleri
                "disapproval": "disgusted", "revolted": "disgusted", "judgmental": "disgusted",
                "avoidant": "disgusted", "loathing": "disgusted",
                
                # Calm alt tipleri
                "relaxed": "calm", "peaceful": "calm", "serene": "calm",
                "tranquil": "calm", "composed": "calm",
                
                # Neutral alt tipleri
                "indifferent": "neutral", "objective": "neutral", "detached": "neutral", 
                "unconcerned": "neutral", "balanced": "neutral",
                
                # Özel duygu ifadeleri
                "sleepy": "sleepy", "bored": "bored", "love": "love"
            }
        
        # Alt duygu tipini ana duyguya eşle - önbellek kullan
        base_emotion = emotion
        if emotion in self._emotion_subtypes_map:
            base_emotion = self._emotion_subtypes_map[emotion]
        
        # Göz şekilleri ve parametrelerini hesapla - çoklu göz çizimleri için önbellek
        eye_params = {}
        eye_width = 0
        eye_height = 0
        
        # Performans optimizasyonu: Göz parametrelerini tek seferde hesapla
        if blink_state:
            # Duyguya göre göz biçimini belirle
            eye_width = self.width * 3 // 4  # Varsayılan göz genişliği
            eye_height = self.height * 2 // 3  # Varsayılan göz yüksekliği
            
            # Duyguya göre göz boyutlarını ayarla
            if base_emotion == "happy" or base_emotion == "excited":
                eye_height = self.height * 1 // 2  # Mutlu gözler daha küçük
            elif base_emotion == "surprised" or base_emotion == "fearful":
                eye_height = self.height * 3 // 4  # Şaşkın gözler daha büyük
                eye_width = self.width * 4 // 5
            elif base_emotion == "angry":
                eye_height = self.height * 1 // 2  # Kızgın gözler daha dar
                
            # Göz parametrelerini kaydet
            eye_params["width"] = eye_width
            eye_params["height"] = eye_height
        
        # Sol göz ve sağ göz ekranlarını çiz
        for eye_name in ["left_eye", "right_eye"]:
            if self.displays[eye_name] is None or self.draw_objects[eye_name] is None:
                continue
            
            try:
                # Tampon görüntüyü temizle - optimize edilmiş yaklaşım
                buffer = self.buffers[eye_name]
                draw = self.draw_objects[eye_name]
                
                # Performans optimizasyonu: Tüm ekranı temizleme hızlı yöntem
                buffer.paste(0, (0, 0, buffer.width, buffer.height))
                
                # Ekran boyutlarını al
                width, height = buffer.width, buffer.height
                center_x, center_y = width // 2, height // 2
                
                if blink_state:
                    # Göz açık
                    
                    # Parametreleri al
                    eye_width = eye_params["width"]
                    eye_height = eye_params["height"]
                    
                    # Duyguya göre göz şekli çizimi
                    if base_emotion == "angry":
                        # Kızgın göz için açıyı ayarla
                        if eye_name == "left_eye":
                            # Performans optimizasyonu: polygon çizimlerini optimize et
                            points = [(center_x - eye_width//2, center_y - 5), 
                                     (center_x - eye_width//2 + 5, center_y - 15), 
                                     (center_x + eye_width//2, center_y - 5),
                                     (center_x + eye_width//2, center_y + eye_height//3),
                                     (center_x - eye_width//2, center_y + eye_height//3)]
                            draw.polygon(points, outline=1, width=1)
                        else:
                            points = [(center_x - eye_width//2, center_y - 5), 
                                     (center_x + eye_width//2 - 5, center_y - 15), 
                                     (center_x + eye_width//2, center_y - 5),
                                     (center_x + eye_width//2, center_y + eye_height//3),
                                     (center_x - eye_width//2, center_y + eye_height//3)]
                            draw.polygon(points, outline=1, width=1)
                    elif base_emotion == "disgusted":
                        # Tiksinmiş göz şekli
                        if eye_name == "left_eye":
                            points = [(center_x - eye_width//2, center_y), 
                                     (center_x, center_y - eye_height//3), 
                                     (center_x + eye_width//2, center_y),
                                     (center_x + eye_width//2, center_y + eye_height//3),
                                     (center_x - eye_width//2, center_y + eye_height//3)]
                            draw.polygon(points, outline=1, width=1)
                        else:
                            points = [(center_x - eye_width//2, center_y), 
                                     (center_x, center_y - eye_height//3), 
                                     (center_x + eye_width//2, center_y),
                                     (center_x + eye_width//2, center_y + eye_height//3),
                                     (center_x - eye_width//2, center_y + eye_height//3)]
                            draw.polygon(points, outline=1, width=1)
                    elif base_emotion == "sad":
                        # Üzgün göz için açıyı ayarla
                        if eye_name == "left_eye":
                            points = [(center_x - eye_width//2, center_y), 
                                     (center_x - eye_width//4, center_y - eye_height//4), 
                                     (center_x + eye_width//2, center_y),
                                     (center_x + eye_width//3, center_y + eye_height//3),
                                     (center_x - eye_width//3, center_y + eye_height//3)]
                            draw.polygon(points, outline=1, width=1)
                        else:
                            points = [(center_x - eye_width//2, center_y), 
                                     (center_x + eye_width//4, center_y - eye_height//4), 
                                     (center_x + eye_width//2, center_y),
                                     (center_x + eye_width//3, center_y + eye_height//3),
                                     (center_x - eye_width//3, center_y + eye_height//3)]
                            draw.polygon(points, outline=1, width=1)
                    elif base_emotion == "sleepy" or base_emotion == "bored":
                        # Uykulu/sıkılmış göz çizimi
                        eye_height = height * 1 // 3  # Göz kapakları yarı açık
                        draw.ellipse((center_x - eye_width//2, center_y - eye_height//2, 
                                     center_x + eye_width//2, center_y + eye_height//2), outline=1)
                    elif base_emotion == "confused":
                        # Kafası karışmış göz - bir göz normal diğeri farklı
                        if eye_name == "left_eye":
                            eye_height = height * 2 // 3
                            draw.ellipse((center_x - eye_width//2, center_y - eye_height//2, 
                                         center_x + eye_width//2, center_y + eye_height//2), outline=1)
                        else:
                            # Sağ göz daha küçük ve açılı
                            eye_height = height * 1 // 2
                            draw.arc((center_x - eye_width//2, center_y - eye_height//2, 
                                     center_x + eye_width//2, center_y + eye_height//2),
                                     180, 0, fill=1, width=1)
                    elif base_emotion == "love":
                        # Aşık göz - kalp şeklinde
                        heart_size = min(width, height) // 3
                        
                        # İki daire yan yana ve bir üçgen altında (kalp şekli)
                        draw.ellipse(
                            (center_x - heart_size, center_y - heart_size // 2, 
                             center_x, center_y + heart_size // 2),
                            outline=1
                        )
                        draw.ellipse(
                            (center_x, center_y - heart_size // 2, 
                             center_x + heart_size, center_y + heart_size // 2),
                            outline=1
                        )
                        draw.polygon(
                            [(center_x - heart_size, center_y),
                             (center_x + heart_size, center_y),
                             (center_x, center_y + heart_size)],
                            outline=1
                        )
                    else:
                        # Normal göz çizimi - optimizasyon için parametreleri önbelleğe al
                        ellipse_coords = (center_x - eye_width//2, center_y - eye_height//2, 
                                        center_x + eye_width//2, center_y + eye_height//2)
                        draw.ellipse(ellipse_coords, outline=1)
                    
                    # Göz bebeği çizimi (duyguya ve göz pozisyonuna göre)
                    # Normal göz bebeği boyutu
                    pupil_size = min(width, height) // 8
                    
                    # Duyguya göre göz bebeği boyutunu ayarla
                    if base_emotion == "fearful" or base_emotion == "surprised":
                        pupil_size = min(width, height) // 6  # Daha büyük göz bebeği
                    elif base_emotion == "disgusted" or base_emotion == "angry":
                        pupil_size = min(width, height) // 10  # Daha küçük göz bebeği
                        
                    # Performans optimizasyonu: Göz bebeği pozisyonunu tek seferde hesapla
                    max_offset_x = eye_width // 4
                    max_offset_y = eye_height // 4
                    
                    pupil_offset_x = int(self.eye_position[0] * max_offset_x)
                    pupil_offset_y = int(self.eye_position[1] * max_offset_y)
                    
                    # Kısıtlamaları uygula
                    pupil_offset_x = max(-max_offset_x, min(max_offset_x, pupil_offset_x))
                    pupil_offset_y = max(-max_offset_y, min(max_offset_y, pupil_offset_y))
                    
                    # Love duygusu haricinde göz bebeği çiz
                    if base_emotion != "love":
                        # Optimizasyon: Ellips koordinatlarını önbelleğe al
                        ellipse_coords = (center_x - pupil_size + pupil_offset_x, 
                                        center_y - pupil_size + pupil_offset_y, 
                                        center_x + pupil_size + pupil_offset_x, 
                                        center_y + pupil_size + pupil_offset_y)
                        draw.ellipse(ellipse_coords, fill=1)
                
                else:
                    # Göz kapalı - daha basit çizimler, optimize edildi
                    line_width = 2  # Varsayılan çizgi kalınlığı
                    
                    if base_emotion == "angry":
                        # Kızgın kapalı göz - açılı çizgiler
                        offset = 8
                        draw.line([(center_x - width//3, center_y - offset), 
                                  (center_x + width//3, center_y)], fill=1, width=line_width)
                    elif base_emotion == "sad":
                        # Üzgün kapalı göz - aşağı eğri çizgiler
                        draw.arc((center_x - width//3, center_y, 
                                 center_x + width//3, center_y + height//3), 
                                 0, 180, fill=1, width=line_width)
                    else:
                        # Normal kapalı göz - düz çizgi
                        line_coords = [(center_x - width//3, center_y), 
                                     (center_x + width//3, center_y)]
                        draw.line(line_coords, fill=1, width=line_width)
                
            except Exception as e:
                logger.error(f"Göz çizilirken hata: {eye_name}, duygu: {emotion}, hata: {e}")
                # Hata oluşursa varsayılan bir göz çiz
                try:
                    buffer = self.buffers[eye_name]
                    draw = self.draw_objects[eye_name]
                    width, height = buffer.width, buffer.height
                    center_x, center_y = width // 2, height // 2
                    
                    # Basit oval göz
                    draw.ellipse((center_x - width//4, center_y - height//4, 
                                 center_x + width//4, center_y + height//4), outline=1)
    
                except Exception as e:
                    logger.error(f"Varsayılan göz çizilirken bile hata: {e}")
    def draw_mouth(self, emotion: str) -> None:
        """
        Ağız ekranına çizim yapar
        
        Args:
            emotion (str): Duygu durumu
        """
        if self.displays["mouth"] is None or self.draw_objects["mouth"] is None:
            return
        
        try:
            # Tampon görüntüyü temizle - optimize edilmiş yöntemle
            buffer = self.buffers["mouth"]
            draw = self.draw_objects["mouth"]
            
            # Performans optimizasyonu: Daha hızlı ekran temizleme
            buffer.paste(0, (0, 0, buffer.width, buffer.height))
            
            # Ekran boyutlarını al
            width, height = buffer.width, buffer.height
            center_x, center_y = width // 2, height // 2
            
            # Performans optimizasyonu: Duygu tipi haritasını önbelleğe alma
            if not hasattr(self, "_emotion_subtypes_map"):
                # Alt duygu tiplerini ana duygulara eşle (draw_eyes metodu ile paylaşılacak)
                self._emotion_subtypes_map = {
                    # Happy alt tipleri
                    "joy": "happy", "content": "happy", "excited": "excited",
                    "amused": "happy", "proud": "happy",
                    
                    # Sad alt tipleri
                    "disappointed": "sad", "lonely": "sad", "depressed": "sad",
                    "miserable": "sad", "guilty": "sad",
                    
                    # Angry alt tipleri
                    "frustrated": "angry", "irritated": "angry", "enraged": "angry",
                    "annoyed": "angry", "bitter": "angry",
                    
                    # Surprised alt tipleri
                    "amazed": "surprised", "astonished": "surprised", "shocked": "surprised",
                    "startled": "surprised", "confused": "confused",
                    
                    # Fearful alt tipleri
                    "anxious": "fearful", "terrified": "fearful", "nervous": "fearful", 
                    "worried": "fearful", "scared": "fearful",
                    
                    # Disgusted alt tipleri
                    "disapproval": "disgusted", "revolted": "disgusted", "judgmental": "disgusted",
                    "avoidant": "disgusted", "loathing": "disgusted",
                    
                    # Calm alt tipleri
                    "relaxed": "calm", "peaceful": "calm", "serene": "calm",
                    "tranquil": "calm", "composed": "calm",
                    
                    # Neutral alt tipleri
                    "indifferent": "neutral", "objective": "neutral", "detached": "neutral", 
                    "unconcerned": "neutral", "balanced": "neutral",
                    
                    # Özel duygu ifadeleri
                    "sleepy": "sleepy", "bored": "bored", "love": "love"
                }
            
            # Alt duygu tipi analizi ve görsel ifade seçimi - önbelleği kullan
            base_emotion = emotion
            if emotion in self._emotion_subtypes_map:
                base_emotion = self._emotion_subtypes_map[emotion]
            
            # Performans optimizasyonu: Sık kullanılan parametreleri önbelleğe al
            # Ağız boyutları için standart değerler - birçok duyguda tekrar kullanılır
            standard_mouth_width = width * 2 // 3
            standard_mouth_height = height // 3
            
            # Happy duygu tipi ve alt tipleri
            if base_emotion == "happy":
                mouth_width = standard_mouth_width
                mouth_height = standard_mouth_height
                
                # Alt tiplere göre ağız ifadesi ayarlaması
                if emotion == "joy":
                    # Geniş gülümseme, dişler gösterilir
                    arc_coords = (center_x - mouth_width//2, center_y - mouth_height//2,
                                center_x + mouth_width//2, center_y + mouth_height)
                    draw.arc(arc_coords, 0, 180, fill=1, width=2)
                    
                    # Diş çizgisi
                    line_coords = [(center_x - mouth_width//3, center_y), 
                                  (center_x + mouth_width//3, center_y)]
                    draw.line(line_coords, fill=1, width=1)
                        
                elif emotion == "content":
                    # Orta seviyeli gülümseme
                    arc_coords = (center_x - mouth_width//2, center_y - mouth_height//4,
                                center_x + mouth_width//2, center_y + mouth_height//2)
                    draw.arc(arc_coords, 0, 180, fill=1, width=2)
                    
                elif emotion == "amused":
                    # Eğlenen gülümseme, biraz daha geniş
                    arc_coords = (center_x - mouth_width//2, center_y - mouth_height//4,
                                center_x + mouth_width//2, center_y + mouth_height//2)
                    draw.arc(arc_coords, 0, 180, fill=1, width=2)
                    
                    # Küçük bir çizgi daha ekle, gülüşü vurgulamak için
                    small_arc_coords = (center_x - mouth_width//4, center_y, 
                                      center_x + mouth_width//4, center_y + mouth_height//4)
                    draw.arc(small_arc_coords, 0, 180, fill=1, width=1)
                    
                elif emotion == "proud":
                    # Gurur duyduğunu gösteren gülümseme, daha ölçülü
                    arc_coords = (center_x - mouth_width//2, center_y - mouth_height//8,
                                center_x + mouth_width//2, center_y + mouth_height//3)
                    draw.arc(arc_coords, 0, 180, fill=1, width=2)
                    
                else:
                    # Varsayılan mutlu ağız
                    arc_coords = (center_x - mouth_width//2, center_y - mouth_height//4,
                                center_x + mouth_width//2, center_y + mouth_height//2)
                    draw.arc(arc_coords, 0, 180, fill=1, width=2)
            
            # Sad duygu tipi ve alt tipleri
            elif base_emotion == "sad":
                mouth_width = standard_mouth_width
                mouth_height = standard_mouth_height
                
                # Alt tiplere göre ağız ifadesi ayarlaması - ortak parametreleri önbelleğe al
                arc_params = {
                    "depressed": {
                        "coords": (center_x - mouth_width//2, center_y + mouth_height//2,
                                center_x + mouth_width//2, center_y - mouth_height//4),
                        "line": None
                    },
                    "miserable": {
                        "coords": (center_x - mouth_width//2, center_y + mouth_height//2,
                                center_x + mouth_width//2, center_y - mouth_height//3),
                        "line": [(center_x - mouth_width//4, center_y + mouth_height//8),
                              (center_x + mouth_width//4, center_y + mouth_height//8)]
                    },
                    "guilty": {
                        "coords": (center_x - mouth_width//2, center_y + mouth_height//3,
                                center_x + mouth_width//2, center_y - mouth_height//8),
                        "line": None
                    },
                    "lonely": {
                        "coords": (center_x - mouth_width//2, center_y + mouth_height//3,
                                center_x + mouth_width//2, center_y - mouth_height//8),
                        "line": None
                    },
                    "disappointed": {
                        "coords": (center_x - mouth_width//2, center_y + mouth_height//4,
                                center_x + mouth_width//2, center_y - mouth_height//8),
                        "line": None
                    },
                    "default": {
                        "coords": (center_x - mouth_width//2, center_y + mouth_height//4,
                                center_x + mouth_width//2, center_y - mouth_height//8),
                        "line": None
                    }
                }
                
                # Parametreleri seç
                params = arc_params.get(emotion, arc_params["default"])
                
                # Arc çiz
                draw.arc(params["coords"], 180, 360, fill=1, width=2)
                
                # Ek çizgi varsa çiz
                if params["line"]:
                    draw.line(params["line"], fill=1, width=1)
            
            # Angry duygu tipi ve alt tipleri
            elif base_emotion == "angry":
                mouth_width = standard_mouth_width
                
                # Alt tiplere göre ağız ifadesi seçimi
                if emotion == "enraged":
                    # Çok kızgın ağız - dişler görünüyor ve açık
                    rect_coords = (center_x - mouth_width//2, center_y - height//8,
                                  center_x + mouth_width//2, center_y + height//4)
                    draw.rectangle(rect_coords, outline=1)
                    
                    # Diş çizgileri
                    for i in range(5):
                        x = center_x - mouth_width//3 + (mouth_width*2//3) * i // 4
                        tooth_coords = [(x, center_y - height//8), (x, center_y + height//4)]
                        draw.line(tooth_coords, fill=1, width=1)
                    
                elif emotion == "frustrated" or emotion == "irritated":
                    # Sinirli/tahriş olmuş ağız - sıkılmış
                    line_coords = [(center_x - mouth_width//2, center_y),
                                  (center_x + mouth_width//2, center_y)]
                    draw.line(line_coords, fill=1, width=3)
                
                elif emotion == "bitter":
                    # Acı ağız - aşağı bükük ve sıkı
                    arc_coords = (center_x - mouth_width//2, center_y + height//6,
                                 center_x + mouth_width//2, center_y - height//8)
                    draw.arc(arc_coords, 190, 350, fill=1, width=2)
                    
                else:
                    # Varsayılan kızgın ağız - düz çizgi
                    line_coords = [(center_x - mouth_width//2, center_y + height//20),
                                  (center_x + mouth_width//2, center_y + height//20)]
                    draw.line(line_coords, fill=1, width=2)
            
            # Surprised duygu tipi ve alt tipleri
            elif base_emotion == "surprised":
                # Performans optimizasyonu: Ortak elips parametrelerini hesapla
                ellipse_params = {
                    "shocked": (center_x - width//4, center_y - height//6,
                               center_x + width//4, center_y + height//4),
                    "amazed": (center_x - width//4, center_y - height//8,
                              center_x + width//4, center_y + height//4),
                    "startled": (center_x - width//5, center_y - height//10,
                                center_x + width//5, center_y + height//5),
                    "astonished": (center_x - width//4, center_y - height//6,
                                  center_x + width//4, center_y + height//4),
                    "default": (center_x - width//5, center_y - height//8,
                               center_x + width//5, center_y + height//5)
                }
                
                # Parametreleri seç
                ellipse_coords = ellipse_params.get(emotion, ellipse_params["default"])
                
                # Elips çiz
                draw.ellipse(ellipse_coords, outline=1, width=2)
                
                # Ek özellikler
                if emotion == "astonished":
                    # Ünlem işareti
                    line_coords = [(center_x, center_y - height//10), 
                                  (center_x, center_y + height//10)]
                    draw.line(line_coords, fill=1, width=1)
                    
                    dot_coords = (center_x - 1, center_y + height//8 - 1,
                                 center_x + 1, center_y + height//8 + 1)
                    draw.ellipse(dot_coords, fill=1)
            
            # Fearful duygu tipi ve alt tipleri
            elif base_emotion == "fearful":
                mouth_width = width // 2
                mouth_height = height // 4
                
                # Alt tiplere göre ağız ifadesi ayarlaması
                if emotion == "terrified":
                    # Dehşete düşmüş ağız - büyük oval
                    ellipse_coords = (center_x - width//3, center_y - height//6,
                                     center_x + width//3, center_y + height//3)
                    draw.ellipse(ellipse_coords, outline=1, width=2)
                    
                elif emotion == "anxious" or emotion == "nervous":
                    # Endişeli/sinirli ağız - ince ve titrek çizgi
                    # Performans optimizasyonu: Önbelleğe nokta listesi al
                    points = []
                    num_points = 10
                    
                    # Daha az rastgele sayı üretimi ile nokta hesaplama
                    seed_vals = [0, -2, -1, 1, 2, -1, -2, 0, 1, 2]
                    for i in range(num_points):
                        x = center_x - mouth_width//2 + mouth_width * i // (num_points-1)
                        # Titrek çizgi için yarı-rastgele dikey offset
                        y_offset = seed_vals[i % len(seed_vals)]
                        points.append((x, center_y + y_offset))
                    
                    # Titrek çizgi çiz - tek seferde çiz
                    for i in range(1, len(points)):
                        draw.line([points[i-1], points[i]], fill=1, width=1)
                    
                elif emotion == "worried" or emotion == "scared":
                    # Endişeli/korkmuş ağız - aşağı eğimli çizgi
                    arc_coords = (center_x - mouth_width//2, center_y + mouth_height//2,
                                 center_x + mouth_width//2, center_y - mouth_height//8)
                    draw.arc(arc_coords, 190, 350, fill=1, width=2)
                    
                else:
                    # Varsayılan korku ağız ifadesi - hafif oval
                    ellipse_coords = (center_x - mouth_width//2, center_y - mouth_height//4,
                                     center_x + mouth_width//2, center_y + mouth_height//2)
                    draw.ellipse(ellipse_coords, outline=1, width=1)
            
            # Disgusted duygu tipi ve alt tipleri
            elif base_emotion == "disgusted":
                mouth_width = standard_mouth_width
                
                # Alt tiplere göre ağız ifadesi ayarlaması
                if emotion == "revolted":
                    # Tiksinen ağız - çok çarpık
                    # Performans optimizasyonu: Poligon noktalarını tek seferde hesapla
                    points = [(center_x - mouth_width//2, center_y),
                             (center_x - mouth_width//4, center_y + height//6),
                             (center_x, center_y),
                             (center_x + mouth_width//4, center_y - height//8),
                             (center_x + mouth_width//2, center_y)]
                    
                    # Çizgiyi çiz - tek seferde poligon
                    for i in range(1, len(points)):
                        draw.line([points[i-1], points[i]], fill=1, width=2)
                    
                elif emotion in ["disapproval", "judgmental"]:
                    # Onaylamayan/yargılayıcı ağız - tek taraflı aşağı eğimli
                    arc_coords = (center_x - mouth_width//2, center_y + height//8,
                                 center_x + mouth_width//2, center_y - height//8)
                    draw.arc(arc_coords, 200, 340, fill=1, width=2)
                
                elif emotion == "loathing":
                    # Nefret ağzı - çok çarpık ve biraz açık
                    # Dış çizgi
                    arc_coords = (center_x - mouth_width//2, center_y + height//6,
                                 center_x + mouth_width//2, center_y - height//8)
                    draw.arc(arc_coords, 210, 330, fill=1, width=2)
                    
                    # İç çizgi
                    inner_arc_coords = (center_x - mouth_width//3, center_y + height//10,
                                       center_x + mouth_width//3, center_y)
                    draw.arc(inner_arc_coords, 210, 330, fill=1, width=1)
                
                else:
                    # Varsayılan tiksinme ifadesi
                    arc_coords = (center_x - mouth_width//2, center_y + height//10,
                                 center_x + mouth_width//2, center_y - height//10)
                    draw.arc(arc_coords, 190, 350, fill=1, width=2)
            
            # Confused duygu tipi
            elif emotion == "confused":
                # Kafası karışık ağız - zikzak veya dalgalı
                mouth_width = standard_mouth_width
                mouth_height = height // 6
                
                # Performans optimizasyonu: Önişlenmiş zikzak noktaları
                # Bir kereliğine sinüs hesapla ve önbelleğe al
                if not hasattr(self, "_confused_wave_points"):
                    segments = 8
                    self._confused_wave_points = []
                    
                    for i in range(segments + 1):
                        x_ratio = i / segments
                        x = center_x - mouth_width // 2 + int(mouth_width * x_ratio)
                        # Sinüs dalgası şeklinde dikey ofset (daha az hesaplama)
                        y_offset = int(math.sin(i * math.pi / 2) * mouth_height / 3)
                        self._confused_wave_points.append((x, center_y + y_offset))
                
                # Önbelleğe alınmış noktaları kullan
                for i in range(len(self._confused_wave_points) - 1):
                    draw.line([self._confused_wave_points[i], 
                              self._confused_wave_points[i+1]], fill=1, width=2)
            
            # Excited duygu tipi
            elif emotion == "excited":
                # Heyecanlı ağız - büyük açık gülümseme
                mouth_width = width * 3 // 4
                mouth_height = height // 2
                
                # Eliptik gülümseme
                outer_arc_coords = (center_x - mouth_width // 2, center_y - mouth_height // 3, 
                                   center_x + mouth_width // 2, center_y + mouth_height)
                draw.arc(outer_arc_coords, 0, 180, fill=1, width=2)
                
                # İç çizgi (diş veya dil)
                inner_arc_coords = (center_x - mouth_width // 3, center_y, 
                                   center_x + mouth_width // 3, center_y + mouth_height // 2)
                draw.arc(inner_arc_coords, 0, 180, fill=1, width=1)
            
            # Bored duygu tipi
            elif emotion == "bored":
                # Sıkılmış ağız - çok az eğri, neredeyse düz
                mouth_width = width // 2
                
                # Hafif aşağı eğri
                arc_coords = (center_x - mouth_width // 2, center_y - 5, 
                             center_x + mouth_width // 2, center_y + 15)
                draw.arc(arc_coords, 190, 350, fill=1, width=2)
            
            # Sleepy duygu tipi
            elif emotion == "sleepy":
                # Uykulu ağız - esniyor gibi
                mouth_width = width // 3
                mouth_height = height // 3
                
                # Oval ağız
                ellipse_coords = (center_x - mouth_width // 2, center_y - mouth_height // 2, 
                                 center_x + mouth_width // 2, center_y + mouth_height // 2)
                draw.ellipse(ellipse_coords, outline=1, width=2)
                
                # İçine "Z" harfi çiz (uyku sembolü)
                z_width = mouth_width // 3
                z_height = mouth_height // 3
                z_x = center_x + z_width // 2
                z_y = center_y - z_height // 2
                
                # Z harfini oluşturan çizgiler
                z_top = (z_x - z_width, z_y - z_height, z_x + z_width, z_y - z_height)
                z_diag = (z_x + z_width, z_y - z_height, z_x - z_width, z_y + z_height)
                z_bottom = (z_x - z_width, z_y + z_height, z_x + z_width, z_y + z_height)
                
                draw.line(z_top, fill=1)
                draw.line(z_diag, fill=1)
                draw.line(z_bottom, fill=1)
            
            # Love duygu tipi
            elif emotion == "love":
                # Aşık ağız - büyük gülümseme, kalp şekli
                mouth_width = standard_mouth_width
                mouth_height = height // 3
                
                # Geniş gülümseme
                arc_coords = (center_x - mouth_width // 2, center_y - mouth_height, 
                             center_x + mouth_width // 2, center_y + mouth_height)
                draw.arc(arc_coords, 0, 180, fill=1, width=2)
                
                # Küçük kalp (ağzın üzerinde) - performans için optimize edilmiş
                heart_size = mouth_height // 2
                heart_y = center_y - mouth_height - heart_size
                
                # İki daire yan yana - tek seferde hesapla
                left_circle = (center_x - heart_size, heart_y, 
                             center_x, heart_y + heart_size)
                right_circle = (center_x, heart_y, 
                              center_x + heart_size, heart_y + heart_size)
                
                draw.ellipse(left_circle, fill=1)
                draw.ellipse(right_circle, fill=1)
                
                # Üçgen (kalp alt kısmı)
                heart_points = [(center_x - heart_size, heart_y + heart_size // 2),
                               (center_x + heart_size, heart_y + heart_size // 2),
                               (center_x, heart_y + heart_size * 2)]
                draw.polygon(heart_points, fill=1)
                
            # Calm duygu tipi ve alt tipleri
            elif base_emotion == "calm":
                mouth_width = standard_mouth_width
                
                # Alt tiplere göre ağız ifadesi parametrelerini önbelleğe al
                arc_params = {
                    "relaxed": {
                        "coords": (center_x - mouth_width//2, center_y - height//16,
                                 center_x + mouth_width//2, center_y + height//6),
                        "angles": (0, 180)
                    },
                    "peaceful": {
                        "coords": (center_x - mouth_width//2, center_y - height//16,
                                 center_x + mouth_width//2, center_y + height//6),
                        "angles": (0, 180)
                    },
                    "serene": {
                        "coords": (center_x - mouth_width//2, center_y - height//10,
                                 center_x + mouth_width//2, center_y + height//20),
                        "angles": (0, 180)
                    },
                    "tranquil": {
                        "coords": (center_x - mouth_width//2, center_y - height//10,
                                 center_x + mouth_width//2, center_y + height//20),
                        "angles": (0, 180)
                    },
                    "default": {
                        "coords": [(center_x - mouth_width//2, center_y),
                                  (center_x + mouth_width//2, center_y)],
                        "angles": None  # Çizgi için açı yok
                    }
                }
                
                params = arc_params.get(emotion, arc_params["default"])
                
                # Eğer açılar tanımlandıysa arc çiz, değilse çizgi
                if params["angles"]:
                    draw.arc(params["coords"], params["angles"][0], params["angles"][1], 
                            fill=1, width=1)
                else:
                    draw.line(params["coords"], fill=1, width=1)
            
            # Neutral duygu tipi ve alt tipleri
            elif base_emotion == "neutral":
                mouth_width = standard_mouth_width
                
                # Alt tiplere göre ağız ifadesi - parametre sözlüğü
                neutral_params = {
                    "detached": {
                        "type": "line",
                        "coords": [(center_x - mouth_width//2, center_y),
                                  (center_x + mouth_width//2, center_y)]
                    },
                    "objective": {
                        "type": "line",
                        "coords": [(center_x - mouth_width//2, center_y),
                                  (center_x + mouth_width//2, center_y)]
                    },
                    "indifferent": {
                        "type": "arc",
                        "coords": (center_x - mouth_width//2, center_y + height//30,
                                 center_x + mouth_width//2, center_y - height//30),
                        "angles": (190, 350)
                    },
                    "unconcerned": {
                        "type": "arc",
                        "coords": (center_x - mouth_width//2, center_y + height//30,
                                 center_x + mouth_width//2, center_y - height//30),
                        "angles": (190, 350)
                    },
                    "default": {
                        "type": "line",
                        "coords": [(center_x - mouth_width//2, center_y),
                                  (center_x + mouth_width//2, center_y)]
                    }
                }
                
                params = neutral_params.get(emotion, neutral_params["default"])
                
                # Parametre türüne göre çiz
                if params["type"] == "arc":
                    draw.arc(params["coords"], params["angles"][0], params["angles"][1],
                            fill=1, width=1)
                else:
                    draw.line(params["coords"], fill=1, width=1)
            
            # Diğer durumlar için varsayılan hafif gülümseme
            else:
                # Nötr ağız - hafif gülümseme
                mouth_width = standard_mouth_width
                arc_coords = (center_x - mouth_width//2, center_y - height//20,
                             center_x + mouth_width//2, center_y + height//10)
                draw.arc(arc_coords, 0, 180, fill=1, width=1)
            
        except Exception as e:
            logger.error(f"Ağız çizilirken hata: {e}")
            # Hata durumunda basit bir ağız çiz
            try:
                width, height = buffer.width, buffer.height
                center_x, center_y = width // 2, height // 2
                
                # Basit düz çizgi
                draw.line([(center_x - width//4, center_y), 
                          (center_x + width//4, center_y)], 
                         fill=1, width=1)
            except:
                pass

    def _draw_startup_eye_animation(self, eye_name: str) -> None:
        """
        Göz için başlangıç animasyonu çizer
        
        Args:
            eye_name (str): Göz adı ("left_eye" veya "right_eye")
        """
        buffer = self.buffers[eye_name]
        draw = self.draw_objects[eye_name]
        
        # Ekran boyutlarını al
        width, height = buffer.width, buffer.height
        center_x, center_y = width // 2, height // 2
        
        # İlk aşama: Ekranı temizle
        draw.rectangle((0, 0, width, height), fill=0)
        self.update_display()
        time.sleep(0.3)
        
        # İkinci aşama: Dışarıdan içeriye doğru büyüyen daireler
        max_radius = min(width, height) // 2
        for radius in range(2, max_radius, 2):
            draw.rectangle((0, 0, width, height), fill=0)  # Temizle
            draw.ellipse(
                (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
                outline=1
            )
            self.update_display()
            time.sleep(0.05)
        
        # Üçüncü aşama: Göz bebeği oluştur
        pupil_size = max_radius // 3
        draw.ellipse(
            (center_x - pupil_size, center_y - pupil_size, 
            center_x + pupil_size, center_y + pupil_size),
            fill=1
        )
        self.update_display()
        time.sleep(0.2)
        
        # Dördüncü aşama: Göz kırpma
        draw.rectangle((0, 0, width, height), fill=0)  # Temizle
        draw.line(
            (center_x - max_radius, center_y, center_x + max_radius, center_y),
            fill=1, width=3
        )
        self.update_display()
        time.sleep(0.2)
        
        # Son aşama: Standart göze geri dön
        draw.rectangle((0, 0, width, height), fill=0)  # Temizle
        draw.ellipse(
            (center_x - max_radius, center_y - max_radius, 
            center_x + max_radius, center_y + max_radius),
            outline=1
        )
        draw.ellipse(
            (center_x - pupil_size, center_y - pupil_size, 
            center_x + pupil_size, center_y + pupil_size),
            fill=1
        )
        self.update_display()
    
    def _draw_startup_mouth_animation(self) -> None:
        """
        Ağız için başlangıç animasyonu çizer
        """
        buffer = self.buffers["mouth"]
        draw = self.draw_objects["mouth"]
        
        # Ekran boyutlarını al
        width, height = buffer.width, buffer.height
        center_x, center_y = width // 2, height // 2
        
        # İlk aşama: Ekranı temizle
        draw.rectangle((0, 0, width, height), fill=0)
        self.update_display()
        time.sleep(0.3)
        
        # İkinci aşama: Düz bir çizgi çiz
        mouth_width = width * 2 // 3
        draw.line(
            (center_x - mouth_width // 2, center_y, center_x + mouth_width // 2, center_y),
            fill=1, width=2
        )
        self.update_display()
        time.sleep(0.5)
        
        # Üçüncü aşama: Yavaşça gülümsemeye dönüştür
        mouth_height = height // 3
        steps = 10
        for i in range(steps):
            # Değişim oranı (0-1)
            ratio = i / (steps - 1)
            
            # Temizle
            draw.rectangle((0, 0, width, height), fill=0)
            
            # Arc parametreleri - düz çizgiden eğriye
            arc_height = int(mouth_height * ratio)
            
            # Gülümseme yay çiz
            draw.arc(
                (center_x - mouth_width // 2, center_y - arc_height // 2, 
                center_x + mouth_width // 2, center_y + arc_height),
                0, 180, fill=1, width=2
            )
            
            self.update_display()
            time.sleep(0.05)
        
        # Son aşama: Biraz bekle
        time.sleep(0.3)
    
    def show_startup_animation(self) -> None:
        """
        Başlangıç animasyonunu gösterir
        """
        try:
            logger.info("Başlangıç animasyonu gösteriliyor...")
            
            # Aktivite zamanlayıcısını sıfırla
            self.reset_activity_timer()
            
            # Güç modu kapalıysa açık moda geç
            if self.power_mode != "on":
                self.set_power_mode("on")
            
            # Sol göz animasyonu
            if self.displays["left_eye"] is not None and self.draw_objects["left_eye"] is not None:
                self._draw_startup_eye_animation("left_eye")
            
            # Sağ göz animasyonu
            if self.displays["right_eye"] is not None and self.draw_objects["right_eye"] is not None:
                self._draw_startup_eye_animation("right_eye")
            
            # Ağız animasyonu
            if self.displays["mouth"] is not None and self.draw_objects["mouth"] is not None:
                self._draw_startup_mouth_animation()
                
            # Ekranları güncelle
            self.update_display()
            
            logger.info("Başlangıç animasyonu tamamlandı")
            
        except Exception as e:
            logger.error(f"Başlangıç animasyonu gösterilirken hata: {e}")

    def clear_eyes(self) -> None:
        """
        Göz ekranlarını temizler
        """
        for eye_name in ["left_eye", "right_eye"]:
            if eye_name in self.displays and self.displays[eye_name] is not None:
                draw = self.draw_objects[eye_name]
                buffer = self.buffers[eye_name]
                width, height = buffer.width, buffer.height
                
                # Ekranı temizle
                draw.rectangle((0, 0, width, height), fill=0)
                
        self.update_display()

    def clear_mouth(self) -> None:
        """
        Ağız ekranını temizler
        """
        if "mouth" in self.displays and self.displays["mouth"] is not None:
            draw = self.draw_objects["mouth"]
            buffer = self.buffers["mouth"]
            width, height = buffer.width, buffer.height
            
            # Ekranı temizle
            draw.rectangle((0, 0, width, height), fill=0)
            
        self.update_display()
        
    def show_eyes_growing_circle(self, duration: float = 1.0) -> None:
        """
        Gözlerde büyüyen çember animasyonu gösterir
        
        Args:
            duration (float): Animasyon süresi (saniye)
        """
        for eye_name in ["left_eye", "right_eye"]:
            if eye_name in self.displays and self.displays[eye_name] is not None:
                buffer = self.buffers[eye_name]
                draw = self.draw_objects[eye_name]
                
                # Ekran boyutlarını al
                width, height = buffer.width, buffer.height
                center_x, center_y = width // 2, height // 2
                
                # Maksimum yarıçap
                max_radius = min(width, height) // 2
                
                # Büyüyen çemberler için adım sayısı
                step_count = int(10 * duration)
                
                # Ekranı temizle
                draw.rectangle((0, 0, width, height), fill=0)
                self.update_display()
                
                # Büyüyen çember
                for i in range(step_count):
                    radius = int((i / step_count) * max_radius)
                    if radius < 1:
                        radius = 1
                    
                    # Ekranı temizle
                    draw.rectangle((0, 0, width, height), fill=0)
                    
                    # Çemberi çiz
                    draw.ellipse(
                        (center_x - radius, center_y - radius, center_x + radius, center_y + radius),
                        outline=1
                    )
                    
                    self.update_display()
                    time.sleep(duration / step_count)
                
                # Son olarak göz bebeği ekle
                pupil_size = max_radius // 3
                draw.ellipse(
                    (center_x - pupil_size, center_y - pupil_size, 
                     center_x + pupil_size, center_y + pupil_size),
                    fill=1
                )
                self.update_display()
    
    def blink(self, duration: float = 0.2) -> None:
        """
        Göz kırpma animasyonu gösterir
        
        Args:
            duration (float): Kırpma süresi (saniye)
        """
        for eye_name in ["left_eye", "right_eye"]:
            if eye_name in self.displays and self.displays[eye_name] is not None:
                buffer = self.buffers[eye_name]
                draw = self.draw_objects[eye_name]
                
                # Ekran boyutlarını al
                width, height = buffer.width, buffer.height
                center_x, center_y = width // 2, height // 2
                
                # Mevcut ekran içeriğini yedekle
                original_image = buffer.copy()
                
                # Ekranı temizle ve yatay çizgi çiz
                draw.rectangle((0, 0, width, height), fill=0)
                draw.line((0, center_y, width, center_y), fill=1, width=3)
                self.update_display()
                
                # Belirlenen süre kadar bekle
                time.sleep(duration)
                
                # Orijinal görüntüyü geri yükle
                self.buffers[eye_name].paste(original_image)
                self.update_display()
    
    def show_mouth_expression(self, emotion: str = "happy", intensity: float = 0.7) -> None:
        """
        Belirli bir duyguya göre ağız ifadesi gösterir
        
        Args:
            emotion (str): Gösterilecek duygu
            intensity (float): İfade yoğunluğu
        """
        if "mouth" in self.displays and self.displays["mouth"] is not None:
            # Ekranı temizle
            self.clear_mouth()
            
            # Ağız ifadesini çiz
            self.draw_mouth(emotion)
            self.update_display()
    
    def animate_mouth_speaking(self, duration: float = 1.0, pattern: str = "default", volume: float = 0.5) -> None:
        """
        Konuşma animasyonuyla ağzın hareket etmesini sağlar
        
        Args:
            duration (float): Animasyon süresi
            pattern (str): Konuşma deseni
            volume (float): Ses seviyesi (0.0-1.0 arası), ağız açıklığını etkiler
        """
        if "mouth" not in self.displays or self.displays["mouth"] is None:
            return
            
        buffer = self.buffers["mouth"]
        draw = self.draw_objects["mouth"]
        
        # Ekran boyutlarını al
        width, height = buffer.width, buffer.height
        
        # Konuşma için ağız durumları
        states = 5
        iterations = int(duration * 4)  # Saniyede yaklaşık 4 durum değişikliği
        
        # Konuşma desenleri
        patterns = {
            "default": [0, 1, 2, 3, 4, 3, 2, 1],
            "fast": [0, 2, 4, 2, 0, 3, 1],
            "slow": [0, 1, 2, 2, 3, 3, 4, 4, 3, 3, 2, 2, 1, 1]
        }
        
        # Deseni seç (yoksa varsayılanı kullan)
        speak_pattern = patterns.get(pattern, patterns["default"])
        
        # Ses seviyesini normalize et (0.0-1.0 arası)
        volume = max(0.0, min(1.0, volume))
        
        for i in range(iterations):
            # Ağzı temizle
            draw.rectangle((0, 0, width, height), fill=0)
            
            # Konuşma durumuna göre ağzı çiz
            state = speak_pattern[i % len(speak_pattern)]
            
            # Ağız açıklığı hesaplama (ses seviyesi ile etkilenir)
            # 0: kapalı, 4: tam açık - ses seviyesi ağız açıklığını artırır
            raw_mouth_open = state / 4
            
            # Ses seviyesi düşükse ağız daha az açılır, yüksekse daha fazla açılır
            mouth_open = raw_mouth_open * (0.3 + 0.7 * volume)
            
            # Ağız şeklini çiz
            center_x, center_y = width // 2, height // 2
            mouth_width = int(width * 0.6)
            mouth_height = int(height * 0.2 * mouth_open) + 3
            
            # Ağız dış çizgisi
            draw.ellipse(
                (center_x - mouth_width // 2, center_y - mouth_height // 2,
                 center_x + mouth_width // 2, center_y + mouth_height // 2),
                outline=1
            )
            
            # Ağız içi (konuşurken açık ağız için)
            if mouth_open > 0.1:
                inner_height = max(1, int(mouth_height * 0.7))
                draw.ellipse(
                    (center_x - mouth_width // 2 + 3, center_y - inner_height // 2,
                     center_x + mouth_width // 2 - 3, center_y + inner_height // 2),
                    fill=1
                )
            
            self.update_display()
            time.sleep(duration / iterations)

# OLEDController sınıfını OLEDDisplayMixin ile bağla
try:
    from .oled_controller_base import OLEDController
    # Mixin sınıfını OLEDController ile birleştir - Bu adım normalde oled_controller.py'de yapılacak
except ImportError:
    logger.warning("OLEDController sınıfı içe aktarılamadı, bağımsız olarak çalışıyor.")

if __name__ == "__main__":
    # Test kodu buraya gelecek, ancak modüller bölündüğü için main kodu oled_controller.py'ye taşınacak
    pass