#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: face_plugin_api.py
# Açıklama: FacePlugin sınıfının API işlevleri, FastAPI ve HTTP sunucu
# Bağımlılıklar: fastapi, uvicorn, logging, threading
# Bağlı Dosyalar: face_plugin.py, face_plugin_base.py, face_plugin_lifecycle.py

# Versiyon: 0.4.1
# Değişiklikler:
# - [0.4.1] Gelişmiş yaşam döngüsü yönetimi API'ye entegre edildi
# - [0.4.0] FacePlugin modülerleştirildi, API işlevleri ayrı dosyaya taşındı
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-03
===========================================================
"""

import logging
import threading
import os
import json
import time as time_module
import traceback
from typing import Dict, List, Optional, Union, Any
import uvicorn
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .face_plugin_lifecycle import PluginState

# Loglama yapılandırması
logger = logging.getLogger("FacePluginAPI")

class FacePluginAPI:
    """
    FacePlugin API sınıfı
    
    Bu sınıf FacePlugin sınıfı için API işlevlerini içerir:
    - FastAPI sunucu kurulumu ve yönetimi
    - API rotaları ve endpoint'leri
    """
    
    def _setup_api(self) -> None:
        """
        REST API'yi ayarlar ve başlatır
        """
        try:
            api_config = self.config.get("api", {})
            if not api_config.get("enabled", True):
                logger.info("API devre dışı bırakıldı.")
                return
            
            # FastAPI nesnesini oluştur
            self.api = FastAPI(title="FACE1 API", version="0.4.1")
            
            # CORS ayarları
            self.api.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],  # Tüm kökenlere izin ver
                allow_credentials=True,
                allow_methods=["*"],  # Tüm metotlara izin ver
                allow_headers=["*"],  # Tüm başlıklara izin ver
            )
            
            # Statik dosyalar
            from pathlib import Path
            static_dir = os.path.join(str(Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))), "web", "static")
            if os.path.exists(static_dir):
                self.api.mount("/static", StaticFiles(directory=static_dir), name="static")
            
            # Şablonlar
            templates_dir = os.path.join(str(Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))), "web", "templates")
            templates = None
            if os.path.exists(templates_dir):
                templates = Jinja2Templates(directory=templates_dir)
            
            # API rotalarını tanımla
            @self.api.get("/")
            async def read_root():
                return {"status": "ok", "message": "FACE1 API çalışıyor", "version": "0.4.1"}
            
            @self.api.get("/status")
            async def get_status():
                # Durum bilgisini al - artık yaşam döngüsü durumu da dahil
                status = {
                    "status": "ok",
                    "running": self.is_running,
                    "state": self.state_name,
                    "emotion": self.get_current_emotion(),
                    "uptime": self.get_uptime(),
                    "last_heartbeat": time_module.time() - self.last_heartbeat,
                    "hardware": {
                        "platform": hardware_module.detect_platform(),
                        "oled_status": self.oled_controller.get_status() if self.oled_controller else "unavailable",
                        "led_status": self.led_controller.get_state() if self.led_controller else "unavailable"
                    }
                }
                return status
                
            @self.api.get("/lifecycle/status")
            async def get_lifecycle_status():
                """
                Plugin'in yaşam döngüsü durum raporunu döndürür
                """
                return self.get_status_report()
                
            @self.api.post("/lifecycle/maintenance")
            async def enter_maintenance_mode(background_tasks: BackgroundTasks = None):
                """
                Plugin'i bakım moduna alır
                """
                if self.state == PluginState.MAINTENANCE:
                    return {"status": "ok", "message": "Plugin zaten bakım modunda"}
                
                # Eğer çalışma durumundaysa bakım moduna al
                if not self.can_transition_to(PluginState.MAINTENANCE):
                    raise HTTPException(status_code=400, detail=f"Mevcut durumdan ({self.state_name}) bakım moduna geçiş yapılamaz")
                
                # Eğer background_tasks verilmişse arka planda yap
                if background_tasks:
                    background_tasks.add_task(self.enter_maintenance_mode)
                    return {"status": "ok", "message": "Plugin bakım moduna alınıyor"}
                else:
                    success = self.enter_maintenance_mode()
                    if not success:
                        raise HTTPException(status_code=500, detail="Plugin bakım moduna alınamadı")
                    return {"status": "ok", "message": "Plugin bakım moduna alındı", "state": self.state_name}
                
            @self.api.post("/lifecycle/exit_maintenance")
            async def exit_maintenance_mode():
                """
                Plugin'i bakım modundan çıkarır
                """
                if self.state != PluginState.MAINTENANCE:
                    raise HTTPException(status_code=400, detail=f"Plugin bakım modunda değil, mevcut durum: {self.state_name}")
                
                success = self.exit_maintenance_mode()
                if not success:
                    raise HTTPException(status_code=500, detail="Plugin bakım modundan çıkarılamadı")
                
                return {"status": "ok", "message": "Plugin bakım modundan çıkarıldı", "state": self.state_name}
                
            @self.api.post("/lifecycle/pause")
            async def pause_plugin():
                """
                Plugin'i duraklatır
                """
                if self.state == PluginState.PAUSED:
                    return {"status": "ok", "message": "Plugin zaten duraklatılmış"}
                
                if self.state != PluginState.RUNNING:
                    raise HTTPException(status_code=400, detail=f"Plugin duraklatılamıyor: mevcut durum {self.state_name}")
                
                success = self.pause()
                if not success:
                    raise HTTPException(status_code=500, detail="Plugin duraklatılamadı")
                
                return {"status": "ok", "message": "Plugin duraklatıldı", "state": self.state_name}
                
            @self.api.post("/lifecycle/resume")
            async def resume_plugin():
                """
                Plugin'i devam ettirir
                """
                if self.state == PluginState.RUNNING:
                    return {"status": "ok", "message": "Plugin zaten çalışıyor"}
                
                if self.state != PluginState.PAUSED:
                    raise HTTPException(status_code=400, detail=f"Plugin devam ettirilemiyor: mevcut durum {self.state_name}")
                
                success = self.resume()
                if not success:
                    raise HTTPException(status_code=500, detail="Plugin devam ettirilemedi")
                
                return {"status": "ok", "message": "Plugin devam ettirildi", "state": self.state_name}
                
            @self.api.get("/lifecycle/history")
            async def get_lifecycle_history(limit: int = Query(10, ge=1, le=100)):
                """
                Plugin'in durum geçiş tarihçesini döndürür
                """
                history = self.get_state_history()
                # Sınırlı sayıda kayıt döndür
                history = history[-limit:]
                
                # Okunabilir formata dönüştür
                formatted_history = []
                for old_state, new_state, timestamp in history:
                    formatted_history.append({
                        "from": old_state.value,
                        "to": new_state.value,
                        "timestamp": timestamp
                    })
                
                return {
                    "status": "ok",
                    "history": formatted_history,
                    "count": len(formatted_history)
                }
            
            @self.api.post("/emotion/{emotion}")
            async def set_emotion(emotion: str, intensity: float = 1.0):
                if not self.is_running:
                    raise HTTPException(status_code=503, detail="Yüz eklentisi çalışmıyor")
                
                success = self.set_emotion(emotion, intensity)
                if not success:
                    raise HTTPException(status_code=400, detail=f"Geçersiz duygu: {emotion}")
                
                return {"status": "ok", "emotion": emotion, "intensity": intensity}
            
            @self.api.post("/transition/{emotion}")
            async def transition_to_emotion(emotion: str, transition_time: float = None):
                if not self.is_running:
                    raise HTTPException(status_code=503, detail="Yüz eklentisi çalışmıyor")
                
                success = self.transition_to_emotion(emotion, transition_time)
                if not success:
                    raise HTTPException(status_code=400, detail=f"Geçersiz duygu: {emotion}")
                
                return {"status": "ok", "emotion": emotion, "transition_time": transition_time}
            
            @self.api.post("/micro_expression")
            async def add_micro_expression(
                emotion: str, 
                intensity: float = 1.0,
                duration: float = 0.5,
                delay: float = 0.0
            ):
                if not self.is_running:
                    raise HTTPException(status_code=503, detail="Yüz eklentisi çalışmıyor")
                
                success = self.add_micro_expression(emotion, intensity, duration, delay)
                if not success:
                    raise HTTPException(status_code=400, detail=f"Geçersiz mikro ifade: {emotion}")
                
                return {
                    "status": "ok", 
                    "emotion": emotion, 
                    "intensity": intensity,
                    "duration": duration,
                    "delay": delay
                }
            
            @self.api.post("/restart")
            async def restart_plugin(background_tasks: BackgroundTasks):
                if not self.is_running:
                    raise HTTPException(status_code=503, detail="Yüz eklentisi çalışmıyor")
                
                # Yeniden başlatmayı arka plan görevine ekle
                # Bu, API'nin yanıt vermesine izin verir
                background_tasks.add_task(self.restart)
                
                return {"status": "ok", "message": "Yüz eklentisi yeniden başlatılıyor"}
            
            @self.api.get("/theme")
            async def get_theme():
                if not self.is_running:
                    raise HTTPException(status_code=503, detail="Yüz eklentisi çalışmıyor")
                
                current_theme = self.get_current_theme()
                theme_list = self.get_theme_list()
                
                return {
                    "status": "ok",
                    "current_theme": current_theme,
                    "available_themes": theme_list
                }
            
            @self.api.post("/theme/{theme_name}")
            async def set_theme(theme_name: str):
                if not self.is_running:
                    raise HTTPException(status_code=503, detail="Yüz eklentisi çalışmıyor")
                
                success = self.set_theme(theme_name)
                if not success:
                    raise HTTPException(status_code=400, detail=f"Geçersiz tema: {theme_name}")
                
                return {"status": "ok", "theme": theme_name}
                
            @self.api.post("/shutdown")
            async def shutdown_plugin(background_tasks: BackgroundTasks):
                """
                Plugin'i tamamen kapatır (shutdown)
                """
                # Kapanışı arka plan görevine ekle
                # Bu, API'nin yanıt vermesine izin verir
                background_tasks.add_task(self.shutdown)
                
                return {"status": "ok", "message": "Yüz eklentisi kapatılıyor"}
            
            if templates:
                @self.api.get("/dashboard", response_class=JSONResponse)
                async def get_dashboard(request: Request):
                    if not self.is_running:
                        return templates.TemplateResponse(
                            "error.html",
                            {"request": request, "message": "Yüz eklentisi çalışmıyor"}
                        )
                    
                    return templates.TemplateResponse(
                        "dashboard.html",
                        {
                            "request": request,
                            "emotion": self.get_current_emotion(),
                            "platform": hardware_module.detect_platform(),
                            "state": self.state_name,
                            "version": "0.4.1"
                        }
                    )
                    
                @self.api.get("/lifecycle", response_class=JSONResponse)
                async def get_lifecycle_dashboard(request: Request):
                    """
                    Plugin yaşam döngüsü durumunu gösteren dashboard
                    """
                    status_report = self.get_status_report()
                    
                    # Mevcut durumda plugin çalışmasa bile dashboard'u göster
                    return templates.TemplateResponse(
                        "lifecycle_dashboard.html",
                        {
                            "request": request,
                            "status": status_report,
                            "state": self.state_name,
                            "uptime": self.get_uptime(),
                            "error_count": self._error_count,
                            "history": self.get_state_history()[-10:],
                            "version": "0.4.1"
                        }
                    )
            
            # API sunucusunu başlat
            host = api_config.get("host", "0.0.0.0")
            port = api_config.get("port", 8000)
            debug = api_config.get("debug", False)
            
            def run_api():
                import time as time_module
                from include import hardware_defines as hardware_module
                uvicorn.run(
                    self.api, 
                    host=host, 
                    port=port, 
                    log_level="debug" if debug else "info"
                )
            
            self.api_thread = threading.Thread(target=run_api, daemon=True)
            self.api_thread.start()
            self.is_api_running = True
            
            logger.info(f"API başlatıldı: http://{host}:{port}")
            
        except Exception as e:
            logger.error(f"API başlatılırken hata: {e}")
            logger.error(traceback.format_exc())
    
    def _notify_websocket_clients(self, message: Dict[str, Any]) -> None:
        """
        WebSocket istemcilerine bildirim gönderir
        
        Args:
            message (Dict[str, Any]): Gönderilecek mesaj
        """
        # Bu metod, alt sınıflar tarafından override edilebilir
        # Varsayılan olarak hiçbir şey yapmaz
        pass
    
    def _stop_api(self) -> None:
        """
        API sunucusunu durdurur
        """
        if not self.is_api_running:
            return
        
        try:
            # API sunucusu başka bir iş parçacığında çalışıyor
            # ve uvicorn.run() ile başlatıldığında temiz bir şekilde durdurulamıyor.
            # Burada sadece durumu güncelleyeceğiz ve iş parçacığı daemon olduğu için
            # ana program sonlandığında otomatik olarak duracak.
            
            logger.info("API sunucusu durduruluyor...")
            self.is_api_running = False
            
            # Kapanış olayını WebSocket istemcilerine bildir
            try:
                self._notify_websocket_clients({
                    'type': 'shutdown',
                    'message': 'API sunucusu kapatılıyor',
                    'timestamp': time_module.time()
                })
            except Exception as ws_error:
                logger.error(f"WebSocket bildirimi gönderilirken hata: {ws_error}")
            
        except Exception as e:
            logger.error(f"API sunucusu durdurulurken hata: {e}")