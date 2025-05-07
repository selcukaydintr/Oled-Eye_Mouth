#!/bin/bash

# =========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: run_face.sh
# Açıklama: Yüz eklentisini çalıştırmak için betik
# 
# Versiyon: 0.1.0
# Değişiklikler:
# - [0.1.0] Çalıştırma betiği oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-04-28
# =========================================================

# Proje dizinini belirle
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

# Logları saklamak için dizin oluştur
mkdir -p logs

# Python sanal ortamını kontrol et ve aktifleştir
if [ -d "venv" ]; then
    echo "Sanal ortam bulundu, aktifleştiriliyor..."
    source venv/bin/activate
else
    echo "Sanal ortam bulunamadı, oluşturuluyor..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Gerekli paketler yükleniyor..."
    pip install -r requirements.txt
fi

# Eklentiyi başlat
echo "Yüz eklentisi başlatılıyor..."
python src/face_plugin.py

# Çıkış durumunu kontrol et
EXIT_CODE=$?
if [ $EXIT_CODE -ne 0 ]; then
    echo "Hata: Yüz eklentisi $EXIT_CODE çıkış koduyla sonlandı."
    echo "Hata detayları için logs/face_plugin.log dosyasını kontrol edin."
    exit $EXIT_CODE
fi

# Sanal ortamı deaktifleştir
deactivate
