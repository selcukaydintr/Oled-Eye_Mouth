#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: dashboard_stats.py
# Açıklama: Dashboard için sistem istatistikleri modülü
# Bağımlılıklar: psutil
# Bağlı Dosyalar: dashboard_server.py

# Versiyon: 0.1.0
# Değişiklikler:
# - [0.1.0] dashboard_server.py dosyasından ayrıldı
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-02
===========================================================
"""

import os
import psutil
import logging
from typing import Dict

# Proje dizinini Python yoluna ekle
import sys
from pathlib import Path
PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.append(str(PROJECT_DIR))

from include import hardware_defines

# Logger yapılandırması
logger = logging.getLogger("DashboardStats")

def get_system_stats() -> Dict:
    """
    Sistem istatistiklerini alır
    
    Returns:
        Dict: Sistem istatistikleri
    """
    stats = {
        "cpu": {
            "percent": psutil.cpu_percent(interval=0.1),
            "count": psutil.cpu_count(),
            "frequency": psutil.cpu_freq().current if psutil.cpu_freq() else None
        },
        "memory": {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "percent": psutil.virtual_memory().percent
        },
        "disk": {
            "total": psutil.disk_usage('/').total,
            "used": psutil.disk_usage('/').used,
            "free": psutil.disk_usage('/').free,
            "percent": psutil.disk_usage('/').percent
        }
    }
    
    # Raspberry Pi platformunda CPU sıcaklığını al
    if hardware_defines.detect_platform() == "raspberry_pi":
        try:
            stats["cpu"]["temperature"] = hardware_defines.get_cpu_temperature()
        except Exception:
            pass
    
    return stats