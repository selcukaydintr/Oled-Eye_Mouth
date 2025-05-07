#!/usr/bin/env python3
"""
Simülasyon görüntüleri oluşturmak için test script
"""

import os
import time
import random
from pathlib import Path
from PIL import Image, ImageDraw

# Proje dizinini belirle
PROJECT_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
SIMULATION_DIR = Path(os.path.join(PROJECT_DIR, "simulation"))

# Simulation klasörünü oluştur
SIMULATION_DIR.mkdir(exist_ok=True)

def create_simulation_image(image_type, index):
    """Simülasyon görüntüsü oluşturur"""
    timestamp = int(time.time())
    
    if image_type == "left_eye":
        width, height = 128, 64
        filename = f"display_left_eye_{timestamp}_{index:04d}.png"
        bg_color = (0, 0, 0)
        shape_color = (0, 0, 255)  # Mavi
    elif image_type == "right_eye":
        width, height = 128, 64
        filename = f"display_right_eye_{timestamp}_{index:04d}.png"
        bg_color = (0, 0, 0)
        shape_color = (0, 0, 255)  # Mavi
    elif image_type == "mouth":
        width, height = 128, 32
        filename = f"display_mouth_{timestamp}_{index:04d}.png"
        bg_color = (0, 0, 0)
        shape_color = (255, 255, 255)  # Beyaz
    elif image_type == "leds":
        width, height = 300, 30
        filename = f"leds_{timestamp}_{index:04d}.png"
        bg_color = (0, 0, 0)
        
        # LED renklerini oluştur
        image = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(image)
        
        led_count = 10
        led_radius = 10
        spacing = 5
        start_x = (width - (led_count * (led_radius * 2 + spacing))) // 2
        
        for i in range(led_count):
            x = start_x + i * (led_radius * 2 + spacing)
            y = height // 2
            
            # Her LED için rastgele renk
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            
            draw.ellipse(
                (x - led_radius, y - led_radius, x + led_radius, y + led_radius),
                fill=(r, g, b)
            )
        
        filepath = os.path.join(SIMULATION_DIR, filename)
        image.save(filepath)
        return filepath
    
    # Diğer görüntü tipleri için
    image = Image.new('RGB', (width, height), bg_color)
    draw = ImageDraw.Draw(image)
    
    if image_type == "left_eye" or image_type == "right_eye":
        # Gözler için dairesel bir iris çiz
        center_x, center_y = width // 2, height // 2
        
        # Rastgele göz pozisyonu
        offset_x = random.randint(-10, 10)
        offset_y = random.randint(-5, 5)
        
        # İris çiz
        draw.ellipse(
            (center_x - 15 + offset_x, center_y - 15 + offset_y, 
             center_x + 15 + offset_x, center_y + 15 + offset_y),
            fill=shape_color
        )
        
        # Göz bebeği çiz
        draw.ellipse(
            (center_x - 5 + offset_x, center_y - 5 + offset_y, 
             center_x + 5 + offset_x, center_y + 5 + offset_y),
            fill=(0, 0, 0)
        )
    
    elif image_type == "mouth":
        # Ağız için basit bir çizgi
        
        # Rastgele ağız ifadesi seç
        expression = random.choice(["smile", "neutral", "sad"])
        
        if expression == "smile":
            # Gülümseyen ağız
            draw.arc(
                (width // 4, -height // 2, width * 3 // 4, height),
                180, 0, 
                fill=shape_color, 
                width=2
            )
        elif expression == "sad":
            # Üzgün ağız
            draw.arc(
                (width // 4, height // 2, width * 3 // 4, height * 2),
                0, 180, 
                fill=shape_color, 
                width=2
            )
        else:
            # Nötr ağız
            draw.line(
                (width // 4, height // 2, width * 3 // 4, height // 2),
                fill=shape_color,
                width=2
            )
    
    filepath = os.path.join(SIMULATION_DIR, filename)
    image.save(filepath)
    return filepath

print("Simülasyon görüntüleri oluşturuluyor...")

for i in range(10):
    # Her görüntü tipinden örnek oluştur
    left_eye_path = create_simulation_image("left_eye", i)
    right_eye_path = create_simulation_image("right_eye", i)
    mouth_path = create_simulation_image("mouth", i)
    leds_path = create_simulation_image("leds", i)
    
    # İlerlemeyi göster
    print(f"Görüntü seti {i+1}/10 oluşturuldu.")
    
    # Kısa bir bekleme ekle
    time.sleep(0.5)

print(f"\nSimülasyon görüntüleri oluşturuldu: {SIMULATION_DIR}")
print("Dashboard'da 'Simülasyon Akışını Başlat' düğmesine tıklayarak görüntüleri görebilirsiniz.")