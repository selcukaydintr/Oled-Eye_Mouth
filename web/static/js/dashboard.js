// FACE1 Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Debug işaretçileri yapılandırması
    const DEBUG_MODE = true; // Geliştirme sırasında true, canlıda false
    const VERBOSE_LOGGING = true; // Ayrıntılı günlük
    
    // WebSocket bağlantıları
    window.socket = null; // *** Global olarak erişim için window.socket olarak değiştirdik ***
    let simulationSocket = null;
    let simulationActive = false;
    let reconnectAttempts = 0;
    const MAX_RECONNECT_ATTEMPTS = 5;
    const RECONNECT_DELAY_MS = 2000;
    
    // DOM elementleri
    const logViewer = document.getElementById('log-viewer');
    const emotionButtons = document.querySelectorAll('.emotion-btn');
    const animationButtons = document.querySelectorAll('.animation-btn');
    const themeSelect = document.getElementById('theme-select');
    const applyThemeButton = document.getElementById('apply-theme');
    const emotionIntensity = document.getElementById('emotion-intensity');
    const intensityValue = document.getElementById('intensity-value');
    const toggleSimulationButton = document.getElementById('toggle-simulation');
    const logLevelFilter = document.getElementById('log-level');
    const clearLogsButton = document.getElementById('clear-logs');
    
    // Yeni: Tab yapısı elementleri
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabContents = document.querySelectorAll('.tab-content');
    
    // Yeni: Animasyon elemanları
    const animationSelect = document.getElementById('animation-select');
    const animationDescription = document.getElementById('animation-description');
    const animationDuration = document.getElementById('animation-duration');
    const playAnimationButton = document.getElementById('play-animation');
    const stopAnimationButton = document.getElementById('stop-animation');
    const refreshAnimationsButton = document.getElementById('refresh-animations');
    
    // Durum değişkenleri
    let currentEmotion = 'neutral';
    let currentIntensity = 1.0;
    let availableAnimations = [];
    let currentAnimation = null;
    let currentLogLevel = 'all';
    let activeTab = 'dashboard';
    
    // Tab işlemleri
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const tabId = this.getAttribute('data-tab');
            
            // Aktif tab butonunu güncelle
            tabButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            
            // Aktif içeriği göster
            tabContents.forEach(content => content.classList.remove('active'));
            document.getElementById(`${tabId}-tab`).classList.add('active');
            
            // İlgili tab ile ilişkili işlemler
            handleTabChange(tabId);
            
            // Debug log
            if (DEBUG_MODE) {
                console.log(`[DEBUG] Tab değiştirildi: ${tabId}`);
            }
            
            // Aktif sekmeyi kaydet
            activeTab = tabId;
        });
    });
    
    // Log seviyesi filtreleme
    logLevelFilter.addEventListener('change', function() {
        currentLogLevel = this.value;
        applyLogFilter();
        
        if (DEBUG_MODE) {
            console.log(`[DEBUG] Log seviyesi değiştirildi: ${currentLogLevel}`);
        }
    });
    
    // Log temizleme
    clearLogsButton.addEventListener('click', function() {
        logViewer.innerHTML = '';
        if (DEBUG_MODE) {
            console.log('[DEBUG] Günlükler temizlendi');
        }
    });
    
    // Ana WebSocket bağlantısını aç
    function connectMainWebSocket() {
        if (socket && (socket.readyState === WebSocket.OPEN || socket.readyState === WebSocket.CONNECTING)) {
            return; // Zaten bağlıysa veya bağlanıyorsa işlem yapma
        }
        
        socket = new WebSocket(`ws://${window.location.host}/ws`);
        
        socket.onopen = function(e) {
            addLog('Dashboard WebSocket bağlantısı kuruldu', 'info');
            reconnectAttempts = 0; // Bağlantı başarılı, sayacı sıfırla
            
            // Animasyon listesini yükle
            loadAnimationList();
        };
        
        socket.onmessage = function(event) {
            const data = JSON.parse(event.data);
            
            // Mesaj tipine göre işlem yap
            switch (data.type) {
                case 'welcome':
                    addLog(data.message, 'info');
                    break;
                    
                case 'stats':
                    updateSystemStats(data.data);
                    break;
                    
                case 'theme_changed':
                    addLog(`Tema değiştirildi: ${data.theme}`, 'info');
                    themeSelect.value = data.theme;
                    break;
                    
                case 'emotion_changed':
                    const emotion = data.emotion;
                    updateFaceDisplay(emotion, data.intensity || 1.0);
                    addLog(`Duygu değiştirildi: ${emotion}`, 'info');
                    break;
                    
                case 'animation_started':
                    addLog(`Animasyon başladı: ${data.animation}`, 'info');
                    break;
                    
                case 'animation_stopped':
                case 'animation_completed':
                    addLog(`Animasyon bitti: ${data.animation}`, 'info');
                    break;
                    
                case 'volume_update':
                    updateVolumeDisplay(data.volume);
                    break;
                    
                case 'speaking_update':
                    updateSpeakingStatus(data.speaking);
                    break;
                    
                case 'error':
                    addLog(`Hata: ${data.message}`, 'error');
                    break;
            }
        };
        
        socket.onclose = function(event) {
            addLog('WebSocket bağlantısı kapatıldı', 'warn');
            
            // Bağlantı kesilmesi durumunda yeniden bağlanmayı dene
            if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
                reconnectAttempts++;
                const delay = RECONNECT_DELAY_MS * reconnectAttempts; // Artan gecikme süresi
                addLog(`${delay/1000} saniye sonra tekrar bağlanmaya çalışılacak (${reconnectAttempts}/${MAX_RECONNECT_ATTEMPTS})`, 'info');
                
                setTimeout(connectMainWebSocket, delay);
            } else {
                addLog('Maksimum yeniden bağlantı denemesi aşıldı. Sayfayı yenileyin.', 'error');
                showBadge('BAĞLANTI-HATASI', 'error');
            }
        };
        
        socket.onerror = function(error) {
            addLog('WebSocket hatası', 'error');
            console.error('WebSocket hatası:', error);
        };
    }
    
    // İlk bağlantıyı kur
    connectMainWebSocket();
    
    // Tema listesini yükle
    loadThemeList();
    
    // Simülasyon WebSocket bağlantısını başlat/durdur
    toggleSimulationButton.addEventListener('click', function() {
        if (simulationActive) {
            stopSimulation();
        } else {
            startSimulation();
        }
    });
    
    // Simülasyon akışını başlat
    function startSimulation() {
        if (simulationSocket) {
            simulationSocket.close();
        }
        
        addLog("Simülasyon akışı başlatılıyor...", 'info');
        simulationSocket = new WebSocket(`ws://${window.location.host}/ws/simulation`);
        
        simulationSocket.onopen = function() {
            simulationActive = true;
            toggleSimulationButton.textContent = "Simülasyon Akışını Durdur";
            toggleSimulationButton.classList.add("active");
            addLog("Simülasyon akışı başlatıldı", 'info');
            
            // Debug işaretçisini göster
            showBadge('SİMÜLASYON-AKTİF', 'info');
        };
        
        simulationSocket.onmessage = function(event) {
            try {
                const data = JSON.parse(event.data);
                
                if (data.type === 'simulation_update' && data.images) {
                    updateSimulationDisplay(data.images);
                    if (DEBUG_MODE && VERBOSE_LOGGING) {
                        console.log("Simülasyon veri alındı:", data);
                    }
                }
            } catch (error) {
                console.error("Simülasyon veri işleme hatası:", error);
                addLog("Simülasyon verisi işlenirken hata oluştu", 'error');
            }
        };
        
        simulationSocket.onclose = function(event) {
            simulationActive = false;
            toggleSimulationButton.textContent = "Simülasyon Akışını Başlat";
            toggleSimulationButton.classList.remove("active");
            
            // Beklenmedik kapanma durumunda uyarı göster
            if (event.code !== 1000) { // Normal kapanma dışında
                addLog(`Simülasyon WebSocket beklenmedik şekilde kapandı (kod: ${event.code})`, 'warn');
                showBadge('SİMÜLASYON-KAPANDI', 'warn');
                
                // 3 saniye sonra tekrar bağlanmayı dene
                setTimeout(() => {
                    if (!simulationActive) {
                        addLog("Simülasyon akışına tekrar bağlanmaya çalışılıyor...", 'info');
                        startSimulation();
                    }
                }, 3000);
            } else {
                addLog("Simülasyon akışı durduruldu", 'info');
                hideBadge('SİMÜLASYON-AKTİF');
            }
        };
        
        simulationSocket.onerror = function(error) {
            simulationActive = false;
            toggleSimulationButton.textContent = "Simülasyon Akışını Başlat";
            toggleSimulationButton.classList.remove("active");
            addLog("Simülasyon WebSocket hatası", 'error');
            console.error("Simülasyon bağlantı hatası:", error);
            
            // Hata işaretçisi göster
            showBadge('SİMÜLASYON-HATASI', 'error');
        };
    }
    
    // Simülasyon akışını durdur
    function stopSimulation() {
        if (simulationSocket) {
            simulationSocket.close(1000, "Kullanıcı tarafından kapatıldı");
            simulationSocket = null;
            simulationActive = false;
            toggleSimulationButton.textContent = "Simülasyon Akışını Başlat";
            toggleSimulationButton.classList.remove("active");
            addLog("Simülasyon akışı durduruldu", 'info');
            hideBadge('SİMÜLASYON-AKTİF');
            hideBadge('SİMÜLASYON-HATASI');
        }
    }
    
    // Duygu butonları
    emotionButtons.forEach(button => {
        button.addEventListener('click', function() {
            const emotion = this.getAttribute('data-emotion');
            const intensity = parseFloat(emotionIntensity.value);
            setEmotion(emotion, intensity);
        });
    });
    
    // Temel animasyon butonları
    animationButtons.forEach(button => {
        button.addEventListener('click', function() {
            const animation = this.getAttribute('data-animation');
            playBasicAnimation(animation);
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
    
    // Yeni: Animasyon seçimi
    animationSelect.addEventListener('change', function() {
        const selectedIndex = this.selectedIndex;
        
        if (selectedIndex >= 0 && selectedIndex < availableAnimations.length) {
            const selectedAnimation = availableAnimations[selectedIndex];
            currentAnimation = selectedAnimation;
            
            // Animasyon bilgilerini göster
            animationDescription.textContent = selectedAnimation.description || selectedAnimation.name;
            animationDuration.textContent = `Süre: ${selectedAnimation.duration || '?'} saniye`;
            
            // Oynat butonunu etkinleştir
            playAnimationButton.disabled = false;
        } else {
            currentAnimation = null;
            animationDescription.textContent = "Bir animasyon seçin";
            animationDuration.textContent = "";
            playAnimationButton.disabled = true;
        }
    });
    
    // Yeni: Animasyon oynatma butonu
    playAnimationButton.addEventListener('click', function() {
        if (currentAnimation) {
            playJsonAnimation(currentAnimation.name);
        }
    });
    
    // Yeni: Animasyonu durdurma butonu
    stopAnimationButton.addEventListener('click', function() {
        stopAnimation();
        this.disabled = true;
    });
    
    // Yeni: Animasyon listesini yenileme butonu
    refreshAnimationsButton.addEventListener('click', function() {
        loadAnimationList();
    });
    
    // Tab değişikliği işlemleri
    function handleTabChange(tabId) {
        switch (tabId) {
            case 'simulation':
                // Simülasyon sekmesi açıldığında son görüntüleri yükle
                if (!simulationActive) {
                    fetch('/api/simulation')
                        .then(response => response.json())
                        .then(data => {
                            if (data.images) {
                                updateSimulationDisplay(data.images);
                            }
                        })
                        .catch(error => {
                            if (DEBUG_MODE) {
                                console.error('Simülasyon yükleme hatası:', error);
                            }
                            addLog(`Simülasyon görüntüleri yüklenemedi: ${error.message}`, 'error');
                        });
                }
                break;
                
            case 'logs':
                // Günlük sekmesi açıldığında filtreleri uygula
                applyLogFilter();
                break;
        }
    }
    
    // Duygu ayarlama fonksiyonu
    function setEmotion(emotion, intensity) {
        if (!socket || socket.readyState !== WebSocket.OPEN) {
            addLog('WebSocket bağlantısı yok', 'error');
            return;
        }
        
        socket.send(JSON.stringify({
            action: 'set_emotion',
            emotion: emotion,
            intensity: intensity
        }));
        
        updateFaceDisplay(emotion, intensity);
    }
    
    // Temel animasyon oynatma fonksiyonu (eski)
    function playBasicAnimation(animation) {
        addLog(`Temel animasyon oynatılıyor: ${animation}`, 'info');
        
        socket.send(JSON.stringify({
            action: 'play_animation',
            animation: animation
        }));
    }
    
    // Yeni: JSON animasyonu oynatma fonksiyonu
    function playJsonAnimation(animationName) {
        addLog(`JSON animasyonu oynatılıyor: ${animationName}`, 'info');
        
        fetch(`/api/animations/${animationName}/play`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.status === 503) {
                throw new Error('Animasyon servisi şu anda çalışmıyor (503 Service Unavailable). Animasyon motorunun durumunu kontrol edin.');
            }
            if (!response.ok) {
                throw new Error(`Animasyon çalıştırılamadı (${response.status}: ${response.statusText})`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                addLog(`Animasyon başlatıldı: ${animationName}`, 'info');
                // Durdur butonunu etkinleştir
                stopAnimationButton.disabled = false;
                
                // Debug işaretçisi göster
                showBadge('ANİMASYON-ÇALIŞIYOR', 'info');
            } else {
                addLog(`Animasyon başlatılamadı: ${animationName} - ${data.message || 'Bilinmeyen hata'}`, 'error');
            }
        })
        .catch(error => {
            addLog(`Animasyon API hatası: ${error.message}`, 'error');
            showBadge('ANİMASYON-HATA', 'error');
        });
    }
    
    // Yeni: Animasyonu durdurma fonksiyonu
    function stopAnimation() {
        addLog("Animasyon durduruluyor...", 'info');
        
        fetch('/api/animations/stop', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => {
            if (response.status === 503) {
                throw new Error('Animasyon servisi şu anda çalışmıyor (503 Service Unavailable). Animasyon motorunun durumunu kontrol edin.');
            }
            if (!response.ok) {
                throw new Error(`Animasyon durdurulamadı (${response.status}: ${response.statusText})`);
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                addLog("Animasyon durduruldu", 'info');
                
                // Debug işaretçisi gizle
                hideBadge('ANİMASYON-ÇALIŞIYOR');
                hideBadge('ANİMASYON-HATA');
            } else {
                addLog(`Animasyon durdurulamadı: ${data.message || 'Bilinmeyen hata'}`, 'error');
            }
        })
        .catch(error => {
            addLog(`Animasyon durdurma API hatası: ${error.message}`, 'error');
            showBadge('ANİMASYON-DURDURMA-HATASI', 'error');
        });
    }
    
    // Yeni: Animasyon listesini yükleme fonksiyonu
    function loadAnimationList() {
        addLog("Animasyon listesi yükleniyor...", 'info');
        
        fetch('/api/animations')
            .then(response => {
                if (response.status === 503) {
                    throw new Error('Animasyon servisi şu anda çalışmıyor (503 Service Unavailable). Lütfen animasyon motorunun çalıştığından emin olun.');
                }
                if (!response.ok) {
                    throw new Error(`Animasyon listesi alınamadı (${response.status}: ${response.statusText})`);
                }
                return response.json();
            })
            .then(data => {
                availableAnimations = data.animations || [];
                
                // Listeyi temizle
                animationSelect.innerHTML = '';
                
                // Listeyi doldur
                if (availableAnimations.length > 0) {
                    availableAnimations.forEach(animation => {
                        const option = document.createElement('option');
                        option.value = animation.name;
                        option.textContent = animation.display_name || animation.name;
                        animationSelect.appendChild(option);
                    });
                    
                    addLog(`${availableAnimations.length} animasyon yüklendi`, 'info');
                    
                    // Debug bilgisi
                    if (DEBUG_MODE && VERBOSE_LOGGING) {
                        console.log('Yüklenen animasyonlar:', availableAnimations);
                    }
                } else {
                    const option = document.createElement('option');
                    option.textContent = "Hiç animasyon bulunamadı";
                    option.disabled = true;
                    animationSelect.appendChild(option);
                    
                    addLog("Hiç animasyon bulunamadı", 'warn');
                }
            })
            .catch(error => {
                addLog(`Animasyon listesi yüklenirken hata: ${error.message}`, 'error');
                showBadge('ANİMASYON-SERVİS-HATASI', 'error');
                
                // Hata durumunda boş bir seçenek ekle
                animationSelect.innerHTML = '';
                const option = document.createElement('option');
                option.textContent = "Animasyonlar yüklenemedi";
                option.disabled = true;
                animationSelect.appendChild(option);
                
                // Hata detayları ile kullanıcıya belirgin uyarı ver
                if (error.message.includes('503')) {
                    addLog("Animasyon sistemi servisi çalışmıyor. Kontrol panelinden animasyon motorunun durumunu kontrol edin.", 'warn');
                }
            });
    }
    
    // Yeni: Tema listesini yükleme fonksiyonu
    function loadThemeList() {
        addLog("Tema listesi yükleniyor...", 'info');
        
        fetch('/api/themes')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Tema listesi alınamadı');
                }
                return response.json();
            })
            .then(data => {
                const themes = data.themes || [];
                const currentTheme = data.current_theme || 'default';
                
                // Listeyi temizle
                themeSelect.innerHTML = '';
                
                // Listeyi doldur
                if (themes.length > 0) {
                    themes.forEach(theme => {
                        const option = document.createElement('option');
                        option.value = theme;
                        option.textContent = theme.charAt(0).toUpperCase() + theme.slice(1); // İlk harf büyük
                        
                        // Eğer mevcut tema ise seçili yap
                        if (theme === currentTheme) {
                            option.selected = true;
                        }
                        
                        themeSelect.appendChild(option);
                    });
                    
                    addLog(`${themes.length} tema yüklendi`, 'info');
                    
                    // Debug bilgisi
                    if (DEBUG_MODE && VERBOSE_LOGGING) {
                        console.log('Yüklenen temalar:', themes);
                    }
                } else {
                    const option = document.createElement('option');
                    option.value = "default";
                    option.textContent = "Varsayılan";
                    themeSelect.appendChild(option);
                    
                    addLog("Hiç tema bulunamadı, varsayılan tema kullanılıyor", 'warn');
                }
            })
            .catch(error => {
                addLog(`Tema listesi yüklenirken hata: ${error.message}`, 'error');
                
                // Hata durumunda varsayılan bir seçenek ekle
                themeSelect.innerHTML = '';
                const option = document.createElement('option');
                option.value = "default";
                option.textContent = "Varsayılan";
                themeSelect.appendChild(option);
                
                // Debug işaretçisi göster
                showBadge('TEMA-YÜKLENEMEDİ', 'error');
            });
    }
    
    // Tema değiştirme fonksiyonu
    function setTheme(theme) {
        if (!socket || socket.readyState !== WebSocket.OPEN) {
            addLog('WebSocket bağlantısı yok', 'error');
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
        
        // Yüksek CPU veya RAM kullanımında debug işareti göster
        if (stats.cpu && stats.cpu.percent > 80) {
            showBadge('YÜKSEK-CPU', 'warn');
        } else {
            hideBadge('YÜKSEK-CPU');
        }
        
        if (stats.memory && stats.memory.percent > 80) {
            showBadge('YÜKSEK-RAM', 'warn');
        } else {
            hideBadge('YÜKSEK-RAM');
        }
    }
    
    // Yüz görünümünü güncelle
    function updateFaceDisplay(emotion, intensity) {
        const face = document.querySelector('.face');
        const mouth = document.querySelector('.face .mouth');
        const leftEye = document.querySelector('.face .eye.left');
        const rightEye = document.querySelector('.face .eye.right');
        
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
        if (DEBUG_MODE && VERBOSE_LOGGING) {
            console.log("Simülasyon görüntüleri güncelleniyor:", images);
        }
        
        // Sol göz
        if (images.left_eye) {
            const leftEye = document.querySelector('.simulation-images .sim-left-eye');
            if (leftEye) {
                leftEye.style.backgroundImage = `url('/simulation/${images.left_eye}')`;
                leftEye.textContent = ''; // İçerideki yazıyı temizle
                addLog(`Sol göz görüntüsü güncellendi: ${images.left_eye}`, 'info', true); // Ayrıntı log
            } else if (DEBUG_MODE) {
                console.error("Sol göz elementi bulunamadı");
            }
        }
        
        // Sağ göz
        if (images.right_eye) {
            const rightEye = document.querySelector('.simulation-images .sim-right-eye');
            if (rightEye) {
                rightEye.style.backgroundImage = `url('/simulation/${images.right_eye}')`;
                rightEye.textContent = ''; // İçerideki yazıyı temizle
                addLog(`Sağ göz görüntüsü güncellendi: ${images.right_eye}`, 'info', true); // Ayrıntı log
            } else if (DEBUG_MODE) {
                console.error("Sağ göz elementi bulunamadı");
            }
        }
        
        // Ağız
        if (images.mouth) {
            const mouth = document.querySelector('.simulation-images .sim-mouth');
            if (mouth) {
                mouth.style.backgroundImage = `url('/simulation/${images.mouth}')`;
                mouth.textContent = ''; // İçerideki yazıyı temizle
                addLog(`Ağız görüntüsü güncellendi: ${images.mouth}`, 'info', true); // Ayrıntı log
            } else if (DEBUG_MODE) {
                console.error("Ağız elementi bulunamadı");
            }
        }
        
        // LED'ler
        if (images.leds) {
            const leds = document.querySelector('.simulation-images .sim-leds');
            if (leds) {
                leds.style.backgroundImage = `url('/simulation/${images.leds}')`;
                leds.textContent = ''; // İçerideki yazıyı temizle
                addLog(`LED görüntüsü güncellendi: ${images.leds}`, 'info', true); // Ayrıntı log
            } else if (DEBUG_MODE) {
                console.error("LED elementi bulunamadı");
            }
        }
        
        // Tüm görüntüler boşsa
        if (!images.left_eye && !images.right_eye && !images.mouth && !images.leds) {
            addLog("Hiç simülasyon görüntüsü bulunamadı", 'warn');
        }
    }
    
    // Ses seviyesini görsel olarak gösterme
    function updateVolumeDisplay(volume) {
        // DOM elementlerini al
        const volumeMeter = document.getElementById('volume-meter');
        const volumeValue = document.getElementById('volume-value');
        
        if (volumeMeter && volumeValue) {
            // Ses seviyesi değerini metni güncelle (0.00 - 1.00)
            volumeValue.textContent = volume.toFixed(2);
            
            // Ses çubuğunu güncelle (0% - 100%)
            volumeMeter.style.width = `${volume * 100}%`;
        }
    }
    
    // Konuşma durumunu güncelleme
    function updateSpeakingStatus(isSpeaking) {
        const speakingStatus = document.getElementById('speaking-status');
        
        if (speakingStatus) {
            if (isSpeaking) {
                speakingStatus.textContent = 'Konuşuyor';
                speakingStatus.classList.add('active');
                // Konuşma sırasında ses göstergesini animasyonlu hale getir
                document.querySelector('.volume-meter').style.transition = 'width 0.1s ease';
                
                // Debug işaretçisi
                showBadge('KONUŞUYOR', 'info');
            } else {
                speakingStatus.textContent = 'Sessiz';
                speakingStatus.classList.remove('active');
                // Konuşma bittiğinde ses göstergesini daha yavaş güncelle
                document.querySelector('.volume-meter').style.transition = 'width 0.5s ease';
                
                // Debug işaretçisi
                hideBadge('KONUŞUYOR');
            }
        }
    }
    
    // Günlük mesajı ekle
    function addLog(message, level = 'info', silent = false) {
        // Sessiz mod için - konsolda göster ama arayüzde gösterme
        if (silent && !VERBOSE_LOGGING) return;
        
        // Log girdisini oluştur
        const logEntry = document.createElement('div');
        logEntry.textContent = `[${new Date().toLocaleTimeString()}] ${message}`;
        logEntry.dataset.level = level;
        
        // Log seviyesine göre stil uygula
        switch (level) {
            case 'error':
                logEntry.style.color = 'red';
                logEntry.classList.add('log-error');
                break;
            case 'warn':
                logEntry.style.color = 'orange';
                logEntry.classList.add('log-warn');
                break;
            case 'info':
                logEntry.classList.add('log-info');
                break;
        }
        
        // Log görünümüne ekle
        logViewer.appendChild(logEntry);
        logViewer.scrollTop = logViewer.scrollHeight;
        
        // Maksimum 100 mesaj tut
        while (logViewer.children.length > 100) {
            logViewer.removeChild(logViewer.firstChild);
        }
        
        // Log filtresini uygula
        if (currentLogLevel !== 'all' && level !== currentLogLevel) {
            logEntry.style.display = 'none';
        }
        
        // Debug konsolu
        if (DEBUG_MODE) {
            switch (level) {
                case 'error':
                    console.error(`[FACE1] ${message}`);
                    break;
                case 'warn':
                    console.warn(`[FACE1] ${message}`);
                    break;
                case 'info':
                    console.info(`[FACE1] ${message}`);
                    break;
            }
        }
    }
    
    // Log filtresini uygula
    function applyLogFilter() {
        const logEntries = logViewer.querySelectorAll('div');
        
        logEntries.forEach(entry => {
            if (currentLogLevel === 'all' || entry.dataset.level === currentLogLevel) {
                entry.style.display = '';
            } else {
                entry.style.display = 'none';
            }
        });
    }
    
    // Debug işaretçileri için fonksiyonlar
    function showBadge(message, level = 'info') {
        if (!DEBUG_MODE) return;
        
        let badge = document.querySelector(`.debug-badge[data-message="${message}"]`);
        
        if (!badge) {
            badge = document.createElement('span');
            badge.className = `debug-badge debug-${level}`;
            badge.dataset.message = message;
            badge.textContent = message;
            
            // Badge'i ekranın sağ üst köşesine yerleştir
            badge.style.position = 'fixed';
            badge.style.top = `${70 + document.querySelectorAll('.debug-badge[style*="position: fixed"]').length * 30}px`;
            badge.style.right = '20px';
            badge.style.zIndex = '1000';
            
            document.body.appendChild(badge);
        }
        
        // Sınıf güncelle
        badge.className = `debug-badge debug-${level}`;
    }
    
    function hideBadge(message) {
        if (!DEBUG_MODE) return;
        
        const badge = document.querySelector(`.debug-badge[data-message="${message}"]`);
        if (badge) {
            badge.remove();
            
            // Diğer badge'lerin pozisyonunu yeniden ayarla
            const badges = document.querySelectorAll('.debug-badge[style*="position: fixed"]');
            badges.forEach((b, index) => {
                b.style.top = `${70 + index * 30}px`;
            });
        }
    }
    
    // Sayfa yüklendiğinde son simülasyon görüntülerini al
    fetch('/api/simulation')
        .then(response => {
            if (!response.ok) {
                throw new Error('Simülasyon görüntüleri alınamadı');
            }
            return response.json();
        })
        .then(data => {
            if (data.images) {
                updateSimulationDisplay(data.images);
                addLog('Simülasyon görüntüleri yüklendi', 'info');
            }
        })
        .catch(error => {
            addLog(`API hatası: ${error.message}`, 'error');
        });
    
    // İlk başlangıç için günlük mesajı
    addLog('Dashboard yüklendi', 'info');
    
    if (DEBUG_MODE) {
        showBadge('DEBUG-MODU-AKTİF', 'info');
        console.log('[FACE1] Dashboard.js çalıştırıldı - DEBUG MODU ETKİN');
    }
});
