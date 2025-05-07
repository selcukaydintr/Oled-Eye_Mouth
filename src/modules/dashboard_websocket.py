#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: dashboard_websocket.py
# Açıklama: Dashboard için WebSocket işlemleri ve Durum Yansıtma Protokolü desteği
# Bağımlılıklar: fastapi, websockets
# Bağlı Dosyalar: dashboard_server.py, state_reflector.js, iframe_bridge.js

# Versiyon: 0.5.1
# Değişiklikler:
# - [0.1.0] dashboard_server.py dosyasından ayrıldı
# - [0.5.0] Durum Yansıtma Protokolü desteği eklendi
# - [0.5.0] İki yönlü durum senkronizasyonu eklendi
# - [0.5.0] Ses ve animasyon olayları iyileştirildi
# - [0.5.1] Simülasyon WebSocket bağlantı yönetimi iyileştirildi 
# - [0.5.1] Hata işleme mekanizması geliştirildi
#
# Yazar: GitHub Copilot
# Son Güncelleme: 2025-05-06
===========================================================
"""

import os
import sys
import json
import logging
import time
import asyncio
import glob
from typing import Dict, Any, Dict, Callable, List, Optional
from pathlib import Path

# Proje dizinini Python yoluna ekle
PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
SRC_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(str(PROJECT_DIR))
sys.path.append(str(SRC_DIR))

from fastapi import WebSocket, WebSocketDisconnect

# Logger yapılandırması
logger = logging.getLogger("DashboardWebSocket")

class WebSocketManager:
    """
    WebSocket bağlantı yönetim sınıfı
    """
    def __init__(self):
        self.active_connections = {}
        self.face_plugin = None
        # Ses işlemesi için durumlar
        self.last_volume_broadcast = 0
        self.last_speaking_state = False
        # Simülasyon modu için durumlar
        self.simulation_directory = os.path.join(PROJECT_DIR, "simulation")
        self.simulation_update_interval = 0.5  # Saniye
        self.max_image_age = 3600  # 1 saat
        self.max_simulation_files = 1000  # Maksimum dosya sayısı
    
    def set_face_plugin(self, face_plugin) -> None:
        """
        Face Plugin referansını ayarlar
        
        Args:
            face_plugin: FacePlugin nesnesi
        """
        self.face_plugin = face_plugin
        
        # Face plugin referansı ayarlandığında animasyon callback'lerini kaydet
        if face_plugin and hasattr(face_plugin, "animation_engine"):
            self.register_animation_callbacks()
            
        # Ses işleme modülü varsa callback'leri kaydet
        if face_plugin and hasattr(face_plugin, "sound_processor"):
            self.register_sound_callbacks()

        # Simülasyon dizinini oluştur
        os.makedirs(self.simulation_directory, exist_ok=True)
        logger.info(f"Simülasyon dizini: {self.simulation_directory}")
    
    async def handle_websocket(self, websocket: WebSocket) -> None:
        """
        WebSocket bağlantısını işler
        
        Args:
            websocket (WebSocket): WebSocket bağlantısı
        """
        # Bağlantıyı kabul et
        await websocket.accept()
        
        # İstemci bilgisini al
        client_id = f"{id(websocket)}"
        self.active_connections[client_id] = websocket
        
        try:
            # Hoş geldin mesajını gönder
            await websocket.send_json({
                "type": "welcome",
                "message": "FACE1 Dashboard WebSocket bağlantısı kuruldu"
            })
            
            # Mevcut durumu gönder
            if self.face_plugin:
                if self.face_plugin.theme_manager:
                    theme = self.face_plugin.theme_manager.get_current_theme()
                    await websocket.send_json({
                        "type": "theme_changed",
                        "theme": theme
                    })
                
                if self.face_plugin.emotion_engine:
                    emotion = self.face_plugin.emotion_engine.get_current_emotion()
                    await websocket.send_json({
                        "type": "emotion_changed",
                        "emotion": emotion
                    })
            
            # İstemciden gelen mesajları işle
            while True:
                message = await websocket.receive_text()
                try:
                    data = json.loads(message)
                    action = data.get("action")
                    
                    if action == "set_theme" and self.face_plugin:
                        theme_name = data.get("theme")
                        if theme_name:
                            self.face_plugin.set_theme(theme_name)
                    
                    elif action == "set_emotion" and self.face_plugin:
                        emotion = data.get("emotion")
                        intensity = data.get("intensity", 1.0)
                        if emotion:
                            self.face_plugin.set_emotion(emotion, intensity)
                    
                    # Diğer mesaj türleri buraya eklenebilir
                
                except json.JSONDecodeError:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Geçersiz JSON formatı"
                    })
                except Exception as e:
                    logger.error(f"WebSocket mesajı işlenirken hata: {e}")
                    await websocket.send_json({
                        "type": "error",
                        "message": str(e)
                    })
                
        except WebSocketDisconnect:
            logger.info(f"WebSocket bağlantısı kapandı: {client_id}")
        except Exception as e:
            logger.error(f"WebSocket işleme hatası: {e}")
        finally:
            # Bağlantıyı kaldır
            if client_id in self.active_connections:
                del self.active_connections[client_id]

    async def broadcast(self, message: Dict) -> None:
        """
        Tüm bağlı WebSocket istemcilerine mesaj gönderir
        
        Args:
            message (Dict): Gönderilecek mesaj
        """
        for client_id, connection in list(self.active_connections.items()):
            try:
                await connection.send_json(message)
            except Exception:
                # Bağlantı kesilmiş olabilir, temizle
                if client_id in self.active_connections:
                    del self.active_connections[client_id]

    def notify_animation_event(self, event_type: str, animation_name: str, additional_data: Dict = None) -> None:
        """
        Animasyon olaylarını bildirir ve WebSocket üzerinden istemcilere iletir
        
        Args:
            event_type (str): Olay türü ('started', 'stopped', 'completed', 'error', 'transition', 'progress')
            animation_name (str): Animasyon adı
            additional_data (Dict, optional): Ek veri alanları. Varsayılan: None
        """
        try:
            if not self.active_connections:
                return
                
            message = {
                "type": f"animation_{event_type}",
                "animation": animation_name,
                "timestamp": __import__('time').time()
            }
            
            # Eğer ek veri varsa, mesaja ekle
            if additional_data and isinstance(additional_data, dict):
                message.update(additional_data)
            
            logger.debug(f"Animasyon olayı bildiriliyor: {event_type} - {animation_name}")
            asyncio.run(self.broadcast(message))
                
        except Exception as e:
            logger.error(f"Animasyon olayı bildirirken hata: {e}")
            logger.debug("Hata ayrıntıları:", exc_info=True)
    
    def notify_animation_transition(self, source_state: str, target_state: str, 
                                   progress: float, intensity: float) -> None:
        """
        Duygu durumları arasındaki geçiş animasyonlarını bildirir
        
        Args:
            source_state (str): Kaynak duygu durumu
            target_state (str): Hedef duygu durumu
            progress (float): İlerleme durumu (0.0-1.0)
            intensity (float): Duygu yoğunluğu
        """
        if not self.active_connections:
            return
            
        try:
            # Çok fazla güncelleme göndermemek için %5'lik artışlarla filtreleme yap
            progress_rounded = round(progress * 20) / 20  # 0.05 artışlarla yuvarla
            
            # WebSocket üzerinden ilerleme durumunu bildir
            animation_name = f"transition_{source_state}_to_{target_state}"
            additional_data = {
                "source_state": source_state,
                "target_state": target_state,
                "progress": progress_rounded,
                "intensity": round(intensity, 2),
                "eased_progress": self._ease_progress(progress)  # Yumuşatılmış ilerleme
            }
            
            self.notify_animation_event("transition", animation_name, additional_data)
            
        except Exception as e:
            logger.error(f"Animasyon geçişi bildirirken hata: {e}")

    def _ease_progress(self, progress: float) -> float:
        """
        İlerleme değerini yumuşatmak için easing fonksiyonu
        
        Args:
            progress (float): Ham ilerleme (0.0-1.0)
            
        Returns:
            float: Yumuşatılmış ilerleme (0.0-1.0)
        """
        # Cubic easing fonksiyonu (yavaş başla, hızlan, yavaş bitir)
        if progress < 0.5:
            return 4 * (progress ** 3)
        else:
            return 1 - (4 * ((1 - progress) ** 3))
    
    def notify_animation_error(self, animation_name: str, error_message: str, 
                              error_code: int = None, recoverable: bool = True) -> None:
        """
        Animasyon hatalarını bildirir
        
        Args:
            animation_name (str): Animasyon adı
            error_message (str): Hata mesajı
            error_code (int, optional): Hata kodu. Varsayılan: None
            recoverable (bool, optional): Hata giderilebilir mi. Varsayılan: True
        """
        try:
            additional_data = {
                "error": {
                    "message": error_message,
                    "code": error_code,
                    "recoverable": recoverable,
                    "timestamp": __import__('time').time()
                }
            }
            
            # Hatayı dashboard'a bildir
            self.notify_animation_event("error", animation_name, additional_data)
            
            # Hatayı loglara kaydet
            if recoverable:
                logger.warning(f"Animasyon hatası ({animation_name}): {error_message}")
            else:
                logger.error(f"Kritik animasyon hatası ({animation_name}): {error_message}")
                
        except Exception as e:
            logger.error(f"Animasyon hatası bildirirken hata: {e}")

    def register_animation_callbacks(self) -> None:
        """
        Animasyon olayları için callback'leri kaydeder
        """
        if not self.face_plugin or not hasattr(self.face_plugin, "animation_engine"):
            logger.warning("Animasyon motoru bulunamadı, olaylar kaydedilemedi")
            return
            
        try:
            # Animasyon motorunu al
            engine = self.face_plugin.animation_engine
            
            if hasattr(engine, "register_event_callback"):
                # Temel animasyon olayları
                engine.register_event_callback("animation_started", 
                                              lambda data: self.notify_animation_event("started", data.get('name', 'unknown')))
                engine.register_event_callback("animation_stopped", 
                                              lambda data: self.notify_animation_event("stopped", data.get('name', 'unknown')))
                engine.register_event_callback("animation_completed", 
                                              lambda data: self.notify_animation_event("completed", data.get('name', 'unknown')))
                
                # İlerleme ve geçiş durumu
                engine.register_event_callback("animation_progress", 
                                              lambda data: self.notify_animation_event("progress", data.get('name', 'unknown'), {
                                                  "progress": data.get('progress', 0),
                                                  "total_time": data.get('total_time', 0),
                                                  "current_time": data.get('current_time', 0)
                                              }))
                
                # Geçiş animasyonları için
                engine.register_event_callback("emotion_transition", 
                                              lambda data: self.notify_animation_transition(
                                                  data.get('source', 'neutral'),
                                                  data.get('state', 'neutral'),
                                                  data.get('raw_progress', 0),
                                                  data.get('intensity', 1.0)
                                              ))
                
                # Hata işleme
                engine.register_event_callback("animation_error", 
                                              lambda data: self.notify_animation_error(
                                                  data.get('animation', 'unknown'),
                                                  data.get('error', 'Bilinmeyen hata'),
                                                  data.get('code', None),
                                                  data.get('recoverable', True)
                                              ))
                
                logger.info("Animasyon olayları için gelişmiş callback'ler kaydedildi")
            else:
                logger.warning("Animasyon motoru callback kayıt fonksiyonu bulunamadı")
        except Exception as e:
            logger.error(f"Animasyon callback'leri kaydedilirken hata: {e}")
            logger.debug("Hata ayrıntıları:", exc_info=True)

    async def handle_simulation_websocket(self, websocket: WebSocket) -> None:
        """
        Simülasyon WebSocket bağlantısını işler
        
        Args:
            websocket (WebSocket): WebSocket bağlantısı
        """
        await websocket.accept()
        
        try:
            client_id = f"sim_{id(websocket)}"
            self.active_connections[client_id] = websocket
            
            # Bağlantı durumunu izlemek için bayrak
            connection_active = True
            
            # Hoş geldin mesajını gönder
            await websocket.send_json({
                "type": "welcome",
                "message": "Simülasyon akışı başlatıldı"
            })
            
            # Simülasyon klasörünü temizle (eski dosyaları sil)
            await self._cleanup_simulation_files()
            
            logger.info(f"Simülasyon WebSocket bağlantısı başlatıldı: {client_id}")
            
            # İlk simülasyon görüntülerini gönder
            initial_images = await self._gather_simulation_images()
            if initial_images and any(initial_images.values()):
                try:
                    await websocket.send_json({
                        "type": "simulation_update",
                        "timestamp": time.time(),
                        "images": initial_images
                    })
                except Exception as e:
                    logger.error(f"İlk simülasyon görüntüleri gönderilirken hata: {e}")
            
            # İstemci bağlantıyı kesene kadar düzenli güncellemeler gönder
            last_update_time = time.time()
            last_update_images = initial_images
            
            while connection_active:
                try:
                    # Son simülasyon görüntülerini al
                    current_time = time.time()
                    
                    # Güncelleme aralığını kontrol et
                    if current_time - last_update_time >= self.simulation_update_interval:
                        images = await self._gather_simulation_images()
                        
                        # Sadece yeni görüntüler varsa gönder
                        if images and self._has_new_images(images, last_update_images):
                            # Bağlantı aktif mi kontrol et
                            if not websocket.client_state.CONNECTED:
                                logger.info(f"İstemci artık bağlı değil, simülasyon döngüsü durduruluyor: {client_id}")
                                connection_active = False
                                break
                            
                            # Görüntü güncellemesini gönder
                            try:
                                await websocket.send_json({
                                    "type": "simulation_update",
                                    "timestamp": current_time,
                                    "images": images
                                })
                                
                                # Başarılı gönderimden sonra son güncelleme değerlerini kaydet
                                last_update_time = current_time
                                last_update_images = images.copy()
                                
                            except RuntimeError as e:
                                # WebSocket bağlantı hatası, döngüyü sonlandır
                                if "close message has been sent" in str(e) or "connection is closed" in str(e):
                                    logger.info(f"WebSocket bağlantısı kapandı, simülasyon döngüsü durduruluyor: {client_id}")
                                    connection_active = False
                                    break
                                else:
                                    # Başka bir hata ise yükselt
                                    raise
                    
                    # Her döngüde kısa bir bekleme yap
                    await asyncio.sleep(0.1)
                    
                except Exception as e:
                    logger.error(f"Simülasyon güncellemesi gönderilirken hata: {e}")
                    
                    # Ciddi bir hata oluştuğunda da döngüyü sonlandır
                    if "close message has been sent" in str(e) or "connection is closed" in str(e):
                        connection_active = False
                        break
                        
                    # Diğer hatalar için kısa bir süre bekle ve devam et
                    await asyncio.sleep(1)
                
        except WebSocketDisconnect:
            logger.info(f"Simülasyon WebSocket bağlantısı kapandı: {client_id}")
        except Exception as e:
            logger.error(f"Simülasyon WebSocket hatası: {e}")
        finally:
            # Bağlantıyı kaldır
            if client_id in self.active_connections:
                del self.active_connections[client_id]
    
    async def _gather_simulation_images(self) -> Dict[str, str]:
        """
        Son simülasyon görüntülerini bulur ve döndürür
        
        Returns:
            Dict[str, str]: Görüntü türlerine göre dosya isimleri
        """
        try:
            # Simülasyon dizini yoksa oluştur
            os.makedirs(self.simulation_directory, exist_ok=True)
            
            images = {
                "left_eye": None,
                "right_eye": None,
                "mouth": None,
                "leds": None
            }
            
            # Sol göz görüntüleri
            left_eye_images = sorted(glob.glob(os.path.join(self.simulation_directory, "display_left_eye_*.png")))
            if left_eye_images:
                images["left_eye"] = os.path.basename(left_eye_images[-1])
            
            # Sağ göz görüntüleri
            right_eye_images = sorted(glob.glob(os.path.join(self.simulation_directory, "display_right_eye_*.png")))
            if right_eye_images:
                images["right_eye"] = os.path.basename(right_eye_images[-1])
            
            # Ağız görüntüleri
            mouth_images = sorted(glob.glob(os.path.join(self.simulation_directory, "display_mouth_*.png")))
            if mouth_images:
                images["mouth"] = os.path.basename(mouth_images[-1])
            
            # LED görüntüleri
            led_images = sorted(glob.glob(os.path.join(self.simulation_directory, "leds_*.png")))
            if led_images:
                images["leds"] = os.path.basename(led_images[-1])
            
            # Hiç görüntü bulunamazsa log ekle
            if not any(images.values()):
                logger.warning("Simülasyon klasöründe hiç görüntü bulunamadı")
                
            return images
            
        except Exception as e:
            logger.error(f"Simülasyon görüntüleri toplanırken hata: {e}")
            return {}
    
    def _has_new_images(self, new_images: Dict[str, str], old_images: Dict[str, str]) -> bool:
        """
        Yeni görüntüler olup olmadığını kontrol eder
        
        Args:
            new_images (Dict[str, str]): Yeni görüntü dosyaları
            old_images (Dict[str, str]): Eski görüntü dosyaları
            
        Returns:
            bool: Yeni görüntü varsa True
        """
        if not old_images:
            return bool(new_images and any(new_images.values()))
            
        # Herhangi bir görüntü türü değiştiyse true döndür
        for img_type in ["left_eye", "right_eye", "mouth", "leds"]:
            if new_images.get(img_type) != old_images.get(img_type):
                return True
                
        return False
    
    async def _cleanup_simulation_files(self) -> None:
        """
        Eski simülasyon dosyalarını temizler
        """
        try:
            # Simülasyon dizini yoksa oluştur ve işlemi atla
            if not os.path.exists(self.simulation_directory):
                os.makedirs(self.simulation_directory, exist_ok=True)
                return
                
            # Tüm simülasyon görüntülerini bul
            pattern = os.path.join(self.simulation_directory, "*.png")
            all_files = glob.glob(pattern)
            
            # Dosya sayısı limiti aşılmadıysa işlem yapma
            if len(all_files) <= self.max_simulation_files:
                return
                
            # Dosyaları oluşturma zamanına göre sırala
            sorted_files = sorted(all_files, key=os.path.getctime)
            
            # Silinecek dosya sayısını hesapla (dosya sayısını limitle sınırla)
            files_to_delete = sorted_files[:len(sorted_files) - self.max_simulation_files]
            
            # Eski dosyaları sil
            for file_path in files_to_delete:
                try:
                    os.remove(file_path)
                except Exception as e:
                    logger.warning(f"Eski simülasyon dosyası silinirken hata: {e}")
            
            if files_to_delete:
                logger.info(f"{len(files_to_delete)} eski simülasyon dosyası temizlendi")
                
        except Exception as e:
            logger.error(f"Simülasyon dosyaları temizlenirken hata: {e}")

    def register_sound_callbacks(self) -> None:
        """
        Ses olayları için callback'leri kaydeder
        """
        if not self.face_plugin or not hasattr(self.face_plugin, "sound_processor"):
            logger.warning("Ses işleme modülü bulunamadı, olaylar kaydedilemedi")
            return
            
        try:
            # Ses işleme modülünü al
            sound_processor = self.face_plugin.sound_processor
            
            # Callback'leri kaydet
            sound_processor.register_volume_callback(self.handle_volume_change)
            sound_processor.register_speaking_callback(self.handle_speaking_change)
            
            logger.info("Ses olayları için callback'ler kaydedildi")
        except Exception as e:
            logger.error(f"Ses callback'leri kaydedilirken hata: {e}")
    
    def handle_volume_change(self, volume: float) -> None:
        """
        Ses seviyesi değiştiğinde çağrılır
        
        Args:
            volume (float): Güncel ses seviyesi (0.0-1.0 arası)
        """
        try:
            current_time = time.time()
            
            # Ses seviyesini çok sık bildirmemek için throttling uygula (saniyede en fazla 5 bildirim)
            if current_time - self.last_volume_broadcast < 0.2:
                return
                
            self.last_volume_broadcast = current_time
            
            # WebSocket üzerinden ses seviyesini bildir
            if self.active_connections:
                message = {
                    "type": "volume_update",
                    "volume": round(volume, 2),
                    "timestamp": current_time
                }
                
                asyncio.run(self.broadcast(message))
        except Exception as e:
            logger.error(f"Ses seviyesi bildirirken hata: {e}")

    def handle_speaking_change(self, speaking: bool) -> None:
        """
        Konuşma durumu değiştiğinde çağrılır
        
        Args:
            speaking (bool): Konuşma algılandıysa True, değilse False
        """
        try:
            # Sadece durum değiştiğinde bildir
            if speaking == self.last_speaking_state:
                return
                
            self.last_speaking_state = speaking
            
            # WebSocket üzerinden konuşma durumunu bildir
            if self.active_connections:
                message = {
                    "type": "speaking_update",
                    "speaking": speaking,
                    "timestamp": time.time()
                }
                
                asyncio.run(self.broadcast(message))
        except Exception as e:
            logger.error(f"Konuşma durumu bildirirken hata: {e}")