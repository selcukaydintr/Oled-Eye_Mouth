#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: io_manager.py
# Açıklama: I/O yöneticisi modülü. İletişim arayüzlerini ve veri alışverişini yönetir.
# Bağımlılıklar: websockets, asyncio, json, logging
# Bağlı Dosyalar: face_plugin.py, dashboard_server.py

# Versiyon: 0.2.0
# Değişiklikler:
# - [0.1.0] Temel I/O yöneticisi sınıfı oluşturuldu
# - [0.2.0] WebSocket sunucusu, olay yönetimi ve komut işleyici sistemleri geliştirildi
# - [0.2.0] Kimlik doğrulama, hız sınırlama ve MQTT altyapısı eklendi
#
# Yazar: GitHub Copilot
# Tarih: 2025-04-30
===========================================================
"""

import os
import sys
import json
import time
import logging
import asyncio
import threading
import websockets
from typing import Dict, List, Optional, Union, Callable, Any
from pathlib import Path
from enum import Enum

# Proje dizinini Python yoluna ekle
PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(str(PROJECT_DIR))

# Opsiyonel MQTT desteği
try:
    import paho.mqtt.client as mqtt
    MQTT_AVAILABLE = True
except ImportError:
    MQTT_AVAILABLE = False

# Logger yapılandırması
logger = logging.getLogger("IOManager")


class MessageType(Enum):
    """Mesaj türleri için enum sınıfı"""
    COMMAND = "command"
    EVENT = "event"
    RESPONSE = "response"
    ERROR = "error"


class IOManager:
    """
    I/O yöneticisi sınıfı
    
    Bu sınıf, dışarıdan gelen komutları işleyerek sistemin diğer bileşenlerine 
    iletir ve sistemden dışarıya olayları bildirir. WebSocket, REST API ve 
    opsiyonel olarak MQTT protokollerini destekler.
    """
    
    def __init__(self, config):
        """
        I/O yöneticisini başlatır
        
        Args:
            config (dict): Yapılandırma ayarları
        """
        logger.info("I/O Yöneticisi başlatılıyor...")
        self.config = config
        
        # I/O yapılandırması
        self.io_config = config.get("io", {})
        
        # WebSocket sunucu ayarları
        self.ws_host = self.io_config.get("websocket", {}).get("host", "0.0.0.0")
        self.ws_port = self.io_config.get("websocket", {}).get("port", 8765)
        self.ws_server = None
        self.ws_connections = set()
        
        # MQTT ayarları
        self.mqtt_enabled = self.io_config.get("mqtt", {}).get("enabled", False)
        self.mqtt_broker = self.io_config.get("mqtt", {}).get("broker", "localhost")
        self.mqtt_port = self.io_config.get("mqtt", {}).get("port", 1883)
        self.mqtt_topic_prefix = self.io_config.get("mqtt", {}).get("topic_prefix", "face1")
        self.mqtt_client = None
        
        # Olay ve geri çağrılar
        self.event_callbacks = {}
        self.command_handlers = {}
        
        # Çalışma durumu
        self.is_running = False
        self.ws_thread = None
        self.event_loop = None
        
        # Kimlik doğrulama
        self.auth_enabled = self.io_config.get("auth", {}).get("enabled", False)
        self.api_tokens = self.io_config.get("auth", {}).get("api_tokens", [])
        
        # Hız sınırlama
        self.rate_limit = self.io_config.get("rate_limit", {})
        self.rate_limit_enabled = self.rate_limit.get("enabled", False)
        self.request_timestamps = {}  # IP adresi bazlı istek zaman damgaları
        
        logger.info("I/O Yöneticisi başlatıldı.")
    
    def start(self) -> bool:
        """
        I/O yöneticisini başlatır
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        if self.is_running:
            logger.warning("I/O yöneticisi zaten çalışıyor.")
            return True
        
        try:
            # MQTT istemcisini başlat (eğer etkinse)
            if self.mqtt_enabled and MQTT_AVAILABLE:
                self._init_mqtt_client()
            
            # WebSocket sunucusunu başlat
            self.ws_thread = threading.Thread(target=self._start_websocket_server)
            self.ws_thread.daemon = True
            self.ws_thread.start()
            
            self.is_running = True
            logger.info(f"I/O yöneticisi başlatıldı. WebSocket sunucusu: {self.ws_host}:{self.ws_port}")
            return True
            
        except Exception as e:
            logger.error(f"I/O yöneticisi başlatılırken hata: {e}")
            return False
    
    def stop(self) -> None:
        """
        I/O yöneticisini durdurur
        """
        if not self.is_running:
            return
        
        self.is_running = False
        
        # WebSocket sunucusunu durdur
        if self.event_loop and self.ws_server:
            async def close_server():
                self.ws_server.close()
                await self.ws_server.wait_closed()
            
            if self.event_loop.is_running():
                future = asyncio.run_coroutine_threadsafe(close_server(), self.event_loop)
                future.result(timeout=5)
        
        # MQTT istemcisini durdur
        if self.mqtt_client:
            self.mqtt_client.disconnect()
        
        logger.info("I/O yöneticisi durduruldu.")
    
    def _start_websocket_server(self) -> None:
        """
        WebSocket sunucusunu başlatır
        """
        try:
            # Yeni bir olay döngüsü oluştur
            self.event_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.event_loop)
            
            # WebSocket sunucusu oluştur ve başlat
            start_server = websockets.serve(
                self._handle_websocket,
                self.ws_host,
                self.ws_port
            )
            
            self.ws_server = self.event_loop.run_until_complete(start_server)
            logger.info(f"WebSocket sunucusu başlatıldı: {self.ws_host}:{self.ws_port}")
            
            # Olay döngüsünü süresiz çalıştır
            self.event_loop.run_forever()
            
        except Exception as e:
            logger.error(f"WebSocket sunucusu başlatılırken hata: {e}")
        finally:
            if self.event_loop:
                self.event_loop.close()
    
    async def _handle_websocket(self, websocket, path) -> None:
        """
        WebSocket bağlantı işleyicisi
        
        Args:
            websocket: WebSocket bağlantısı
            path: İstek yolu
        """
        client_info = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        logger.info(f"Yeni WebSocket bağlantısı: {client_info}")
        
        # Bağlantıyı kaydet
        self.ws_connections.add(websocket)
        
        try:
            # Hoş geldin mesajını gönder
            welcome_msg = {
                "type": MessageType.EVENT.value,
                "event": "connected",
                "data": {
                    "message": "FACE1 robota bağlandınız",
                    "timestamp": time.time()
                }
            }
            await websocket.send(json.dumps(welcome_msg))
            
            # İstemciden gelen mesajları işle
            async for message in websocket:
                try:
                    # Hız sınırlaması kontrolü
                    if self.rate_limit_enabled:
                        if not self._check_rate_limit(websocket.remote_address[0]):
                            await websocket.send(json.dumps({
                                "type": MessageType.ERROR.value,
                                "error": "rate_limit_exceeded",
                                "message": "İstek sayısı sınırı aşıldı. Lütfen daha sonra tekrar deneyin."
                            }))
                            continue
                    
                    # JSON mesajını ayrıştır
                    data = json.loads(message)
                    
                    # Mesaj türünü kontrol et
                    msg_type = data.get("type")
                    if msg_type != MessageType.COMMAND.value:
                        await websocket.send(json.dumps({
                            "type": MessageType.ERROR.value,
                            "error": "invalid_message_type",
                            "message": f"Geçersiz mesaj türü: {msg_type}"
                        }))
                        continue
                    
                    # Kimlik doğrulama kontrolü
                    if self.auth_enabled:
                        token = data.get("token")
                        if not token or token not in self.api_tokens:
                            await websocket.send(json.dumps({
                                "type": MessageType.ERROR.value,
                                "error": "unauthorized",
                                "message": "Yetkisiz erişim. Geçerli bir API anahtarı gerekli."
                            }))
                            continue
                    
                    # Komutu işle
                    command = data.get("command")
                    command_data = data.get("data", {})
                    
                    # Cevabı hesapla
                    response = await self._process_command(command, command_data)
                    
                    # Cevabı gönder
                    await websocket.send(json.dumps({
                        "type": MessageType.RESPONSE.value,
                        "command": command,
                        "data": response
                    }))
                    
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        "type": MessageType.ERROR.value,
                        "error": "invalid_json",
                        "message": "Geçersiz JSON formatı"
                    }))
                except Exception as e:
                    logger.error(f"WebSocket mesajı işlenirken hata: {e}")
                    await websocket.send(json.dumps({
                        "type": MessageType.ERROR.value,
                        "error": "server_error",
                        "message": str(e)
                    }))
                
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"WebSocket bağlantısı kapandı: {client_info}")
        finally:
            # Bağlantıyı kaldır
            self.ws_connections.remove(websocket)
    
    def _init_mqtt_client(self) -> None:
        """
        MQTT istemcisini başlatır
        """
        if not MQTT_AVAILABLE:
            logger.warning("MQTT kütüphanesi yüklü değil, MQTT devre dışı bırakılıyor.")
            return
        
        try:
            # MQTT istemcisini oluştur
            client_id = f"face1_io_manager_{os.getpid()}"
            self.mqtt_client = mqtt.Client(client_id=client_id)
            
            # Geri çağrıları ayarla
            self.mqtt_client.on_connect = self._on_mqtt_connect
            self.mqtt_client.on_message = self._on_mqtt_message
            self.mqtt_client.on_disconnect = self._on_mqtt_disconnect
            
            # Kimlik doğrulama
            mqtt_auth = self.io_config.get("mqtt", {}).get("auth", {})
            if mqtt_auth.get("enabled", False):
                self.mqtt_client.username_pw_set(
                    mqtt_auth.get("username"),
                    mqtt_auth.get("password")
                )
            
            # Bağlantı kur
            self.mqtt_client.connect(
                self.mqtt_broker,
                self.mqtt_port,
                keepalive=60
            )
            
            # Arka planda çalıştır
            self.mqtt_client.loop_start()
            
        except Exception as e:
            logger.error(f"MQTT istemcisi başlatılırken hata: {e}")
            self.mqtt_client = None
    
    def _on_mqtt_connect(self, client, userdata, flags, rc) -> None:
        """
        MQTT bağlantı geri çağrısı
        """
        if rc == 0:
            logger.info(f"MQTT sunucusuna bağlandı: {self.mqtt_broker}:{self.mqtt_port}")
            # Komut kanalına abone ol
            command_topic = f"{self.mqtt_topic_prefix}/commands/#"
            client.subscribe(command_topic)
            logger.info(f"MQTT kanalına abone olundu: {command_topic}")
        else:
            logger.error(f"MQTT bağlantısı başarısız, kod: {rc}")
    
    def _on_mqtt_message(self, client, userdata, msg) -> None:
        """
        MQTT mesaj geri çağrısı
        """
        try:
            # Mesajı ayrıştır
            payload = json.loads(msg.payload.decode())
            topic_parts = msg.topic.split('/')
            
            # Komut kanalını kontrol et
            if len(topic_parts) >= 3 and topic_parts[1] == "commands":
                command = topic_parts[2]
                
                # Komutu işle
                asyncio.run_coroutine_threadsafe(
                    self._process_command(command, payload),
                    self.event_loop
                )
        except json.JSONDecodeError:
            logger.error(f"Geçersiz MQTT mesajı formatı: {msg.payload}")
        except Exception as e:
            logger.error(f"MQTT mesajı işlenirken hata: {e}")
    
    def _on_mqtt_disconnect(self, client, userdata, rc) -> None:
        """
        MQTT bağlantı kesme geri çağrısı
        """
        if rc != 0:
            logger.warning(f"Beklenmeyen MQTT bağlantı kesintisi, kod: {rc}")
    
    async def _process_command(self, command: str, data: Dict) -> Dict:
        """
        Komutu işler ve yanıt döndürür
        
        Args:
            command (str): Komut adı
            data (Dict): Komut parametreleri
            
        Returns:
            Dict: İşlem sonucu
        """
        # Komut işleyicisini bul
        handler = self.command_handlers.get(command)
        
        if handler:
            try:
                result = handler(data)
                
                # Eğer sonuç bir coroutine ise, bekle
                if asyncio.iscoroutine(result):
                    result = await result
                
                return {
                    "success": True,
                    "result": result
                }
                
            except Exception as e:
                logger.error(f"Komut işlenirken hata: {command}, hata: {e}")
                return {
                    "success": False,
                    "error": str(e)
                }
        else:
            logger.warning(f"Bilinmeyen komut: {command}")
            return {
                "success": False,
                "error": f"Bilinmeyen komut: {command}"
            }
    
    def register_command_handler(self, command: str, handler: Callable) -> None:
        """
        Komut işleyici kaydeder
        
        Args:
            command (str): Komut adı
            handler (Callable): İşleyici fonksiyon
        """
        self.command_handlers[command] = handler
        logger.debug(f"Komut işleyici kaydedildi: {command}")
    
    def unregister_command_handler(self, command: str) -> None:
        """
        Komut işleyici kaydını siler
        
        Args:
            command (str): Komut adı
        """
        if command in self.command_handlers:
            del self.command_handlers[command]
            logger.debug(f"Komut işleyici kaydı silindi: {command}")
    
    def register_callback(self, event_type: str, callback: Callable) -> None:
        """
        Olay geri çağrısı kaydeder
        
        Args:
            event_type (str): Olay türü
            callback (Callable): Geri çağrı fonksiyonu
        """
        if event_type not in self.event_callbacks:
            self.event_callbacks[event_type] = []
        
        if callback not in self.event_callbacks[event_type]:
            self.event_callbacks[event_type].append(callback)
            logger.debug(f"Olay geri çağrısı kaydedildi: {event_type}")
    
    def unregister_callback(self, event_type: str, callback: Callable) -> None:
        """
        Olay geri çağrı kaydını siler
        
        Args:
            event_type (str): Olay türü
            callback (Callable): Geri çağrı fonksiyonu
        """
        if event_type in self.event_callbacks and callback in self.event_callbacks[event_type]:
            self.event_callbacks[event_type].remove(callback)
            logger.debug(f"Olay geri çağrı kaydı silindi: {event_type}")
    
    def send_event(self, event_type: str, data: Any) -> None:
        """
        Olay gönderir
        
        Args:
            event_type (str): Olay türü
            data (Any): Olay verileri
        """
        # Olayı WebSocket istemcilerine gönder
        if self.event_loop and self.ws_connections:
            message = {
                "type": MessageType.EVENT.value,
                "event": event_type,
                "data": data,
                "timestamp": time.time()
            }
            
            # JSON uyumluluğunu sağla
            json_message = json.dumps(message, default=str)
            
            # Her bir bağlantıya gönder
            for websocket in self.ws_connections:
                asyncio.run_coroutine_threadsafe(
                    websocket.send(json_message),
                    self.event_loop
                )
        
        # Olayı MQTT kanalına yayınla
        if self.mqtt_client and self.is_running:
            try:
                topic = f"{self.mqtt_topic_prefix}/events/{event_type}"
                payload = json.dumps(data, default=str)
                self.mqtt_client.publish(topic, payload)
            except Exception as e:
                logger.error(f"MQTT olay yayını başarısız: {e}")
        
        # Yerel olay geri çağrılarını tetikle
        if event_type in self.event_callbacks:
            for callback in self.event_callbacks[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    logger.error(f"Olay geri çağrısı başarısız: {event_type}, hata: {e}")
    
    def _check_rate_limit(self, ip_address: str) -> bool:
        """
        Hız sınırı kontrolü yapar
        
        Args:
            ip_address (str): İstemci IP adresi
            
        Returns:
            bool: Sınır aşılmamışsa True, aksi halde False
        """
        if not self.rate_limit_enabled:
            return True
        
        current_time = time.time()
        time_window = self.rate_limit.get("time_window", 60)  # saniye
        max_requests = self.rate_limit.get("max_requests", 100)  # pencere başına maksimum istek
        
        # IP adresini kontrol et
        if ip_address not in self.request_timestamps:
            self.request_timestamps[ip_address] = []
        
        # Eski zaman damgalarını temizle
        self.request_timestamps[ip_address] = [
            ts for ts in self.request_timestamps[ip_address] 
            if current_time - ts < time_window
        ]
        
        # İstek sayısını kontrol et
        if len(self.request_timestamps[ip_address]) >= max_requests:
            logger.warning(f"Hız sınırı aşıldı: {ip_address}, {max_requests}/{time_window}s")
            return False
        
        # Yeni zaman damgasını ekle
        self.request_timestamps[ip_address].append(current_time)
        return True


# Test kodu
if __name__ == "__main__":
    # Logging yapılandırması
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Varsayılan yapılandırma
    test_config = {
        "io": {
            "websocket": {
                "host": "localhost",
                "port": 8765
            },
            "mqtt": {
                "enabled": False,
                "broker": "localhost",
                "port": 1883,
                "topic_prefix": "face1"
            },
            "auth": {
                "enabled": False,
                "api_tokens": ["test_token"]
            },
            "rate_limit": {
                "enabled": True,
                "max_requests": 100,
                "time_window": 60
            }
        }
    }
    
    print("I/O Yöneticisi Test")
    print("-----------------")
    
    # I/O yöneticisi örneği oluştur
    io_manager = IOManager(test_config)
    
    # Test komut işleyicisi
    def handle_test_command(data):
        print(f"Test komutu çalıştırıldı: {data}")
        return {"status": "success", "message": "Test komutu işlendi"}
    
    # Test olay geri çağrısı
    def on_test_event(data):
        print(f"Test olayı alındı: {data}")
    
    # Komut işleyici ve olay geri çağrısı kaydı
    io_manager.register_command_handler("test", handle_test_command)
    io_manager.register_callback("test_event", on_test_event)
    
    # I/O yöneticisini başlat
    if io_manager.start():
        print(f"I/O yöneticisi başlatıldı. WebSocket sunucusu: {io_manager.ws_host}:{io_manager.ws_port}")
        
        # Test olayı gönder
        io_manager.send_event("test_event", {"message": "Bu bir test mesajıdır", "timestamp": time.time()})
        
        # Terminal istemleri
        print("\nI/O yöneticisi test modunda çalışıyor. Çıkmak için Ctrl+C tuşlarına basın.")
        print("WebSocket test istemcisi bağlanabilir: ws://localhost:8765")
        
        try:
            # Çıkış için bekle
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            # I/O yöneticisini durdur
            io_manager.stop()
            print("\nI/O yöneticisi durduruldu.")
    else:
        print("I/O yöneticisi başlatılamadı!")