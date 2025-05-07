#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: face_plugin.py
# Açıklama: Ana yüz eklentisi kontrolcüsü. Modüler mimariden gelen sınıfları kullanır.
# Bağımlılıklar: fastapi, uvicorn, logging, threading, time, json
# Bağlı Dosyalar: 
#   - modules/face1_plugin.py (yeni modüler yapı)

# Versiyon: 0.4.0
# Değişiklikler:
# - [0.4.0] FacePlugin modülerleştirildi, yeni modüler yapıya yönlendirildi
# - [0.3.3] Animasyon motoru entegrasyonu ve JSON formatı desteği eklendi
# - [0.3.2] Çevresel faktörlere tepki veren ifadeler eklendi
# - [0.3.1] Duygu geçişleri iyileştirildi
# - [0.3.0] Duygu alt tiplerinin görsel ifadeleri geliştirildi, tema yöneticisi entegrasyonu yapıldı
# - [0.2.0] Web arayüzü ve API eklendi
# - [0.1.0] Ana yüz eklentisi sınıfı oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-02
===========================================================
"""

import os
import sys
from pathlib import Path

# Bu dosya artık bir yönlendirici (redirector) olarak hizmet vermekte ve
# modülerleştirilmiş sınıfı içe aktararak kullanmaktadır.

# Proje dizinini Python yoluna ekle
PROJECT_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(str(PROJECT_DIR))

# Modülerleştirilmiş FacePlugin sınıfını içe aktar
from src.modules.face1_plugin import FacePlugin, main

# Ana fonksiyon çağrıldığında, modules/face1_plugin.py içindeki main fonksiyonu çalıştırılır
if __name__ == "__main__":
    main()
