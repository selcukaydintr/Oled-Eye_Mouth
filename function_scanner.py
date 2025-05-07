#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FACE1 Projesi Fonksiyon Tarayıcı
--------------------------------

Bu betik, FACE1 projesi içindeki tüm Python dosyalarını tarayarak fonksiyonları çıkarır ve
bir markdown dosyasına kaydeder.

Çıktı formatı:
- Fonksiyon adı
- Bulunduğu dosya
- Versiyon bilgisi (varsa)
- Değiştirilme tarihi (git log kullanarak)
- İşlevi ve amacı (docstring'den çıkarılır)

Kullanım:
    python function_scanner.py

Oluşturulan dosya:
    function_list.md
"""

import os
import re
import ast
import subprocess
from datetime import datetime
import logging

# Loglama ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("function_scanner")

# Proje kök dizini
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Çıktı dosyası
OUTPUT_FILE = os.path.join(PROJECT_ROOT, "function_list.md")

# Taranacak dizinler
SCAN_DIRS = [
    os.path.join(PROJECT_ROOT, "src"),
    os.path.join(PROJECT_ROOT, "include"),
    os.path.join(PROJECT_ROOT, "utils"),
]

# İstisna klasörler (taranmayacak)
EXCLUDE_DIRS = [
    "__pycache__",
    "venv",
    ".git",
]

# İstisna dosyalar (taranmayacak)
EXCLUDE_FILES = [
    "__init__.py",
]


def get_git_last_modified_date(file_path):
    """Git log kullanarak bir dosyanın son değiştirilme tarihini alır."""
    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%ad", "--date=short", "--", file_path],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.stdout.strip():
            return result.stdout.strip()
    except (subprocess.SubprocessError, FileNotFoundError):
        pass
    
    # Git bilgisi alınamazsa dosya değiştirilme tarihini kullan
    try:
        mtime = os.path.getmtime(file_path)
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    except (IOError, OSError):
        return "Bilinmiyor"


def extract_version_from_docstring(docstring):
    """Docstring içinden versiyon bilgisini çıkarır."""
    if not docstring:
        return "Belirtilmemiş"
    
    # Versiyon desenlerini ara
    version_patterns = [
        r"Versiyon\s*:\s*([0-9]+\.[0-9]+\.[0-9]+)",
        r"Version\s*:\s*([0-9]+\.[0-9]+\.[0-9]+)",
        r"v([0-9]+\.[0-9]+\.[0-9]+)",
    ]
    
    for pattern in version_patterns:
        match = re.search(pattern, docstring, re.IGNORECASE)
        if match:
            return match.group(1)
    
    # Değişiklik kayıtlarını kontrol et
    changelog_patterns = [
        r"\[([0-9]+\.[0-9]+\.[0-9]+)\]",
    ]
    
    for pattern in changelog_patterns:
        match = re.search(pattern, docstring, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return "Belirtilmemiş"


def extract_purpose_from_docstring(docstring):
    """Docstring içinden fonksiyonun amacını çıkarır."""
    if not docstring:
        return "Belirtilmemiş"
    
    # Docstring'i temizle ve ilk cümleyi veya paragrafı al
    lines = docstring.split("\n")
    clean_lines = [line.strip() for line in lines if line.strip()]
    
    if not clean_lines:
        return "Belirtilmemiş"
    
    # İlk anlamlı satırı al
    purpose = clean_lines[0]
    
    # Bazı temizleme işlemleri
    purpose = purpose.replace('"""', '').replace("'''", '').strip()
    
    # Maksimum 100 karakter
    if len(purpose) > 100:
        purpose = purpose[:97] + "..."
    
    return purpose


def parse_python_file(file_path):
    """Python dosyasını ayrıştırarak fonksiyonları ve sınıfları çıkarır."""
    functions = []
    
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # AST (Abstract Syntax Tree) ile dosyayı ayrıştır
        try:
            tree = ast.parse(content)
        except SyntaxError as e:
            logger.error(f"Söz dizimi hatası: {file_path} - {e}")
            return []
        
        # Dosyanın son değiştirilme tarihini al
        last_modified = get_git_last_modified_date(file_path)
        
        # Dosya yolunu göreceli hale getir
        rel_path = os.path.relpath(file_path, PROJECT_ROOT)
        
        # Modül düzeyindeki fonksiyonları işle
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Fonksiyon bilgilerini çıkar
                name = node.name
                docstring = ast.get_docstring(node) or ""
                version = extract_version_from_docstring(docstring)
                purpose = extract_purpose_from_docstring(docstring)
                
                # Sonuçları ekle
                functions.append({
                    "name": name,
                    "file_path": rel_path,
                    "version": version,
                    "modified_date": last_modified,
                    "purpose": purpose,
                    "type": "function"
                })
            
            # Sınıfları ve metotları işle
            elif isinstance(node, ast.ClassDef):
                class_name = node.name
                class_docstring = ast.get_docstring(node) or ""
                
                # Sınıfın kendisini ekle
                functions.append({
                    "name": class_name,
                    "file_path": rel_path,
                    "version": extract_version_from_docstring(class_docstring),
                    "modified_date": last_modified,
                    "purpose": extract_purpose_from_docstring(class_docstring),
                    "type": "class"
                })
                
                # Sınıfın metotlarını işle
                for class_node in node.body:
                    if isinstance(class_node, ast.FunctionDef):
                        method_name = class_node.name
                        method_docstring = ast.get_docstring(class_node) or ""
                        
                        functions.append({
                            "name": f"{class_name}.{method_name}",
                            "file_path": rel_path,
                            "version": extract_version_from_docstring(method_docstring),
                            "modified_date": last_modified,
                            "purpose": extract_purpose_from_docstring(method_docstring),
                            "type": "method"
                        })
        
        return functions
    
    except Exception as e:
        logger.error(f"Dosya işlenirken hata: {file_path} - {e}")
        return []


def generate_markdown(functions):
    """Fonksiyon listesinden markdown çıktısı oluşturur"""
    markdown = "# FACE1 Projesi Fonksiyon Listesi\n\n"
    markdown += "Bu liste, FACE1 projesi içindeki tüm fonksiyon ve sınıfları içerir.\n\n"
    markdown += "Oluşturulma Tarihi: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n"
    markdown += "| Fonksiyon | Bulunduğu Dosya | Versiyon | Değiştirme Tarihi | İşlevi ve Amacı |\n"
    markdown += "|-----------|----------------|----------|-------------------|----------------|\n"
    
    # Fonksiyonları dosya yoluna göre gruplandır
    functions_by_file = {}
    for func in functions:
        if func["file_path"] not in functions_by_file:
            functions_by_file[func["file_path"]] = []
        functions_by_file[func["file_path"]].append(func)
    
    # Her dosya için fonksiyonları sırala ve ekle
    for file_path in sorted(functions_by_file.keys()):
        for func in sorted(functions_by_file[file_path], key=lambda x: x["name"]):
            name_with_prefix = func["name"]
            if func["type"] == "class":
                name_with_prefix = f"🔶 {name_with_prefix}"  # Sınıflar için emoji
            elif func["type"] == "method":
                name_with_prefix = f"↪ {name_with_prefix}"   # Metotlar için emoji
            
            markdown += f"| `{name_with_prefix}` | {func['file_path']} | {func['version']} | {func['modified_date']} | {func['purpose']} |\n"
    
    return markdown


def scan_directory(directory):
    """Belirtilen dizini ve alt dizinlerini tarayarak Python dosyalarını bulur."""
    all_functions = []
    
    for root, dirs, files in os.walk(directory):
        # İstisna klasörleri atla
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        for file in files:
            # Sadece Python dosyalarını al ve istisnaları atla
            if file.endswith(".py") and file not in EXCLUDE_FILES:
                file_path = os.path.join(root, file)
                logger.info(f"İşleniyor: {file_path}")
                functions = parse_python_file(file_path)
                all_functions.extend(functions)
    
    return all_functions


def main():
    """Ana fonksiyon."""
    logger.info("FACE1 Fonksiyon Tarayıcı başlatılıyor...")
    
    all_functions = []
    
    # Belirtilen dizinleri tara
    for directory in SCAN_DIRS:
        if os.path.exists(directory):
            logger.info(f"Dizin taranıyor: {directory}")
            functions = scan_directory(directory)
            all_functions.extend(functions)
        else:
            logger.warning(f"Dizin bulunamadı: {directory}")
    
    # Kök dizindeki Python dosyalarını tara
    root_py_files = [f for f in os.listdir(PROJECT_ROOT) 
                     if f.endswith(".py") and f not in EXCLUDE_FILES]
    
    for file in root_py_files:
        file_path = os.path.join(PROJECT_ROOT, file)
        logger.info(f"İşleniyor: {file_path}")
        functions = parse_python_file(file_path)
        all_functions.extend(functions)
    
    # Toplam sayıyı günlüğe kaydet
    logger.info(f"Toplam {len(all_functions)} fonksiyon/metot bulundu")
    
    # Markdown oluştur ve dosyaya kaydet
    markdown = generate_markdown(all_functions)
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(markdown)
    
    logger.info(f"Fonksiyon listesi oluşturuldu: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()