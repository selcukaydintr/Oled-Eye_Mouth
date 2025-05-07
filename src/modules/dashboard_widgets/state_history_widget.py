#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FACE1 Durum İzleme ve Tarihçe Widget'ı
Bu modül, sistem durumunu ve durum tarihçesini görselleştiren widget için backend işlevlerini içerir.
"""

import time
import logging
import json
from typing import Dict, List, Any, Optional, Union
from datetime import datetime, timedelta

# Modül seviyesinde logger
logger = logging.getLogger(__name__)

class StateHistoryWidget:
    """
    Sistem durumu ve durum tarihçesi widget sınıfı
    """
    
    def __init__(self, state_history_manager=None, emotion_engine=None):
        """
        StateHistoryWidget sınıfını başlatır
        
        Args:
            state_history_manager: Sistem durum tarihçesini yöneten sınıf örneği
            emotion_engine: Duygu motoru kontrolü (opsiyonel)
        """
        self.widget_id = "state_history"
        self.state_history_manager = state_history_manager
        self.emotion_engine = emotion_engine
        self.default_history_limit = 50
        
        # Widget verilerini saklamak için sözlükler
        self._current_state = {
            "system": "initializing",
            "emotion": {"state": "neutral", "intensity": 1.0},
            "speaking": False,
            "animation": {"current": None, "playing": False},
            "metrics": {
                "cpu": 0.0,
                "memory": 0.0,
                "temperature": 0.0,
                "uptime": 0.0
            }
        }
        
        logger.info(f"StateHistoryWidget başlatıldı: {self.widget_id}")
    
    def get_widget_data(self, limit: int = None) -> Dict[str, Any]:
        """
        Widget'ın şablon verilerini döndürür
        
        Args:
            limit: Tarihçe girişi sınırı
            
        Returns:
            Widget şablon verileri
        """
        if limit is None:
            limit = self.default_history_limit
            
        # Mevcut sistem durumu bilgilerini al
        system_state = self._current_state["system"]
        emotion_state = f"{self._current_state['emotion']['state']} ({self._current_state['emotion']['intensity']:.1f})"
        speaking_state = "Konuşuyor" if self._current_state["speaking"] else "Sessiz"
        animation_state = self._current_state["animation"]["current"] if self._current_state["animation"]["playing"] else "Yok"
        
        # Metrikler
        metrics = self._current_state["metrics"]
        cpu_usage = f"{metrics['cpu']:.1f}%"
        memory_usage = f"{metrics['memory']:.1f}%"
        temperature = f"{metrics['temperature']:.1f}°C"
        uptime = self._format_uptime(metrics["uptime"])
        
        # Tarihçe girişleri
        history_entries = self.get_history_entries(limit) if self.state_history_manager else []
        
        return {
            "widget_id": self.widget_id,
            "system_state": system_state,
            "emotion_state": emotion_state,
            "speaking_state": speaking_state,
            "animation_state": animation_state,
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "temperature": temperature,
            "uptime": uptime,
            "history_entries": history_entries
        }
    
    def update_state(self, state_type: str, state_value: Union[str, Dict, bool]) -> None:
        """
        Belirli bir durum tipinin değerini günceller
        
        Args:
            state_type: Durum tipi ('system', 'emotion', 'speaking', 'animation', 'metrics')
            state_value: Durum değeri
        """
        if state_type == "system":
            self._current_state["system"] = state_value
        elif state_type == "emotion":
            if isinstance(state_value, dict):
                self._current_state["emotion"] = state_value
            else:
                self._current_state["emotion"]["state"] = state_value
        elif state_type == "speaking":
            self._current_state["speaking"] = bool(state_value)
        elif state_type == "animation":
            if isinstance(state_value, dict):
                self._current_state["animation"] = state_value
        elif state_type == "metrics":
            if isinstance(state_value, dict):
                self._current_state["metrics"].update(state_value)
        
        logger.debug(f"Widget durum güncellendi: {state_type} = {state_value}")
    
    def get_history_entries(self, limit: int = 50) -> List[Dict[str, Any]]:
        """
        Durum tarihçesi girişlerini döndürür
        
        Args:
            limit: Döndürülecek giriş sayısı
            
        Returns:
            Tarihçe girişleri listesi
        """
        if not self.state_history_manager:
            return []
        
        history_data = self.state_history_manager.get_history(limit)
        
        # Girişleri widget formatına dönüştür
        entries = []
        for entry in history_data:
            entry_type = entry.get("type", "system")
            entry_message = entry.get("message", "")
            entry_time = entry.get("timestamp", datetime.now())
            
            # Zamanı formatla
            if isinstance(entry_time, (int, float)):
                entry_time = datetime.fromtimestamp(entry_time)
            
            # İkon belirle
            icon_map = {
                "system": "🖥️",
                "emotion": "😀",
                "speaking": "🗣️",
                "animation": "🎭",
                "error": "⚠️"
            }
            icon = icon_map.get(entry_type, "📝")
            
            # Zamanı formatla (örn: "2 dakika önce")
            time_str = self._format_relative_time(entry_time)
            
            entries.append({
                "type": entry_type,
                "message": entry_message,
                "time": time_str,
                "icon": icon
            })
        
        return entries
    
    def get_activity_data(self, hours: int = 24) -> Dict[str, Any]:
        """
        Etkinlik grafiği için gerekli verileri döndürür
        
        Args:
            hours: Kaç saat geriye gidileceği
            
        Returns:
            Etkinlik verileri
        """
        if not self.state_history_manager:
            return {"points": []}
        
        # Belirli bir süre içindeki tüm olayları al
        since_time = datetime.now() - timedelta(hours=hours)
        events = self.state_history_manager.get_events_since(since_time)
        
        # Her olay tipi için noktalar oluştur
        points = []
        for event in events:
            event_type = event.get("type", "system")
            event_time = event.get("timestamp", datetime.now())
            
            if isinstance(event_time, (int, float)):
                event_time = datetime.fromtimestamp(event_time)
                
            points.append({
                "type": event_type,
                "timestamp": event_time.isoformat()
            })
        
        return {"points": points}
    
    def add_history_entry(self, entry_type: str, message: str) -> None:
        """
        Tarihçeye yeni bir giriş ekler
        
        Args:
            entry_type: Giriş tipi ('system', 'emotion', 'speaking', 'animation', 'error')
            message: Giriş mesajı
        """
        if self.state_history_manager:
            self.state_history_manager.add_entry(entry_type, message)
    
    @staticmethod
    def _format_uptime(seconds: float) -> str:
        """
        Çalışma süresini okunabilir bir formata dönüştürür
        
        Args:
            seconds: Saniye cinsinden çalışma süresi
            
        Returns:
            Biçimlendirilmiş çalışma süresi
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f"{hours}sa {minutes}dk {secs}sn"
        else:
            return f"{minutes}dk {secs}sn"
    
    @staticmethod
    def _format_relative_time(timestamp: datetime) -> str:
        """
        Bir zaman damgasını göreceli bir zaman ifadesine dönüştürür
        
        Args:
            timestamp: Zaman damgası
            
        Returns:
            Göreceli zaman ifadesi (örn. "2 dakika önce")
        """
        now = datetime.now()
        diff = now - timestamp
        seconds = diff.total_seconds()
        
        if seconds < 60:
            return f"{int(seconds)} saniye önce"
        elif seconds < 3600:
            return f"{int(seconds // 60)} dakika önce"
        elif seconds < 86400:
            return f"{int(seconds // 3600)} saat önce"
        else:
            return timestamp.strftime("%H:%M:%S %d.%m.%Y")
    
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
            "id": "state_history",
            "name": "Durum İzleme ve Tarihçe",
            "description": "Sistem durumunu ve durum tarihçesini görüntüler",
            "type": "state_history",
            "widget_id": "state_history",
            "current_state": self._current_state
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
        
        if action == "get_history":
            limit = message_data.get("limit", self.default_history_limit)
            return {
                "status": "success",
                "history": self.get_history_entries(limit)
            }
        elif action == "get_activity_data":
            hours = message_data.get("hours", 24)
            return {
                "status": "success",
                "activity": self.get_activity_data(hours)
            }
        
        return None
    
    def render(self, widget_id: str = "state_history1") -> str:
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
            template_path = os.path.join(template_dir, "state_history_widget.html")
            
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Widget verileri
            data = self.get_widget_data()
            data["widget_id"] = widget_id
            
            # Şablonu işle
            template = Template(template_content)
            return template.render(**data)
        except Exception as e:
            logger.error(f"Widget şablonu oluşturulurken hata: {str(e)}")
            return f"<div>Widget yüklenemedi: {str(e)}</div>"
    
    def get_template_name(self) -> str:
        """
        Şablon dosyasının adını döndürür
        
        Returns:
            Şablon dosyasının adı
        """
        return "widgets/state_history_widget.html"
    
    def get_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Son durum tarihçesini döndürür (API için)
        
        Args:
            limit: Döndürülecek giriş sayısı
            
        Returns:
            Tarihçe girişleri listesi
        """
        return self.get_history_entries(limit)
    
    def get_config(self) -> Dict[str, Any]:
        """
        Widget yapılandırmasını döndürür
        
        Returns:
            Widget yapılandırmasını içeren sözlük
        """
        return {
            "historyLimit": self.default_history_limit
        }
        
    def update_config(self, config: Dict[str, Any]) -> bool:
        """
        Widget yapılandırmasını günceller
        
        Args:
            config: Yeni yapılandırma
            
        Returns:
            İşlem başarılı ise True, değilse False
        """
        if "historyLimit" in config:
            self.default_history_limit = config["historyLimit"]
            return True
        return True
        
    def update_data(self, data: Dict[str, Any]) -> bool:
        """
        Widget verilerini günceller
        
        Args:
            data: Yeni veriler
            
        Returns:
            İşlem başarılı ise True, değilse False
        """
        try:
            if "system" in data:
                self.update_state("system", data["system"])
                
            if "emotion" in data:
                self.update_state("emotion", data["emotion"])
                
            if "speaking" in data:
                self.update_state("speaking", data["speaking"])
                
            if "animation" in data:
                self.update_state("animation", data["animation"])
                
            if "metrics" in data:
                self.update_state("metrics", data["metrics"])
                
            if "historyEntry" in data:
                self.add_history_entry(
                    data["historyEntry"].get("type", "system"),
                    data["historyEntry"].get("message", "")
                )
                
            return True
        except Exception as e:
            logger.error(f"Widget verileri güncellenirken hata: {str(e)}")
            return False