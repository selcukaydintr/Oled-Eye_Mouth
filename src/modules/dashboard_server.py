#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: dashboard_server.py
# Açıklama: Web tabanlı kontrol paneli sunucu modülü ve IFrame entegrasyonu
# Bağımlılıklar: fastapi, uvicorn, jinja2, aiofiles, psutil, websockets
# Bağlı Dosyalar: face_plugin.py, io_manager.py, dashboard_websocket.py, state_reflector.js

# Versiyon: 0.5.0
# Değişiklikler:
# - [0.5.0] Durum Yansıtma Protokolü (State Reflection Protocol) entegrasyonu eklendi
# - [0.5.0] Ses tepkimeli ifade sistemi için WebSocket entegrasyonu eklendi
# - [0.5.0] IFrame Bridge entegrasyon desteği eklendi
# - [0.4.0] Modüler yapıya dönüştürüldü, dosya bölme işlemi yapıldı
# - [0.3.3] Animasyon API Endpoint'leri eklendi ve JSON formatı desteğiyle tam entegrasyon yapıldı
# - [0.3.2] Tema editör arayüzü iyileştirildi
# - [0.3.1] Çevresel faktör simülasyon görüntüleme desteği eklendi
# - [0.3.0] Tema yönetimi için API endpoint'leri eklendi
# - [0.2.0] Simülasyon görüntülerini görüntüleme özelliği eklendi
# - [0.1.0] Temel dashboard sunucu sınıfı oluşturuldu
#
# Yazar: GitHub Copilot
# Son Güncelleme: 2025-05-04
===========================================================
"""

import os
import sys
import time
import logging
import threading
import asyncio
import uvicorn
import json
import importlib
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, Callable
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# Proje dizinini Python yoluna ekle
PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SRC_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(str(PROJECT_DIR))
sys.path.append(str(SRC_DIR))

# Bağımlı modülleri içe aktar
from modules.dashboard_stats import get_system_stats
from modules.dashboard_templates import TemplateManager
from modules.dashboard_websocket import WebSocketManager
from modules.dashboard_routes import RoutesManager
from modules.dashboard_widgets.widget_manager import WidgetManager

# Logger yapılandırması
logger = logging.getLogger("DashboardServer")

# Face Plugin durum dosyası yolu
STATUS_FILE = os.path.join(str(PROJECT_DIR), "face_plugin_status.json")


class DashboardServer:
    """
    Dashboard sunucu sınıfı
    
    Bu sınıf, FACE1 robotun web tabanlı kontrol panelini sunar. FastAPI 
    backend, gerçek zamanlı WebSocket güncellemeleri ve robotun durumunu 
    izlemek için çeşitli sayfa ve API endpoint'leri içerir.
    """
    
    def __init__(self, config):
        """
        Dashboard sunucusunu başlatır
        
        Args:
            config (dict): Yapılandırma ayarları
        """
        logger.info("Dashboard Sunucu başlatılıyor...")
        self.config = config
        
        # Dashboard yapılandırması
        self.dashboard_config = config.get("dashboard", {})
        
        # Sunucu ayarları
        self.host = self.dashboard_config.get("host", "0.0.0.0")
        self.port = self.dashboard_config.get("port", 8000)
        self.debug = self.dashboard_config.get("debug", False)
        
        # Dosya yolları
        self.static_dir = os.path.join(PROJECT_DIR, "web", "static")
        self.templates_dir = os.path.join(PROJECT_DIR, "web", "templates")
        
        # Alt bileşenler
        self.websocket_manager = WebSocketManager()
        self.widget_manager = WidgetManager()
        self.template_manager = TemplateManager(self.templates_dir, self.static_dir)
        
        # Jinja2 şablonları
        self.templates = None
        if os.path.exists(self.templates_dir):
            self.templates = Jinja2Templates(directory=self.templates_dir)
        
        # Rota yöneticisi
        self.routes_manager = RoutesManager(
            face_plugin=None,
            templates=self.templates,
            templates_manager=self.template_manager,
            websocket_manager=self.websocket_manager,
            widget_manager=self.widget_manager,
            project_dir=PROJECT_DIR
        )
        self.routes_manager.set_config(self.config)
        
        # FastAPI uygulamasını oluştur
        self.app = self.create_app()
        
        # Durum izleme değişkenleri
        self.is_running = False
        self.server_thread = None
        self.system_stats_thread = None
        self.stop_event = threading.Event()
        
        # İletişim geriye doğru referansları
        self.face_plugin = None
        
        logger.info("Dashboard Sunucu başlatıldı.")
    
    def create_app(self) -> FastAPI:
        """
        FastAPI uygulamasını oluşturur ve yapılandırır
        
        Returns:
            FastAPI: Yapılandırılmış FastAPI uygulaması
        """
        app = FastAPI(
            title="FACE1 Dashboard",
            description="Raspberry Pi 5 Robot AI için Yüz Eklentisi Kontrol Paneli",
            version="0.5.0"
        )
        
        # CORS yapılandırması
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Tüm kaynaklara izin ver (geliştirme için)
            allow_credentials=True,
            allow_methods=["*"],   # Tüm HTTP metodlarına izin ver
            allow_headers=["*"],   # Tüm başlıklara izin ver
        )
        
        # Rotaları kaydet
        self.routes_manager.register_routes(app, self.static_dir, self.templates_dir)
        
        return app
    
    def start(self) -> bool:
        """
        Dashboard sunucusunu başlatır
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        if self.is_running:
            logger.warning("Dashboard sunucusu zaten çalışıyor.")
            return True
        
        try:
            # Dizin yapısını kontrol et
            os.makedirs(self.static_dir, exist_ok=True)
            os.makedirs(self.templates_dir, exist_ok=True)
            
            # Yoksa varsayılan şablonları oluştur
            self.template_manager.ensure_templates()
            
            # Sistem istatistikleri iş parçacığını başlat
            self.stop_event.clear()
            self.system_stats_thread = threading.Thread(target=self._system_stats_loop)
            self.system_stats_thread.daemon = True
            self.system_stats_thread.start()
            
            # Sunucuyu ayrı bir iş parçacığında başlat
            self.server_thread = threading.Thread(target=self._run_server)
            self.server_thread.daemon = True
            self.server_thread.start()
            
            self.is_running = True
            logger.info(f"Dashboard sunucusu başlatıldı: http://{self.host}:{self.port}")
            return True
            
        except Exception as e:
            logger.error(f"Dashboard sunucusu başlatılırken hata: {e}")
            return False
    
    def stop(self) -> None:
        """
        Dashboard sunucusunu durdurur
        """
        if not self.is_running:
            return
        
        self.is_running = False
        self.stop_event.set()
        
        logger.info("Dashboard sunucusu durduruldu.")
    
    def _run_server(self) -> None:
        """
        FastAPI sunucusunu başlatır
        """
        try:
            uvicorn.run(
                self.app, 
                host=self.host, 
                port=self.port,
                log_level="debug" if self.debug else "info"
            )
        except Exception as e:
            logger.error(f"FastAPI sunucusu başlatılırken hata: {e}")
    
    def _system_stats_loop(self) -> None:
        """
        Sistem istatistiklerini düzenli aralıklarla toplar ve istemcilere gönderir
        """
        while not self.stop_event.is_set():
            try:
                # Sistem istatistiklerini al
                stats = get_system_stats()
                
                # WebSocket istemcilerine gönder
                if self.websocket_manager.active_connections:
                    asyncio.run(self.websocket_manager.broadcast({"type": "stats", "data": stats}))
                
            except Exception as e:
                logger.error(f"Sistem istatistikleri iş parçacığında hata: {e}")
            
            # Her 5 saniyede bir güncelle
            time.sleep(5)
    
    def set_face_plugin(self, face_plugin) -> None:
        """
        Face Plugin referansını ayarlar
        
        Args:
            face_plugin: FacePlugin nesnesi
        """
        self.face_plugin = face_plugin
        self.websocket_manager.set_face_plugin(face_plugin)
        self.routes_manager.set_face_plugin(face_plugin)
        
        # Face Plugin referansını widget yöneticisine de ilet
        self.widget_manager.set_face_plugin(face_plugin)
        
        # Widget'ları yükle
        self.widget_manager.load_widgets()
        
        # Face plugin referansı ayarlandığında animasyon callback'lerini kaydet
        if face_plugin and hasattr(face_plugin, "animation_engine"):
            self.websocket_manager.register_animation_callbacks()
            
        # Face plugin referansı ayarlandığında ses işleme callback'lerini kaydet
        if face_plugin and hasattr(face_plugin, "sound_processor"):
            self.websocket_manager.register_sound_callbacks()
    
    def load_face_plugin_status(self) -> None:
        """
        Face Plugin durum dosyasını okur ve bağlantı kurar
        """
        if not os.path.exists(STATUS_FILE):
            logger.warning(f"Face Plugin durum dosyası bulunamadı: {STATUS_FILE}")
            return
        
        try:
            with open(STATUS_FILE, "r") as f:
                status_data = json.load(f)
                plugin_module = status_data.get("plugin_module")
                plugin_class = status_data.get("plugin_class")
                status = status_data.get("status")
                
                logger.info(f"Face plugin durumu dosyadan okundu: {status}")
                
                # Sadece plugin çalışırken bağlanmaya çalış
                if status != "running":
                    logger.warning(f"Face plugin çalışmıyor, durum: {status}")
                    return
                
                if plugin_module and plugin_class:
                    try:
                        # Modülü dinamik olarak içe aktar
                        module = importlib.import_module(plugin_module)
                        if hasattr(module, plugin_class):
                            # Sınıfı al
                            plugin_cls = getattr(module, plugin_class)
                            
                            # Instance oluştur, çalışan plugin'e bağlan
                            config_path = os.path.join(PROJECT_DIR, "config", "config.json")
                            face_plugin = plugin_cls(config_path)
                            
                            # Gerekli alt modüllerin başlatılıp başlatılmadığını kontrol et
                            if not hasattr(face_plugin, "animation_engine") or face_plugin.animation_engine is None:
                                logger.warning("Face plugin'in animation_engine modülü başlatılmamış veya None")
                                
                                # Animasyon motoru için varsayılan değer atamaya çalış
                                try:
                                    if hasattr(face_plugin, "init_animation_engine"):
                                        logger.info("Animation engine başlatılmaya çalışılıyor...")
                                        face_plugin.init_animation_engine()
                                except Exception as init_error:
                                    logger.error(f"Animation engine başlatılamadı: {init_error}")
                            
                            # Widget'ları başlatmak için plugin referansını ayarla
                            self.set_face_plugin(face_plugin)
                            
                            logger.info(f"Face plugin referansı hazırlandı ve widget'lar yüklendi")
                            
                            # Animation engine kontrolünü yap
                            if not hasattr(face_plugin, "animation_engine") or face_plugin.animation_engine is None:
                                logger.warning("Dashboard üzerindeki animasyon özellikleri çalışmayabilir, animation_engine mevcut değil")
                            else:
                                logger.info("Animation engine başarıyla referanslandı")
                        else:
                            logger.error(f"Plugin sınıfı bulunamadı: {plugin_class}")
                    except Exception as e:
                        logger.error(f"Plugin modülü içe aktarılırken hata: {e}")
                else:
                    logger.warning("Face Plugin durum dosyasında eksik modül/sınıf bilgisi.")
        
        except Exception as e:
            logger.error(f"Face Plugin durumu yüklenirken hata: {e}")


# Test kodu
if __name__ == "__main__":
    # Logging yapılandırması
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Alt modüllerin log seviyelerini ayarla
    logging.getLogger("DashboardRoutes").setLevel(logging.INFO)
    logging.getLogger("DashboardTemplates").setLevel(logging.INFO)
    logging.getLogger("DashboardWebSocket").setLevel(logging.INFO)
    logging.getLogger("DashboardStats").setLevel(logging.INFO)
    
    # Varsayılan yapılandırma
    test_config = {
        "dashboard": {
            "host": "localhost",
            "port": 8000,
            "debug": True
        }
    }
    
    print("Dashboard Sunucu Test")
    print("--------------------")
    
    # Dashboard sunucu örneği oluştur
    dashboard = DashboardServer(test_config)
    
    # Face Plugin durumunu yükle
    dashboard.load_face_plugin_status()
    
    # Dashboard sunucuyu başlat
    if dashboard.start():
        print(f"Dashboard sunucu başlatıldı: http://{dashboard.host}:{dashboard.port}")
        print("Dashboard test modunda çalışıyor. Çıkmak için Ctrl+C tuşlarına basın.")
        
        try:
            # Çıkış için bekle
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            # Dashboard sunucuyu durdur
            dashboard.stop()
            print("\nDashboard sunucu durduruldu.")
    else:
        print("Dashboard sunucu başlatılamadı!")