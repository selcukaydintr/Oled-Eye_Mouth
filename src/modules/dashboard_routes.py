#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: dashboard_routes.py
# Açıklama: Dashboard için API ve web endpoint modülü
# Bağımlılıklar: fastapi
# Bağlı Dosyalar: dashboard_server.py, dashboard_websocket.py

# Versiyon: 0.3.0
# Değişiklikler:
# - [0.3.0] Widget sistemi entegrasyonu eklendi
# - [0.2.0] Yapılandırma editörü endpoint'leri eklendi
# - [0.1.0] dashboard_server.py dosyasından ayrıldı
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-05
===========================================================
"""

import os
import time
import glob
import json
import logging
import copy
from typing import Dict, Optional, Any, List, Callable

from fastapi import FastAPI, Request, WebSocket, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Logger yapılandırması
logger = logging.getLogger("DashboardRoutes")

class RoutesManager:
    """
    Dashboard rotalarını yöneten sınıf
    """
    def __init__(self, face_plugin=None, templates=None, templates_manager=None, websocket_manager=None, widget_manager=None, project_dir=None):
        """
        Routes Manager'ı başlatır
        
        Args:
            face_plugin: FacePlugin nesnesi
            templates: Jinja2Templates nesnesi
            templates_manager: Template Manager nesnesi
            websocket_manager: WebSocket Manager nesnesi
            widget_manager: Widget Manager nesnesi
            project_dir: Proje dizini
        """
        self.face_plugin = face_plugin
        self.templates = templates
        self.templates_manager = templates_manager
        self.websocket_manager = websocket_manager
        self.widget_manager = widget_manager
        self.project_dir = project_dir
        self.config = {}
        
        # Widget yönetimi için değişkenler
        self.widget_configs = {}
        self.available_widgets = []
        self.active_widgets = []

        # Yüz eklentisinin durum dosya yolu
        self.face_plugin_status_file = os.path.join(project_dir, "face_plugin_status.json") if project_dir else None
    
    def set_face_plugin(self, face_plugin) -> None:
        """
        Face Plugin referansını ayarlar
        
        Args:
            face_plugin: FacePlugin nesnesi
        """
        self.face_plugin = face_plugin
    
    def set_config(self, config: Dict) -> None:
        """
        Yapılandırma ayarlarını ayarlar
        
        Args:
            config: Yapılandırma ayarları
        """
        self.config = config
    
    def register_routes(self, app: FastAPI, static_dir: str, templates_dir: str) -> None:
        """
        API rotalarını kaydeder
        
        Args:
            app (FastAPI): FastAPI uygulaması
            static_dir (str): Statik dosya dizini
            templates_dir (str): Şablon dizini
        """
        # Statik dosya sunucusunu ekle
        if os.path.exists(static_dir):
            app.mount("/static", StaticFiles(directory=static_dir), name="static")
            logger.info(f"Statik dosyalar yüklendi: {static_dir}")
        
        # Simülasyon klasörünü statik dosya olarak sun (eğer mevcutsa)
        simulation_dir = os.path.join(self.project_dir, "simulation")
        if os.path.exists(simulation_dir):
            app.mount("/simulation", StaticFiles(directory=simulation_dir), name="simulation")
            logger.info(f"Simülasyon klasörü yüklendi: {simulation_dir}")
            
        # Ana sayfa
        @app.get("/", response_class=HTMLResponse)
        async def root(request: Request):
            if not self.templates:
                # Şablonlar mevcut değilse basit bir mesaj döndür
                return HTMLResponse(content=self.templates_manager.get_default_html())
            
            # Face Plugin referansını kontrol et
            face_plugin_running = False
            
            # Önce doğrudan referans ile kontrol et
            if self.face_plugin and hasattr(self.face_plugin, 'is_running') and self.face_plugin.is_running:
                face_plugin_running = True
            else:
                # Durum dosyasından kontrol et
                if self.face_plugin_status_file and os.path.exists(self.face_plugin_status_file):
                    try:
                        with open(self.face_plugin_status_file, 'r') as f:
                            status_data = json.load(f)
                            if status_data.get('status') == 'running':
                                face_plugin_running = True
                                logger.info("Face plugin durumu dosyadan okundu: çalışıyor")
                    except Exception as e:
                        logger.warning(f"Face plugin durum dosyası okunamadı: {e}")
            
            if not face_plugin_running:
                return self.templates.TemplateResponse(
                    "error.html",
                    {"request": request, "message": "Yüz eklentisi başlatılmamış"}
                )
            
            # Tema listesini al
            themes = []
            if self.face_plugin and hasattr(self.face_plugin, 'theme_manager') and self.face_plugin.theme_manager:
                themes = self.face_plugin.theme_manager.get_theme_list()
            
            # Mevcut duygular
            current_emotion = {}
            if self.face_plugin and hasattr(self.face_plugin, 'emotion_engine') and self.face_plugin.emotion_engine:
                current_emotion = self.face_plugin.emotion_engine.get_current_emotion()
            
            # Mevcut widget'ları al
            available_widgets = []
            if self.widget_manager:
                available_widgets = self.widget_manager.get_all_widgets()
            
            return self.templates.TemplateResponse(
                "dashboard.html",
                {
                    "request": request,
                    "themes": themes,
                    "current_theme": self.face_plugin.theme_manager.get_current_theme() if (self.face_plugin and hasattr(self.face_plugin, 'theme_manager') and self.face_plugin.theme_manager) else "default",
                    "current_emotion": current_emotion,
                    "available_widgets": available_widgets
                }
            )
        
        # WebSocket endpoint
        @app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await self.websocket_manager.handle_websocket(websocket)
        
        # API endpoint'leri
        @app.get("/api/status")
        async def get_status():
            if not self.face_plugin or not self.face_plugin.is_running:
                raise HTTPException(status_code=503, detail="Yüz eklentisi çalışmıyor")
            
            from dashboard_stats import get_system_stats
            system_stats = get_system_stats()
            
            # Mevcut durum
            current_theme = "unknown"
            current_emotion = {}
            
            if self.face_plugin.theme_manager:
                current_theme = self.face_plugin.theme_manager.get_current_theme()
            
            if self.face_plugin.emotion_engine:
                current_emotion = self.face_plugin.emotion_engine.get_current_emotion()
            
            return {
                "status": "running" if self.face_plugin.is_running else "stopped",
                "uptime": self.face_plugin.uptime if hasattr(self.face_plugin, "uptime") else 0,
                "theme": current_theme,
                "emotion": current_emotion,
                "system": system_stats
            }
        
        @app.get("/api/themes")
        async def get_themes():
            if not self.face_plugin or not self.face_plugin.theme_manager:
                raise HTTPException(status_code=503, detail="Tema yöneticisi çalışmıyor")
            
            themes = self.face_plugin.theme_manager.get_theme_list()
            current_theme = self.face_plugin.theme_manager.get_current_theme()
            
            return {
                "themes": themes,
                "current": current_theme
            }
        
        @app.post("/api/themes/{theme_name}")
        async def set_theme(theme_name: str):
            if not self.face_plugin:
                raise HTTPException(status_code=503, detail="Yüz eklentisi çalışmıyor")
            
            success = self.face_plugin.set_theme(theme_name)
            
            if not success:
                raise HTTPException(status_code=400, detail=f"Tema ayarlanamadı: {theme_name}")
            
            return {"success": True, "theme": theme_name}
        
        @app.post("/api/emotions/{emotion}")
        async def set_emotion(emotion: str, intensity: float = 1.0):
            if not self.face_plugin:
                raise HTTPException(status_code=503, detail="Yüz eklentisi çalışmıyor")
            
            # Yoğunluk değerini sınırla
            intensity = max(0.0, min(1.0, intensity))
            
            success = self.face_plugin.set_emotion(emotion, intensity)
            
            if not success:
                raise HTTPException(status_code=400, detail=f"Duygu ayarlanamadı: {emotion}")
            
            return {"success": True, "emotion": emotion, "intensity": intensity}
        
        @app.get("/api/simulation")
        async def get_simulation_images():
            """
            Simülasyon klasöründeki son görüntüleri döndürür
            """
            simulation_dir = os.path.join(self.project_dir, "simulation")
            if not os.path.exists(simulation_dir):
                raise HTTPException(status_code=404, detail="Simülasyon klasörü bulunamadı")
            
            # Son oluşturulan görüntüleri bul
            images = {
                "left_eye": None,
                "right_eye": None,
                "mouth": None,
                "leds": None
            }
            
            try:
                # Sol göz görüntüleri
                left_eye_images = sorted(glob.glob(os.path.join(simulation_dir, "display_left_eye_*.png")))
                if left_eye_images:
                    images["left_eye"] = os.path.basename(left_eye_images[-1])
                
                # Sağ göz görüntüleri
                right_eye_images = sorted(glob.glob(os.path.join(simulation_dir, "display_right_eye_*.png")))
                if right_eye_images:
                    images["right_eye"] = os.path.basename(right_eye_images[-1])
                
                # Ağız görüntüleri
                mouth_images = sorted(glob.glob(os.path.join(simulation_dir, "display_mouth_*.png")))
                if mouth_images:
                    images["mouth"] = os.path.basename(mouth_images[-1])
                
                # LED görüntüleri
                led_images = sorted(glob.glob(os.path.join(simulation_dir, "leds_*.png")))
                if led_images:
                    images["leds"] = os.path.basename(led_images[-1])
                
                return {
                    "timestamp": time.time(),
                    "images": images
                }
            except Exception as e:
                logger.error(f"Simülasyon görüntüleri alınırken hata: {e}")
                raise HTTPException(status_code=500, detail=f"Simülasyon görüntüleri alınamadı: {e}")
        
        # WebSocket endpoint'i yoluyla düzenli simülasyon güncellemeleri göndermek için yeni bir fonksiyon
        @app.websocket("/ws/simulation")
        async def simulation_updates(websocket: WebSocket):
            await self.websocket_manager.handle_simulation_websocket(websocket)
        
        # Tema detayları ve düzenleme endpoint'i
        @app.get("/api/themes/{theme_name}/details")
        async def get_theme_details(theme_name: str):
            """Tema detaylarını döndürür"""
            if not self.face_plugin or not self.face_plugin.theme_manager:
                raise HTTPException(status_code=503, detail="Tema yöneticisi çalışmıyor")
            
            theme_details = self.face_plugin.theme_manager.get_theme_details(theme_name)
            
            if not theme_details:
                raise HTTPException(status_code=404, detail=f"Tema bulunamadı: {theme_name}")
            
            return theme_details
            
        @app.post("/api/themes/{theme_name}/edit")
        async def edit_theme(theme_name: str, theme_data: Dict):
            """Temayı düzenler"""
            if not self.face_plugin or not self.face_plugin.theme_manager:
                raise HTTPException(status_code=503, detail="Tema yöneticisi çalışmıyor")
                
            # Varsayılan temaların düzenlenmesini engelle (güvenlik)
            if theme_name in ["default", "minimal"] and not self.config.get("allow_default_theme_edit", False):
                raise HTTPException(status_code=403, detail="Varsayılan temalar düzenlenemez")
                
            success = self.face_plugin.theme_manager.edit_theme(theme_name, theme_data)
            
            if not success:
                raise HTTPException(status_code=400, detail=f"Tema düzenlenemedi: {theme_name}")
                
            return {"success": True, "theme": theme_name}
        
        @app.post("/api/themes/create")
        async def create_theme(theme_name: str, theme_data: Dict):
            """Yeni tema oluşturur"""
            if not self.face_plugin or not self.face_plugin.theme_manager:
                raise HTTPException(status_code=503, detail="Tema yöneticisi çalışmıyor")
                
            success = self.face_plugin.theme_manager.create_theme(theme_name, theme_data)
            
            if not success:
                raise HTTPException(status_code=400, detail=f"Tema oluşturulamadı: {theme_name}")
                
            return {"success": True, "theme": theme_name}
            
        @app.post("/api/themes/{source_theme}/copy/{target_theme}")
        async def copy_theme(source_theme: str, target_theme: str):
            """Temayı kopyalar"""
            if not self.face_plugin or not self.face_plugin.theme_manager:
                raise HTTPException(status_code=503, detail="Tema yöneticisi çalışmıyor")
                
            success = self.face_plugin.theme_manager.copy_theme(source_theme, target_theme)
            
            if not success:
                raise HTTPException(status_code=400, detail=f"Tema kopyalanamadı: {source_theme} -> {target_theme}")
                
            return {"success": True, "source": source_theme, "target": target_theme}
            
        # Animasyon listesi ve kontrol endpoint'leri
        @app.get("/api/animations")
        async def get_animations():
            """Kullanılabilir animasyonları listeler"""
            if not self.face_plugin or not hasattr(self.face_plugin, "animation_engine") or self.face_plugin.animation_engine is None:
                raise HTTPException(status_code=503, detail="Animasyon motoru çalışmıyor")
                
            animations = []
            for anim_name in self.face_plugin.animation_engine.get_animation_names():
                anim_info = self.face_plugin.animation_engine.get_animation_info(anim_name)
                if anim_info:
                    animations.append({
                        "name": anim_name,
                        "display_name": anim_info.get("name", anim_name),
                        "description": anim_info.get("description", ""),
                        "duration": anim_info.get("duration", 0)
                    })
            
            return {"animations": animations}
            
        @app.post("/api/animations/{name}/play")
        async def play_animation(name: str):
            """Animasyon oynatır"""
            if not self.face_plugin or not hasattr(self.face_plugin, "animation_engine") or self.face_plugin.animation_engine is None:
                raise HTTPException(status_code=503, detail="Animasyon motoru çalışmıyor")
                
            success = self.face_plugin.animation_engine.play_animation(name)
            
            if not success:
                raise HTTPException(status_code=400, detail=f"Animasyon oynatılamadı: {name}")
                
            return {"success": True, "animation": name}
            
        @app.post("/api/animations/stop")
        async def stop_animation():
            """Çalışan animasyonu durdurur"""
            if not self.face_plugin or not hasattr(self.face_plugin, "animation_engine") or self.face_plugin.animation_engine is None:
                raise HTTPException(status_code=503, detail="Animasyon motoru çalışmıyor")
                
            self.face_plugin.animation_engine.stop_current_animation()
            return {"success": True}
        
        @app.get("/api/animations/{name}/details")
        async def get_animation_details(name: str):
            """Animasyon detaylarını döndürür"""
            if not self.face_plugin or not hasattr(self.face_plugin, "animation_engine") or self.face_plugin.animation_engine is None:
                raise HTTPException(status_code=503, detail="Animasyon motoru çalışmıyor")
                
            animation_details = self.face_plugin.animation_engine.get_animation_details(name)
            
            if not animation_details:
                raise HTTPException(status_code=404, detail=f"Animasyon bulunamadı: {name}")
                
            return animation_details
            
        @app.post("/api/animations/{name}/save")
        async def save_animation(name: str, animation_data: Dict):
            """Animasyonu kaydeder"""
            if not self.face_plugin or not hasattr(self.face_plugin, "animation_engine") or self.face_plugin.animation_engine is None:
                raise HTTPException(status_code=503, detail="Animasyon motoru çalışmıyor")
                
            success = self.face_plugin.animation_engine.save_animation(name, animation_data)
            
            if not success:
                raise HTTPException(status_code=400, detail=f"Animasyon kaydedilemedi: {name}")
                
            return {"success": True, "animation": name}
            
        @app.delete("/api/animations/{name}/delete")
        async def delete_animation(name: str):
            """Animasyonu siler"""
            if not self.face_plugin or not hasattr(self.face_plugin, "animation_engine") or self.face_plugin.animation_engine is None:
                raise HTTPException(status_code=503, detail="Animasyon motoru çalışmıyor")
                
            success = self.face_plugin.animation_engine.delete_animation(name)
            
            if not success:
                raise HTTPException(status_code=400, detail=f"Animasyon silinemedi: {name}")
                
            return {"success": True, "animation": name}
            
        @app.get("/api/animations/status")
        async def get_animation_status():
            """Mevcut animasyon durumunu döndürür"""
            if not self.face_plugin or not hasattr(self.face_plugin, "animation_engine") or self.face_plugin.animation_engine is None:
                raise HTTPException(status_code=503, detail="Animasyon motoru çalışmıyor")
                
            return self.face_plugin.animation_engine.get_animation_status()
        
        # Tema editörü sayfa endpoint'i
        @app.get("/theme-editor/{theme_name}", response_class=HTMLResponse)
        async def theme_editor(request: Request, theme_name: str):
            """Tema editörü sayfası"""
            if not self.templates:
                return HTMLResponse(content="<h1>Tema Editörü</h1><p>Şablonlar yüklenemedi</p>")
                
            if not self.face_plugin or not self.face_plugin.theme_manager:
                return self.templates.TemplateResponse(
                    "error.html",
                    {"request": request, "message": "Tema yöneticisi çalışmıyor"}
                )
                
            # Tema detaylarını kontrol et
            theme_details = self.face_plugin.theme_manager.get_theme_details(theme_name)
            
            if not theme_details:
                return self.templates.TemplateResponse(
                    "error.html",
                    {"request": request, "message": f"Tema bulunamadı: {theme_name}"}
                )
                
            # Tüm duygu isimlerini al
            emotions = ["happy", "sad", "angry", "surprised", "fearful", "disgusted", "calm", "neutral"]
                
            return self.templates.TemplateResponse(
                "theme_editor.html",
                {
                    "request": request,
                    "theme_name": theme_name,
                    "theme_details": theme_details,
                    "emotions": emotions
                }
            )

        # Animasyon editörü sayfa endpoint'i
        @app.get("/animation-editor", response_class=HTMLResponse)
        async def animation_editor(request: Request):
            """Animasyon editörü sayfası"""
            if not self.templates:
                return HTMLResponse(content="<h1>Animasyon Editörü</h1><p>Şablonlar yüklenemedi</p>")
                
            if not self.face_plugin or not hasattr(self.face_plugin, "animation_engine"):
                return self.templates.TemplateResponse(
                    "error.html",
                    {"request": request, "message": "Animasyon motoru çalışmıyor"}
                )
                
            return self.templates.TemplateResponse(
                "animation_editor.html",
                {"request": request}
            )

        # Yapılandırma editörü endpoint'leri
        @app.get("/config-editor", response_class=HTMLResponse)
        async def config_editor(request: Request):
            """Yapılandırma editörü sayfası"""
            if not self.templates:
                return HTMLResponse(content="<h1>Yapılandırma Editörü</h1><p>Şablonlar yüklenemedi</p>")
                
            if not self.face_plugin:
                return self.templates.TemplateResponse(
                    "error.html",
                    {"request": request, "message": "Yüz eklentisi çalışmıyor"}
                )
                
            return self.templates.TemplateResponse(
                "configuration_editor.html",
                {
                    "request": request,
                }
            )
            
        @app.get("/api/config")
        async def get_config():
            """Mevcut yapılandırmayı döndürür"""
            if not self.face_plugin:
                raise HTTPException(status_code=503, detail="Yüz eklentisi çalışmıyor")
                
            # Hassas bilgileri filtrele
            config_copy = copy.deepcopy(self.face_plugin.config)
            
            # Şifre gibi hassas bilgileri kaldır
            if "dashboard" in config_copy and "security" in config_copy["dashboard"]:
                if "password" in config_copy["dashboard"]["security"]:
                    config_copy["dashboard"]["security"]["password"] = "" if config_copy["dashboard"]["security"]["password"] else ""
            
            return config_copy
            
        @app.post("/api/config/update")
        async def update_config(config_data: Dict):
            """Yapılandırmayı günceller"""
            if not self.face_plugin:
                raise HTTPException(status_code=503, detail="Yüz eklentisi çalışmıyor")
                
            try:
                # Yapılandırmayı derin birleştirme ile güncelle
                merged_config = self._deep_merge_dict(self.face_plugin.config, config_data)
                
                # Yeni yapılandırmayı kaydet ve uygula
                success = self.face_plugin.update_config(merged_config)
                
                if not success:
                    raise HTTPException(status_code=500, detail="Yapılandırma güncellenemedi")
                    
                return {"success": True, "message": "Yapılandırma güncellendi"}
            
            except Exception as e:
                logger.error(f"Yapılandırma güncellenirken hata: {e}")
                raise HTTPException(status_code=500, detail=f"Yapılandırma güncelleme hatası: {str(e)}")
                
        @app.post("/api/config/reset")
        async def reset_config():
            """Yapılandırmayı varsayılan değerlere sıfırlar"""
            if not self.face_plugin:
                raise HTTPException(status_code=503, detail="Yüz eklentisi çalışmıyor")
                
            try:
                # Varsayılan yapılandırmayı yükle
                default_config = self.face_plugin._create_default_config()
                
                # Varsayılan yapılandırmayı uygula
                success = self.face_plugin.update_config(default_config)
                
                if not success:
                    raise HTTPException(status_code=500, detail="Yapılandırma sıfırlanamadı")
                    
                return default_config
                
            except Exception as e:
                logger.error(f"Yapılandırma sıfırlanırken hata: {e}")
                raise HTTPException(status_code=500, detail=f"Yapılandırma sıfırlama hatası: {str(e)}")

        # IFrame entegrasyon test sayfası endpoint'i
        @app.get("/iframe-integration", response_class=HTMLResponse)
        async def iframe_integration(request: Request):
            """IFrame entegrasyonu test sayfası"""
            if not self.templates:
                return HTMLResponse(content="<h1>IFrame Entegrasyonu</h1><p>Şablonlar yüklenemedi</p>")
            
            return self.templates.TemplateResponse(
                "iframe_integration.html",
                {"request": request}
            )
            
        # IFrame entegrasyonu için üst proje embed endpoint'i
        @app.get("/embed", response_class=HTMLResponse)
        async def embed_page(request: Request):
            """Dış projelerde embed edilebilecek basit sayfa"""
            if not self.templates:
                return HTMLResponse(content="<h1>FACE1 Embed</h1><p>Şablonlar yüklenemedi</p>")
            
            if not self.face_plugin:
                return self.templates.TemplateResponse(
                    "error.html",
                    {"request": request, "message": "Yüz eklentisi çalışmıyor"}
                )
            
            # Gömülü iframe için özel sayfa
            return self.templates.TemplateResponse(
                "dashboard.html",
                {
                    "request": request, 
                    "embed_mode": True,
                    "themes": self.face_plugin.theme_manager.get_theme_list() if self.face_plugin.theme_manager else [],
                    "current_theme": self.face_plugin.theme_manager.get_current_theme() if self.face_plugin.theme_manager else "default",
                }
            )

        # Üst proje entegrasyon örnek sayfası endpoint'i
        @app.get("/parent-integration-example", response_class=HTMLResponse)
        async def parent_integration_example(request: Request):
            """Üst proje entegrasyon örnek sayfası"""
            if not self.templates:
                return HTMLResponse(content="<h1>Üst Proje Entegrasyonu</h1><p>Şablonlar yüklenemedi</p>")
            
            return self.templates.TemplateResponse(
                "parent_integration_example.html",
                {"request": request}
            )

        # Widget endpoint'leri
        self._register_widget_endpoints(app)

    def _register_widget_endpoints(self, app: FastAPI):
        """
        Widget endpoint'lerini kaydeder
        
        Args:
            app (FastAPI): FastAPI uygulaması
        """
        if not self.widget_manager:
            logger.warning("Widget yöneticisi bulunamadığından widget endpoint'leri kaydedilemiyor")
            return
        
        @app.get("/api/widgets", tags=["widgets"])
        async def get_available_widgets():
            """Kullanılabilir widget'ları listeler"""
            if not self.widget_manager:
                raise HTTPException(status_code=503, detail="Widget yöneticisi çalışmıyor")
            
            return {"widgets": self.widget_manager.get_all_widgets()}
        
        @app.get("/api/widgets/{widget_id}", tags=["widgets"])
        async def get_widget_details(widget_id: str):
            """Widget detaylarını döndürür"""
            if not self.widget_manager:
                raise HTTPException(status_code=503, detail="Widget yöneticisi çalışmıyor")
            
            widget = self.widget_manager.get_widget(widget_id)
            if not widget:
                raise HTTPException(status_code=404, detail=f"Widget bulunamadı: {widget_id}")
            
            return widget.get_details()
        
        @app.get("/api/widgets/{widget_id}/render", response_class=HTMLResponse, tags=["widgets"])
        async def render_widget(request: Request, widget_id: str):
            """Widget HTML görünümünü döndürür"""
            if not self.widget_manager:
                raise HTTPException(status_code=503, detail="Widget yöneticisi çalışmıyor")
            
            try:
                # Widget Manager'dan doğrudan render fonksiyonunu çağır
                html_content = self.widget_manager.render_widget(widget_id)
                if not html_content:
                    raise HTTPException(status_code=404, detail=f"Widget render edilemedi: {widget_id}")
                
                # HTML içeriğini döndür
                return HTMLResponse(content=html_content)
                
            except Exception as e:
                logger.error(f"Widget render hatası: {e}", exc_info=True)
                raise HTTPException(status_code=500, detail=f"Widget render hatası: {str(e)}")
        
        # Widget veri endpoint'leri
        @app.get("/api/widgets/{widget_id}/data", tags=["widgets"])
        async def get_widget_data(widget_id: str):
            """Widget verilerini döndürür"""
            if not self.widget_manager:
                raise HTTPException(status_code=503, detail="Widget yöneticisi çalışmıyor")
            
            widget = self.widget_manager.get_widget(widget_id)
            if not widget:
                raise HTTPException(status_code=404, detail=f"Widget bulunamadı: {widget_id}")
            
            return widget.get_data()
        
        @app.post("/api/widgets/{widget_id}/data", tags=["widgets"])
        async def update_widget_data(widget_id: str, data: Dict):
            """Widget verilerini günceller"""
            if not self.widget_manager:
                raise HTTPException(status_code=503, detail="Widget yöneticisi çalışmıyor")
            
            widget = self.widget_manager.get_widget(widget_id)
            if not widget:
                raise HTTPException(status_code=404, detail=f"Widget bulunamadı: {widget_id}")
            
            success = widget.update_data(data)
            if not success:
                raise HTTPException(status_code=400, detail=f"Widget verisi güncellenemedi: {widget_id}")
            
            return {"success": True, "widget_id": widget_id}
        
        # Widget yapılandırma endpoint'leri
        @app.get("/api/widgets/{widget_id}/config", tags=["widgets"])
        async def get_widget_config(widget_id: str):
            """Widget yapılandırmasını döndürür"""
            if not self.widget_manager:
                raise HTTPException(status_code=503, detail="Widget yöneticisi çalışmıyor")
            
            widget = self.widget_manager.get_widget(widget_id)
            if not widget:
                raise HTTPException(status_code=404, detail=f"Widget bulunamadı: {widget_id}")
            
            return widget.get_config()
        
        @app.post("/api/widgets/{widget_id}/config", tags=["widgets"])
        async def update_widget_config(widget_id: str, config: Dict):
            """Widget yapılandırmasını günceller"""
            if not self.widget_manager:
                raise HTTPException(status_code=503, detail="Widget yöneticisi çalışmıyor")
            
            widget = self.widget_manager.get_widget(widget_id)
            if not widget:
                raise HTTPException(status_code=404, detail=f"Widget bulunamadı: {widget_id}")
            
            success = widget.update_config(config)
            if not success:
                raise HTTPException(status_code=400, detail=f"Widget yapılandırması güncellenemedi: {widget_id}")
            
            return {"success": True, "widget_id": widget_id}
        
        # Widget aksiyon endpoint'leri - belirli bir durum için eylem çağırır
        @app.post("/api/widgets/{widget_id}/action/{action_name}", tags=["widgets"])
        async def execute_widget_action(widget_id: str, action_name: str, params: Dict = None):
            """Widget aksiyonunu çalıştırır"""
            if not self.widget_manager:
                raise HTTPException(status_code=503, detail="Widget yöneticisi çalışmıyor")
            
            widget = self.widget_manager.get_widget(widget_id)
            if not widget:
                raise HTTPException(status_code=404, detail=f"Widget bulunamadı: {widget_id}")
            
            try:
                result = widget.execute_action(action_name, params or {})
                return {"success": True, "widget_id": widget_id, "action": action_name, "result": result}
            except Exception as e:
                logger.error(f"Widget aksiyonu çalıştırılamadı: {e}")
                raise HTTPException(status_code=400, detail=f"Widget aksiyonu çalıştırılamadı: {str(e)}")
        
        # Özel widget endpoint'leri
        
        # Yüz ifadesi widget'ı için özel endpoint'ler
        @app.post("/api/widgets/expression_control/set_expression", tags=["widgets", "expression"])
        async def set_expression(expression_data: Dict):
            """Yüz ifadesini ayarlar"""
            if not self.widget_manager:
                raise HTTPException(status_code=503, detail="Widget yöneticisi çalışmıyor")
            
            widget = self.widget_manager.get_widget("expression_control")
            if not widget:
                raise HTTPException(status_code=404, detail="Yüz ifadesi kontrol widget'ı bulunamadı")
            
            success = widget.set_expression(expression_data)
            if not success:
                raise HTTPException(status_code=400, detail="Yüz ifadesi ayarlanamadı")
            
            return {"success": True}
        
        # Durum izleme widget'ı için özel endpoint'ler
        @app.get("/api/widgets/state_history/history", tags=["widgets", "state"])
        async def get_state_history(limit: int = 10):
            """Durum geçmişini döndürür"""
            if not self.widget_manager:
                raise HTTPException(status_code=503, detail="Widget yöneticisi çalışmıyor")
            
            widget = self.widget_manager.get_widget("state_history")
            if not widget:
                raise HTTPException(status_code=404, detail="Durum izleme widget'ı bulunamadı")
            
            return {"history": widget.get_history(limit)}
        
        # Duygu geçişleri widget'ı için özel endpoint'ler
        @app.post("/api/widgets/emotion_transitions/trigger/{emotion}", tags=["widgets", "emotion"])
        async def trigger_emotion_transition(emotion: str, intensity: float = 1.0):
            """Duygu geçişini tetikler"""
            if not self.widget_manager:
                raise HTTPException(status_code=503, detail="Widget yöneticisi çalışmıyor")
            
            widget = self.widget_manager.get_widget("emotion_transitions")
            if not widget:
                raise HTTPException(status_code=404, detail="Duygu geçişleri widget'ı bulunamadı")
            
            success = widget.trigger_transition(emotion, intensity)
            if not success:
                raise HTTPException(status_code=400, detail=f"Duygu geçişi tetiklenemedi: {emotion}")
            
            return {"success": True, "emotion": emotion, "intensity": intensity}

    def _deep_merge_dict(self, base_dict: Dict, update_dict: Dict) -> Dict:
        """
        İki sözlüğü derin birleştirir, iç içe yapıları korur
        
        Args:
            base_dict (Dict): Temel sözlük
            update_dict (Dict): Güncelleme sözlüğü
        
        Returns:
            Dict: Birleştirilmiş sözlük
        """
        result = copy.deepcopy(base_dict)
        
        for key, value in update_dict.items():
            # Eğer iki sözlükte de aynı anahtar var ve her ikisi de sözlük ise
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                # İç içe sözlükleri derin birleştir
                result[key] = self._deep_merge_dict(result[key], value)
            else:
                # Aksi takdirde direkt değeri güncelle
                result[key] = value
                
        return result