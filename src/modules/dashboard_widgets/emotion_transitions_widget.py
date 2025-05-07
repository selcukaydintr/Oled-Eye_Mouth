# -*- coding: utf-8 -*-
"""
FACE1 Hızlı Duygu Geçişleri Widget'ı

Bu modül, robot yüzünün duygu durumlarını sekanslar halinde 
kontrol etmek için gereken backend işlevlerini sağlar.
"""

import logging
import json
import uuid
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class EmotionTransitionsWidget:
    """
    Hızlı Duygu Geçişleri Widget Sınıfı
    
    Dashboard'da gösterilen duygu geçişleri kontrol arayüzü için 
    backend işlevselliği sağlar.
    """
    
    def __init__(self, emotion_engine=None):
        """
        Widget'ı başlatır
        
        Args:
            emotion_engine: Duygu motoru referansı
        """
        self.emotion_engine = emotion_engine
        self.transitions = []
        self.quick_emotions = [
            {"id": "neutral", "name": "Nötr", "intensity": 1.0},
            {"id": "happy", "name": "Mutlu", "intensity": 0.8},
            {"id": "sad", "name": "Üzgün", "intensity": 0.7},
            {"id": "angry", "name": "Kızgın", "intensity": 0.8},
            {"id": "surprised", "name": "Şaşkın", "intensity": 0.9},
            {"id": "fearful", "name": "Korkmuş", "intensity": 0.7},
            {"id": "disgusted", "name": "İğrenmiş", "intensity": 0.6},
            {"id": "calm", "name": "Sakin", "intensity": 0.9}
        ]
        self.recent_transitions = []
        self._load_transitions()
        logger.info("Hızlı Duygu Geçişleri Widget'ı başlatıldı")
    
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
        return {
            "transitions": self.transitions,
            "quick_emotions": self.quick_emotions,
            "recent_transitions": self.recent_transitions[:5]  # Son 5 transition
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
        
        if action == "play_emotion_transition":
            return self._handle_play_transition(message_data)
        elif action == "update_recent_transitions":
            return self._handle_update_recent(message_data)
        elif action == "save_transition":
            return self._handle_save_transition(message_data)
        elif action == "delete_transition":
            return self._handle_delete_transition(message_data)
        
        return None
    
    def _handle_play_transition(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Duygu geçişi oynatma mesajını işler
        
        Args:
            message_data: Mesaj verisi
            
        Returns:
            İşlem sonucunu içeren yanıt
        """
        transition_id = message_data.get("transition_id")
        
        if not transition_id:
            return {"status": "error", "message": "Geçiş ID'si belirtilmedi"}
        
        # Geçişi bul
        transition = None
        for t in self.transitions:
            if t["id"] == transition_id:
                transition = t
                break
        
        if not transition:
            return {"status": "error", "message": f"Geçiş bulunamadı: {transition_id}"}
        
        if not self.emotion_engine:
            logger.error("Duygu motoru bulunamadığı için duygu geçişi oynatılamıyor")
            return {"status": "error", "message": "Duygu motoru mevcut değil"}
        
        try:
            # Geçişi duygu motoru üzerinden oynat
            self.emotion_engine.play_emotion_sequence(transition["emotions"])
            
            # Son kullanılanlar listesine ekle
            self._add_to_recent_transitions(transition)
            
            return {
                "status": "success", 
                "message": f"Duygu geçişi başlatıldı: {transition['name']}",
                "transition": transition
            }
            
        except Exception as e:
            logger.error(f"Duygu geçişi oynatılırken hata: {str(e)}")
            return {"status": "error", "message": f"Duygu geçişi oynatılamadı: {str(e)}"}
    
    def _handle_update_recent(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Son kullanılanlar listesini güncelleme mesajını işler
        
        Args:
            message_data: Mesaj verisi
            
        Returns:
            İşlem sonucunu içeren yanıt
        """
        transition_ids = message_data.get("transitions", [])
        
        # Yeni son kullanılanlar listesini oluştur
        new_recent = []
        for transition_id in transition_ids:
            for t in self.transitions:
                if t["id"] == transition_id:
                    new_recent.append(t)
                    break
        
        # Son kullanılanları güncelle (en fazla 5 öğe)
        self.recent_transitions = new_recent[:5]
        
        # Kaydet
        self._save_transitions()
        
        return {
            "status": "success",
            "recent_transitions": self.recent_transitions
        }
    
    def _handle_save_transition(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Duygu geçişi kaydetme mesajını işler
        
        Args:
            message_data: Mesaj verisi
            
        Returns:
            İşlem sonucunu içeren yanıt
        """
        transition_id = message_data.get("id")
        name = message_data.get("name")
        description = message_data.get("description", "")
        emotions = message_data.get("emotions", [])
        
        if not name:
            return {"status": "error", "message": "Geçiş ismi belirtilmedi"}
        
        if not emotions or not isinstance(emotions, list):
            return {"status": "error", "message": "Geçerli duygular listesi belirtilmedi"}
        
        # Düzenleme mi yoksa yeni oluşturma mı?
        if transition_id:
            # Mevcut geçişi güncelle
            for i, transition in enumerate(self.transitions):
                if transition["id"] == transition_id:
                    self.transitions[i] = {
                        "id": transition_id,
                        "name": name,
                        "description": description,
                        "emotions": emotions,
                        "updated_at": datetime.now().isoformat()
                    }
                    break
            else:
                return {"status": "error", "message": f"Güncellenecek geçiş bulunamadı: {transition_id}"}
        else:
            # Yeni geçiş oluştur
            new_transition = {
                "id": str(uuid.uuid4()),
                "name": name,
                "description": description,
                "emotions": emotions,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
            self.transitions.append(new_transition)
        
        # Geçişleri kaydet
        self._save_transitions()
        
        return {
            "status": "success",
            "message": "Duygu geçişi kaydedildi",
            "transitions": self.transitions
        }
    
    def _handle_delete_transition(self, message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Duygu geçişi silme mesajını işler
        
        Args:
            message_data: Mesaj verisi
            
        Returns:
            İşlem sonucunu içeren yanıt
        """
        transition_id = message_data.get("id")
        
        if not transition_id:
            return {"status": "error", "message": "Silinecek geçiş ID'si belirtilmedi"}
        
        # Geçişi listeden kaldır
        for i, transition in enumerate(self.transitions):
            if transition["id"] == transition_id:
                del self.transitions[i]
                break
        else:
            return {"status": "error", "message": f"Silinecek geçiş bulunamadı: {transition_id}"}
        
        # Son kullanılanlar listesinden de kaldır
        self.recent_transitions = [t for t in self.recent_transitions if t["id"] != transition_id]
        
        # Geçişleri kaydet
        self._save_transitions()
        
        return {
            "status": "success",
            "message": "Duygu geçişi silindi",
            "transitions": self.transitions
        }
    
    def _add_to_recent_transitions(self, transition: Dict[str, Any]) -> None:
        """
        Son kullanılanlar listesine bir geçiş ekler
        
        Args:
            transition: Eklenecek geçiş verisi
        """
        # Önceden bu geçiş zaten listede var mı kontrol et
        for i, recent in enumerate(self.recent_transitions):
            if recent["id"] == transition["id"]:
                # Varsa, listeden kaldır (sonra başa ekleyeceğiz)
                del self.recent_transitions[i]
                break
        
        # Başa ekle
        self.recent_transitions.insert(0, transition)
        
        # Limit aşılmışsa sondan kırp
        if len(self.recent_transitions) > 5:
            self.recent_transitions = self.recent_transitions[:5]
        
        # Değişiklikleri kaydet
        self._save_transitions()
    
    def _load_transitions(self) -> None:
        """
        Duygu geçişlerini ve son kullanılanları yükler
        """
        try:
            import os
            import json
            
            config_dir = os.path.abspath(os.path.join(
                os.path.dirname(__file__), 
                "../../../config"
            ))
            
            transitions_path = os.path.join(config_dir, "emotion_transitions.json")
            
            if (os.path.exists(transitions_path)):
                with open(transitions_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.transitions = data.get("transitions", [])
                    self.recent_transitions = data.get("recent_transitions", [])
            else:
                # Varsayılan geçişler
                self._create_default_transitions()
                self._save_transitions()
                
        except Exception as e:
            logger.error(f"Duygu geçişleri yüklenirken hata: {str(e)}")
            self._create_default_transitions()
    
    def _save_transitions(self) -> None:
        """
        Duygu geçişlerini ve son kullanılanları kaydeder
        """
        try:
            import os
            import json
            
            config_dir = os.path.abspath(os.path.join(
                os.path.dirname(__file__), 
                "../../../config"
            ))
            
            # Klasörün varlığını kontrol et, yoksa oluştur
            os.makedirs(config_dir, exist_ok=True)
            
            transitions_path = os.path.join(config_dir, "emotion_transitions.json")
            
            data = {
                "transitions": self.transitions,
                "recent_transitions": self.recent_transitions
            }
            
            with open(transitions_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Duygu geçişleri kaydedilirken hata: {str(e)}")
    
    def _create_default_transitions(self) -> None:
        """
        Varsayılan duygu geçişleri oluşturur
        """
        self.transitions = [
            {
                "id": str(uuid.uuid4()),
                "name": "Mutluluk Patlaması",
                "description": "Nötr durumdan mutluluğa hızlı bir geçiş",
                "emotions": [
                    {"id": "neutral", "name": "Nötr", "intensity": 1.0, "duration": 0.5},
                    {"id": "happy", "name": "Mutlu", "intensity": 0.5, "duration": 0.8},
                    {"id": "happy", "name": "Mutlu", "intensity": 1.0, "duration": 1.5}
                ],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Şaşkınlık ve Merak",
                "description": "Şaşkınlıktan meraklı bir ifadeye geçiş",
                "emotions": [
                    {"id": "neutral", "name": "Nötr", "intensity": 1.0, "duration": 0.5},
                    {"id": "surprised", "name": "Şaşkın", "intensity": 0.8, "duration": 1.0},
                    {"id": "neutral", "name": "Nötr", "intensity": 0.6, "duration": 0.8}
                ],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Üzgün ve Kızgın",
                "description": "Üzgünlükten kızgınlığa geçiş",
                "emotions": [
                    {"id": "sad", "name": "Üzgün", "intensity": 0.7, "duration": 1.0},
                    {"id": "angry", "name": "Kızgın", "intensity": 0.5, "duration": 0.5},
                    {"id": "angry", "name": "Kızgın", "intensity": 0.8, "duration": 1.0}
                ],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Sakinleşme",
                "description": "Kızgınlıktan sakinliğe geçiş",
                "emotions": [
                    {"id": "angry", "name": "Kızgın", "intensity": 0.8, "duration": 0.8},
                    {"id": "neutral", "name": "Nötr", "intensity": 0.6, "duration": 1.0},
                    {"id": "calm", "name": "Sakin", "intensity": 0.7, "duration": 1.5}
                ],
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat()
            }
        ]
        
        # İlk kez oluşturulduğunda, ilk geçişi son kullanılanlara ekle
        if self.transitions and not self.recent_transitions:
            self.recent_transitions.append(self.transitions[0])
    
    def render(self, widget_id: str = "emotion_transitions1") -> str:
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
            template_path = os.path.join(template_dir, "emotion_transitions_widget.html")
            
            with open(template_path, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            # Şablonu işle
            template = Template(template_content)
            return template.render(
                widget_id=widget_id,
                widget_type="emotion_transitions",
                widget_title="Hızlı Duygu Geçişleri",
                transitions=self.transitions,
                quick_emotions=self.quick_emotions,
                recent_transitions=self.recent_transitions
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
            "id": "emotion_transitions",
            "name": "Hızlı Duygu Geçişleri",
            "description": "Duygu geçişlerini yönetmek ve oynatmak için kullanılır",
            "type": "emotion_transitions",
            "widget_id": "emotion_transitions",
            "quick_emotions": self.quick_emotions
        }
    
    def get_template_name(self) -> str:
        """
        Şablon dosyasının adını döndürür
        
        Returns:
            Şablon dosyasının adı
        """
        return "widgets/emotion_transitions_widget.html"
    
    def trigger_transition(self, emotion: str, intensity: float = 1.0) -> bool:
        """
        Duygu geçişini tetikler (HTTP API için)
        
        Args:
            emotion: Duygu adı
            intensity: Duygu yoğunluğu
            
        Returns:
            İşlem başarılı ise True, değilse False
        """
        if not self.emotion_engine:
            logger.error("Duygu motoru bulunamadığı için geçiş tetiklenemedi")
            return False
        
        try:
            # Tek adımlık bir duygu geçişi tanımla ve hemen oynat
            transition = {
                "id": str(uuid.uuid4()),
                "name": f"{emotion.capitalize()} Hızlı Geçiş",
                "description": f"{emotion} duygusuna hızlı geçiş",
                "emotions": [
                    {"id": emotion, "name": emotion.capitalize(), "intensity": intensity, "duration": 1.0}
                ]
            }
            
            self.emotion_engine.play_emotion_sequence(transition["emotions"])
            return True
            
        except Exception as e:
            logger.error(f"Duygu geçişi tetiklenirken hata: {str(e)}")
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
        try:
            if "transitions" in data:
                self.transitions = data["transitions"]
                self._save_transitions()
                
            if "recent_transitions" in data:
                self.recent_transitions = data["recent_transitions"]
                self._save_transitions()
                
            return True
        except Exception as e:
            logger.error(f"Widget verileri güncellenirken hata: {str(e)}")
            return False