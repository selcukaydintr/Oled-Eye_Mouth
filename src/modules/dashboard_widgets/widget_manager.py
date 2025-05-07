#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: widget_manager.py
# Açıklama: Dashboard widget'larını yöneten sınıf
# Bağımlılıklar: fastapi, jinja2
# Bağlı Dosyalar: dashboard_routes.py, dashboard_server.py

# Versiyon: 0.1.0
# Değişiklikler:
# - [0.1.0] İlk sürüm oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-05
===========================================================
"""

import logging
import os
import importlib
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class WidgetManager:
    """
    Dashboard widget'larını yöneten sınıf
    """
    
    def __init__(self, face_plugin=None):
        """
        Widget Manager'ı başlatır
        
        Args:
            face_plugin: FacePlugin nesnesi
        """
        self.face_plugin = face_plugin
        self.widgets = {}
        self.widget_modules = {}
        self.widget_instances = {}
        self.widget_order = []
        self.widget_path = os.path.dirname(os.path.abspath(__file__))
        logger.info("Widget Manager başlatıldı")
    
    def set_face_plugin(self, face_plugin) -> None:
        """
        Face Plugin referansını ayarlar ve tüm widget'lara iletir
        
        Args:
            face_plugin: FacePlugin nesnesi
        """
        self.face_plugin = face_plugin
        
        # Yüz eklentisi referansını tüm widget'lara ilet
        for widget_id, widget in self.widget_instances.items():
            if hasattr(widget, 'set_emotion_engine') and self.face_plugin and hasattr(self.face_plugin, 'emotion_engine'):
                widget.set_emotion_engine(self.face_plugin.emotion_engine)
    
    def load_widgets(self) -> None:
        """
        Tüm widget modüllerini dinamik olarak yükler
        """
        logger.info("Widget'lar yükleniyor...")
        
        # Dashboard widget klasörünü tara
        widget_modules = {}
        
        # Widget yükleme sırası - önemli olanlar önce
        widget_load_order = [
            "expression_widget",
            "state_history_widget",
            "emotion_transitions_widget"
        ]
        
        # Zorunlu widget'lar
        required_widgets = {
            "expression_widget": "Yüz İfadesi Kontrolü",
            "state_history_widget": "Durum İzleme ve Tarihçe",
            "emotion_transitions_widget": "Hızlı Duygu Geçişleri"
        }
        
        # Önce belirtilen sırada yükle
        for module_name in widget_load_order:
            try:
                # Import the module (doğru importlama yolu kullan)
                # Modül yolu hiyerarşik yapıya uygun olmalı (projenin yapısına göre değişebilir)
                try:
                    # Önce mutlak yol ile deniyoruz
                    module = importlib.import_module(f"modules.dashboard_widgets.{module_name}")
                except ModuleNotFoundError:
                    try:
                        # Modülün doğrudan adıyla deniyoruz 
                        module = importlib.import_module(module_name)
                    except ModuleNotFoundError:
                        # Son olarak tam yolu deniyoruz
                        module = importlib.import_module(f"src.modules.dashboard_widgets.{module_name}")
                        
                logger.info(f"Widget modülü yüklendi: {module_name}")
                
                # Her widget modülünde ana sınıf ismi genellikle dosya ismiyle aynıdır
                # Örneğin, "expression_widget" modülünden "ExpressionWidget" sınıfını alıyoruz
                class_name = ''.join(word.capitalize() for word in module_name.split('_'))
                
                # Sınıfı modülden al
                if hasattr(module, class_name):
                    widget_class = getattr(module, class_name)
                    widget_instance = widget_class(
                        emotion_engine=self.face_plugin.emotion_engine if self.face_plugin else None
                    )
                    widget_id = module_name.replace('_widget', '')
                    
                    self.widget_modules[widget_id] = module
                    self.widget_instances[widget_id] = widget_instance
                    self.widget_order.append(widget_id)
                    
                    logger.info(f"Widget {class_name} başlatıldı (ID: {widget_id})")
                else:
                    logger.error(f"Widget modülünde {class_name} sınıfı bulunamadı: {module_name}")
                
            except Exception as e:
                logger.error(f"Widget modülü yüklenirken hata: {module_name}, {str(e)}")
                logger.error(f"Hata detayları: ", exc_info=True)
                
                # Eğer zorunlu bir widget yüklenemezse, bir varsayılan widget oluştur
                if module_name in required_widgets:
                    logger.warning(f"Zorunlu widget yüklenemedi: {module_name}. Varsayılan yüklenecek.")
                    widget_id = module_name.replace('_widget', '')
                    self.widget_order.append(widget_id)
        
        logger.info(f"Toplam {len(self.widget_instances)} widget yüklendi")
    
    def get_widget(self, widget_id: str) -> Optional[Any]:
        """
        Belirtilen widget örneğini döndürür
        
        Args:
            widget_id (str): Widget ID'si
            
        Returns:
            Optional[Any]: Widget örneği veya None
        """
        # Tire işareti içeriyorsa alt çizgi formatına dönüştür (kabap-case -> snake_case)
        if "-" in widget_id:
            widget_id = widget_id.replace("-", "_")
        
        if widget_id not in self.widget_instances:
            logger.error(f"Widget bulunamadı: {widget_id}")
            return None
            
        return self.widget_instances[widget_id]
    
    def render_widget(self, widget_id: str, instance_id: str = None) -> str:
        """
        Belirtilen widget'ın HTML içeriğini oluşturur
        
        Args:
            widget_id (str): Widget ID'si (ör. expression, state_history)
            instance_id (str, optional): Widget örnek ID'si (Aynı widget'ın birden fazla örneği için)
            
        Returns:
            str: Widget'ın HTML içeriği
        """
        if not instance_id:
            instance_id = f"{widget_id}1"  # Varsayılan ID oluştur
        
        if widget_id not in self.widget_instances:
            logger.error(f"Widget bulunamadı: {widget_id}")
            return f"<div class='widget-error'>Widget '{widget_id}' bulunamadı</div>"
        
        try:
            # Widget'ın render metodunu çağır
            widget = self.widget_instances[widget_id]
            if hasattr(widget, 'render'):
                return widget.render(instance_id)
            else:
                logger.error(f"Widget'da render metodu bulunamadı: {widget_id}")
                return f"<div class='widget-error'>Widget '{widget_id}' render edilemiyor</div>"
        
        except Exception as e:
            logger.error(f"Widget render edilirken hata: {widget_id}, {str(e)}")
            return f"<div class='widget-error'>Widget render hatası: {str(e)}</div>"
    
    def get_all_widgets(self) -> List[Dict[str, Any]]:
        """
        Tüm yüklü widget'ların listesini döndürür
        
        Returns:
            List[Dict[str, Any]]: Widget listesi
        """
        widgets = []
        
        for widget_id in self.widget_order:
            widget = self.widget_instances.get(widget_id)
            if widget:
                widget_info = {
                    "id": widget_id,
                    "name": getattr(widget, "name", widget_id.replace("_", " ").title()),
                    "description": getattr(widget, "description", ""),
                    "type": getattr(widget, "widget_type", widget_id)
                }
                widgets.append(widget_info)
        
        return widgets
    
    def get_widget_data(self, widget_id: str) -> Optional[Dict[str, Any]]:
        """
        Belirtilen widget'ın veri güncellemesi için gerekli verileri döndürür
        
        Args:
            widget_id (str): Widget ID'si
            
        Returns:
            Optional[Dict[str, Any]]: Widget verileri
        """
        if widget_id not in self.widget_instances:
            logger.error(f"Widget verileri alınırken widget bulunamadı: {widget_id}")
            return None
        
        try:
            widget = self.widget_instances[widget_id]
            if hasattr(widget, 'get_widget_data'):
                return widget.get_widget_data()
            else:
                logger.warning(f"Widget'da get_widget_data metodu bulunamadı: {widget_id}")
                return {}
        
        except Exception as e:
            logger.error(f"Widget verileri alınırken hata: {widget_id}, {str(e)}")
            return None
    
    def handle_websocket_message(self, message_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        WebSocket mesajını ilgili widget'a yönlendirir
        
        Args:
            message_data (Dict[str, Any]): WebSocket mesaj verileri
            
        Returns:
            Optional[Dict[str, Any]]: İşlenmiş yanıt
        """
        widget_id = message_data.get("widget")
        
        if not widget_id:
            logger.error("WebSocket mesajında widget ID'si bulunamadı")
            return {"error": "Widget ID is missing", "status": "error"}
        
        if widget_id not in self.widget_instances:
            logger.error(f"WebSocket mesajı için widget bulunamadı: {widget_id}")
            return {"error": f"Widget {widget_id} not found", "status": "error"}
        
        try:
            widget = self.widget_instances[widget_id]
            if hasattr(widget, 'handle_websocket_message'):
                return widget.handle_websocket_message(message_data)
            else:
                logger.warning(f"Widget'da handle_websocket_message metodu bulunamadı: {widget_id}")
                return {"status": "error", "message": f"Widget {widget_id} cannot handle WebSocket messages"}
        
        except Exception as e:
            logger.error(f"Widget WebSocket mesajı işlenirken hata: {widget_id}, {str(e)}")
            return {"error": str(e), "status": "error"}