#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: create_venv.py
# Açıklama: Python sanal ortamını oluşturur ve gerekli paketleri yükler
# 
# Versiyon: 0.1.0
# Değişiklikler:
# - [0.1.0] Sanal ortam oluşturma betiği oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-04-28
===========================================================
"""

import os
import sys
import subprocess
import platform
import shutil
import argparse
from pathlib import Path

# Proje dizini
PROJECT_DIR = Path(__file__).parent.absolute()


def check_python_version():
    """
    Python sürümünü kontrol eder
    """
    required_version = (3, 9)
    current_version = sys.version_info[:2]
    
    if current_version < required_version:
        print(f"Hata: Python {required_version[0]}.{required_version[1]} veya üstü gerekli.")
        print(f"Mevcut Python sürümü: {current_version[0]}.{current_version[1]}")
        return False
    
    return True


def create_virtual_environment(force=False):
    """
    Python sanal ortamını oluşturur
    
    Args:
        force (bool): Eğer True ise, mevcut sanal ortamı siler ve yeniden oluşturur
    
    Returns:
        bool: İşlem başarılı ise True, değilse False
    """
    venv_path = PROJECT_DIR / "venv"
    
    # Mevcut sanal ortamı kontrol et
    if venv_path.exists():
        if force:
            print(f"Mevcut sanal ortam siliniyor: {venv_path}")
            try:
                shutil.rmtree(venv_path)
            except Exception as e:
                print(f"Hata: Sanal ortam silinemedi: {e}")
                return False
        else:
            print(f"Sanal ortam zaten mevcut: {venv_path}")
            print("Yeniden oluşturmak için --force parametresini kullanın.")
            return True
    
    # Sanal ortam oluştur
    print(f"Python sanal ortamı oluşturuluyor: {venv_path}")
    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Hata: Sanal ortam oluşturulamadı: {e}")
        return False
    
    print("Sanal ortam başarıyla oluşturuldu.")
    return True


def install_requirements():
    """
    Gerekli paketleri sanal ortama yükler
    
    Returns:
        bool: İşlem başarılı ise True, değilse False
    """
    venv_path = PROJECT_DIR / "venv"
    requirements_path = PROJECT_DIR / "requirements.txt"
    
    # requirements.txt dosyasını kontrol et
    if not requirements_path.exists():
        print(f"Hata: {requirements_path} dosyası bulunamadı.")
        print("requirements.txt dosyasını oluşturun ve tekrar deneyin.")
        return False
    
    # Platforma göre pip yolunu belirle
    if platform.system() == "Windows":
        pip_path = venv_path / "Scripts" / "pip"
    else:
        pip_path = venv_path / "bin" / "pip"
    
    # pip'i güncelle
    print("pip güncelleniyor...")
    try:
        if platform.system() == "Windows":
            subprocess.run([str(pip_path), "install", "--upgrade", "pip"], check=True)
        else:
            activate_path = venv_path / "bin" / "activate"
            cmd = f"source {activate_path} && pip install --upgrade pip"
            subprocess.run(cmd, shell=True, check=True, executable="/bin/bash")
    except subprocess.CalledProcessError as e:
        print(f"Uyarı: pip güncellenemedi: {e}")
    
    # Gereksinimleri yükle
    print(f"Gerekli paketler yükleniyor ({requirements_path})...")
    try:
        if platform.system() == "Windows":
            subprocess.run([str(pip_path), "install", "-r", str(requirements_path)], check=True)
        else:
            activate_path = venv_path / "bin" / "activate"
            cmd = f"source {activate_path} && pip install -r {requirements_path}"
            subprocess.run(cmd, shell=True, check=True, executable="/bin/bash")
    except subprocess.CalledProcessError as e:
        print(f"Hata: Paketler yüklenemedi: {e}")
        return False
    
    print("Tüm paketler başarıyla yüklendi.")
    return True


def check_rpi_specific_packages():
    """
    Raspberry Pi'ye özgü paketlerin kullanılabilirliğini kontrol eder
    """
    try:
        import platform
        if platform.machine() in ["armv7l", "aarch64"]:
            print("Raspberry Pi platformu algılandı.")
            
            # RPi.GPIO veya gpiozero paketlerinin kullanılabilirliğini kontrol et
            try:
                import RPi.GPIO
                print("RPi.GPIO paketi kurulu.")
            except ImportError:
                print("Uyarı: RPi.GPIO paketi kurulu değil. GPIO işlevselliği sınırlı olacaktır.")
            
            try:
                import gpiozero
                print("gpiozero paketi kurulu.")
            except ImportError:
                print("Uyarı: gpiozero paketi kurulu değil. GPIO işlevselliği sınırlı olacaktır.")
            
            # I2C araçlarının kurulu olup olmadığını kontrol et
            try:
                result = subprocess.run(["which", "i2cdetect"], capture_output=True, text=True)
                if result.returncode == 0:
                    print("I2C araçları kurulu.")
                else:
                    print("Uyarı: I2C araçları kurulu değil. I2C aygıtları algılanamayacak.")
                    print("I2C araçlarını kurmak için: sudo apt-get install i2c-tools")
            except Exception:
                print("I2C araçlarının kurulumu kontrol edilemedi.")
    except Exception as e:
        print(f"Raspberry Pi spesifik paketler kontrol edilirken hata: {e}")


def main():
    """
    Ana fonksiyon
    """
    parser = argparse.ArgumentParser(description="Python sanal ortamı oluşturma aracı")
    parser.add_argument("--force", action="store_true", help="Mevcut sanal ortamı sil ve yeniden oluştur")
    parser.add_argument("--check-only", action="store_true", help="Sadece gereksinimleri kontrol et, kurulum yapma")
    args = parser.parse_args()
    
    print("FACE1 Yüz Eklentisi - Sanal Ortam Kurulumu")
    print("=" * 50)
    
    # Python sürümünü kontrol et
    if not check_python_version():
        sys.exit(1)
    
    if args.check_only:
        print("Sadece kontrol modu.")
        print(f"Python sürümü: {sys.version}")
        check_rpi_specific_packages()
        sys.exit(0)
    
    # Sanal ortamı oluştur
    if not create_virtual_environment(force=args.force):
        sys.exit(1)
    
    # Gereksinimleri yükle
    if not install_requirements():
        sys.exit(1)
    
    # Raspberry Pi spesifik paketleri kontrol et
    check_rpi_specific_packages()
    
    print("\nKurulum tamamlandı! Yüz eklentisini çalıştırmak için:")
    print("  ./run_face.sh")
    
    # Çalıştırma iznini kontrol et
    run_script = PROJECT_DIR / "run_face.sh"
    if run_script.exists() and not os.access(run_script, os.X_OK):
        print("\nÇalıştırma izinleri ayarlanıyor...")
        try:
            run_script.chmod(0o755)
            print(f"{run_script} için çalıştırma izni verildi.")
        except Exception as e:
            print(f"Uyarı: Çalıştırma izni verilemedi: {e}")
            print("Çalıştırma iznini manuel olarak ayarlamanız gerekebilir:")
            print("  chmod +x run_face.sh")


if __name__ == "__main__":
    main()