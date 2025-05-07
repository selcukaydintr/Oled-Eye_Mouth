# -*- coding: utf-8 -*-
"""
FACE1 Yüz İfadesi Kontrolü Widget'ı

Bu modül, dashboard üzerinden robot yüzünün ifadesini kontrol
etmek için gereken backend işlevlerini sağlar.
"""

import logging
import json
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class ExpressionWidget:
    """
    Yüz İfadesi Kontrolü Widget'ı
    
    Dashboard'da gösterilecek duygu durumu kontrol arayüzü için
    backend işlevselliği sağlar.
    """
    
    def __init__(self, emotion_engine=None):
        """
        Widget'ı başlat
        
        Args:
            emotion_engine: Duygu motoru referansı
        """
        self.emotion_engine = emotion_engine
        self.emotions = [
            {"id": "neutral", "name": "Nötr"},
            {"id": "happy", "name": "Mutlu"},
            {"id": "sad", "name": "Üzgün"},
            {"id": "angry", "name": "Kızgın"},
            {"id": "surprised", "name": "Şaşkın"},
            {"id": "fearful", "name": "Korkmuş"},
            {"id": "disgusted", "name": "İğrenmiş"},
            {"id": "calm", "name": "Sakin"}
        ]
        logger.info("Yüz İfadesi Kontrolü Widget'ı başlatıldı")
    
    def set_emotion_engine(self, emotion_engine) -> None:
        """
        Duygu motoru referansını ayarlar
        
        Args:
            emotion_engine: Duygu motoru nesnesi
        """
        self.emotion_engine = emotion_engine
    
    def get_widget_data(self) -> Dict[str, Any]:
        """
        Widget tarafından ihtiyaç duyulan verileri döndürür
        
        Returns:
            Widget için gereken verileri içeren sözlük
        """
        data = {
            "emotions": self.emotions,
            "current_emotion": self._get_current_emotion()
        }
        return data
    
    def _get_current_emotion(self) -> Dict[str, Any]:
        """
        Mevcut duygu durumunu alır
        
        Returns:
            Mevcut duygu durumu bilgilerini içeren sözlük
        """
        if not self.emotion_engine:
            return {"state": "neutral", "intensity": 1.0}
        
        return {
            "state": self.emotion_engine.get_current_emotion().get("state", "neutral"),
            "intensity": self.emotion_engine.get_current_emotion().get("intensity", 1.0)
        }
    
    def handle_websocket_message(self, message_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        WebSocket mesajını işler
        
        Args:
            message_data: İşlenecek WebSocket mesaj verisi
            
        Returns:
            İşlem sonucunu içeren yanıt (varsa)
        """
        action = message_data.get("action")
        
        if action == "set_emotion":
            return self._handle_set_emotion(message_data)
        elif action == "show_micro_expression":
            return self._handle_micro_expression(message_data)
        elif action == "get_emotion_state":
            return self._handle_get_emotion_state()
        
        return None
    
    def _handle_set_emotion(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Duygu durumu değiştirme mesajını işler
        
        Args:
            message_data: Mesaj verisi
            
        Returns:
            İşlem sonucunu içeren yanıt
        """
        if not self.emotion_engine:
            return {"status": "error", "message": "Duygu motoru mevcut değil"}
        
        emotion = message_data.get("emotion", "neutral")
        intensity = message_data.get("intensity", 1.0)
        duration = message_data.get("duration", 1.0)
        
        try:
            self.emotion_engine.set_emotion(emotion, intensity=intensity, transition_time=duration)
            
            return {
                "status": "success",
                "emotion": {
                    "state": emotion,
                    "intensity": intensity
                }
            }
        except Exception as e:
            logger.error(f"Duygu durumu ayarlanırken hata: {str(e)}")
            return {"status": "error", "message": f"Duygu ayarlanamadı: {str(e)}"}
    
    def _handle_micro_expression(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Mikro ifade gösterme mesajını işler
        
        Args:
            message_data: Mesaj verisi
            
        Returns:
            İşlem sonucunu içeren yanıt
        """
        if not self.emotion_engine:
            return {"status": "error", "message": "Duygu motoru mevcut değil"}
        
        emotion = message_data.get("emotion", "neutral")
        intensity = message_data.get("intensity", 1.0)
        duration = message_data.get("duration", 0.5)  # Mikro ifadeler genellikle kısa sürer
        
        try:
            self.emotion_engine.show_micro_expression(emotion, duration=duration, intensity=intensity)
            
            return {
                "status": "success",
                "micro_expression": {
                    "state": emotion,
                    "intensity": intensity,
                    "duration": duration
                }
            }
        except Exception as e:
            logger.error(f"Mikro ifade gösterilirken hata: {str(e)}")
            return {"status": "error", "message": f"Mikro ifade gösterilemedi: {str(e)}"}
    
    def _handle_get_emotion_state(self) -> Dict[str, Any]:
        """
        Mevcut duygu durumu sorgulama mesajını işler
        
        Returns:
            Mevcut duygu durumunu içeren yanıt
        """
        current_emotion = self._get_current_emotion()
        
        return {
            "status": "success",
            "type": "emotion_state",
            "emotion": current_emotion
        }
    
    def render(self, widget_id: str = "expression1") -> str:
        """
        Widget HTML içeriğini oluşturur
        
        Args:
            widget_id: Widget benzersiz kimliği
            
        Returns:
            HTML içeriği
        """
        try:
            from jinja2 import Template
            import os
            
            # Şablon dosyasını oku
            template_dir = os.path.abspath(os.path.join(
                os.path.dirname(__file__), 
                "../../../web/templates/widgets"
            ))
            template_path = os.path.join(template_dir, "expression_control_widget.html")
            
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Şablonu işle
            template = Template(template_content)
            return template.render(
                widget_id=widget_id,
                widget_type="expression_control",
                widget_title="Yüz İfadesi Kontrolü",
                emotions=self.emotions,
                last_update_time=""  # Boş bırakılabilir, client tarafında doldurulacak
            )
        except Exception as e:
            logger.error(f"Widget şablonu oluşturulurken hata: {str(e)}")
            return f"<div>Widget yüklenemedi: {str(e)}</div>"
    
    def get_data(self) -> Dict[str, Any]:
        """
        Widget veri API'si için gerekli metot
        
        Returns:
            Widget verilerini içeren sözlük
        """
        return self.get_widget_data()
    
    def get_details(self) -> Dict[str, Any]:
        """
        Widget detaylarını döndürür
        
        Returns:
            Widget detaylarını içeren sözlük
        """
        return {
            "id": "expression_control",
            "name": "Yüz İfadesi Kontrolü",
            "description": "FACE1 yüz ifadesi kontrol arayüzü",
            "type": "expression_control",
            "emotions": self.emotions,
            "widget_id": "expression_control",
            "current_emotion": self._get_current_emotion()
        }
        
    def get_template_name(self) -> str:
        """
        Şablon dosyasının adını döndürür
        
        Returns:
            Şablon dosyasının adı
        """
        return "widgets/expression_control_widget.html"
    
    def set_expression(self, expression_data: Dict[str, Any]) -> bool:
        """
        Yüz ifadesini ayarlar (HTTP API için)
        
        Args:
            expression_data: İfade verileri
            
        Returns:
            İşlem başarılı ise True, değilse False
        """
        if not self.emotion_engine:
            return False
        
        emotion = expression_data.get("emotion", "neutral")
        intensity = expression_data.get("intensity", 1.0)
        duration = expression_data.get("duration", 1.0)
        is_micro = expression_data.get("is_micro", False)
        
        try:
            if is_micro:
                self.emotion_engine.show_micro_expression(emotion, duration=duration, intensity=intensity)
            else:
                self.emotion_engine.set_emotion(emotion, intensity=intensity, transition_time=duration)
            return True
        except Exception as e:
            logger.error(f"İfade ayarlanırken hata: {str(e)}")
            return False
            
    def get_config(self) -> Dict[str, Any]:
        """
        Widget yapılandırmasını döndürür
        
        Returns:
            Widget yapılandırmasını içeren sözlük
        """
        return {}
        
    def update_config(self, config: Dict[str, Any]) -> bool:
        """
        Widget yapılandırmasını günceller
        
        Args:
            config: Yeni yapılandırma
            
        Returns:
            İşlem başarılı ise True, değilse False
        """
        return True
        
    def update_data(self, data: Dict[str, Any]) -> bool:
        """
        Widget verilerini günceller
        
        Args:
            data: Yeni veriler
            
        Returns:
            İşlem başarılı ise True, değilse False
        """
        return True