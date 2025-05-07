# platform_test.py dosyası oluşturalım
from pathlib import Path
import sys
import os

# Proje dizinini Python yoluna ekle
PROJECT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(str(PROJECT_DIR))

# Doğrudan hardware_defines modülünü import et
from include import hardware_defines

def test_platform():
    platform_type = hardware_defines.detect_platform()
    print(f"Tespit edilen platform: {platform_type}")
    
    if platform_type == "raspberry_pi":
        cpu_temp = hardware_defines.get_cpu_temperature()
        print(f"CPU sıcaklığı: {cpu_temp:.1f}°C")
    else:
        print("Bu platform Raspberry Pi değil, CPU sıcaklığı alınamıyor.")

if __name__ == "__main__":
    test_platform()