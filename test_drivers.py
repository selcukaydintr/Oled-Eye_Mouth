#!/usr/bin/env python3
"""
FACE1 Projesi için sürücü test betiği
Bu betik, donanım ve yazılım modüllerini test etmek için kullanılır.
"""

import os
import sys
import time
import argparse
import logging
from pathlib import Path
from typing import Dict

# Proje dizinini Python yoluna ekle
PROJECT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(str(PROJECT_DIR))

# Modülleri içe aktar
try:
    from include import hardware_defines
    from src.modules.oled_controller import OLEDController
    from src.modules.led_controller import LEDController
    from src.modules.theme_manager import ThemeManager
    from src.modules.io_manager import IOManager
    from src.modules.dashboard_server import DashboardServer
except ImportError as e:
    print(f"Hata: Gerekli modüller yüklenemedi: {e}")
    print("Lütfen 'pip install -r requirements.txt' komutunu çalıştırarak gerekli bağımlılıkları yükleyin.")
    sys.exit(1)

# Logging yapılandırması
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Varsayılan yapılandırma
DEFAULT_CONFIG = {
    "hardware": {
        "platform": "desktop",  # raspberry_pi, desktop, veya other
        "oled_displays": {
            "left_eye": {"i2c_address": "0x3C", "width": 128, "height": 64},
            "right_eye": {"i2c_address": "0x3D", "width": 128, "height": 64},
            "mouth": {"i2c_address": "0x3E", "width": 128, "height": 64}
        },
        "use_multiplexer": False,
        "led_strip": {
            "pin": 18,
            "count": 30,
            "brightness": 0.5
        }
    },
    "emotions": {
        "default_emotion": "neutral",
        "transition_speed": 0.5,
        "personality": {
            "baseline_emotions": {
                "happy": 0.7,
                "angry": 0.3
            }
        }
    },
    "animation": {
        "fps": 30,
        "blink_interval_min": 2.0,
        "blink_interval_max": 8.0,
        "idle_animations": True
    },
    "theme": {
        "default_theme": "default"
    },
    "io": {
        "websocket": {
            "host": "localhost",
            "port": 8765
        },
        "mqtt": {
            "enabled": False,
            "broker": "localhost",
            "port": 1883,
            "topic_prefix": "face1"
        },
        "auth": {
            "enabled": False,
            "api_tokens": ["test_token"]
        }
    },
    "dashboard": {
        "host": "localhost",
        "port": 8000,
        "debug": True
    }
}

def test_platform_info():
    """Platform bilgileri testi"""
    print("\n==== Platform Bilgileri Testi ====")
    
    try:
        platform_type = hardware_defines.detect_platform()
        print(f"Tespit edilen platform: {platform_type}")
        
        cpu_temp = None
        if platform_type == "raspberry_pi":
            cpu_temp = hardware_defines.get_cpu_temperature()
            print(f"CPU sıcaklığı: {cpu_temp:.1f}°C")
        else:
            print("Bu platform Raspberry Pi değil, CPU sıcaklığı alınamıyor.")
        
        print("Platform bilgileri başarıyla alındı.")
        return True
    
    except Exception as e:
        print(f"HATA: Platform bilgileri alınırken hata oluştu: {e}")
        return False

def test_i2c_scan():
    """I2C tarama testi"""
    print("\n==== I2C Tarama Testi ====")
    
    try:
        platform_type = hardware_defines.detect_platform()
        
        if platform_type != "raspberry_pi":
            print("UYARI: Bu platform Raspberry Pi değil. Simülasyon modunda I2C taraması yapılıyor.")
            
            # Simüle edilmiş I2C cihaz listesi
            devices = [0x3C, 0x3D, 0x3E, 0x70]
            print("Simüle edilmiş I2C cihazlar:")
            
        else:
            # Gerçek I2C taraması
            i2c = hardware_defines.get_platform_i2c()
            if i2c is None:
                print("HATA: I2C başlatılamadı.")
                return False
            
            print("I2C cihazları taranıyor...")
            devices = hardware_defines.scan_i2c_devices(i2c)
            print("Bulunan I2C cihazlar:")
        
        # Bulunan cihazları göster
        if devices:
            for device in devices:
                print(f"  0x{device:02X}")
        else:
            print("  Hiçbir I2C cihaz bulunamadı!")
        
        return len(devices) > 0
    
    except Exception as e:
        print(f"HATA: I2C taraması sırasında hata oluştu: {e}")
        return False

def test_led_controller():
    """LED kontrolcü testi"""
    print("\n==== LED Kontrolcü Testi ====")
    
    try:
        led_controller = LEDController(DEFAULT_CONFIG)
        
        if led_controller.start():
            print("LED kontrolcü başlatıldı")
            
            # Renk testi
            print("Renk testi yapılıyor...")
            colors = [
                (255, 0, 0),    # Kırmızı
                (0, 255, 0),    # Yeşil
                (0, 0, 255),    # Mavi
                (255, 255, 0),  # Sarı
                (0, 255, 255),  # Cyan
                (255, 0, 255),  # Magenta
                (255, 255, 255) # Beyaz
            ]
            
            for r, g, b in colors:
                color_name = "Kırmızı" if (r, g, b) == (255, 0, 0) else \
                            "Yeşil" if (r, g, b) == (0, 255, 0) else \
                            "Mavi" if (r, g, b) == (0, 0, 255) else \
                            "Sarı" if (r, g, b) == (255, 255, 0) else \
                            "Cyan" if (r, g, b) == (0, 255, 255) else \
                            "Magenta" if (r, g, b) == (255, 0, 255) else \
                            "Beyaz"
                
                print(f"  Renk: {color_name} ({r}, {g}, {b})")
                led_controller.set_color(r, g, b)
                time.sleep(1)
            
            # Duygu renk testi
            print("Duygu renkleri testi yapılıyor...")
            for emotion in ["happy", "sad", "angry", "surprised", "calm"]:
                print(f"  Duygu: {emotion}")
                led_controller.set_emotion_color(emotion)
                time.sleep(1)
            
            # Parlaklık testi
            print("Parlaklık testi yapılıyor...")
            for brightness in [0.2, 0.5, 0.8, 1.0]:
                print(f"  Parlaklık: {brightness}")
                led_controller.set_brightness(brightness)
                time.sleep(1)
            
            # LEDleri temizle ve kontrolcüyü durdur
            led_controller.clear()
            led_controller.stop()
            print("LED kontrolcü durduruldu.")
            
            return True
        else:
            print("HATA: LED kontrolcü başlatılamadı.")
            return False
    
    except Exception as e:
        print(f"HATA: LED kontrolcü testi sırasında hata oluştu: {e}")
        return False

def test_oled_controller():
    """OLED kontrolcü testi"""
    print("\n==== OLED Kontrolcü Testi ====")
    
    try:
        oled_controller = OLEDController(DEFAULT_CONFIG)
        
        if oled_controller.start():
            print("OLED kontrolcü başlatıldı.")
            
            # Ekranları temizle
            oled_controller.clear_displays()
            print("Tüm ekranlar temizlendi.")
            time.sleep(1)
            
            # Duygu gösterimlerini test et
            print("Duygu gösterimleri test ediliyor...")
            
            emotions = ["happy", "sad", "angry", "surprised", "neutral", "calm"]
            for emotion in emotions:
                print(f"  {emotion}")
                oled_controller.draw_eyes(emotion, True)  # gözler açık
                oled_controller.draw_mouth(emotion)
                oled_controller.update_display()
                time.sleep(2)
            
            # Göz kırpma testi
            print("Göz kırpma testi...")
            for _ in range(3):
                oled_controller.draw_eyes("happy", False)  # gözler kapalı
                oled_controller.update_display()
                time.sleep(0.2)
                oled_controller.draw_eyes("happy", True)  # gözler açık
                oled_controller.update_display()
                time.sleep(0.5)
            
            # Ekranları temizle ve kontrolcüyü durdur
            oled_controller.clear_displays()
            oled_controller.stop()
            print("OLED kontrolcü durduruldu.")
            
            return True
        else:
            print("HATA: OLED kontrolcü başlatılamadı.")
            return False
    
    except Exception as e:
        print(f"HATA: OLED kontrolcü testi sırasında hata oluştu: {e}")
        return False

def test_theme_manager():
    """Tema yöneticisi testi"""
    print("\n==== Tema Yöneticisi Testi ====")
    
    try:
        theme_manager = ThemeManager(DEFAULT_CONFIG)
        
        if theme_manager.start():
            print("Tema yöneticisi başlatıldı.")
            
            # Mevcut temaları listele
            themes = theme_manager.get_theme_list()
            print(f"Mevcut temalar: {themes}")
            
            # Her temayı yükle ve kontrol et
            for theme_name in themes:
                print(f"  Tema yükleniyor: {theme_name}")
                if theme_manager.set_theme(theme_name):
                    # Her duygu için tema varlıklarını kontrol et
                    for emotion in ["happy", "sad", "angry"]:
                        assets = theme_manager.get_emotion_assets(emotion)
                        print(f"    {emotion} duygusu varlıkları:")
                        print(f"      Göz stili: {assets['eyes'].get('style', 'yok')}")
                        print(f"      Ağız stili: {assets['mouth'].get('style', 'yok')}")
                        print(f"      LED rengi: {assets['led'].get('color', 'yok')}")
                else:
                    print(f"    HATA: {theme_name} teması yüklenemedi.")
            
            # Tema yöneticisini durdur
            theme_manager.stop()
            print("Tema yöneticisi durduruldu.")
            
            return True
        else:
            print("HATA: Tema yöneticisi başlatılamadı.")
            return False
    
    except Exception as e:
        print(f"HATA: Tema yöneticisi testi sırasında hata oluştu: {e}")
        return False

def test_io_manager():
    """I/O yöneticisi testi"""
    print("\n==== I/O Yöneticisi Testi ====")
    
    try:
        io_manager = IOManager(DEFAULT_CONFIG)
        
        # Test komut işleyicisi
        def handle_test_command(data):
            print(f"  Test komutu çalıştırıldı: {data}")
            return {"status": "success", "message": "Test komutu işlendi"}
        
        # Test olay geri çağrısı
        def on_test_event(data):
            print(f"  Test olayı alındı: {data}")
        
        # Komut işleyici ve olay geri çağrısı kaydı
        io_manager.register_command_handler("test", handle_test_command)
        io_manager.register_callback("test_event", on_test_event)
        
        if io_manager.start():
            print(f"I/O yöneticisi başlatıldı. WebSocket sunucusu: {io_manager.ws_host}:{io_manager.ws_port}")
            
            # Test olayını gönder
            print("Test olayı gönderiliyor...")
            io_manager.send_event("test_event", {"message": "Bu bir test mesajıdır", "timestamp": time.time()})
            
            # Geri çağrı testinin çalışması için bekle
            time.sleep(2)
            
            # Geri çağrı kaydını sil
            io_manager.unregister_callback("test_event", on_test_event)
            print("Test olay geri çağrısı kaydı silindi.")
            
            # Komut işleyici kaydını sil
            io_manager.unregister_command_handler("test")
            print("Test komut işleyicisi kaydı silindi.")
            
            # I/O yöneticisini durdur
            io_manager.stop()
            print("I/O yöneticisi durduruldu.")
            
            return True
        else:
            print("HATA: I/O yöneticisi başlatılamadı.")
            return False
    
    except Exception as e:
        print(f"HATA: I/O yöneticisi testi sırasında hata oluştu: {e}")
        return False

def test_dashboard_server():
    """Dashboard sunucusu testi"""
    print("\n==== Dashboard Sunucusu Testi ====")
    
    try:
        dashboard_server = DashboardServer(DEFAULT_CONFIG)
        
        if dashboard_server.start():
            print(f"Dashboard sunucusu başlatıldı: http://{dashboard_server.host}:{dashboard_server.port}")
            
            # Şablon dosyalarını kontrol et
            templates_dir = os.path.join(PROJECT_DIR, "web", "templates")
            print(f"Şablon dizini: {templates_dir}")
            
            if os.path.exists(templates_dir):
                template_files = os.listdir(templates_dir)
                print(f"Şablon dosyaları: {template_files}")
            
            # Statik dosyaları kontrol et
            static_dir = os.path.join(PROJECT_DIR, "web", "static")
            print(f"Statik dosya dizini: {static_dir}")
            
            if os.path.exists(static_dir):
                css_dir = os.path.join(static_dir, "css")
                js_dir = os.path.join(static_dir, "js")
                
                if os.path.exists(css_dir):
                    css_files = os.listdir(css_dir)
                    print(f"CSS dosyaları: {css_files}")
                
                if os.path.exists(js_dir):
                    js_files = os.listdir(js_dir)
                    print(f"JavaScript dosyaları: {js_files}")
            
            # Sistem istatistiklerini al
            stats = dashboard_server.get_system_stats()
            print("Sistem İstatistikleri:")
            print(f"  CPU Kullanımı: {stats['cpu']['percent']:.1f}%")
            print(f"  Bellek Kullanımı: {stats['memory']['percent']:.1f}%")
            print(f"  Disk Kullanımı: {stats['disk']['percent']:.1f}%")
            
            # Dashboard sunucuyu durdur
            time.sleep(2)
            dashboard_server.stop()
            print("Dashboard sunucusu durduruldu.")
            
            return True
        else:
            print("HATA: Dashboard sunucusu başlatılamadı.")
            return False
    
    except Exception as e:
        print(f"HATA: Dashboard sunucusu testi sırasında hata oluştu: {e}")
        return False

def main():
    """Ana fonksiyon"""
    parser = argparse.ArgumentParser(description='FACE1 sürücü test betiği')
    parser.add_argument('--all', action='store_true', help='Tüm testleri çalıştır')
    parser.add_argument('--platform', action='store_true', help='Platform bilgileri testini çalıştır')
    parser.add_argument('--i2c', action='store_true', help='I2C tarama testini çalıştır')
    parser.add_argument('--led', action='store_true', help='LED kontrolcü testini çalıştır')
    parser.add_argument('--oled', action='store_true', help='OLED kontrolcü testini çalıştır')
    parser.add_argument('--theme', action='store_true', help='Tema yöneticisi testini çalıştır')
    parser.add_argument('--io', action='store_true', help='I/O yöneticisi testini çalıştır')
    parser.add_argument('--dashboard', action='store_true', help='Dashboard sunucusu testini çalıştır')
    
    args = parser.parse_args()
    
    # Eğer hiçbir argüman verilmezse, --all kullan
    if not any(vars(args).values()):
        args.all = True
    
    print("FACE1 Sürücü Test Betiği")
    print("========================")
    print(f"Tarih: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    results = {}
    
    # Platform testi
    if args.all or args.platform:
        results["Platform Bilgileri"] = test_platform_info()
    
    # I2C testi
    if args.all or args.i2c:
        results["I2C Tarama"] = test_i2c_scan()
    
    # LED kontrolcü testi
    if args.all or args.led:
        results["LED Kontrolcü"] = test_led_controller()
    
    # OLED kontrolcü testi
    if args.all or args.oled:
        results["OLED Kontrolcü"] = test_oled_controller()
    
    # Tema yöneticisi testi
    if args.all or args.theme:
        results["Tema Yöneticisi"] = test_theme_manager()
    
    # I/O yöneticisi testi
    if args.all or args.io:
        results["I/O Yöneticisi"] = test_io_manager()
    
    # Dashboard sunucusu testi
    if args.all or args.dashboard:
        results["Dashboard Sunucusu"] = test_dashboard_server()
    
    # Sonuçları göster
    print("\n==== Test Sonuçları ====")
    
    for test_name, test_result in results.items():
        status = "BAŞARILI" if test_result else "BAŞARISIZ"
        print(f"{test_name}: {status}")
    
    # Genel sonuç
    if all(results.values()):
        print("\nTÜM TESTLER BAŞARILI!")
        return 0
    else:
        print("\nBAZI TESTLER BAŞARISIZ!")
        return 1

if __name__ == "__main__":
    sys.exit(main())