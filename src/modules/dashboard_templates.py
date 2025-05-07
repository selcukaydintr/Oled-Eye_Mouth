#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: dashboard_templates.py
# Açıklama: Dashboard için şablonlar ve varsayılan içerik modülü
# Bağımlılıklar: -
# Bağlı Dosyalar: dashboard_server.py

# Versiyon: 0.1.0
# Değişiklikler:
# - [0.1.0] dashboard_server.py dosyasından ayrıldı
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-02
===========================================================
"""

import os
import logging
from typing import Dict, Optional

# Logger yapılandırması
logger = logging.getLogger("DashboardTemplates")

class TemplateManager:
    """
    Dashboard şablonlarını ve varsayılan içerikleri yöneten sınıf
    """
    def __init__(self, templates_dir: str, static_dir: str):
        """
        Template Manager'ı başlatır
        
        Args:
            templates_dir (str): Şablonların bulunduğu dizin
            static_dir (str): Statik dosyaların bulunduğu dizin
        """
        self.templates_dir = templates_dir
        self.static_dir = static_dir
    
    def ensure_templates(self) -> None:
        """
        Temel şablonların varlığını kontrol eder ve yoksa oluşturur
        """
        # dashboard.html şablonunu kontrol et
        dashboard_template = os.path.join(self.templates_dir, "dashboard.html")
        if not os.path.exists(dashboard_template):
            logger.info(f"Varsayılan dashboard.html şablonu oluşturuluyor: {dashboard_template}")
            os.makedirs(os.path.dirname(dashboard_template), exist_ok=True)
            with open(dashboard_template, 'w') as f:
                f.write(self.get_default_dashboard_template())
        
        # error.html şablonunu kontrol et
        error_template = os.path.join(self.templates_dir, "error.html")
        if not os.path.exists(error_template):
            logger.info(f"Varsayılan error.html şablonu oluşturuluyor: {error_template}")
            with open(error_template, 'w') as f:
                f.write(self.get_default_error_template())
        
        # Temel CSS dosyası
        css_file = os.path.join(self.static_dir, "css", "style.css")
        if not os.path.exists(css_file):
            logger.info(f"Varsayılan CSS dosyası oluşturuluyor: {css_file}")
            os.makedirs(os.path.dirname(css_file), exist_ok=True)
            with open(css_file, 'w') as f:
                f.write(self.get_default_css())
        
        # Temel JavaScript dosyası
        js_file = os.path.join(self.static_dir, "js", "dashboard.js")
        if not os.path.exists(js_file):
            logger.info(f"Varsayılan JavaScript dosyası oluşturuluyor: {js_file}")
            os.makedirs(os.path.dirname(js_file), exist_ok=True)
            with open(js_file, 'w') as f:
                f.write(self.get_default_js())
    
    def get_default_html(self) -> str:
        """
        Varsayılan HTML içeriğini döndürür
        
        Returns:
            str: HTML içeriği
        """
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>FACE1 Dashboard</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body { font-family: Arial, sans-serif; margin: 2rem; }
                h1 { color: #333; }
                .message { background-color: #f8f9fa; padding: 1rem; border-radius: 4px; }
            </style>
        </head>
        <body>
            <h1>FACE1 Dashboard</h1>
            <div class="message">
                <p>Dashboard şablonları yüklenemedi. Lütfen web/templates dizinini kontrol edin.</p>
            </div>
        </body>
        </html>
        """
    
    def get_default_dashboard_template(self) -> str:
        """
        Varsayılan dashboard şablonunu döndürür
        
        Returns:
            str: HTML şablonu
        """
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>FACE1 Robot Dashboard</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/static/css/style.css">
        </head>
        <body>
            <header>
                <h1>FACE1 Robot Kontrol Paneli</h1>
                <div class="system-stats">
                    <span id="cpu-usage">CPU: --%</span>
                    <span id="memory-usage">RAM: --%</span>
                    <span id="temperature">Sıcaklık: --°C</span>
                </div>
            </header>
            
            <main>
                <div class="container">
                    <div class="face-preview">
                        <h2>Yüz Önizleme</h2>
                        <div class="face">
                            <div class="eyes">
                                <div class="eye left"></div>
                                <div class="eye right"></div>
                            </div>
                            <div class="mouth"></div>
                        </div>
                    </div>
                    
                    <div class="control-panel">
                        <section class="emotions">
                            <h2>Duygular</h2>
                            <div class="emotion-buttons">
                                <button class="emotion-btn" data-emotion="happy">Mutlu</button>
                                <button class="emotion-btn" data-emotion="sad">Üzgün</button>
                                <button class="emotion-btn" data-emotion="angry">Kızgın</button>
                                <button class="emotion-btn" data-emotion="surprised">Şaşkın</button>
                                <button class="emotion-btn" data-emotion="fearful">Korkmuş</button>
                                <button class="emotion-btn" data-emotion="disgusted">İğrenmiş</button>
                                <button class="emotion-btn" data-emotion="calm">Sakin</button>
                                <button class="emotion-btn" data-emotion="neutral">Nötr</button>
                            </div>
                            <div class="intensity-control">
                                <label for="emotion-intensity">Duygu Yoğunluğu:</label>
                                <input type="range" id="emotion-intensity" min="0" max="1" step="0.1" value="1">
                                <span id="intensity-value">1.0</span>
                            </div>
                        </section>
                        
                        <section class="themes">
                            <h2>Temalar</h2>
                            <div class="theme-selector">
                                <select id="theme-select">
                                    {% for theme in themes %}
                                    <option value="{{ theme }}" {% if theme == current_theme %}selected{% endif %}>{{ theme|title }}</option>
                                    {% endfor %}
                                </select>
                                <button id="apply-theme">Temayı Uygula</button>
                            </div>
                        </section>
                        
                        <section class="animations">
                            <h2>Animasyonlar</h2>
                            <div class="animation-buttons">
                                <button class="animation-btn" data-animation="blink">Göz Kırp</button>
                                <button class="animation-btn" data-animation="nod">Baş Salla</button>
                                <button class="animation-btn" data-animation="shake">Baş Salla (Hayır)</button>
                                <button class="animation-btn" data-animation="random">Rastgele</button>
                            </div>
                        </section>
                    </div>
                </div>
                
                <div class="log-container">
                    <h2>Sistem Günlüğü</h2>
                    <div id="log-viewer"></div>
                </div>
            </main>
            
            <footer>
                <p>&copy; 2025 FACE1 Robot - Version 0.1.0</p>
            </footer>
            
            <script src="/static/js/dashboard.js"></script>
        </body>
        </html>
        """
    
    def get_default_error_template(self) -> str:
        """
        Varsayılan hata şablonunu döndürür
        
        Returns:
            str: HTML şablonu
        """
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Hata - FACE1 Dashboard</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="/static/css/style.css">
        </head>
        <body>
            <header>
                <h1>FACE1 Robot Kontrol Paneli</h1>
            </header>
            
            <main>
                <div class="error-container">
                    <h2>Hata</h2>
                    <p class="error-message">{{ message }}</p>
                    <a href="/" class="button">Ana Sayfaya Dön</a>
                </div>
            </main>
            
            <footer>
                <p>&copy; 2025 FACE1 Robot - Version 0.1.0</p>
            </footer>
        </body>
        </html>
        """
    
    def get_default_css(self) -> str:
        """
        Varsayılan CSS stilini döndürür
        
        Returns:
            str: CSS içeriği
        """
        return """
        /* FACE1 Dashboard CSS */
        :root {
          --primary-color: #3498db;
          --secondary-color: #2c3e50;
          --accent-color: #e74c3c;
          --text-color: #333;
          --bg-color: #f4f6f9;
          --card-bg: #ffffff;
        }

        * {
          box-sizing: border-box;
          margin: 0;
          padding: 0;
        }

        body {
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          background-color: var(--bg-color);
          color: var(--text-color);
          line-height: 1.6;
        }

        header {
          background-color: var(--secondary-color);
          color: white;
          padding: 1rem;
          display: flex;
          justify-content: space-between;
          align-items: center;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        header h1 {
          margin: 0;
          font-size: 1.5rem;
        }

        .system-stats {
          font-size: 0.85rem;
        }

        .system-stats span {
          margin-left: 1rem;
        }

        main {
          padding: 1rem;
          max-width: 1200px;
          margin: 0 auto;
        }

        .container {
          display: flex;
          flex-wrap: wrap;
          gap: 1rem;
          margin-bottom: 1rem;
        }

        .face-preview {
          flex: 1;
          min-width: 300px;
          background-color: var(--card-bg);
          padding: 1rem;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .control-panel {
          flex: 2;
          min-width: 300px;
          background-color: var(--card-bg);
          padding: 1rem;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        h2 {
          color: var(--secondary-color);
          margin-bottom: 1rem;
          padding-bottom: 0.5rem;
          border-bottom: 1px solid #eee;
        }

        section {
          margin-bottom: 1.5rem;
        }

        .face {
          width: 200px;
          height: 250px;
          background-color: #f9f9f9;
          border-radius: 50% 50% 40% 40%;
          position: relative;
          margin: 2rem auto;
          border: 2px solid #ddd;
        }

        .eyes {
          display: flex;
          justify-content: space-around;
          position: relative;
          top: 75px;
        }

        .eye {
          width: 40px;
          height: 40px;
          background-color: white;
          border-radius: 50%;
          border: 2px solid #333;
          position: relative;
        }

        .eye::after {
          content: '';
          width: 20px;
          height: 20px;
          background-color: #333;
          border-radius: 50%;
          position: absolute;
          top: 50%;
          left: 50%;
          transform: translate(-50%, -50%);
        }

        .mouth {
          width: 80px;
          height: 40px;
          border-radius: 0 0 40px 40px;
          border: 2px solid #333;
          position: absolute;
          bottom: 50px;
          left: 50%;
          transform: translateX(-50%);
          background-color: white;
        }

        .emotion-buttons, .animation-buttons {
          display: flex;
          flex-wrap: wrap;
          gap: 0.5rem;
          margin-top: 0.5rem;
        }

        button {
          background-color: var(--primary-color);
          color: white;
          border: none;
          padding: 0.5rem 1rem;
          border-radius: 4px;
          cursor: pointer;
          font-size: 0.9rem;
          transition: background-color 0.2s;
        }

        button:hover {
          background-color: #2980b9;
        }

        .intensity-control {
          margin-top: 1rem;
          display: flex;
          align-items: center;
          gap: 0.5rem;
        }

        input[type="range"] {
          flex: 1;
        }

        select {
          padding: 0.5rem;
          border-radius: 4px;
          border: 1px solid #ddd;
          font-size: 0.9rem;
          width: 200px;
        }

        .theme-selector {
          display: flex;
          gap: 0.5rem;
        }

        .log-container {
          background-color: var(--card-bg);
          padding: 1rem;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        #log-viewer {
          height: 200px;
          overflow-y: auto;
          background-color: #f9f9f9;
          padding: 0.5rem;
          border: 1px solid #ddd;
          border-radius: 4px;
          font-family: monospace;
          font-size: 0.85rem;
        }

        footer {
          text-align: center;
          padding: 1rem;
          color: #777;
          font-size: 0.8rem;
          margin-top: 2rem;
          border-top: 1px solid #eee;
        }

        .error-container {
          max-width: 600px;
          margin: 2rem auto;
          background-color: var(--card-bg);
          padding: 2rem;
          border-radius: 8px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
          text-align: center;
        }

        .error-message {
          color: var(--accent-color);
          margin: 1rem 0;
        }

        .button {
          display: inline-block;
          background-color: var(--primary-color);
          color: white;
          padding: 0.5rem 1rem;
          text-decoration: none;
          border-radius: 4px;
          font-weight: bold;
        }

        /* Duyarlı tasarım */
        @media (max-width: 768px) {
          .container {
            flex-direction: column;
          }
        }
        """
    
    def get_default_js(self) -> str:
        """
        Varsayılan JavaScript kodunu döndürür
        
        Returns:
            str: JavaScript içeriği
        """
        return """
        // FACE1 Dashboard JavaScript
        document.addEventListener('DOMContentLoaded', function() {
            // WebSocket bağlantısı
            const socket = new WebSocket(`ws://${window.location.host}/ws`);
            const logViewer = document.getElementById('log-viewer');
            const emotionButtons = document.querySelectorAll('.emotion-btn');
            const animationButtons = document.querySelectorAll('.animation-btn');
            const themeSelect = document.getElementById('theme-select');
            const applyThemeButton = document.getElementById('apply-theme');
            const emotionIntensity = document.getElementById('emotion-intensity');
            const intensityValue = document.getElementById('intensity-value');
            
            let currentEmotion = 'neutral';
            let currentIntensity = 1.0;
            
            // WebSocket olayları
            socket.onopen = function(e) {
                addLog('Dashboard WebSocket bağlantısı kuruldu');
            };
            
            socket.onmessage = function(event) {
                const data = JSON.parse(event.data);
                
                // Mesaj tipine göre işlem yap
                switch (data.type) {
                    case 'welcome':
                        addLog(data.message);
                        break;
                        
                    case 'stats':
                        updateSystemStats(data.data);
                        break;
                        
                    case 'theme_changed':
                        addLog(`Tema değiştirildi: ${data.theme}`);
                        themeSelect.value = data.theme;
                        break;
                        
                    case 'emotion_changed':
                        const emotion = data.emotion;
                        addLog(`Duygu durumu değişti: ${emotion.state} (${emotion.intensity.toFixed(1)})`);
                        updateFaceDisplay(emotion.state, emotion.intensity);
                        currentEmotion = emotion.state;
                        currentIntensity = emotion.intensity;
                        break;
                        
                    case 'simulation_update':
                        // Simülasyon güncellemesi alındığında yüzü güncelle
                        const images = data.images;
                        updateSimulationDisplay(images);
                        break;
                        
                    case 'error':
                        addLog(`Hata: ${data.message}`, true);
                        break;
                }
            };
            
            socket.onclose = function(event) {
                addLog('WebSocket bağlantısı kapatıldı', true);
            };
            
            socket.onerror = function(error) {
                addLog('WebSocket hatası', true);
            };
            
            // Duygu butonları
            emotionButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const emotion = this.getAttribute('data-emotion');
                    const intensity = parseFloat(emotionIntensity.value);
                    setEmotion(emotion, intensity);
                });
            });
            
            // Animasyon butonları
            animationButtons.forEach(button => {
                button.addEventListener('click', function() {
                    const animation = this.getAttribute('data-animation');
                    playAnimation(animation);
                });
            });
            
            // Tema değiştirme
            applyThemeButton.addEventListener('click', function() {
                const theme = themeSelect.value;
                setTheme(theme);
            });
            
            // Yoğunluk kaydırıcı
            emotionIntensity.addEventListener('input', function() {
                const value = parseFloat(this.value).toFixed(1);
                intensityValue.textContent = value;
                currentIntensity = parseFloat(value);
            });
            
            // Duygu ayarlama fonksiyonu
            function setEmotion(emotion, intensity) {
                if (!socket || socket.readyState !== WebSocket.OPEN) {
                    addLog('WebSocket bağlantısı yok', true);
                    return;
                }
                
                socket.send(JSON.stringify({
                    action: 'set_emotion',
                    emotion: emotion,
                    intensity: intensity
                }));
                
                updateFaceDisplay(emotion, intensity);
            }
            
            // Animasyon oynatma fonksiyonu
            function playAnimation(animation) {
                // Burada önizleme animasyonları oynatılacak
                addLog(`Animasyon oynatılıyor: ${animation}`);
                
                // TODO: Animasyon komutlarını WebSocket üzerinden gönder
                // Şimdilik sadece günlüğe yazıyoruz
            }
            
            // Tema değiştirme fonksiyonu
            function setTheme(theme) {
                if (!socket || socket.readyState !== WebSocket.OPEN) {
                    addLog('WebSocket bağlantısı yok', true);
                    return;
                }
                
                socket.send(JSON.stringify({
                    action: 'set_theme',
                    theme: theme
                }));
            }
            
            // Sistem istatistiklerini güncelleme
            function updateSystemStats(stats) {
                if (stats.cpu) {
                    document.getElementById('cpu-usage').textContent = `CPU: ${stats.cpu.percent.toFixed(1)}%`;
                }
                
                if (stats.memory) {
                    document.getElementById('memory-usage').textContent = `RAM: ${stats.memory.percent.toFixed(1)}%`;
                }
                
                if (stats.cpu && stats.cpu.temperature) {
                    document.getElementById('temperature').textContent = `Sıcaklık: ${stats.cpu.temperature.toFixed(1)}°C`;
                }
            }
            
            // Yüz görünümünü güncelle
            function updateFaceDisplay(emotion, intensity) {
                const face = document.querySelector('.face');
                const mouth = document.querySelector('.mouth');
                const leftEye = document.querySelector('.eye.left');
                const rightEye = document.querySelector('.eye.right');
                
                // Tüm önceki duygu sınıflarını temizle
                face.classList.remove('happy', 'sad', 'angry', 'surprised', 'fearful', 'disgusted', 'calm', 'neutral');
                
                // Yeni duygu sınıfını ekle
                face.classList.add(emotion);
                
                // Duygu yoğunluğunu yansıt
                face.style.setProperty('--intensity', intensity);
                
                // Duygulara özgü basit stil değişiklikleri
                switch (emotion) {
                    case 'happy':
                        mouth.style.borderRadius = '0 0 50% 50%';
                        mouth.style.height = `${40 * intensity}px`;
                        break;
                        
                    case 'sad':
                        mouth.style.borderRadius = '50% 50% 0 0';
                        mouth.style.height = `${30 * intensity}px`;
                        break;
                        
                    case 'angry':
                        mouth.style.borderRadius = '0';
                        mouth.style.height = '5px';
                        break;
                        
                    case 'surprised':
                        mouth.style.borderRadius = '50%';
                        mouth.style.height = `${50 * intensity}px`;
                        break;
                        
                    default:
                        mouth.style.borderRadius = '0 0 40px 40px';
                        mouth.style.height = '30px';
                }
            }
            
            // Simülasyon görüntülerini güncelle
            function updateSimulationDisplay(images) {
                const leftEye = document.querySelector('.face-preview .left-eye');
                const rightEye = document.querySelector('.face-preview .right-eye');
                const mouth = document.querySelector('.face-preview .mouth');
                const leds = document.querySelector('.face-preview .leds');
                
                // Sol göz
                if (images.left_eye) {
                    leftEye.style.backgroundImage = `url('/simulation/${images.left_eye}')`;
                }
                
                // Sağ göz
                if (images.right_eye) {
                    rightEye.style.backgroundImage = `url('/simulation/${images.right_eye}')`;
                }
                
                // Ağız
                if (images.mouth) {
                    mouth.style.backgroundImage = `url('/simulation/${images.mouth}')`;
                }
                
                // LED'ler
                if (images.leds) {
                    leds.style.backgroundImage = `url('/simulation/${images.leds}')`;
                }
            }
            
            // Günlük mesajı ekle
            function addLog(message, isError = false) {
                const logEntry = document.createElement('div');
                logEntry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
                
                if (isError) {
                    logEntry.style.color = 'red';
                }
                
                logViewer.appendChild(logEntry);
                logViewer.scrollTop = logViewer.scrollHeight;
                
                // Maksimum 100 mesaj tut
                while (logViewer.children.length > 100) {
                    logViewer.removeChild(logViewer.firstChild);
                }
            }
            
            // İlk başlangıç için günlük mesajı
            addLog('Dashboard yüklendi');
        });
        """