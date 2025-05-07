#!/usr/bin/env python3
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

# Dosyaların varlığını kontrol et
print("Web panel dosyaları kontrol ediliyor...")

# Templates dizinini kontrol et
templates_dir = os.path.join(PROJECT_DIR, "web", "templates")
print(f"Şablon dizini: {templates_dir}")
if os.path.exists(templates_dir):
    templates = os.listdir(templates_dir)
    print(f"Bulunan şablonlar: {templates}")

# Static dosya dizinini kontrol et
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

# Dashboard modüllerini kontrol et
dashboard_modules = []
for item in os.listdir(MODULES_DIR):
    if item.startswith("dashboard_") and item.endswith(".py"):
        dashboard_modules.append(item)

print(f"Dashboard modülleri: {dashboard_modules}")

print("\nÖzet:")
print(f"- Şablon dizini mevcut: {'Evet' if os.path.exists(templates_dir) else 'Hayır'}")
print(f"- Statik dosya dizini mevcut: {'Evet' if os.path.exists(static_dir) else 'Hayır'}")
print(f"- CSS dizini mevcut: {'Evet' if os.path.exists(css_dir) else 'Hayır'}")
print(f"- JS dizini mevcut: {'Evet' if os.path.exists(js_dir) else 'Hayır'}")
print(f"- Dashboard modül sayısı: {len(dashboard_modules)}")

# Main bloğu ekle
print("\nWeb panel test edildi.")
print("Not: Web paneli başlatmak için aşağıdaki komutları kullanabilirsiniz:")
print("  1. Dashboard sunucusu: python src/modules/dashboard_server.py")
print("  2. WebSocket sunucusu: python src/modules/dashboard_websocket.py")
print("  3. Tüm proje: python src/face_plugin.py")

# Eksik modüllerin listesini kontrol et
required_modules = ["dashboard_stats.py", "dashboard_templates.py", "dashboard_routes.py", "dashboard_websocket.py"]
missing_modules = [module for module in required_modules if module not in dashboard_modules]
if missing_modules:
    print(f"\nUyarı: Bazı gerekli dashboard modülleri eksik: {missing_modules}")
    print("Bu modüller olmadan web panel düzgün çalışmayabilir.")

