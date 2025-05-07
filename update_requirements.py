#!/usr/bin/env python3
"""
FACE1 - requirements.txt Güncelleme Betiği
-------------------------------------------
Bu betik, projedeki Python dosyalarını tarar, kullanılan kütüphaneleri tespit eder
ve requirements.txt dosyasını otomatik olarak günceller.

Kullanım:
    python update_requirements.py [--dry-run]
    
Parametreler:
    --dry-run: Gerçek bir güncelleme yapmadan sadece değişiklikleri gösterir
"""

import os
import sys
import re
import subprocess
import importlib
import pkg_resources
from pathlib import Path
import argparse
from collections import defaultdict
import shutil

# Proje dizin yapısı
PROJECT_ROOT = Path(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
REQUIREMENTS_FILE = os.path.join(PROJECT_ROOT, "requirements.txt")
REQUIREMENTS_BACKUP = os.path.join(PROJECT_ROOT, "requirements.txt.bak")

# Yoksayılacak dizinler
IGNORE_DIRS = ['__pycache__', 'venv', '.git', '.vscode']

# Standart kütüphaneler listesi
STDLIB_MODULES = set(sys.builtin_module_names)
try:
    STDLIB_MODULES.update([m.name for m in list(pkg_resources.iter_distribution())
                        if m.key == 'python'])
except:
    pass

# Bazı yaygın standart kütüphaneler
COMMON_STDLIB = {
    'os', 'sys', 'time', 'datetime', 're', 'json', 'math', 'random',
    'traceback', 'logging', 'threading', 'multiprocessing', 'argparse',
    'collections', 'copy', 'functools', 'itertools', 'pathlib', 'shutil',
    'signal', 'socket', 'struct', 'subprocess', 'tempfile', 'typing'
}
STDLIB_MODULES.update(COMMON_STDLIB)

# Proje içi modüller (yoksayılacak)
PROJECT_MODULES = {
    'src', 'modules', 'include', 'plugins', 'dashboard_widgets', 'face',
    'hardware_defines', 'face_plugin', 'animation_engine', 'emotion_engine',
    'theme_manager', 'oled_controller', 'led_controller', 'performance_optimizer', 
    'sound_processor', 'state_history_manager'
}

# Kütüphane adı dönüşümleri (paket != import adı durumları)
PACKAGE_MAPPING = {
    'PIL': 'Pillow',
    'cv2': 'opencv-python',
    'sklearn': 'scikit-learn',
    'yaml': 'pyyaml',
    'RPi': 'RPi.GPIO',
    'lgpio': 'lgpio',
}

def find_python_files(directory):
    """Verilen dizindeki tüm Python dosyalarını bulur"""
    python_files = []
    
    for root, dirs, files in os.walk(directory):
        # Yoksayılacak dizinleri atla
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
                
    return python_files

def extract_imports(file_path):
    """Python dosyasındaki import ifadelerini analiz eder"""
    imports = set()
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            # İçe aktarma ifadelerini bul
            import_pattern = re.compile(r'^import\s+(\w+)(?:\.\w+)*|^from\s+(\w+)(?:\.\w+)*\s+import', re.MULTILINE)
            matches = import_pattern.findall(content)
            
            for match in matches:
                module_name = match[0] if match[0] else match[1]
                if module_name and module_name not in PROJECT_MODULES and module_name not in STDLIB_MODULES:
                    imports.add(module_name)
    except Exception as e:
        print(f"Uyarı: {file_path} dosyası işlenirken hata: {e}")
    
    return imports

def get_package_version(package_name):
    """Yüklü paket sürümünü alır"""
    mapped_name = PACKAGE_MAPPING.get(package_name, package_name)
    
    try:
        # pip komutunu çalıştırarak sürümü al
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', mapped_name],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            # Sürüm bilgisini regex ile çıkar
            version_match = re.search(r'Version: ([\d\.]+)', result.stdout)
            if version_match:
                return version_match.group(1)
    except Exception:
        pass
    
    # Alternatif yöntem: importlib kullanarak
    try:
        module = importlib.import_module(package_name)
        if hasattr(module, '__version__'):
            return module.__version__
        elif hasattr(module, 'version'):
            return module.version
        elif hasattr(module, 'VERSION'):
            return module.VERSION
    except (ImportError, AttributeError):
        pass
    
    return None

def parse_existing_requirements():
    """Mevcut requirements.txt dosyasını kategorilerine göre ayrıştırır"""
    categories = defaultdict(list)
    current_category = "general"  # Varsayılan kategori
    
    try:
        with open(REQUIREMENTS_FILE, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
            for line in lines:
                line = line.rstrip()
                
                # Kategori başlığı mı?
                if line.startswith('#') and (':' in line or '-' in line):
                    current_category = line
                    categories[current_category] = []
                    continue
                
                # Sıradan yorum satırı veya boş satır
                if line.startswith('#') or line.strip() == '':
                    categories[current_category].append(line)
                    continue
                
                # Paket gerekliliği
                categories[current_category].append(line)
    except FileNotFoundError:
        # Dosya yoksa boş bir kategori yapısı döndür
        categories["# FACE1 - Raspberry Pi Robot Yüz Eklentisi Bağımlılıkları"] = []
    
    return categories

def update_requirements(imports, dry_run=False):
    """Requirements.txt dosyasını günceller"""
    # Mevcut dosyayı kategorilerine göre ayrıştır
    categories = parse_existing_requirements()
    
    # Her kategorideki paketleri dictionary olarak tut (paket adı -> tam satır)
    packages_by_category = {}
    for category, lines in categories.items():
        packages = {}
        for line in lines:
            if not line.startswith('#') and line.strip():
                package_name = line.split('==')[0].strip() if '==' in line else line.strip()
                packages[package_name] = line
        packages_by_category[category] = packages
    
    # Alınan importları kategorilere yerleştir veya güncelle
    for module_name in imports:
        mapped_name = PACKAGE_MAPPING.get(module_name, module_name)
        version = get_package_version(module_name) or get_package_version(mapped_name)
        
        if not version:
            print(f"Uyarı: {module_name} için sürüm bilgisi bulunamadı, atlanıyor...")
            continue
        
        package_line = f"{mapped_name}=={version}"
        
        # Modülü uygun kategoriye yerleştir veya güncelle
        assigned = False
        for category, packages in packages_by_category.items():
            if mapped_name in packages:
                # Paket zaten bu kategoride, sürümünü güncelle
                old_line = packages[mapped_name]
                packages[mapped_name] = package_line
                assigned = True
                
                if dry_run and old_line != package_line:
                    print(f"DEĞİŞTİRİLECEK: {old_line} -> {package_line}")
                break
        
        # Eğer hiçbir kategoride yoksa, uygun bir kategori bul veya genele ekle
        if not assigned:
            if any(kwd in mapped_name.lower() for kwd in ['gpio', 'spi', 'i2c', 'serial', 'usb', 'ft', 'adafruit']):
                key = next((k for k in categories.keys() if 'donanım' in k.lower()), "# Donanım erişimi için kütüphaneler")
            elif any(kwd in mapped_name.lower() for kwd in ['image', 'pil', 'cv', 'numpy', 'plot']):
                key = next((k for k in categories.keys() if 'görüntü' in k.lower()), "# Görüntü işleme ve gösterimi için kütüphaneler")
            elif any(kwd in mapped_name.lower() for kwd in ['web', 'http', 'api', 'fast', 'uvicorn', 'flask', 'jinja', 'wsgi']):
                key = next((k for k in categories.keys() if 'web' in k.lower() or 'api' in k.lower()), "# Web arayüzü ve API için")
            else:
                key = "# Genel yardımcı kütüphaneler"
            
            # Paket kategorisi yoksa oluştur
            if key not in categories:
                categories[key] = []
                packages_by_category[key] = {}
            
            packages_by_category[key][mapped_name] = package_line
            
            if dry_run:
                print(f"EKLENECEK: {key} kategorisine {package_line}")
    
    if dry_run:
        return
    
    # Yedek al
    try:
        shutil.copy2(REQUIREMENTS_FILE, REQUIREMENTS_BACKUP)
        print(f"Yedek alındı: {REQUIREMENTS_BACKUP}")
    except FileNotFoundError:
        pass
    
    # Yeni requirements.txt dosyasını oluştur
    with open(REQUIREMENTS_FILE, 'w', encoding='utf-8') as file:
        for category, lines in categories.items():
            # Kategori başlığını yaz
            file.write(f"{category}\n")
            
            # Yorumları ve boş satırları olduğu gibi yaz
            comment_lines = [line for line in lines if line.startswith('#') or line.strip() == '']
            for line in comment_lines:
                file.write(f"{line}\n")
            
            # Paketleri sıralayarak yaz
            packages = packages_by_category.get(category, {})
            for package_name in sorted(packages.keys()):
                file.write(f"{packages[package_name]}\n")
            
            # Kategorileri boş satırla ayır
            file.write("\n")
    
    print(f"Requirements dosyası güncellendi: {REQUIREMENTS_FILE}")

def main():
    parser = argparse.ArgumentParser(description="FACE1 requirements.txt güncelleme aracı")
    parser.add_argument('--dry-run', action='store_true', help="Değişiklikleri göster ama uygulamadan çık")
    args = parser.parse_args()
    
    print("FACE1 - Requirements.txt Güncelleme Aracı")
    print("="*40)
    
    if args.dry_run:
        print("DRY RUN MODU: Değişiklikler dosyaya yazılmayacak")
    
    # Python dosyalarını bul
    python_files = find_python_files(PROJECT_ROOT)
    print(f"{len(python_files)} Python dosyası bulundu.")
    
    # İçe aktarmaları çıkar
    all_imports = set()
    for file in python_files:
        imports = extract_imports(file)
        all_imports.update(imports)
    
    print(f"{len(all_imports)} benzersiz import tespit edildi:")
    for imp in sorted(all_imports):
        print(f" - {imp}")
    
    # Requirements.txt dosyasını güncelle
    update_requirements(all_imports, dry_run=args.dry_run)
    
    if not args.dry_run:
        print("\nİşlem tamamlandı!")
        print(f"Dosya güncellendi: {REQUIREMENTS_FILE}")
    else:
        print("\nDRY RUN tamamlandı. Gerçek güncellemeler yapılmadı.")

if __name__ == "__main__":
    main()