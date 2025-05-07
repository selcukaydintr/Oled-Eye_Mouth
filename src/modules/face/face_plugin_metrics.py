#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: face_plugin_metrics.py
# Açıklama: FacePlugin metrik toplama, izleme ve raporlama işlevleri
# Bağımlılıklar: logging, psutil, time
# Bağlı Dosyalar: face_plugin_base.py, face_plugin_system.py

# Versiyon: 0.4.4
# Değişiklikler:
# - [0.4.4] Metrik toplama işlevleri modülerleştirildi
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-04
===========================================================
"""

import os
import time
import logging
import threading
from typing import Dict, List, Any, Optional
import json
import psutil

try:
    import RPi.GPIO as GPIO
    RPI_AVAILABLE = True
except ImportError:
    RPI_AVAILABLE = False

# Loglama yapılandırması
logger = logging.getLogger("FacePluginMetrics")

class FacePluginMetricsMixin:
    """
    FacePlugin metrik toplama mixin sınıfı
    
    Bu sınıf FacePlugin için metrik toplama işlevlerini içerir:
    - Sistem kaynaklarını izleme (CPU, RAM, disk, sıcaklık)
    - Performans metriklerini toplama ve raporlama
    - Donanım durumu izleme (sıcaklık, güç)
    - Metrik verilerini kaydetme ve analiz etme
    """
    
    def __init_metrics__(self):
        """
        Metrik sistemini başlatır - ana __init__ metodundan sonra çağrılmalıdır
        """
        # Metrik değişkenleri
        self.system_metrics = {
            "cpu_usage": 0.0,
            "memory_usage": 0.0,
            "disk_usage": 0.0,
            "temperature": 0.0,
            "uptime": 0.0
        }
        
        # Modül metrikleri
        self.module_metrics = {
            "oled_controller": {},
            "led_controller": {},
            "emotion_engine": {},
            "theme_manager": {},
            "animation_engine": {},
            "dashboard_server": {},
            "performance_optimizer": {}
        }
        
        # Performans metrikleri
        self.performance_metrics = {
            "fps": 0.0,
            "frame_time": 0.0,
            "render_time": 0.0,
            "logic_time": 0.0,
            "network_latency": 0.0
        }
        
        # API metrikleri
        self.api_metrics = {
            "requests_per_second": 0.0,
            "avg_response_time": 0.0,
            "active_connections": 0,
            "error_rate": 0.0
        }
        
        # Metrik toplama zamanları
        self.last_metric_collection = 0.0
        self.metric_collection_interval = 5.0  # saniye
        
        # Metrik toplama döngüsü
        self.metrics_thread = None
        self.metrics_thread_running = False
        
        # Metrik geçmişi
        self.metric_history = {
            "system": [],
            "performance": [],
            "api": []
        }
        self.metric_history_max_length = 60  # Son 60 ölçümü tut (~5 dakika, 5s aralıkla)
        
        logger.debug("Metrik sistemi başlatıldı")
    
    def start_metric_collection(self) -> bool:
        """
        Metrik toplama döngüsünü başlatır
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        if self.metrics_thread is not None and self.metrics_thread.is_alive():
            logger.warning("Metrik toplama döngüsü zaten çalışıyor")
            return False
        
        self.metrics_thread_running = True
        self.metrics_thread = threading.Thread(
            target=self._metrics_collection_loop, 
            daemon=True,
            name="MetricsCollectionThread"
        )
        self.metrics_thread.start()
        
        logger.info("Metrik toplama döngüsü başlatıldı")
        return True
    
    def stop_metric_collection(self) -> None:
        """
        Metrik toplama döngüsünü durdurur
        """
        self.metrics_thread_running = False
        if self.metrics_thread and self.metrics_thread.is_alive():
            self.metrics_thread.join(timeout=2.0)
            logger.info("Metrik toplama döngüsü durduruldu")
    
    def _metrics_collection_loop(self) -> None:
        """
        Metrik toplama döngüsünün ana işlevi
        """
        try:
            while self.metrics_thread_running:
                try:
                    # Metrikleri topla
                    self.collect_system_metrics()
                    self.collect_module_metrics()
                    
                    # Metrik geçmişini güncelle
                    self._update_metric_history()
                    
                    # Metrik toplama zamanını güncelle
                    self.last_metric_collection = time.time()
                    
                    # Bir süre bekle
                    time.sleep(self.metric_collection_interval)
                    
                except Exception as e:
                    logger.error(f"Metrik toplama döngüsünde hata: {e}")
                    time.sleep(2.0)  # Hata durumunda daha kısa bir bekleme
                
        except Exception as e:
            logger.error(f"Metrik toplama döngüsü beklenmeyen şekilde sonlandı: {e}")
        finally:
            logger.info("Metrik toplama döngüsü durdu")
    
    def collect_system_metrics(self) -> Dict:
        """
        Sistem metriklerini toplar
        
        Returns:
            Dict: Toplanan sistem metrikleri
        """
        try:
            # CPU kullanımı
            self.system_metrics["cpu_usage"] = psutil.cpu_percent(interval=0.1)
            
            # Bellek kullanımı
            memory = psutil.virtual_memory()
            self.system_metrics["memory_usage"] = memory.percent
            
            # Disk kullanımı
            disk = psutil.disk_usage('/')
            self.system_metrics["disk_usage"] = disk.percent
            
            # Sistem sıcaklığı (Raspberry Pi'de çalışır)
            self.system_metrics["temperature"] = self._get_system_temperature()
            
            # Çalışma süresi
            if hasattr(self, 'start_time'):
                self.system_metrics["uptime"] = time.time() - self.start_time
            
            return self.system_metrics
            
        except Exception as e:
            logger.error(f"Sistem metrikleri toplanırken hata: {e}")
            return self.system_metrics
    
    def collect_module_metrics(self) -> Dict:
        """
        Modül metriklerini toplar
        
        Returns:
            Dict: Toplanan modül metrikleri
        """
        try:
            # OLED kontrolcü metrikleri
            if hasattr(self, 'oled_controller') and self.oled_controller is not None:
                if hasattr(self.oled_controller, 'get_metrics'):
                    self.module_metrics["oled_controller"] = self.oled_controller.get_metrics()
            
            # LED kontrolcü metrikleri
            if hasattr(self, 'led_controller') and self.led_controller is not None:
                if hasattr(self.led_controller, 'get_metrics'):
                    self.module_metrics["led_controller"] = self.led_controller.get_metrics()
            
            # Duygu motoru metrikleri
            if hasattr(self, 'emotion_engine') and self.emotion_engine is not None:
                if hasattr(self.emotion_engine, 'get_metrics'):
                    self.module_metrics["emotion_engine"] = self.emotion_engine.get_metrics()
            
            # Tema yöneticisi metrikleri
            if hasattr(self, 'theme_manager') and self.theme_manager is not None:
                if hasattr(self.theme_manager, 'get_metrics'):
                    self.module_metrics["theme_manager"] = self.theme_manager.get_metrics()
            
            # Animasyon motoru metrikleri
            if hasattr(self, 'animation_engine') and self.animation_engine is not None:
                if hasattr(self.animation_engine, 'get_metrics'):
                    self.module_metrics["animation_engine"] = self.animation_engine.get_metrics()
            
            # Dashboard server metrikleri
            if hasattr(self, 'dashboard_server') and self.dashboard_server is not None:
                if hasattr(self.dashboard_server, 'get_metrics'):
                    self.module_metrics["dashboard_server"] = self.dashboard_server.get_metrics()
            
            # Performans optimize edici metrikleri
            if hasattr(self, 'performance_optimizer') and self.performance_optimizer is not None:
                if hasattr(self.performance_optimizer, 'get_metrics'):
                    self.module_metrics["performance_optimizer"] = self.performance_optimizer.get_metrics()
            
            return self.module_metrics
            
        except Exception as e:
            logger.error(f"Modül metrikleri toplanırken hata: {e}")
            return self.module_metrics
    
    def _get_system_temperature(self) -> float:
        """
        Sistem sıcaklığını alır (Raspberry Pi'de çalışır)
        
        Returns:
            float: Derece Celsius cinsinden sistem sıcaklığı
        """
        try:
            if RPI_AVAILABLE:
                # Raspberry Pi için sıcaklık alma
                temp_file = '/sys/class/thermal/thermal_zone0/temp'
                if os.path.isfile(temp_file):
                    with open(temp_file, 'r') as f:
                        temp = float(f.read()) / 1000.0
                        return temp
            
            # Diğer sistemler için simülasyon sıcaklığı
            return 40.0  # Sabit 40 derece
            
        except Exception as e:
            logger.error(f"Sistem sıcaklığı alınırken hata: {e}")
            return 0.0
    
    def _update_metric_history(self) -> None:
        """
        Metrik geçmişini günceller
        """
        current_time = time.time()
        
        # Sistem metriklerini geçmişe ekle
        self.metric_history["system"].append({
            "timestamp": current_time,
            "cpu_usage": self.system_metrics["cpu_usage"],
            "memory_usage": self.system_metrics["memory_usage"],
            "disk_usage": self.system_metrics["disk_usage"],
            "temperature": self.system_metrics["temperature"]
        })
        
        # Performans metriklerini geçmişe ekle
        self.metric_history["performance"].append({
            "timestamp": current_time,
            "fps": self.performance_metrics["fps"],
            "frame_time": self.performance_metrics["frame_time"],
            "render_time": self.performance_metrics["render_time"],
            "logic_time": self.performance_metrics["logic_time"]
        })
        
        # API metriklerini geçmişe ekle
        self.metric_history["api"].append({
            "timestamp": current_time,
            "requests_per_second": self.api_metrics["requests_per_second"],
            "avg_response_time": self.api_metrics["avg_response_time"],
            "active_connections": self.api_metrics["active_connections"],
            "error_rate": self.api_metrics["error_rate"]
        })
        
        # Geçmiş uzunluğunu sınırla
        for key in self.metric_history:
            while len(self.metric_history[key]) > self.metric_history_max_length:
                self.metric_history[key].pop(0)
    
    def get_metrics(self) -> Dict:
        """
        Tüm metrikleri toplar ve döndürür
        
        Returns:
            Dict: Toplanan tüm metrikler
        """
        # Metrikleri güncelle (son toplama üzerinden belirli bir süre geçtiyse)
        current_time = time.time()
        if current_time - self.last_metric_collection > self.metric_collection_interval:
            self.collect_system_metrics()
            self.collect_module_metrics()
            self.last_metric_collection = current_time
        
        # Tüm metrikleri birleştir
        metrics = {
            "system": self.system_metrics,
            "modules": self.module_metrics,
            "performance": self.performance_metrics,
            "api": self.api_metrics,
            "plugin_state": self.state.value if hasattr(self, 'state') else "unknown",
            "timestamp": time.time()
        }
        
        return metrics
    
    def get_metric_history(self, metric_type: str = None, duration: int = None) -> Dict:
        """
        Metrik geçmişini döndürür
        
        Args:
            metric_type (str, optional): Metrik türü ('system', 'performance', 'api'). None ise tümü döndürülür.
            duration (int, optional): Saniye cinsinden süre limiti. None ise tüm geçmiş döndürülür.
            
        Returns:
            Dict: Metrik geçmişi
        """
        # Süre limiti kontrolü
        if duration is not None:
            now = time.time()
            start_time = now - duration
            
            if metric_type is None:
                # Tüm metrik türleri için süre filtresi uygula
                filtered_history = {}
                for key in self.metric_history:
                    filtered_history[key] = [
                        item for item in self.metric_history[key]
                        if item["timestamp"] >= start_time
                    ]
                return filtered_history
            elif metric_type in self.metric_history:
                # Belirli bir metrik türü için süre filtresi uygula
                return {
                    metric_type: [
                        item for item in self.metric_history[metric_type]
                        if item["timestamp"] >= start_time
                    ]
                }
        
        # Süre limiti yoksa veya geçersiz metrik türü
        if metric_type is None:
            return self.metric_history
        elif metric_type in self.metric_history:
            return {metric_type: self.metric_history[metric_type]}
            
        return {}
    
    def get_health_status(self) -> Dict:
        """
        Sistem sağlık durumu raporu oluşturur
        
        Returns:
            Dict: Sağlık durumu raporu
        """
        metrics = self.get_metrics()
        
        # Sağlık durumunu belirle
        health_status = {
            "status": "healthy",  # "healthy", "warning", "critical"
            "warnings": [],
            "critical_issues": [],
            "components": {}
        }
        
        # CPU kontrolü
        if metrics["system"]["cpu_usage"] > 90:
            health_status["critical_issues"].append("CPU kullanımı çok yüksek")
            health_status["status"] = "critical"
        elif metrics["system"]["cpu_usage"] > 75:
            health_status["warnings"].append("CPU kullanımı yüksek")
            health_status["status"] = "warning" if health_status["status"] != "critical" else "critical"
            
        # Bellek kontrolü
        if metrics["system"]["memory_usage"] > 90:
            health_status["critical_issues"].append("Bellek kullanımı çok yüksek")
            health_status["status"] = "critical"
        elif metrics["system"]["memory_usage"] > 75:
            health_status["warnings"].append("Bellek kullanımı yüksek")
            health_status["status"] = "warning" if health_status["status"] != "critical" else "critical"
            
        # Disk kontrolü
        if metrics["system"]["disk_usage"] > 95:
            health_status["critical_issues"].append("Disk kullanımı çok yüksek")
            health_status["status"] = "critical"
        elif metrics["system"]["disk_usage"] > 85:
            health_status["warnings"].append("Disk kullanımı yüksek")
            health_status["status"] = "warning" if health_status["status"] != "critical" else "critical"
            
        # Sıcaklık kontrolü
        if metrics["system"]["temperature"] > 80:
            health_status["critical_issues"].append("Sistem sıcaklığı çok yüksek")
            health_status["status"] = "critical"
        elif metrics["system"]["temperature"] > 70:
            health_status["warnings"].append("Sistem sıcaklığı yüksek")
            health_status["status"] = "warning" if health_status["status"] != "critical" else "critical"
            
        # Performans kontrolü
        if metrics["performance"]["fps"] < 15 and metrics["performance"]["fps"] > 0:
            health_status["warnings"].append("FPS düşük")
            health_status["status"] = "warning" if health_status["status"] != "critical" else "critical"
            
        # API kontrolü
        if metrics["api"]["error_rate"] > 0.1:  # %10'dan fazla hata oranı
            health_status["warnings"].append("API hata oranı yüksek")
            health_status["status"] = "warning" if health_status["status"] != "critical" else "critical"
            
        # Bileşen durumları
        component_status = {
            "oled_controller": "unknown",
            "led_controller": "unknown",
            "emotion_engine": "unknown",
            "theme_manager": "unknown",
            "animation_engine": "unknown",
            "dashboard_server": "unknown"
        }
        
        # Bileşenler için özel sağlık durumu kontrolleri burada yapılabilir
        
        health_status["components"] = component_status
        health_status["timestamp"] = time.time()
        
        return health_status
    
    def save_metrics_to_file(self, file_path: str) -> bool:
        """
        Metrikleri dosyaya kaydeder
        
        Args:
            file_path (str): Dosya yolu
            
        Returns:
            bool: Başarılı ise True, değilse False
        """
        try:
            metrics = {
                "current_metrics": self.get_metrics(),
                "history": self.metric_history
            }
            
            with open(file_path, 'w') as f:
                json.dump(metrics, f, indent=4)
                
            logger.info(f"Metrikler dosyaya kaydedildi: {file_path}")
            return True
            
        except Exception as e:
            logger.error(f"Metrikler dosyaya kaydedilirken hata: {e}")
            return False
    
    def update_performance_metrics(self, fps: float, frame_time: float, render_time: float, logic_time: float) -> None:
        """
        Performans metriklerini günceller
        
        Args:
            fps (float): FPS değeri
            frame_time (float): Bir kare için toplam süre (ms)
            render_time (float): Render süresi (ms)
            logic_time (float): Mantık işleme süresi (ms)
        """
        self.performance_metrics["fps"] = fps
        self.performance_metrics["frame_time"] = frame_time
        self.performance_metrics["render_time"] = render_time
        self.performance_metrics["logic_time"] = logic_time
    
    def update_api_metrics(self, requests_per_second: float, avg_response_time: float, 
                           active_connections: int, error_rate: float) -> None:
        """
        API metriklerini günceller
        
        Args:
            requests_per_second (float): Saniye başına istek sayısı
            avg_response_time (float): Ortalama yanıt süresi (ms)
            active_connections (int): Aktif bağlantı sayısı
            error_rate (float): Hata oranı (0.0-1.0)
        """
        self.api_metrics["requests_per_second"] = requests_per_second
        self.api_metrics["avg_response_time"] = avg_response_time
        self.api_metrics["active_connections"] = active_connections
        self.api_metrics["error_rate"] = error_rate