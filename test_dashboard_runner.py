#!/usr/bin/env python3
"""
FACE1 Dashboard test betiği
"""

import os
import sys
from pathlib import Path

# Proje dizinini Python yoluna ekle
PROJECT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_DIR, "src")
MODULES_DIR = os.path.join(SRC_DIR, "modules")

sys.path.append(str(PROJECT_DIR))
sys.path.append(str(SRC_DIR))
sys.path.append(str(MODULES_DIR))

# Standart yapılandırma
DEFAULT_CONFIG = {
    "dashboard": {
        "host": "localhost",
        "port": 8000,
        "debug": True
    }
}

# Dashboard sunucu modülünü içe aktar ve çalıştır
try:
    from src.modules.dashboard_server import DashboardServer
    
    print("Dashboard sunucusu başlatılıyor...")
    dashboard = DashboardServer(DEFAULT_CONFIG)
    
    if dashboard.start():
        print(f"Dashboard sunucusu başarıyla başlatıldı: http://{dashboard.host}:{dashboard.port}")
        print("Dashboard sunucusu test modunda çalışıyor.")
        print("Çıkmak için Ctrl+C tuşlarına basın.")
        
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            dashboard.stop()
            print("\nDashboard sunucusu durduruldu.")
    else:
        print("Dashboard sunucusu başlatılamadı!")
        
except ImportError as e:
    print(f"Hata: Gerekli modüller yüklenemedi: {e}")
    print("İçe aktarma yolu:", sys.path)
    print("Mevcut modüller:", os.listdir(MODULES_DIR))
