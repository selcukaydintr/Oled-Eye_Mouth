#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: hardware_defines.py
# Açıklama: Donanım sabitleri ve yardımcı fonksiyonlar
# Bağımlılıklar: smbus2, os, platform, board, busio
# Bağlı Dosyalar: modules/oled_controller.py, modules/led_controller.py

# Versiyon: 0.1.0
# Değişiklikler:
# - [0.1.0] Temel donanım tanımları oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-04-28
===========================================================
"""

import os
import sys
import platform
import logging
import board
import busio
import adafruit_tca9548a
from typing import Optional, Union, Tuple, Any

# Raspberry Pi platformu için smbus2 yüklemeyi dene
try:
    from smbus2 import SMBus
    SMBUS_AVAILABLE = True
except ImportError:
    SMBUS_AVAILABLE = False
    # SMBus tip tanımlaması için bir yer tutucu oluştur
    class SMBus:
        """SMBus modülü import edilemediğinde tip kontrolü için yer tutucu sınıf"""
        pass

# Eğer RPi.GPIO mevcut değilse, çalıştığımız sistem muhtemelen Raspberry Pi değil
try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False

# Logger yapılandırması
logger = logging.getLogger(__name__)

# Platform tespitinin yapılıp yapılmadığını takip etmek için
_platform_logged = False

# Ekran sabitleri
DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
I2C_FREQUENCY = 400000  # 400 kHz

# Varsayılan I2C adresleri
DEFAULT_LEFT_EYE_ADDR = 0x3C
DEFAULT_RIGHT_EYE_ADDR = 0x3D
DEFAULT_MOUTH_ADDR = 0x3E

# TCA9548A I2C çoğaltıcı adresi
TCA9548A_ADDRESS = 0x70

# LED strip sabitleri
DEFAULT_LED_PIN = 18
DEFAULT_LED_COUNT = 30
DEFAULT_LED_BRIGHTNESS = 0.5

def detect_platform() -> str:
    """
    Çalışılan platformu tespit eder
    
    Returns:
        str: Platform tipi (raspberry_pi, desktop, veya other)
    """
    global _platform_logged
    try:
        # Platform bilgilerini al
        system = platform.system().lower()
        machine = platform.machine().lower()
        
        if system == "linux":
            # Raspberry Pi kontrolü
            if "arm" in machine or "aarch64" in machine:
                try:
                    with open('/proc/cpuinfo', 'r') as f:
                        cpuinfo = f.read()
                    if any(name in cpuinfo.lower() for name in ["raspberry", "bcm"]):
                        if not _platform_logged:
                            logger.info("Raspberry Pi platformu tespit edildi: " + get_raspberry_pi_model())
                            _platform_logged = True
                        return "raspberry_pi"
                except:
                    pass
            
            # Simülasyon modunu zorlamak için bu değişkeni kontrol et
            if os.environ.get('FORCE_SIMULATION_MODE') == '1':
                if not _platform_logged:
                    logger.info("Zorunlu simülasyon modu aktif")
                    _platform_logged = True
                return "desktop"
                
            # Desktop Linux
            if not _platform_logged:
                logger.info("Desktop Linux platformu tespit edildi")
                _platform_logged = True
            return "desktop"
        
        elif system == "darwin":
            if not _platform_logged:
                logger.info("macOS platformu tespit edildi")
                _platform_logged = True
            return "desktop"
        
        elif system == "windows":
            if not _platform_logged:
                logger.info("Windows platformu tespit edildi")
                _platform_logged = True
            return "desktop"
        
        else:
            if not _platform_logged:
                logger.info("Bilinmeyen platform: " + system)
                _platform_logged = True
            return "other"
            
    except Exception as e:
        logger.error(f"Platform tespiti sırasında hata: {e}")
        return "other"

def get_raspberry_pi_model() -> str:
    """
    Raspberry Pi modelini tespit eder
    
    Returns:
        str: Raspberry Pi model bilgisi
    """
    try:
        with open('/proc/cpuinfo', 'r') as f:
            cpuinfo = f.read()
        
        # Model bilgisini ara
        model_line = [line for line in cpuinfo.split('\n') if 'Model' in line]
        if model_line:
            return model_line[0].split(': ')[1]
        return "Raspberry Pi (Model bilinmiyor)"
    except:
        return "Raspberry Pi (Model bilgisi okunamadı)"

def init_i2c(bus_number: int = 1) -> Optional[SMBus]:
    """
    I2C veri yolunu başlatır
    
    Args:
        bus_number (int): I2C veri yolu numarası (genelde 1)
    
    Returns:
        SMBus: SMBus nesnesi veya başarısız olursa None
    """
    if not SMBUS_AVAILABLE:
        logger.warning("smbus2 modülü yüklü değil. I2C başlatılamadı.")
        return None
    
    try:
        logger.info(f"I2C veri yolu başlatılıyor: {bus_number}")
        i2c_bus = SMBus(bus_number)
        return i2c_bus
    except Exception as e:
        logger.error(f"I2C veri yolu başlatılırken hata: {e}")
        return None

def init_gpio() -> bool:
    """
    GPIO pinlerini başlatır
    
    Returns:
        bool: Başarılı ise True, değilse False
    """
    if not GPIO_AVAILABLE:
        logger.warning("RPi.GPIO modülü yüklü değil. GPIO başlatılamadı.")
        return False
    
    try:
        logger.info("GPIO başlatılıyor...")
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        return True
    except Exception as e:
        logger.error(f"GPIO başlatılırken hata: {e}")
        return False

def init_i2c_multiplexer(i2c: busio.I2C) -> Optional[adafruit_tca9548a.TCA9548A]:
    """
    TCA9548A I2C çoğaltıcısını başlatır
    
    Args:
        i2c (busio.I2C): I2C veri yolu nesnesi
    
    Returns:
        adafruit_tca9548a.TCA9548A: TCA9548A nesnesi veya başarısız olursa None
    """
    try:
        logger.info(f"TCA9548A I2C çoğaltıcı başlatılıyor: 0x{TCA9548A_ADDRESS:02X}")
        multiplexer = adafruit_tca9548a.TCA9548A(i2c, address=TCA9548A_ADDRESS)
        return multiplexer
    except Exception as e:
        logger.error(f"TCA9548A I2C çoğaltıcı başlatılırken hata: {e}")
        return None

def get_cpu_temperature() -> float:
    """
    CPU sıcaklığını okur (sadece Raspberry Pi için çalışır)
    
    Returns:
        float: CPU sıcaklığı (Celsius) veya başarısız olursa -1.0
    """
    try:
        if os.path.exists('/sys/class/thermal/thermal_zone0/temp'):
            with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
                temp = float(f.read()) / 1000.0
                return temp
        else:
            logger.warning("CPU sıcaklık dosyası bulunamadı")
            return -1.0
    except Exception as e:
        logger.error(f"CPU sıcaklığı okunurken hata: {e}")
        return -1.0

def scan_i2c_devices(i2c: Union[SMBus, busio.I2C]) -> list:
    """
    I2C veri yolundaki cihazları tarar
    
    Args:
        i2c (Union[SMBus, busio.I2C]): I2C veri yolu nesnesi
    
    Returns:
        list: Tespit edilen I2C cihazlarının adresleri
    """
    devices = []
    
    # SMBus nesnesi için
    if isinstance(i2c, SMBus):
        try:
            logger.info("I2C cihazları taranıyor...")
            for addr in range(0x03, 0x78):
                try:
                    i2c.read_byte(addr)
                    devices.append(addr)
                except:
                    pass
        except Exception as e:
            logger.error(f"I2C cihazları tararken hata: {e}")
    
    # busio.I2C nesnesi için
    else:
        try:
            devices = [addr for addr in i2c.scan()]
        except Exception as e:
            logger.error(f"I2C cihazları tararken hata: {e}")
    
    for addr in devices:
        logger.info(f"I2C cihazı tespit edildi: 0x{addr:02X}")
    
    return devices

def cleanup() -> None:
    """
    Donanım kaynaklarını serbest bırakır
    """
    if GPIO_AVAILABLE:
        try:
            GPIO.cleanup()
            logger.info("GPIO kaynakları temizlendi")
        except:
            pass

def get_platform_i2c() -> Optional[busio.I2C]:
    """
    Platform için uygun I2C nesnesini döndürür
    
    Returns:
        busio.I2C: I2C nesnesi veya başarısız olursa None
    """
    try:
        i2c = busio.I2C(board.SCL, board.SDA, frequency=I2C_FREQUENCY)
        logger.info("Platform I2C başlatıldı")
        return i2c
    except Exception as e:
        logger.error(f"Platform I2C başlatılırken hata: {e}")
        return None

def get_platform_info() -> dict:
    """
    Platform hakkında detaylı bilgi sağlar
    
    Returns:
        dict: Platform bilgileri içeren sözlük
    """
    info = {
        "system": platform.system(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "is_raspberry_pi": False,
        "raspberry_pi_model": "",
        "is_raspberry_pi_5": False
    }
    
    # Raspberry Pi tespiti
    if info["system"] == "Linux":
        try:
            with open('/proc/cpuinfo', 'r') as f:
                cpuinfo = f.read()
            
            # Revision değeri var mı?
            if 'Revision' in cpuinfo:
                model_name = ""
                revision = ""
                
                for line in cpuinfo.split('\n'):
                    if line.startswith('Model'):
                        model_name = line.split(':')[1].strip()
                    elif line.startswith('Revision'):
                        revision = line.split(':')[1].strip()
                
                if 'Raspberry Pi' in model_name:
                    info["is_raspberry_pi"] = True
                    info["raspberry_pi_model"] = model_name
                    
                    # Raspberry Pi 5 tespiti
                    if '5' in model_name:
                        info["is_raspberry_pi_5"] = True
        except:
            pass
    
    return info

# Main işlevi - test amaçlı
if __name__ == "__main__":
    # Logging yapılandırması
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    print("FACE1 Donanım Tanımları Test")
    print("--------------------------")
    
    # Platform tespiti
    platform_type = detect_platform()
    print(f"Platform: {platform_type}")
    
    # I2C testi
    if platform_type == 'raspberry_pi':
        print("\nI2C Test:")
        i2c_bus = init_i2c()
        if i2c_bus:
            devices = scan_i2c_devices(i2c_bus)
            if devices:
                print(f"Tespit edilen I2C cihazları: {[hex(addr) for addr in devices]}")
            else:
                print("I2C cihazı tespit edilemedi")
            i2c_bus.close()
        
        # GPIO testi
        print("\nGPIO Test:")
        if init_gpio():
            print("GPIO başlatıldı")
        else:
            print("GPIO başlatılamadı")
        
        # CPU sıcaklık testi
        temp = get_cpu_temperature()
        if temp > 0:
            print(f"CPU Sıcaklığı: {temp:.1f}°C")
    else:
        print("\nUyarı: Bu platform Raspberry Pi değil. Donanım testleri atlanıyor.")
    
    print("\nTest tamamlandı.")