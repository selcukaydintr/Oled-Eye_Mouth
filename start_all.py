import subprocess
import sys
import os
import time
import json
import psutil

# Projenin kök dizinini ekle
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT_DIR, "src")
STATUS_FILE = os.path.join(ROOT_DIR, "face_plugin_status.json")

def start_process(command, name):
    try:
        print(f"{name} başlatılıyor...")
        env = os.environ.copy()
        env["PYTHONPATH"] = f"{SRC_DIR}:{env.get('PYTHONPATH', '')}"
        return subprocess.Popen(command, shell=True, env=env)
    except Exception as e:
        print(f"{name} başlatılamadı: {e}")
        return None

def wait_for_status_file(timeout=30):
    """Durum dosyasının oluşturulmasını ve yüz eklentisinin çalışır duruma gelmesini bekler"""
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        if os.path.exists(STATUS_FILE):
            try:
                with open(STATUS_FILE, 'r') as f:
                    status_data = json.load(f)
                    if status_data.get('status') == 'running':
                        print(f"Yüz eklentisi çalışır durumda tespit edildi")
                        return True
            except Exception:
                pass
        
        # Kısa bir süre bekle ve tekrar kontrol et
        time.sleep(0.5)
    
    print("Yüz eklentisinin çalışır duruma gelmesi zaman aşımına uğradı")
    return False

def cleanup_old_processes():
    """Eski çalışan süreçleri temizle"""
    try:
        # Python ile çalışan tüm face_plugin.py ve dashboard_server.py süreçlerini sonlandır
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                cmdline = ' '.join(proc.cmdline())
                if 'python' in cmdline and ('face_plugin.py' in cmdline or 
                                         'dashboard_server.py' in cmdline or
                                         'dashboard_websocket.py' in cmdline):
                    print(f"Eski süreç sonlandırılıyor (PID: {proc.pid}): {cmdline}")
                    proc.terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
                
        # Biraz bekle ve eski süreçlerin kapanmasına izin ver
        time.sleep(1)
    except Exception as e:
        print(f"Eski süreçler temizlenirken hata: {e}")

if __name__ == "__main__":
    # Önce herhangi bir eski çalışan süreci temizle
    cleanup_old_processes()
    
    # Eğer durum dosyası zaten varsa sil
    if os.path.exists(STATUS_FILE):
        os.remove(STATUS_FILE)
    
    # Önce Face Plugin'i başlat
    face_plugin_process = start_process("python src/face_plugin.py", "FACE1 Ana Plugin")
    
    # Durum dosyasının oluşturulmasını ve pluginin çalışır duruma gelmesini bekle
    if wait_for_status_file(timeout=10):
        # Ardından diğer sunucuları başlat
        dashboard_process = start_process("python src/modules/dashboard_server.py --port 8000", "Dashboard Sunucusu")
        websocket_process = start_process("python src/modules/dashboard_websocket.py --port 8001", "WebSocket Sunucusu")
        
        print("Tüm bileşenler başlatıldı.")
        print("Web panel: http://localhost:8000")
        print("WebSocket: ws://localhost:8001")
    else:
        print("UYARI: Yüz eklentisi başlatılamadı, diğer bileşenler çalışmayabilir")