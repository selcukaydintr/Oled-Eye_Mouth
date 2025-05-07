#!/bin/bash

# Dashboard başlatma scripti
# FACE1 projesi için web arayüzü

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

# Renkli çıktı için
GREEN="\033[0;32m"
YELLOW="\033[1;33m"
RED="\033[0;31m"
NC="\033[0m" # No Color

echo -e "${GREEN}FACE1 Dashboard başlatılıyor...${NC}"

# Sanal ortam kontrolü
if [ -d "venv" ]; then
    echo -e "${YELLOW}Sanal ortam bulundu, aktifleştiriliyor...${NC}"
    source venv/bin/activate
else
    echo -e "${RED}Sanal ortam bulunamadı. Lütfen önce 'python -m venv venv' ile sanal ortam oluşturun.${NC}"
    exit 1
fi

# Gerekli paketlerin kontrolü
REQUIRED_PACKAGES="flask flask-cors dash plotly pandas"
pip install $REQUIRED_PACKAGES > /dev/null

# Log dizini kontrolü
if [ ! -d "logs" ]; then
    echo "Log dizini oluşturuluyor..."
    mkdir -p logs
fi

echo -e "${GREEN}Dashboard başlatılıyor...${NC}"
echo -e "${YELLOW}Dashboard adresine tarayıcıdan erişebilirsiniz: http://localhost:8050${NC}"

# Dashboard'u başlat
python src/modules/dashboard_server.py

# Eğer çıkış yapıldıysa
echo -e "${YELLOW}Dashboard kapatıldı.${NC}"
deactivate