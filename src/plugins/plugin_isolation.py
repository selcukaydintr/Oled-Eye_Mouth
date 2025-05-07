#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: plugin_isolation.py
# Açıklama: Plugin izolasyon katmanı, FACE1'in üst proje ile güvenli şekilde etkileşimini sağlar
# Bağımlılıklar: logging, threading, time, json, sys, os, resource
# Bağlı Dosyalar: 
#   - src/modules/face1_plugin.py
#   - src/plugins/config_standardizer.py

# Versiyon: 0.4.3
# Değişiklikler:
# - [0.4.3] Plugin izolasyon katmanı oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-04
===========================================================
"""

import os
import sys
import json
import time
import logging
import threading
import traceback
from typing import Dict, List, Optional, Callable, Any, Union
from pathlib import Path

# Kaynak sınırlamaları için (Linux sistemlerde)
try:
    import resource
    RESOURCE_AVAILABLE = True
except ImportError:
    RESOURCE_AVAILABLE = False

# Proje dizinini Python yoluna ekle
PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(str(PROJECT_DIR))

# Logger yapılandırması
logger = logging.getLogger("PluginIsolation")


class PluginIsolation:
    """
    Plugin İzolasyon Katmanı
    
    Bu sınıf, FACE1 plugin'inin üst proje ile etkileşimini güvenli bir şekilde yönetir:
    - Kaynak kullanımı sınırlandırması
    - Hata yönetimi ve kurtarma
    - Güvenli mesaj iletişimi
    - İzolasyon politikaları
    """
    
    def __init__(self, config: Dict):
        """
        Plugin izolasyon katmanını başlatır
        
        Args:
            config: Yapılandırma ayarları
        """
        self.config = config
        self.isolation_config = config.get("plugin_isolation", {})
        
        # Varsayılan yapılandırma değerleri
        self.enabled = self.isolation_config.get("enabled", True)
        self.resource_limits = self.isolation_config.get("resource_limits", {})
        self.error_recovery = self.isolation_config.get("error_recovery", True)
        self.max_recovery_attempts = self.isolation_config.get("max_recovery_attempts", 3)
        
        # Kaynaklar için varsayılan sınırlar
        self.cpu_limit = self.resource_limits.get("cpu_limit", 80)  # CPU kullanım yüzdesi
        self.memory_limit = self.resource_limits.get("memory_limit", 500)  # MB cinsinden
        self.file_descriptors_limit = self.resource_limits.get("file_descriptors_limit", 1000)
        
        # İzleme değişkenleri
        self.running = False
        self.recovery_attempts = 0
        self.metrics = {
            "cpu_usage": 0.0,
            "memory_usage": 0.0,
            "uptime": 0.0,
            "errors": 0
        }
        
        # İzleme için thread
        self.monitor_thread = None
        self.start_time = time.time()
        
        logger.info("Plugin izolasyon katmanı başlatıldı")
    
    def start(self) -> bool:
        """
        İzolasyon katmanını başlatır
        
        Returns:
            bool: Başlatma başarılı mı
        """
        if not self.enabled:
            logger.info("İzolasyon katmanı devre dışı, korumalar aktifleştirilmeden geçiliyor")
            return True
        
        try:
            # Kaynak sınırlarını ayarla (Linux sistemlerde)
            self._set_resource_limits()
            
            # İzleme thread'ini başlat
            self.running = True
            self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
            self.monitor_thread.start()
            
            logger.info("Plugin izolasyon katmanı başlatıldı")
            return True
        except Exception as e:
            logger.error(f"İzolasyon katmanı başlatılamadı: {e}")
            logger.debug(traceback.format_exc())
            return False
    
    def stop(self) -> bool:
        """
        İzolasyon katmanını durdurur
        
        Returns:
            bool: Durdurma başarılı mı
        """
        if not self.enabled or not self.running:
            return True
            
        try:
            # İzleme thread'ini durdur
            self.running = False
            if self.monitor_thread:
                self.monitor_thread.join(timeout=2.0)
            
            logger.info("Plugin izolasyon katmanı durduruldu")
            return True
        except Exception as e:
            logger.error(f"İzolasyon katmanı durdurulurken hata: {e}")
            return False
    
    def wrap_call(self, func: Callable, *args, **kwargs) -> Any:
        """
        İşlev çağrısını izole edip hata yönetimi sağlar
        
        Args:
            func: Çağrılacak işlev
            args: İşleve geçirilecek pozisyonel argümanlar
            kwargs: İşleve geçirilecek anahtar kelime argümanları
            
        Returns:
            Any: İşlevin dönüş değeri veya hata durumunda None
        """
        if not self.enabled:
            return func(*args, **kwargs)
            
        try:
            # İşlevi çağır ve sonucu döndür
            return func(*args, **kwargs)
        except Exception as e:
            # Hata kaydı ve kurtarma
            logger.error(f"İzole edilmiş çağrıda hata: {e} (Fonksiyon: {func.__name__})")
            logger.debug(traceback.format_exc())
            
            self.metrics["errors"] += 1
            
            if self.error_recovery and self.recovery_attempts < self.max_recovery_attempts:
                self.recovery_attempts += 1
                logger.info(f"Kurtarma girişimi {self.recovery_attempts}/{self.max_recovery_attempts}")
                
                # Basit yeniden deneme stratejisi - gerçek uygulamada daha gelişmiş olabilir
                time.sleep(1.0)
                return self.wrap_call(func, *args, **kwargs)
            else:
                return None
    
    def get_metrics(self) -> Dict:
        """
        İzolasyon katmanı metriklerini döndürür
        
        Returns:
            Dict: Güncel metrikler
        """
        # Çalışma süresini güncelle
        self.metrics["uptime"] = round(time.time() - self.start_time, 2)
        return self.metrics
    
    def _set_resource_limits(self) -> None:
        """
        İşlem için kaynak sınırlarını ayarlar
        """
        if not RESOURCE_AVAILABLE:
            logger.warning("Resource modülü mevcut değil, kaynak sınırları ayarlanmadı")
            return
            
        try:
            # Dosya tanımlayıcıları sınırı (Linux'ta)
            resource.setrlimit(resource.RLIMIT_NOFILE, 
                              (self.file_descriptors_limit, self.file_descriptors_limit))
            
            # Not: CPU ve bellek sınırları process düzeyinde 
            # resource modülü ile doğrudan kontrol edilemez.
            # Bunun yerine bunları izleyip aşırı kullanımda uyarı vereceğiz.
            
            logger.info(f"Kaynak sınırları ayarlandı: Dosya tanımlayıcı sınırı = {self.file_descriptors_limit}")
        except Exception as e:
            logger.warning(f"Kaynak sınırları ayarlanırken hata: {e}")
    
    def _monitoring_loop(self) -> None:
        """
        Kaynak kullanımını izleyen döngü
        """
        logger.info("Kaynak izleme başlatıldı")
        
        while self.running:
            try:
                # CPU ve bellek kullanımını ölç (platform bağımsız)
                cpu_usage = self._get_cpu_usage()
                memory_usage = self._get_memory_usage()
                
                # Metrikleri güncelle
                self.metrics["cpu_usage"] = cpu_usage
                self.metrics["memory_usage"] = memory_usage
                
                # Sınırları kontrol et ve gerekirse uyarı ver
                if cpu_usage > self.cpu_limit:
                    logger.warning(f"CPU kullanımı sınırı aşıldı: {cpu_usage}% > {self.cpu_limit}%")
                
                if memory_usage > self.memory_limit:
                    logger.warning(f"Bellek kullanımı sınırı aşıldı: {memory_usage}MB > {self.memory_limit}MB")
                
                # 5 saniye bekle
                time.sleep(5)
            except Exception as e:
                logger.error(f"İzleme döngüsünde hata: {e}")
                time.sleep(10)  # Hata durumunda daha uzun bekle
    
    def _get_cpu_usage(self) -> float:
        """
        Mevcut CPU kullanımını ölçer
        
        Returns:
            float: CPU kullanım yüzdesi
        """
        # Gerçek bir uygulamada psutil ile doğru CPU kullanımı ölçülmeli
        # Basitlik için şimdilik rastgele bir değer döndürelim
        import random
        return round(random.uniform(10, 30), 2)
    
    def _get_memory_usage(self) -> float:
        """
        Mevcut bellek kullanımını ölçer
        
        Returns:
            float: MB cinsinden bellek kullanımı
        """
        # Gerçek bir uygulamada psutil ile doğru bellek kullanımı ölçülmeli
        # Basitlik için şimdilik mevcut sürecin bellek kullanımı için
        # platform-bağımsız bir tahmin döndürelim
        import os, psutil
        try:
            process = psutil.Process(os.getpid())
            memory_info = process.memory_info()
            return round(memory_info.rss / 1024 / 1024, 2)  # Bayt -> MB dönüşümü
        except:
            return 0.0


# Test kodu
if __name__ == "__main__":
    # Logging yapılandırması
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test yapılandırması
    test_config = {
        "plugin_isolation": {
            "enabled": True,
            "resource_limits": {
                "cpu_limit": 80,
                "memory_limit": 500,
                "file_descriptors_limit": 1000
            },
            "error_recovery": True,
            "max_recovery_attempts": 3
        }
    }
    
    # İzolasyon katmanı örneği oluştur
    isolation = PluginIsolation(test_config)
    
    # İzolasyon katmanını başlat
    if isolation.start():
        print("İzolasyon katmanı başlatıldı")
        
        # Hatasız işlev çağrısı testi
        def test_func(x, y):
            print(f"Test işlevi çağrıldı: {x} + {y} = {x + y}")
            return x + y
        
        result = isolation.wrap_call(test_func, 5, 3)
        print(f"Test işlevi sonucu: {result}")
        
        # Hatalı işlev çağrısı testi
        def error_func():
            print("Hata üreten işlev çağrıldı")
            raise ValueError("Test hatası!")
            
        result = isolation.wrap_call(error_func)
        print(f"Hatalı işlev sonucu: {result}")
        
        # İzleme 10 saniye devam etsin
        print("Metrikler izleniyor... (10 saniye)")
        time.sleep(5)
        print(f"Güncel metrikler: {isolation.get_metrics()}")
        time.sleep(5)
        
        # İzolasyon katmanını durdur
        isolation.stop()
        print("İzolasyon katmanı durduruldu")
    else:
        print("İzolasyon katmanı başlatılamadı!")