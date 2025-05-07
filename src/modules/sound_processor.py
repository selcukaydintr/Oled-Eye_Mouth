#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: sound_processor.py
# Açıklama: Mikrofon girişinden ses seviyesi ve frekans analizi yaparak 
#           ağız animasyonu ve duygu tepkileri için sinyal üreten modül
# Bağımlılıklar: numpy, pyaudio, logging, threading
# Bağlı Dosyalar:
#   - modules/animation_engine.py
#   - modules/emotion_engine.py
#   - modules/oled_controller.py

# Versiyon: 0.5.0
# Değişiklikler:
# - [0.5.0] İlk sürüm - Faz 4 Ses Tepkimeli İfade Sistemi
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-04
===========================================================
"""

import logging
import threading
import time
import numpy as np
from typing import Dict, Optional, Tuple, List, Any, Callable
import queue
import math

# Koşullu import - PyAudio eğer yüklüyse kullanalım, değilse simule edebiliriz
try:
    import pyaudio
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False
    logging.warning("PyAudio yüklü değil. Simülasyon modu aktif.")

# Loglama yapılandırması
logger = logging.getLogger("SoundProcessor")

class SoundProcessor:
    """
    FACE1 için ses işleme modülü
    
    Bu modül:
    1. Mikrofon girişini okur
    2. Ses seviyesini ve temel frekans dağılımını analiz eder
    3. Ağız animasyonu için sinyal üretir
    4. Ses analizine göre duygu tepkileri üretir
    """
    
    def __init__(self, config: Dict):
        """
        Ses işleme modülünü başlatır
        
        Args:
            config (Dict): Yapılandırma ayarları
        """
        # Yapılandırmayı kaydet
        self.config = config
        self.sound_config = config.get("sound", {})
        
        # Varsayılan yapılandırma değerlerini ayarla
        self.enabled = self.sound_config.get("enabled", True)
        self.sample_rate = self.sound_config.get("sample_rate", 16000)
        self.chunk_size = self.sound_config.get("chunk_size", 1024)
        self.channels = self.sound_config.get("channels", 1)
        self.format = self.sound_config.get("format", 8)  # PyAudio.paInt16
        self.device_index = self.sound_config.get("device_index", None)
        self.volume_threshold = self.sound_config.get("volume_threshold", 0.1)
        self.emotion_sensitivity = self.sound_config.get("emotion_sensitivity", 0.5)
        
        # İş parçacığı ve durum değişkenleri
        self.stream = None
        self.pyaudio_instance = None
        self.running = False
        self.processing_thread = None
        self.data_queue = queue.Queue(maxsize=10)
        
        # Ses ölçümleri
        self.current_volume = 0.0
        self.frequency_distribution = np.zeros(4)  # Düşük, orta-düşük, orta-yüksek, yüksek
        self.speaking_detected = False
        self.last_sound_time = 0
        
        # Geri çağırma işlevleri
        self.volume_callbacks = []
        self.speaking_callbacks = []
        self.emotion_callbacks = []
        
        logger.info("Ses işleme modülü başlatıldı.")
    
    def start(self) -> bool:
        """
        Ses işleme modülünü başlatır
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        if not self.enabled:
            logger.info("Ses işleme modülü devre dışı bırakıldı.")
            return False
        
        if self.running:
            logger.warning("Ses işleme modülü zaten çalışıyor.")
            return True
        
        try:
            # PyAudio yoksa simülasyon modunu kullan
            if not PYAUDIO_AVAILABLE:
                logger.info("Ses işleme modülü simülasyon modunda başlatılıyor.")
                self.running = True
                self.processing_thread = threading.Thread(target=self._simulation_loop)
                self.processing_thread.daemon = True
                self.processing_thread.start()
                return True
            
            # PyAudio başlat
            self.pyaudio_instance = pyaudio.PyAudio()
            
            # Kullanılacak cihazı seç
            if self.device_index is None:
                # Varsayılan giriş cihazını bul
                info = self.pyaudio_instance.get_default_input_device_info()
                self.device_index = info['index']
                logger.info(f"Varsayılan ses giriş cihazı kullanılıyor: {info['name']} (index: {self.device_index})")
            
            # Ses akışını başlat
            self.stream = self.pyaudio_instance.open(
                format=self.format,
                channels=self.channels,
                rate=self.sample_rate,
                input=True,
                frames_per_buffer=self.chunk_size,
                input_device_index=self.device_index
            )
            
            # İşleme iş parçacığını başlat
            self.running = True
            self.processing_thread = threading.Thread(target=self._processing_loop)
            self.processing_thread.daemon = True
            self.processing_thread.start()
            
            logger.info("Ses işleme modülü başarıyla başlatıldı.")
            return True
            
        except Exception as e:
            logger.error(f"Ses işleme modülü başlatılırken hata: {str(e)}")
            # Hata durumunda simülasyon modunu başlat
            self.running = True
            self.processing_thread = threading.Thread(target=self._simulation_loop)
            self.processing_thread.daemon = True
            self.processing_thread.start()
            logger.info("Hata sonrası simülasyon moduna geçildi.")
            return True  # Simülasyon modunda da başarılı döndür
    
    def stop(self) -> bool:
        """
        Ses işleme modülünü durdurur
        
        Returns:
            bool: Başarılı ise True, değilse False
        """
        if not self.running:
            logger.warning("Ses işleme modülü zaten durdurulmuş.")
            return True
        
        try:
            self.running = False
            
            if self.processing_thread and self.processing_thread.is_alive():
                self.processing_thread.join(timeout=2.0)
            
            if self.stream:
                self.stream.stop_stream()
                self.stream.close()
                self.stream = None
            
            if self.pyaudio_instance:
                self.pyaudio_instance.terminate()
                self.pyaudio_instance = None
            
            logger.info("Ses işleme modülü başarıyla durduruldu.")
            return True
        except Exception as e:
            logger.error(f"Ses işleme modülü durdurulurken hata: {str(e)}")
            return False
    
    def update_config(self, config: Dict) -> bool:
        """
        Yapılandırmayı günceller
        
        Args:
            config (Dict): Yeni yapılandırma ayarları
            
        Returns:
            bool: Başarılı ise True, değilse False
        """
        was_running = self.running
        
        if was_running:
            self.stop()
        
        self.config = config
        self.sound_config = config.get("sound", {})
        
        # Yapılandırma değerlerini güncelle
        self.enabled = self.sound_config.get("enabled", True)
        self.sample_rate = self.sound_config.get("sample_rate", 16000)
        self.chunk_size = self.sound_config.get("chunk_size", 1024)
        self.channels = self.sound_config.get("channels", 1)
        self.format = self.sound_config.get("format", 8)
        self.device_index = self.sound_config.get("device_index", None)
        self.volume_threshold = self.sound_config.get("volume_threshold", 0.1)
        self.emotion_sensitivity = self.sound_config.get("emotion_sensitivity", 0.5)
        
        if was_running:
            return self.start()
        
        return True
    
    def register_volume_callback(self, callback: Callable[[float], None]) -> None:
        """
        Ses seviyesi değiştiğinde çağrılacak geri çağırma işlevini kaydeder
        
        Args:
            callback: Ses seviyesi değiştiğinde çağrılacak işlev, parametre olarak ses seviyesi (0.0-1.0) alır
        """
        self.volume_callbacks.append(callback)
    
    def register_speaking_callback(self, callback: Callable[[bool], None]) -> None:
        """
        Konuşma durumu değiştiğinde çağrılacak geri çağırma işlevini kaydeder
        
        Args:
            callback: Konuşma durumu değiştiğinde çağrılacak işlev, parametre olarak konuşma durumu (bool) alır
        """
        self.speaking_callbacks.append(callback)
    
    def register_emotion_callback(self, callback: Callable[[str, float], None]) -> None:
        """
        Duygu değişikliği önerildiğinde çağrılacak geri çağırma işlevini kaydeder
        
        Args:
            callback: Duygu değişikliği önerildiğinde çağrılacak işlev, 
                     parametre olarak duygu adı (str) ve yoğunluk (float) alır
        """
        self.emotion_callbacks.append(callback)
    
    def get_current_volume(self) -> float:
        """
        Mevcut ses seviyesini döndürür
        
        Returns:
            float: Ses seviyesi (0.0 ile 1.0 arasında)
        """
        return self.current_volume
    
    def is_speaking(self) -> bool:
        """
        Konuşma algılanıp algılanmadığını döndürür
        
        Returns:
            bool: Konuşma algılanıyorsa True, değilse False
        """
        return self.speaking_detected
    
    def get_frequency_distribution(self) -> np.ndarray:
        """
        Mevcut frekans dağılımını döndürür
        
        Returns:
            np.ndarray: Frekans dağılımı [düşük, orta-düşük, orta-yüksek, yüksek]
        """
        return self.frequency_distribution
    
    def _processing_loop(self) -> None:
        """
        Ses verilerini sürekli işleyen ana döngü
        """
        try:
            while self.running:
                if self.stream and not self.stream.is_stopped():
                    try:
                        # Ses verilerini oku
                        audio_data = np.frombuffer(
                            self.stream.read(self.chunk_size, exception_on_overflow=False),
                            dtype=np.int16
                        )
                        
                        # Ses verilerini işle
                        self._process_audio_data(audio_data)
                    except Exception as e:
                        logger.error(f"Ses verisi okunurken hata: {str(e)}")
                        time.sleep(0.1)
                else:
                    time.sleep(0.1)
        except Exception as e:
            logger.error(f"Ses işleme döngüsünde hata: {str(e)}")
    
    def _simulation_loop(self) -> None:
        """
        Simülasyon modunda ses verilerini taklit eden döngü
        """
        try:
            # Simüle edilen konuşma için değişkenler
            speaking_duration = 0
            silent_duration = 0
            is_speaking_phase = False
            
            while self.running:
                current_time = time.time()
                
                # Konuşma/sessizlik fazlarını değiştir
                if is_speaking_phase:
                    if current_time - speaking_duration > 2.0:
                        is_speaking_phase = False
                        silent_duration = current_time
                else:
                    if current_time - silent_duration > 1.5:
                        is_speaking_phase = True
                        speaking_duration = current_time
                
                # Ses seviyesini simüle et
                if is_speaking_phase:
                    # Konuşma sesini simüle et (0.3-0.8 arası)
                    simulated_volume = 0.3 + 0.5 * (0.5 + 0.5 * math.sin(current_time * 5))
                    simulated_distribution = np.array([
                        0.2 + 0.2 * math.sin(current_time * 3),      # Düşük frekanslar
                        0.4 + 0.3 * math.sin(current_time * 7),      # Orta-düşük frekanslar
                        0.3 + 0.3 * math.sin(current_time * 11),     # Orta-yüksek frekanslar
                        0.1 + 0.1 * math.sin(current_time * 5)       # Yüksek frekanslar
                    ])
                else:
                    # Sessizliği simüle et (0.0-0.1 arası)
                    simulated_volume = 0.05 * random_noise()
                    simulated_distribution = np.array([0.1, 0.05, 0.02, 0.01]) * random_noise()
                
                # Simüle edilmiş verileri işle
                self._update_measurements(simulated_volume, simulated_distribution)
                
                # Geri çağırma işlevlerini çağır
                self._call_callbacks()
                
                # Küçük bir bekleme ekleyelim
                time.sleep(0.05)
        except Exception as e:
            logger.error(f"Simülasyon döngüsünde hata: {str(e)}")
    
    def _process_audio_data(self, audio_data: np.ndarray) -> None:
        """
        Ham ses verilerini işler
        
        Args:
            audio_data (np.ndarray): Ham ses verileri
        """
        # Ses verisinden mutlak değerleri al
        abs_data = np.abs(audio_data)
        
        # Ses seviyesini hesapla (normalize edilmiş RMS)
        rms = np.sqrt(np.mean(np.square(audio_data.astype(np.float32))))
        normalized_volume = min(1.0, rms / 32767.0)  # 16-bit için normalize et
        
        # Frekans analizi (basit fft aracılığıyla)
        try:
            fft_data = np.abs(np.fft.rfft(audio_data))
            fft_data = fft_data / len(fft_data)  # Normalize et
            
            # Frekans bantlarını oluştur
            freq_bins = len(fft_data)
            low_freq = np.sum(fft_data[:int(freq_bins * 0.1)])
            mid_low_freq = np.sum(fft_data[int(freq_bins * 0.1):int(freq_bins * 0.3)])
            mid_high_freq = np.sum(fft_data[int(freq_bins * 0.3):int(freq_bins * 0.6)])
            high_freq = np.sum(fft_data[int(freq_bins * 0.6):])
            
            # Toplam enerjiyi normalize et
            total_energy = low_freq + mid_low_freq + mid_high_freq + high_freq
            if total_energy > 0:
                freq_distribution = np.array([
                    low_freq / total_energy,
                    mid_low_freq / total_energy,
                    mid_high_freq / total_energy,
                    high_freq / total_energy
                ])
            else:
                freq_distribution = np.array([0.25, 0.25, 0.25, 0.25])
            
            # Ölçümleri güncelle
            self._update_measurements(normalized_volume, freq_distribution)
        except Exception as e:
            logger.error(f"Ses verileri işlenirken hata: {str(e)}")
    
    def _update_measurements(self, volume: float, freq_distribution: np.ndarray) -> None:
        """
        Ses ölçümlerini günceller ve konuşma algılama durumunu değiştirir
        
        Args:
            volume (float): Güncel ses seviyesi (0-1 arası)
            freq_distribution (np.ndarray): Frekans dağılımı [düşük, orta-düşük, orta-yüksek, yüksek]
        """
        current_time = time.time()
        
        # Yumuşatma faktörü
        smooth_factor = 0.7
        
        # Ölçümleri yumuşatarak güncelle
        self.current_volume = smooth_factor * self.current_volume + (1 - smooth_factor) * volume
        self.frequency_distribution = (smooth_factor * self.frequency_distribution + 
                                      (1 - smooth_factor) * freq_distribution)
        
        # Konuşma algılama
        previous_speaking = self.speaking_detected
        
        if volume > self.volume_threshold:
            self.speaking_detected = True
            self.last_sound_time = current_time
        elif current_time - self.last_sound_time > 0.5:  # Yarım saniye sessizlik konuşma bitimi sayılır
            self.speaking_detected = False
        
        # Konuşma durumu değiştiyse geri çağırmaları çağır
        if previous_speaking != self.speaking_detected:
            for callback in self.speaking_callbacks:
                try:
                    callback(self.speaking_detected)
                except Exception as e:
                    logger.error(f"Konuşma geri çağırma işlevinde hata: {str(e)}")
        
        # Duygu analizi yap ve öneri üret (belirli aralıklarla)
        if current_time - getattr(self, "_last_emotion_check_time", 0) > 2.0:
            self._last_emotion_check_time = current_time
            self._analyze_emotion()
        
        # Ses seviyesi geri çağırmalarını çağır
        self._call_volume_callbacks()
    
    def _call_callbacks(self) -> None:
        """
        Tüm geri çağırma işlevlerini çağırır
        """
        self._call_volume_callbacks()
    
    def _call_volume_callbacks(self) -> None:
        """
        Ses seviyesi geri çağırma işlevlerini çağırır
        """
        for callback in self.volume_callbacks:
            try:
                callback(self.current_volume)
            except Exception as e:
                logger.error(f"Ses seviyesi geri çağırma işlevinde hata: {str(e)}")
    
    def _analyze_emotion(self) -> None:
        """
        Ses özelliklerine göre basit bir duygu analizi yapar
        """
        # Ses yoksa emotion analizi yapma
        if self.current_volume < self.volume_threshold:
            return
        
        # Temel duygu analizi kuralları:
        # - Yüksek ses + yüksek frekanslarda yoğunluk = kızgınlık/heyecan
        # - Düşük ses + düşük frekanslarda yoğunluk = üzüntü
        # - Orta ses + dengeli frekanslar = mutluluk/nötr
        # - Ani ses yükselmesi = şaşırma
        
        try:
            # Daha önceki ses seviyelerini takip et
            if not hasattr(self, "_previous_volumes"):
                self._previous_volumes = [0.0] * 10
            
            # Önceki ses seviyelerini shift et
            self._previous_volumes.pop(0)
            self._previous_volumes.append(self.current_volume)
            
            # Ani değişim kontrolü
            volume_gradient = self.current_volume - sum(self._previous_volumes[:-1]) / len(self._previous_volumes[:-1])
            
            # Ses karakteristiği analizi
            low_dominance = self.frequency_distribution[0] > 0.4  # Düşük frekanslar baskın mı?
            high_dominance = self.frequency_distribution[3] > 0.3  # Yüksek frekanslar baskın mı?
            
            # Duygu önerisi oluştur
            emotion = "neutral"
            intensity = 0.5
            
            # Ani artış: Şaşırma
            if volume_gradient > 0.25:
                emotion = "surprised"
                intensity = min(0.9, 0.6 + volume_gradient)
            
            # Yüksek ses + yüksek frekans: Kızgın
            elif self.current_volume > 0.7 and high_dominance:
                emotion = "angry"
                intensity = 0.7 + 0.3 * self.current_volume
            
            # Yüksek ses + dengeli frekans: Heyecanlı/Mutlu
            elif self.current_volume > 0.6:
                emotion = "happy"
                intensity = 0.6 + 0.4 * self.current_volume
            
            # Düşük ses + düşük frekans: Üzgün
            elif self.current_volume < 0.3 and low_dominance and self.speaking_detected:
                emotion = "sad"
                intensity = 0.5 + 0.5 * (1.0 - self.current_volume)
            
            # Orta ses: Nötr
            else:
                emotion = "neutral"
                intensity = 0.5
            
            # Duygu önerisini bildir
            for callback in self.emotion_callbacks:
                try:
                    callback(emotion, intensity * self.emotion_sensitivity)
                except Exception as e:
                    logger.error(f"Duygu geri çağırma işlevinde hata: {str(e)}")
                    
        except Exception as e:
            logger.error(f"Duygu analizi yapılırken hata: {str(e)}")


def random_noise() -> float:
    """
    0 ile 1 arasında rastgele gürültü üretir (simülasyon için)
    """
    return 0.5 + 0.5 * math.sin(time.time() * 10) + 0.2 * math.sin(time.time() * 30)


if __name__ == "__main__":
    # Basit test kodu
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Test yapılandırması
    test_config = {
        "sound": {
            "enabled": True,
            "sample_rate": 16000,
            "chunk_size": 1024,
            "channels": 1,
            "format": 8,
            "device_index": None,
            "volume_threshold": 0.1,
            "emotion_sensitivity": 0.7
        }
    }
    
    # Ses seviyesi geri çağırma işlevi
    def print_volume(volume):
        print(f"Ses seviyesi: {volume:.2f}")
    
    # Konuşma geri çağırma işlevi
    def print_speaking(speaking):
        print(f"Konuşma algılandı: {'Evet' if speaking else 'Hayır'}")
    
    # Duygu geri çağırma işlevi
    def print_emotion(emotion, intensity):
        print(f"Duygu önerisi: {emotion} (yoğunluk: {intensity:.2f})")
    
    # Ses işleme modülünü oluştur ve başlat
    processor = SoundProcessor(test_config)
    processor.register_volume_callback(print_volume)
    processor.register_speaking_callback(print_speaking)
    processor.register_emotion_callback(print_emotion)
    processor.start()
    
    try:
        # 10 saniye çalıştır
        for i in range(100):
            time.sleep(0.1)
    finally:
        processor.stop()