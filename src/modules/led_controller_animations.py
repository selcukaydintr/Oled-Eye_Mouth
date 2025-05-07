#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: led_controller_animations.py
# Açıklama: LED şeridinde çalıştırılacak animasyon fonksiyonları ve animasyon işleme modülü.
# Bağımlılıklar: threading, math, random, time
# Bağlı Dosyalar: led_controller_base.py

# Versiyon: 0.4.0
# Değişiklikler:
# - [0.4.0] led_controller.py dosyasından bölündü (modüler mimari)
# - [0.2.0] Gelişmiş animasyon desenleri (scan, twinkle, wave) eklendi
# - [0.1.1] Temel animasyon modu geliştirildi
# - [0.1.0] Temel LED kontrolcü sınıfı oluşturuldu
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-02
===========================================================
"""

import time
import math
import random
import logging
import threading
from typing import Dict, List, Tuple, Optional, Union, Callable

from .led_controller_base import AnimationPattern, LEDControllerBase

# Logger yapılandırması
logger = logging.getLogger("LEDController")


class LEDControllerAnimations:
    """
    LED animasyonları için karışım (mixin) sınıfı
    
    Bu sınıf, LED kontrolcü için animasyon işlevlerini sağlar.
    LEDControllerBase sınıfını genişletir.
    """
    
    def _wheel(self, pos: int) -> Tuple[int, int, int]:
        """
        Renk tekerleği - 0-255 arası bir pozisyon değerini RGB rengine dönüştürür
        
        Args:
            pos (int): Pozisyon değeri (0-255)
            
        Returns:
            Tuple[int, int, int]: RGB renk değerleri
        """
        pos = pos % 256
        
        if pos < 85:
            return (255 - pos * 3, pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (0, 255 - pos * 3, pos * 3)
        else:
            pos -= 170
            return (pos * 3, 0, 255 - pos * 3)
    
    def animate(self, animation_type: Union[str, AnimationPattern], 
                color: Optional[Tuple[int, int, int]] = None,
                speed: int = 50, zone_name: str = "all") -> None:
        """
        Animasyon başlatır
        
        Args:
            animation_type (Union[str, AnimationPattern]): Animasyon türü
            color (Optional[Tuple[int, int, int]], optional): RGB renk değerleri. Varsayılan: None (beyaz)
            speed (int, optional): Animasyon hızı (ms). Varsayılan: 50
            zone_name (str, optional): Bölge adı. Varsayılan: "all"
        """
        # Bu fonksiyonu LEDControllerBase'den miras aldığımızdan, self değişkenlerini kontrol etmeliyiz
        if not hasattr(self, 'stop_animation'):
            logger.error("animate metodunun kullanılabilmesi için LEDControllerBase sınıfından türetilmiş olmalıdır")
            return
            
        # Daha önce çalışan bir animasyon varsa durdur
        self.stop_animation.set()
        if self.animation_thread:
            self.animation_thread.join(timeout=1.0)
        
        # Animasyon tipini kontrol et
        if isinstance(animation_type, str):
            try:
                animation_type = AnimationPattern(animation_type)
            except ValueError:
                logger.warning(f"Geçersiz animasyon tipi: {animation_type}, 'static' kullanılıyor")
                animation_type = AnimationPattern.STATIC
        
        # Bölgeyi kontrol et
        if zone_name not in self.zones:
            logger.warning(f"Geçersiz bölge adı: {zone_name}, 'all' kullanılıyor")
            zone_name = "all"
        
        # Rengi ayarla
        if color is None:
            color = (255, 255, 255)  # Varsayılan beyaz
        
        # Animasyon parametrelerini ayarla
        self.current_animation = animation_type
        self.animation_color = color
        self.animation_speed = max(10, speed)  # En az 10ms
        
        # Animasyon durumunu sıfırla
        self.stop_animation.clear()
        self.animation_running = True
        
        # Aktivite zamanlayıcısını sıfırla
        self.reset_activity_timer()
        
        # Animasyonu başlat
        self.animation_thread = threading.Thread(
            target=self._run_animation,
            args=(animation_type, color, self.animation_speed, zone_name)
        )
        self.animation_thread.daemon = True
        self.animation_thread.start()
        
        logger.info(f"Animasyon başlatıldı: {animation_type.value}, renk={color}, hız={speed}, bölge={zone_name}")
    
    def _run_animation(self, animation_type: AnimationPattern, 
                      color: Tuple[int, int, int], speed: int, zone_name: str) -> None:
        """
        Animasyon döngüsünü çalıştırır
        
        Args:
            animation_type (AnimationPattern): Animasyon türü
            color (Tuple[int, int, int]): RGB renk değerleri
            speed (int): Animasyon hızı (ms)
            zone_name (str): Bölge adı
        """
        zone = self.zones[zone_name]
        start = zone.start_index
        count = zone.count
        
        try:
            # Performans optimizasyonu: Animasyon fonksiyonlarını önbelleğe al
            if not hasattr(self, '_animation_func_cache'):
                self._animation_func_cache = {
                    AnimationPattern.STATIC: self._animate_static,
                    AnimationPattern.PULSE: self._animate_pulse,
                    AnimationPattern.BREATHE: self._animate_breathe,
                    AnimationPattern.FADE: self._animate_fade,
                    AnimationPattern.RAINBOW: self._animate_rainbow,
                    AnimationPattern.COLOR_WIPE: self._animate_color_wipe,
                    AnimationPattern.THEATER_CHASE: self._animate_theater_chase,
                    AnimationPattern.BOUNCE: self._animate_bounce,
                    AnimationPattern.FIRE: self._animate_fire,
                    AnimationPattern.SPARKLE: self._animate_sparkle
                }
            
            # Doğrudan eşleşen animasyon fonksiyonunu al
            animation_func = self._animation_func_cache.get(animation_type)
            
            if animation_func:
                # Performans optimizasyonu: Animasyona özel ön-hesaplamalar
                # Bellek ve CPU kullanımını optimize etmek için önişleme
                precomputed_data = None
                
                # Bazı animasyonlar için ek optimizasyonlar
                if animation_type == AnimationPattern.RAINBOW:
                    # Gökkuşağı renk dönüşümlerini önceden hesapla
                    precomputed_data = self._precompute_rainbow_cycles(count)
                elif animation_type == AnimationPattern.FIRE:
                    # Ateş simulasyonu için rastgele değerleri önceden üret
                    precomputed_data = self._precompute_fire_values(count)
                
                # Animasyonu çalıştır
                animation_func(color, speed, start, count, precomputed_data)
            else:
                logger.error(f"Desteklenmeyen animasyon türü: {animation_type}")
                
        except Exception as e:
            logger.error(f"Animasyon çalıştırılırken hata: {e}")
            if self.stop_animation.is_set():
                return
            
            # Hatadan sonra LED'leri kapat
            self._clear_zone(start, count)
    
    # Performans optimizasyonu: Ön hesaplama fonksiyonları
    def _precompute_rainbow_cycles(self, count: int) -> List:
        """Gökkuşağı döngülerini önceden hesaplar"""
        cycles = []
        for i in range(256):
            colors = []
            for j in range(count):
                pos = ((i + j) & 255)
                # Optimize edilmiş HSV→RGB dönüşümü
                if pos < 85:
                    colors.append((pos * 3, 255 - pos * 3, 0))
                elif pos < 170:
                    pos -= 85
                    colors.append((255 - pos * 3, 0, pos * 3))
                else:
                    pos -= 170
                    colors.append((0, pos * 3, 255 - pos * 3))
            cycles.append(colors)
        return cycles
    
    def _precompute_fire_values(self, count: int) -> List:
        """Ateş efekti için önceden rastgele değerler üretir"""
        import random
        # Ateş simülasyonu için sabit rastgele değerler üret
        cooling_values = [random.randint(0, 40) for _ in range(count)]
        sparking_values = [random.randint(50, 200) for _ in range(20)]  # Sadece 20 farklı kıvılcım değeri yeterli
        return {
            "cooling": cooling_values,
            "sparking": sparking_values
        }
    
    def _animate_pulse(self, color: Tuple[int, int, int],
                     speed: int, start: int, count: int, precomputed=None) -> None:
        """
        Nabız animasyonu - Parlayıp sönme
        
        Args:
            color (Tuple[int, int, int]): RGB renk değerleri
            speed (int): Animasyon hızı (ms)
            start (int): Başlangıç LED indeksi
            count (int): LED sayısı
            precomputed: Önceden hesaplanmış veriler (kullanılmıyor)
        """
        r, g, b = color
        
        # Performans optimizasyonu: Parlaklık değerlerini önceden hesapla
        brightness_values = []
        steps = 20  # Daha az adımla daha akıcı geçiş
        
        # Yukarı parlaklık (0->100)
        for i in range(steps):
            factor = i / (steps - 1)
            brightness_values.append((
                int(r * factor),
                int(g * factor),
                int(b * factor)
            ))
        
        # Aşağı parlaklık (100->0)
        for i in range(steps):
            factor = 1.0 - (i / (steps - 1))
            brightness_values.append((
                int(r * factor),
                int(g * factor),
                int(b * factor)
            ))
        
        # Animasyon döngüsü - önceden hesaplanmış değerleri kullan
        step_index = 0
        brightness_count = len(brightness_values)
        sleep_time = speed / 1000.0 / steps
        
        while not self.stop_animation.is_set():
            # Mevcut adım için rengi ayarla
            current_color = brightness_values[step_index]
            self._set_zone_color(current_color, start, count)
            
            # Bekleme süresi
            if self.stop_animation.wait(timeout=sleep_time):
                return
            
            # Sonraki adıma geç
            step_index = (step_index + 1) % brightness_count
    
    def _animate_breathe(self, color: Tuple[int, int, int],
                       speed: int, start: int, count: int, precomputed=None) -> None:
        """
        Nefes alma animasyonu - Yumuşak geçişlerle parlama ve sönme
        
        Args:
            color (Tuple[int, int, int]): RGB renk değerleri
            speed (int): Animasyon hızı (ms)
            start (int): Başlangıç LED indeksi
            count (int): LED sayısı
            precomputed: Önceden hesaplanmış veriler (kullanılmıyor)
        """
        r, g, b = color
        
        # Performans optimizasyonu: Sinüs değerlerini önceden hesapla
        import math
        
        # Daha az adım kullan ama daha yumuşak geçişler için yarım sinüs dalgası
        steps = 30
        sin_values = []
        
        for i in range(steps):
            # 0-PI aralığında sinüs değeri (0-1 arası değer verir)
            sin_val = math.sin(math.pi * i / (steps - 1))
            sin_values.append(sin_val)
        
        # Animasyon döngüsü - önbelleğe alınmış sinüs değerlerini kullan
        step_index = 0
        sleep_time = speed / 1000.0 / steps
        
        while not self.stop_animation.is_set():
            # Mevcut adım için parlaklık faktörünü al
            brightness = sin_values[step_index]
            
            # Rengi ayarla
            self._set_zone_color((int(r * brightness), int(g * brightness), int(b * brightness)),
                              start, count)
            
            # Bekleme süresi
            if self.stop_animation.wait(timeout=sleep_time):
                return
            
            # Sonraki adıma geç (ileri-geri hareket)
            if step_index < steps - 1:
                step_index += 1
            else:
                step_index = 0
    
    def _animate_rainbow(self, color: Tuple[int, int, int],
                       speed: int, start: int, count: int, precomputed=None) -> None:
        """
        Gökkuşağı animasyonu - Renk spektrumu boyunca hareket
        
        Args:
            color (Tuple[int, int, int]): Kullanılmıyor (gökkuşağı kendi renklerini kullanır)
            speed (int): Animasyon hızı (ms)
            start (int): Başlangıç LED indeksi
            count (int): LED sayısı
            precomputed: Önceden hesaplanmış gökkuşağı renk döngüleri
        """
        # Performans optimizasyonu: Önceden hesaplanmış döngüleri kullan
        rainbow_cycles = precomputed or self._precompute_rainbow_cycles(count)
        
        # Animasyon döngüsü
        cycle_index = 0
        cycles_count = len(rainbow_cycles)
        sleep_time = speed / 1000.0
        
        while not self.stop_animation.is_set():
            # Mevcut döngüdeki renkleri ayarla
            cycle = rainbow_cycles[cycle_index]
            
            # Tüm LED'leri tek bir seferde ayarla (daha az döngü)
            self._set_zone_multiple_colors(cycle, start, count)
            
            # Bekleme süresi
            if self.stop_animation.wait(timeout=sleep_time):
                return
            
            # Sonraki renk döngüsüne geç
            cycle_index = (cycle_index + 1) % cycles_count
    
    # Performans optimizasyonu: Birden çok rengi tek seferde ayarla
    def _set_zone_multiple_colors(self, colors: List[Tuple[int, int, int]], 
                                start: int, count: int) -> None:
        """
        Bir bölgedeki birden çok LED'i farklı renklerle ayarlar
        
        Args:
            colors (List[Tuple[int, int, int]]): RGB renk değerleri listesi
            start (int): Başlangıç LED indeksi
            count (int): LED sayısı
        """
        if not self.strip:
            return
            
        # Bellek optimizasyonu: Mevcut parlaklık faktörünü bir kez al
        brightness = self.brightness
        
        # Her LED için renk ayarla
        for i in range(min(len(colors), count)):
            if i < len(colors):
                r, g, b = colors[i]
                # Parlaklık faktörünü uygula
                if brightness < 1.0:
                    r = int(r * brightness)
                    g = int(g * brightness)
                    b = int(b * brightness)
                
                # LED'in indeksini hesapla
                index = start + i
                if index < self.strip.numPixels():
                    self.strip.setPixelColor(index, self._color(r, g, b))
        
        # Tüm LED'leri tek seferde güncelle
        self.strip.show()
    
    def _animate_static(self, color: Tuple[int, int, int], 
                      speed: int, start: int, count: int) -> None:
        """
        Sabit renk animasyonu
        
        Args:
            color (Tuple[int, int, int]): RGB renk değerleri
            speed (int): Animasyon hızı (ms)
            start (int): Başlangıç LED indeksi
            count (int): LED sayısı
        """
        if self.simulation_mode:
            # Simülasyon modunda
            for i in range(start, start + count):
                if i < len(self.sim_leds):
                    self.sim_leds[i] = color
            self._save_simulation_image()
        else:
            # Gerçek donanımda
            if self.strip:
                rgb_color = Color(color[0], color[1], color[2])
                for i in range(start, start + count):
                    if i < self.strip.numPixels():
                        self.strip.setPixelColor(i, rgb_color)
                self.strip.show()
        
        # Animasyon sonlandırılana kadar bekle
        while not self.stop_animation.is_set():
            time.sleep(0.1)
    
    def _animate_pulse(self, color: Tuple[int, int, int],
                     speed: int, start: int, count: int) -> None:
        """
        Nabız animasyonu - Parlayıp sönme
        
        Args:
            color (Tuple[int, int, int]): RGB renk değerleri
            speed (int): Animasyon hızı (ms)
            start (int): Başlangıç LED indeksi
            count (int): LED sayısı
        """
        r, g, b = color
        
        while not self.stop_animation.is_set():
            # Yukarı parlaklık
            for brightness in range(0, 100, 5):
                if self.stop_animation.is_set():
                    return
                    
                factor = brightness / 100.0
                self._set_zone_color((int(r * factor), int(g * factor), int(b * factor)), start, count)
                time.sleep(speed / 1000.0)
            
            # Aşağı parlaklık
            for brightness in range(100, 0, -5):
                if self.stop_animation.is_set():
                    return
                    
                factor = brightness / 100.0
                self._set_zone_color((int(r * factor), int(g * factor), int(b * factor)), start, count)
                time.sleep(speed / 1000.0)
    
    def _animate_breathe(self, color: Tuple[int, int, int],
                       speed: int, start: int, count: int) -> None:
        """
        Nefes alma animasyonu - Yumuşak geçişli parlama/sönme
        
        Args:
            color (Tuple[int, int, int]): RGB renk değerleri
            speed (int): Animasyon hızı (ms)
            start (int): Başlangıç LED indeksi
            count (int): LED sayısı
        """
        r, g, b = color
        
        while not self.stop_animation.is_set():
            # Sinüs eğrisi kullanarak yumuşak geçiş
            for i in range(0, 100):
                if self.stop_animation.is_set():
                    return
                    
                # Sinüs dalgası (0.0 - 1.0)
                factor = (math.sin(i / 100.0 * math.pi) + 1) / 2
                self._set_zone_color((int(r * factor), int(g * factor), int(b * factor)), start, count)
                time.sleep(speed / 1000.0)
    
    def _animate_fade(self, color: Tuple[int, int, int],
                    speed: int, start: int, count: int) -> None:
        """
        Solma animasyonu - Tam renkten siyaha doğru geçiş
        
        Args:
            color (Tuple[int, int, int]): RGB renk değerleri
            speed (int): Animasyon hızı (ms)
            start (int): Başlangıç LED indeksi
            count (int): LED sayısı
        """
        r, g, b = color
        
        while not self.stop_animation.is_set():
            # Tam parlaklığa ayarla
            self._set_zone_color((r, g, b), start, count)
            time.sleep(speed / 1000.0 * 2)
            
            # Aşamalı olarak siyaha azalt
            for i in range(100, 0, -2):
                if self.stop_animation.is_set():
                    return
                
                factor = i / 100.0
                self._set_zone_color((int(r * factor), int(g * factor), int(b * factor)), start, count)
                time.sleep(speed / 1000.0)
            
            # Kısa bir süre siyah kalacak
            self._set_zone_color((0, 0, 0), start, count)
            time.sleep(speed / 1000.0 * 3)
    
    def _animate_chase(self, color: Tuple[int, int, int],
                     speed: int, start: int, count: int) -> None:
        """
        Takip animasyonu - Renk noktası şeridi dolaşır
        
        Args:
            color (Tuple[int, int, int]): RGB renk değerleri
            speed (int): Animasyon hızı (ms)
            start (int): Başlangıç LED indeksi
            count (int): LED sayısı
        """
        while not self.stop_animation.is_set():
            # Her LEDi sırayla yak
            for i in range(count):
                if self.stop_animation.is_set():
                    return
                
                # Tüm LEDleri siyah yap
                self._set_zone_color((0, 0, 0), start, count)
                
                # Sadece bir LEDi renkli yap
                self._set_pixel_color(color, start + i)
                
                # LEDleri güncelle
                if not self.simulation_mode and self.strip:
                    self.strip.show()
                else:
                    # Simülasyon modunda görüntüyü güncelle
                    self._save_simulation_image()
                
                time.sleep(speed / 1000.0)
    
    def _animate_rainbow(self, color: Tuple[int, int, int],
                       speed: int, start: int, count: int) -> None:
        """
        Gökkuşağı animasyonu - Spektrum rengi geçişleri
        
        Args:
            color (Tuple[int, int, int]): Bu animasyon tipi için kullanılmaz
            speed (int): Animasyon hızı (ms)
            start (int): Başlangıç LED indeksi
            count (int): LED sayısı
        """
        position = 0
        
        while not self.stop_animation.is_set():
            position = (position + 1) % 256
            
            for i in range(count):
                # Her LED için renk hesapla (renk tekerleği)
                hue = (i * 256 // count + position) % 256
                r, g, b = self._wheel(hue)
                
                # LED rengini ayarla
                self._set_pixel_color((r, g, b), start + i)
            
            # LEDleri güncelle
            if not self.simulation_mode and self.strip:
                self.strip.show()
            else:
                # Simülasyon modunda görüntüyü güncelle
                self._save_simulation_image(skip_frames=3)  # Her 3 karede bir kaydet (performans için)
            
            time.sleep(speed / 1000.0)
    
    def _animate_sparkle(self, color: Tuple[int, int, int],
                       speed: int, start: int, count: int) -> None:
        """
        Pırıltı animasyonu - Rastgele LEDler yanıp söner
        
        Args:
            color (Tuple[int, int, int]): RGB renk değerleri
            speed (int): Animasyon hızı (ms)
            start (int): Başlangıç LED indeksi
            count (int): LED sayısı
        """
        r, g, b = color
        
        while not self.stop_animation.is_set():
            # Tüm LEDleri sönük yap (orijinal rengin %10'u)
            dim_color = (int(r * 0.1), int(g * 0.1), int(b * 0.1))
            self._set_zone_color(dim_color, start, count)
            
            # Rastgele LEDleri parlak yap
            spark_count = max(1, count // 5)
            for _ in range(spark_count):
                i = random.randint(0, count - 1)
                self._set_pixel_color(color, start + i)
            
            # LEDleri güncelle
            if not self.simulation_mode and self.strip:
                self.strip.show()
            else:
                # Simülasyon modunda görüntüyü güncelle
                self._save_simulation_image()
            
            time.sleep(speed / 1000.0)
    
    def _animate_wipe(self, color: Tuple[int, int, int],
                    speed: int, start: int, count: int) -> None:
        """
        Silme animasyonu - Renk bir uçtan diğerine doğru yayılır
        
        Args:
            color (Tuple[int, int, int]): RGB renk değerleri
            speed (int): Animasyon hızı (ms)
            start (int): Başlangıç LED indeksi
            count (int): LED sayısı
        """
        while not self.stop_animation.is_set():
            # Soldan sağa silme
            for i in range(count):
                if self.stop_animation.is_set():
                    return
                
                self._set_pixel_color(color, start + i)
                
                # LEDleri güncelle
                if not self.simulation_mode and self.strip:
                    self.strip.show()
                else:
                    # Simülasyon modunda görüntüyü güncelle (her 2 LED'de bir)
                    if i % 2 == 0:
                        self._save_simulation_image()
                
                time.sleep(speed / 1000.0)
            
            time.sleep(speed / 1000.0 * 5)
            
            # Tüm LEDleri siyah yap
            self._set_zone_color((0, 0, 0), start, count)
            time.sleep(speed / 1000.0 * 5)
    
    def _animate_theater_chase(self, color: Tuple[int, int, int],
                             speed: int, start: int, count: int) -> None:
        """
        Tiyatro takip animasyonu - Sırayla yanıp sönen gruplar
        
        Args:
            color (Tuple[int, int, int]): RGB renk değerleri
            speed (int): Animasyon hızı (ms)
            start (int): Başlangıç LED indeksi
            count (int): LED sayısı
        """
        while not self.stop_animation.is_set():
            for q in range(3):
                if self.stop_animation.is_set():
                    return
                
                # Tüm LEDleri sıfırla
                for i in range(0, count):
                    if i % 3 != q:
                        self._set_pixel_color((0, 0, 0), start + i)
                
                # Her 3. LEDi yak
                for i in range(0, count, 3):
                    if i + q < count:
                        self._set_pixel_color(color, start + i + q)
                
                # LEDleri güncelle
                if not self.simulation_mode and self.strip:
                    self.strip.show()
                else:
                    # Simülasyon modunda görüntüyü güncelle
                    self._save_simulation_image()
                
                time.sleep(speed / 1000.0)
    
    def _animate_color_fade(self, color: Tuple[int, int, int],
                           speed: int, start: int, count: int) -> None:
        """
        Renkler arası geçiş animasyonu
        
        Args:
            color (Tuple[int, int, int]): Temel renk
            speed (int): Animasyon hızı (ms)
            start (int): Başlangıç LED indeksi
            count (int): LED sayısı
        """
        # Birkaç uyumlu renk oluştur
        colors = self._generate_harmony_colors(color, 5)
        
        while not self.stop_animation.is_set():
            # Renkler arası yumuşak geçiş
            for i in range(len(colors)):
                current_color = colors[i]
                next_color = colors[(i + 1) % len(colors)]
                
                # 100 adımda birinden diğerine geçiş
                for step in range(100):
                    if self.stop_animation.is_set():
                        return
                    
                    # İki renk arasında interpolasyon
                    factor = step / 100.0
                    r = int(current_color[0] + (next_color[0] - current_color[0]) * factor)
                    g = int(current_color[1] + (next_color[1] - current_color[1]) * factor)
                    b = int(current_color[2] + (next_color[2] - current_color[2]) * factor)
                    
                    self._set_zone_color((r, g, b), start, count)
                    time.sleep(speed / 1000.0)
    
    def _animate_scan(self, color: Tuple[int, int, int],
                     speed: int, start: int, count: int) -> None:
        """
        Tarama animasyonu - Işık soldan sağa, sonra sağdan sola hareket eder
        
        Args:
            color (Tuple[int, int, int]): RGB renk değerleri
            speed (int): Animasyon hızı (ms)
            start (int): Başlangıç LED indeksi
            count (int): LED sayısı
        """
        # Tarama genişliği
        width = max(1, count // 10)
        
        while not self.stop_animation.is_set():
            # Soldan sağa
            for i in range(start, start + count - width + 1):
                if self.stop_animation.is_set():
                    return
                
                # Tüm LEDleri sönük yap
                dim_color = (color[0] // 8, color[1] // 8, color[2] // 8)
                self._set_zone_color(dim_color, start, count)
                
                # Tarama çubuğunu aydınlat
                for j in range(width):
                    if i + j < start + count:
                        self._set_pixel_color(color, i + j)
                
                # Ekranı güncelle
                if not self.simulation_mode and self.strip:
                    self.strip.show()
                else:
                    self._save_simulation_image()
                
                time.sleep(speed / 1000.0)
            
            # Sağdan sola
            for i in range(start + count - width, start - 1, -1):
                if self.stop_animation.is_set():
                    return
                
                # Tüm LEDleri sönük yap
                dim_color = (color[0] // 8, color[1] // 8, color[2] // 8)
                self._set_zone_color(dim_color, start, count)
                
                # Tarama çubuğunu aydınlat
                for j in range(width):
                    if i + j >= start and i + j < start + count:
                        self._set_pixel_color(color, i + j)
                
                # Ekranı güncelle
                if not self.simulation_mode and self.strip:
                    self.strip.show()
                else:
                    self._save_simulation_image()
                
                time.sleep(speed / 1000.0)
    
    def _animate_twinkle(self, color: Tuple[int, int, int],
                        speed: int, start: int, count: int) -> None:
        """
        Yıldız parıltısı animasyonu - Rastgele LEDler yanıp söner, farklı parlaklık düzeylerinde
        
        Args:
            color (Tuple[int, int, int]): RGB renk değerleri
            speed (int): Animasyon hızı (ms)
            start (int): Başlangıç LED indeksi
            count (int): LED sayısı
        """
        # Arka plan rengi (çok sönük)
        bg_color = (color[0] // 15, color[1] // 15, color[2] // 15)
        
        # Parıltı renkleri (farklı parlaklık düzeylerinde)
        twinkle_colors = [
            (color[0] // 2, color[1] // 2, color[2] // 2),  # 50% parlaklık
            (color[0] * 3 // 4, color[1] * 3 // 4, color[2] * 3 // 4),  # 75% parlaklık
            color,  # 100% parlaklık
        ]
        
        # Her LED için parıltı durumu ve zamanı
        led_states = [0] * count  # 0: kapalı, 1-3: farklı parlaklık seviyeleri
        led_timers = [0] * count
        
        # Arka planı ayarla
        self._set_zone_color(bg_color, start, count)
        
        while not self.stop_animation.is_set():
            # Her LED'i güncelle
            for i in range(count):
                if led_states[i] > 0:
                    # Yanıyor, zamanını kontrol et
                    if led_timers[i] <= 0:
                        # Söndür veya daha az parlak yap
                        led_states[i] -= 1
                        if led_states[i] > 0:
                            # Hala yanıyor, yeni zamanlayıcı ayarla
                            led_timers[i] = random.uniform(1.0, 3.0) * (speed / 50.0)
                            self._set_pixel_color(twinkle_colors[led_states[i] - 1], start + i)
                        else:
                            # Söndü, arka plan rengine dön
                            self._set_pixel_color(bg_color, start + i)
                    else:
                        # Hala yanıyor, zamanı azalt
                        led_timers[i] -= 1
                else:
                    # Şu anda yanmıyor, rastgele yanma olasılığı kontrol et
                    if random.random() < 0.05:  # %5 olasılık
                        led_states[i] = random.randint(1, 3)  # 1-3 arası parlaklık seviyesi
                        led_timers[i] = random.uniform(2.0, 5.0) * (speed / 50.0)
                        self._set_pixel_color(twinkle_colors[led_states[i] - 1], start + i)
            
            # Ekranı güncelle
            if not self.simulation_mode and self.strip:
                self.strip.show()
            else:
                self._save_simulation_image()
            
            time.sleep(speed / 1000.0)
    
    def _animate_wave(self, color: Tuple[int, int, int],
                     speed: int, start: int, count: int) -> None:
        """
        Dalga animasyonu - sinüs dalgası şeklinde renk dalgalanması
        
        Args:
            color (Tuple[int, int, int]): RGB renk değerleri
            speed (int): Animasyon hızı (ms)
            start (int): Başlangıç LED indeksi
            count (int): LED sayısı
        """
        wave_position = 0
        
        while not self.stop_animation.is_set():
            wave_position = (wave_position + 1) % 360
            
            for i in range(count):
                # Dalga efekti için sinüs fonksiyonu kullan
                # Her LED, dalga boyunca farklı bir noktada
                angle = (i * 360 // count + wave_position) % 360
                factor = (math.sin(math.radians(angle)) + 1) / 2  # 0-1 arası değer
                
                # Faktöre göre rengi ayarla
                r = int(color[0] * factor)
                g = int(color[1] * factor)
                b = int(color[2] * factor)
                
                self._set_pixel_color((r, g, b), start + i)
            
            # Ekranı güncelle
            if not self.simulation_mode and self.strip:
                self.strip.show()
            else:
                self._save_simulation_image()
            
            time.sleep(speed / 1000.0)