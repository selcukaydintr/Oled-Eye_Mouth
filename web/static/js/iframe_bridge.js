/**
 * ===========================================================
 * Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
 * Dosya: iframe_bridge.js
 * Açıklama: FACE1 ve üst proje arasındaki iletişimi sağlayan IFrame köprü sınıfı
 * Bağımlılıklar: -
 * Bağlı Dosyalar: state_reflector.js, iframe_integration.html, parent_integration_example.html
 * 
 * Versiyon: 0.5.0
 * Değişiklikler:
 * - [0.1.0] İlk sürüm oluşturuldu
 * - [0.3.0] Güvenlik güncellemeleri ve mesaj doğrulama eklendi
 * - [0.5.0] State Reflection Protocol desteği eklendi
 * - [0.5.0] iki yönlü olay iletimi desteği güçlendirildi
 * 
 * Yazar: GitHub Copilot
 * Son Güncelleme: 2025-05-04
 * ===========================================================
 */

/**
 * IFrameBridge - FACE1 ve üst proje arasındaki güvenli iletişimi sağlayan köprü sınıfı
 * Bu sınıf, iframe içindeki ve dışındaki kodun güvenli bir şekilde haberleşmesini sağlar
 */
class IFrameBridge {
    /**
     * IFrameBridge'i başlatır
     * @param {Object} options - Yapılandırma seçenekleri
     * @param {string[]} options.allowedOrigins - İzin verilen üst proje domain'leri
     * @param {Function} options.onMessage - Mesaj alındığında çağrılacak fonksiyon
     * @param {Function} options.onConnection - Bağlantı kurulduğunda çağrılacak fonksiyon
     * @param {Function} options.onError - Hata durumunda çağrılacak fonksiyon
     * @param {boolean} options.autoResize - Otomatik boyut adaptasyonu aktif mi (varsayılan: true)
     * @param {boolean} options.autoThemeSync - Otomatik tema senkronizasyonu aktif mi (varsayılan: true)
     * @param {boolean} options.strictSecurity - Sıkı güvenlik kontrollerini aktif eder (varsayılan: true)
     * @param {boolean} options.enableStateReflection - Durum yansıtma protokolünü aktifleştirir (varsayılan: true)
     */
    constructor(options = {}) {
        this.allowedOrigins = options.allowedOrigins || ['*'];
        this.onMessageCallback = options.onMessage || null;
        this.onConnectionCallback = options.onConnection || null;
        this.onErrorCallback = options.onError || null;
        this.autoResize = options.autoResize !== undefined ? options.autoResize : true;
        this.autoThemeSync = options.autoThemeSync !== undefined ? options.autoThemeSync : true;
        this.strictSecurity = options.strictSecurity !== undefined ? options.strictSecurity : true;
        this.enableStateReflection = options.enableStateReflection !== undefined ? options.enableStateReflection : true;
        this.parentOrigin = null;
        this.connected = false;
        this.messageQueue = [];
        this.messageHandlers = {};
        this.securityToken = null; // Üst projeden doğrulanmış güvenlik token'ı
        
        // Durum yansıtma protokolü için StateReflector referansı
        this.stateReflector = null;
        
        // Mesaj sayacı ve hız sınırlama (DoS koruması)
        this.messageCounter = 0;
        this.lastMessageTime = Date.now();
        this.rateLimitThreshold = 100; // 1 sn içinde max mesaj sayısı
        this.rateLimitResetInterval = 1000; // ms
        this.isRateLimited = false;
        
        // Event listener'ı ekle
        this.setupMessageListener();
        
        // Hazır olduğumuzda üst pencereyi bilgilendir
        this.sendReadySignal();
        
        // Otomatik boyut adaptasyonu için resize eventlerini dinle
        if (this.autoResize) {
            this.setupAutomaticResizing();
        }
        
        // Tema dinleme
        this.setupThemeListener();
        
        // Hız sınırlama kontrolü için periyodik sıfırlama
        setInterval(() => {
            this.messageCounter = 0;
            this.isRateLimited = false;
            this.lastMessageTime = Date.now();
        }, this.rateLimitResetInterval);
    }
    
    /**
     * Mesaj dinleyicisini kurar
     */
    setupMessageListener() {
        window.addEventListener('message', this.handleMessage.bind(this), false);
        console.log('IFrameBridge: Mesaj dinleyici kuruldu');
    }
    
    /**
     * Hazır sinyali gönderir
     */
    sendReadySignal() {
        try {
            // iframe içinde olduğumuzu kontrol et
            if (window.self !== window.top) {
                window.parent.postMessage({
                    type: 'FACE1_READY',
                    version: '0.5.0',
                    capabilities: this.getCapabilities(),
                    dimensions: {
                        width: document.body.scrollWidth,
                        height: document.body.scrollHeight
                    }
                }, '*'); // Başlangıçta '*' kullanıyoruz, sonra spesifik origin'e geçiyoruz
                console.log('IFrameBridge: Hazır sinyali gönderildi');
            } else {
                console.warn('IFrameBridge: iframe içinde değil, ana pencerede çalışıyor');
            }
        } catch (e) {
            this.handleError('Hazır sinyali gönderilirken hata oluştu', e);
        }
    }
    
    /**
     * Desteklenen özellikleri döndürür
     * @returns {Object} Desteklenen özellikler
     */
    getCapabilities() {
        return {
            emotions: true,
            animations: true,
            themes: true,
            configuration: true,
            metrics: true,
            lifecycle: true,
            responsive: true,
            adaptiveTheming: this.autoThemeSync,
            adaptiveLayout: this.autoResize,
            secureCommunication: this.strictSecurity
        };
    }
    
    /**
     * Mesaj alındığında işler
     * @param {MessageEvent} event - MessageEvent nesnesi
     */
    handleMessage(event) {
        try {
            // Mesajın geçerli olup olmadığını kontrol et
            if (!event.data || typeof event.data !== 'object') {
                return;
            }
            
            // Origin kontrolü (güvenlik)
            if (!this.isAllowedOrigin(event.origin)) {
                console.warn(`IFrameBridge: İzin verilmeyen kaynak: ${event.origin}`);
                return;
            }
            
            // Hız sınırlama kontrolü (DoS koruması)
            if (this.checkRateLimit()) {
                console.warn(`IFrameBridge: Hız sınırı aşıldı, mesajlar geçici olarak engellendi`);
                return;
            }
            
            const message = event.data;
            
            // İlk bağlantı mesajı kontrolü
            if (message.type === 'FACE1_CONNECT') {
                this.handleConnectionRequest(event);
                return;
            }
            
            // Bağlantı kontrolü
            if (!this.connected) {
                this.messageQueue.push(event);
                console.log('IFrameBridge: Bağlantı kurulmadan mesaj alındı, kuyruğa eklendi');
                return;
            }
            
            // Güvenlik token kontrolü (bağlantı kurulduktan sonra)
            if (this.strictSecurity && this.securityToken && 
                (!message.securityToken || message.securityToken !== this.securityToken)) {
                console.warn(`IFrameBridge: Geçersiz güvenlik token'ı`);
                this.notifyError("Güvenlik ihlali: Geçersiz güvenlik token'ı", new Error("Token mismatch"));
                return;
            }
            
            // Mesaj tipine göre işleme
            const handler = this.messageHandlers[message.type] || this.defaultMessageHandler;
            handler.call(this, message, event.origin);
            
            // Callback çağrısı
            if (this.onMessageCallback) {
                this.onMessageCallback(message, event.origin);
            }
        } catch (e) {
            this.handleError('Mesaj işlenirken hata oluştu', e);
        }
    }
    
    /**
     * Bağlantı isteğini işler
     * @param {MessageEvent} event - MessageEvent nesnesi
     */
    handleConnectionRequest(event) {
        // Bağlantı verilerini doğrula
        if (!event.data.data || !event.data.data.clientId) {
            console.warn('IFrameBridge: Geçersiz bağlantı verisi');
            return;
        }
        
        this.parentOrigin = event.origin;
        this.connected = true;
        
        // Güvenlik token'ını kaydet
        if (event.data.data.securityToken) {
            this.securityToken = event.data.data.securityToken;
        }
        
        // Bağlantı yanıtı gönder
        window.parent.postMessage({
            type: 'FACE1_CONNECTED',
            status: 'ok',
            dimensions: {
                width: document.body.scrollWidth,
                height: document.body.scrollHeight
            },
            securityToken: this.securityToken, // Güvenlik token'ını geri gönder
            timestamp: Date.now()
        }, this.parentOrigin);
        
        // Kuyrukta bekleyen mesajları işle
        while (this.messageQueue.length > 0) {
            const queuedEvent = this.messageQueue.shift();
            this.handleMessage(queuedEvent);
        }
        
        // Callback çağrısı
        if (this.onConnectionCallback) {
            this.onConnectionCallback(this.parentOrigin);
        }
        
        // Bağlantı kurulduğunda temayı üst projeden sorgula
        if (this.autoThemeSync) {
            this.requestTheme();
        }
        
        // Durum yansıtma protokolünü başlat
        if (this.enableStateReflection && typeof StateReflector !== 'undefined') {
            this.initStateReflection();
        }
        
        console.log(`IFrameBridge: Bağlantı kuruldu - Origin: ${this.parentOrigin}`);
    }
    
    /**
     * Origin'in izin verilen listede olup olmadığını kontrol eder
     * @param {string} origin - Kontrol edilecek origin
     * @returns {boolean} - Origin'in izin verilip verilmediği
     */
    isAllowedOrigin(origin) {
        // '*' tüm origin'lere izin verir (geliştirme için, üretimde önerilmez)
        if (this.allowedOrigins.includes('*')) {
            return true;
        }
        return this.allowedOrigins.includes(origin);
    }
    
    /**
     * Hız sınırlama kontrolü yapar (DoS koruması)
     * @returns {boolean} - Hız sınırının aşılıp aşılmadığı
     */
    checkRateLimit() {
        this.messageCounter++;
        
        const currentTime = Date.now();
        const timeElapsed = currentTime - this.lastMessageTime;
        
        // Zaman aralığı sıfırlandıysa sayacı da sıfırla
        if (timeElapsed > this.rateLimitResetInterval) {
            this.messageCounter = 1;
            this.lastMessageTime = currentTime;
            this.isRateLimited = false;
            return false;
        }
        
        // Hız sınırının aşılıp aşılmadığını kontrol et
        if (this.messageCounter > this.rateLimitThreshold) {
            this.isRateLimited = true;
            return true;
        }
        
        return this.isRateLimited;
    }
    
    /**
     * Varsayılan mesaj işleyici
     * @param {Object} message - Mesaj içeriği
     * @param {string} origin - Mesajın geldiği origin
     */
    defaultMessageHandler(message, origin) {
        console.log(`IFrameBridge: İşlenmemiş mesaj tipi: ${message.type}`, message);
    }
    
    /**
     * Üst pencereye mesaj gönderir
     * @param {string} type - Mesaj tipi
     * @param {Object} data - Mesaj verileri
     * @returns {boolean} - Mesajın gönderilip gönderilmediği
     */
    sendMessage(type, data = {}) {
        try {
            if (!this.connected || !this.parentOrigin) {
                console.warn('IFrameBridge: Bağlantı kurulmadan mesaj gönderme girişimi');
                return false;
            }
            
            const message = {
                type: type,
                data: data,
                timestamp: Date.now()
            };
            
            // Güvenlik token'ını ekle
            if (this.strictSecurity && this.securityToken) {
                message.securityToken = this.securityToken;
            }
            
            window.parent.postMessage(message, this.parentOrigin);
            return true;
        } catch (e) {
            this.handleError('Mesaj gönderilirken hata oluştu', e);
            return false;
        }
    }
    
    /**
     * Belirli mesaj tipi için işleyici ekler
     * @param {string} messageType - Mesaj tipi
     * @param {Function} handler - İşleyici fonksiyon
     */
    addMessageHandler(messageType, handler) {
        if (typeof handler !== 'function') {
            console.error('IFrameBridge: İşleyici bir fonksiyon olmalıdır');
            return;
        }
        
        this.messageHandlers[messageType] = handler;
    }
    
    /**
     * Duygu durumu değişikliğini üst pencereye bildirir ve iç olayı tetikler
     * @param {string} emotion - Duygu adı
     * @param {number} intensity - Duygu yoğunluğu (0-1 arası)
     */
    notifyEmotionChange(emotion, intensity) {
        this.sendMessage('FACE1_EMOTION_CHANGE', {
            emotion: emotion,
            intensity: intensity
        });
        
        // Duygu değişikliği olayını belgeye yayınla (iç bileşenler için)
        this.dispatchInternalEvent('emotionChanged', {
            emotion: emotion,
            intensity: intensity
        });
    }
    
    /**
     * Animasyon değişikliğini üst pencereye bildirir ve iç olayı tetikler
     * @param {string} animationName - Animasyon adı
     * @param {number} progress - İlerleme durumu (0-1 arası)
     * @param {boolean} isPlaying - Animasyonun oynatılıp oynatılmadığı
     */
    notifyAnimationUpdate(animationName, progress, isPlaying) {
        this.sendMessage('FACE1_ANIMATION_UPDATE', {
            animation: animationName,
            progress: progress,
            playing: isPlaying
        });
        
        // Animasyon değişikliği olayını belgeye yayınla (iç bileşenler için)
        this.dispatchInternalEvent('animationChanged', {
            animation: animationName,
            progress: progress,
            playing: isPlaying
        });
    }
    
    /**
     * Sistem metrikleri güncellemesini üst pencereye bildirir
     * @param {Object} metrics - Sistem metrikleri
     */
    notifyMetricsUpdate(metrics) {
        this.sendMessage('FACE1_METRICS_UPDATE', {
            metrics: metrics
        });
    }
    
    /**
     * Plugin durum değişikliğini üst pencereye bildirir
     * @param {string} state - Plugin durumu
     * @param {Object} details - Ek detaylar
     */
    notifyStateChange(state, details = {}) {
        this.sendMessage('FACE1_STATE_CHANGE', {
            state: state,
            details: details,
            timestamp: Date.now()
        });
        
        // Durum değişikliği olayını belgeye yayınla (iç bileşenler için)
        this.dispatchInternalEvent('systemStateChanged', {
            state: state,
            details: details
        });
    }
    
    /**
     * Konuşma durumu değişikliğini üst pencereye bildirir
     * @param {boolean} isSpeaking - Konuşma durumu
     */
    notifySpeakingUpdate(isSpeaking) {
        this.sendMessage('FACE1_SPEAKING_UPDATE', {
            speaking: isSpeaking
        });
        
        // Konuşma durumu değişikliği olayını belgeye yayınla
        this.dispatchInternalEvent('speakingChanged', {
            speaking: isSpeaking
        });
    }
    
    /**
     * Çevresel faktör değişikliğini üst pencereye bildirir
     * @param {string} factor - Faktör adı (light, temperature, humidity, motion, touch)
     * @param {string} state - Faktör durumu
     * @param {number} value - Faktör değeri
     */
    notifyEnvironmentUpdate(factor, state, value) {
        this.sendMessage('FACE1_ENVIRONMENT_UPDATE', {
            factor: factor,
            state: state,
            value: value
        });
        
        // Çevresel faktör değişikliği olayını belgeye yayınla
        this.dispatchInternalEvent('environmentChanged', {
            factor: factor,
            state: state,
            value: value
        });
    }
    
    /**
     * Hata durumlarını işler ve üst projeye bildirir
     * @param {string} message - Hata mesajı
     * @param {Error} error - Hata nesnesi
     */
    handleError(message, error) {
        console.error(`IFrameBridge Hatası: ${message}`, error);
        
        // Üst projeye hata bildir
        if (this.connected && this.parentOrigin) {
            try {
                window.parent.postMessage({
                    type: 'FACE1_ERROR',
                    data: {
                        message: message,
                        errorType: error ? error.name : 'Unknown',
                        errorDetails: error ? error.message : ''
                    },
                    securityToken: this.securityToken,
                    timestamp: Date.now()
                }, this.parentOrigin);
            } catch (e) {
                // Hata bildiriminde hata oluştuysa sadece log yazalım
                console.error('Hata bildirimi gönderilirken ek hata oluştu:', e);
            }
        }
        
        if (this.onErrorCallback) {
            this.onErrorCallback(message, error);
        }
    }
    
    /**
     * Hata durumunu üst pencereye bildirir
     * @param {string} message - Hata mesajı 
     * @param {Error} error - Hata nesnesi (isteğe bağlı)
     */
    notifyError(message, error = null) {
        if (this.connected && this.parentOrigin) {
            this.sendMessage('FACE1_ERROR', {
                message: message,
                errorType: error ? error.name : 'Unknown',
                errorDetails: error ? error.message : ''
            });
        }
        
        if (this.onErrorCallback) {
            this.onErrorCallback(message, error || new Error(message));
        }
    }
    
    /**
     * IFrame'in boyut değişikliklerini üst pencereye bildirir
     * @param {number} width - Genişlik (piksel)
     * @param {number} height - Yükseklik (piksel)
     */
    notifyResize(width, height) {
        this.sendMessage('FACE1_RESIZE', {
            width: width,
            height: height
        });
    }
    
    /**
     * Otomatik boyut adaptasyonu için resize olaylarını dinler
     */
    setupAutomaticResizing() {
        // ResizeObserver API'sini kullan (modern tarayıcılar destekler)
        if (window.ResizeObserver) {
            const ro = new ResizeObserver(entries => {
                for (let entry of entries) {
                    const { width, height } = entry.contentRect;
                    if (this.connected) {
                        this.notifyResize(Math.ceil(width), Math.ceil(height));
                    }
                }
            });
            
            ro.observe(document.body);
            console.log('IFrameBridge: Otomatik boyut adaptasyonu (ResizeObserver) aktifleştirildi');
        } else {
            // Fallback: window resize olayını dinle
            window.addEventListener('resize', () => {
                if (this.connected) {
                    this.notifyResize(
                        document.body.scrollWidth, 
                        document.body.scrollHeight
                    );
                }
            });
            console.log('IFrameBridge: Otomatik boyut adaptasyonu (resize event) aktifleştirildi');
        }
        
        // MutationObserver ile DOM değişikliklerini izle (içerik değişince boyut da değişebilir)
        const mo = new MutationObserver(() => {
            if (this.connected) {
                // Throttle amaçlı kısa gecikme ver
                setTimeout(() => {
                    this.notifyResize(
                        document.body.scrollWidth, 
                        document.body.scrollHeight
                    );
                }, 100);
            }
        });
        
        mo.observe(document.body, { 
            childList: true, 
            subtree: true, 
            attributes: true,
            attributeFilter: ['style', 'class']
        });
        
        console.log('IFrameBridge: İçerik değişikliği izleme aktifleştirildi');
    }
    
    /**
     * IFrame'in tema değişikliklerini yakalar ve uygular
     */
    setupThemeListener() {
        this.addMessageHandler('FACE1_SET_THEME', (message) => {
            const theme = message.data.theme;
            
            // CSS sınıfı uygulama
            if (theme === 'dark') {
                document.body.classList.add('dark-theme');
                document.body.classList.remove('light-theme');
            } else {
                document.body.classList.add('light-theme');
                document.body.classList.remove('dark-theme');
            }
            
            console.log(`IFrameBridge: Tema değiştirildi - ${theme}`);
            
            // Tema değişikliğini diğer elemanlara da bildir (özel event)
            const themeEvent = new CustomEvent('themeChanged', {
                detail: { theme }
            });
            document.dispatchEvent(themeEvent);
        });
    }
    
    /**
     * Üst projeden tema bilgisini talep eder
     */
    requestTheme() {
        if (this.connected) {
            this.sendMessage('FACE1_REQUEST_THEME');
            console.log('IFrameBridge: Tema bilgisi talep edildi');
        }
    }
    
    /**
     * Üst projeye CSS özelliklerini bildirir
     * Dashboard'un üst projenin stillerine uyum sağlaması için
     * @param {Object} cssProperties - CSS özellikleri
     */
    notifyCssProperties(cssProperties) {
        this.sendMessage('FACE1_CSS_PROPERTIES', {
            cssProperties
        });
    }
    
    /**
     * Durum yansıtma protokolünü başlatır
     */
    initStateReflection() {
        if (!this.enableStateReflection) {
            return;
        }
        
        try {
            // StateReflector sınıfı yüklü mü kontrol et
            if (typeof StateReflector !== 'function') {
                console.warn('IFrameBridge: StateReflector sınıfı yüklenmemiş, durum yansıtma devre dışı.');
                return;
            }
            
            // StateReflector örneği oluştur
            this.stateReflector = new StateReflector(this, {
                debug: true,
                pollInterval: 2000 // Her 2 saniyede bir durum güncellemesi
            });
            
            // Reflector'ı başlat
            this.stateReflector.start();
            
            console.log('IFrameBridge: Durum yansıtma protokolü başlatıldı');
            
            // Durum protokolü hazır bilgisini üst projeye gönder
            this.sendMessage('FACE1_STATE_REFLECTION_READY', {
                status: 'active',
                pollInterval: this.stateReflector.pollInterval,
                stateTypes: ['system', 'emotion', 'animation', 'metrics', 'speaking', 'environment']
            });
        } catch (e) {
            console.error('IFrameBridge: Durum yansıtma protokolü başlatılırken hata:', e);
        }
    }
    
    /**
     * Durum yansıtma protokolünü durdurur
     */
    stopStateReflection() {
        if (this.stateReflector) {
            this.stateReflector.stop();
            this.stateReflector = null;
            console.log('IFrameBridge: Durum yansıtma protokolü durduruldu');
            
            // Durum protokolünün durduğunu bildir
            if (this.connected) {
                this.sendMessage('FACE1_STATE_REFLECTION_STOPPED');
            }
        }
    }
    
    /**
     * Bağlantı kesildiğinde çağrılır
     */
    handleDisconnect() {
        if (!this.connected) {
            return;
        }
        
        // Durum yansıtmayı durdur
        this.stopStateReflection();
        
        this.connected = false;
        this.parentOrigin = null;
        this.securityToken = null;
        
        console.log('IFrameBridge: Bağlantı kesildi');
    }
    
    /**
     * İç bileşenler için olay tetikler
     * @param {string} eventName - Olay adı
     * @param {Object} detail - Olay detayları
     */
    dispatchInternalEvent(eventName, detail = {}) {
        const event = new CustomEvent(eventName, { 
            detail: detail,
            bubbles: true
        });
        
        document.dispatchEvent(event);
    }
    
    /**
     * Üst pencereden durum yansıtma modu kontrolü için işleyici
     * @param {Object} message - Gelen mesaj
     */
    handleStateReflectionControl(message) {
        const command = message.data && message.data.command;
        
        switch (command) {
            case 'start':
                if (!this.stateReflector && this.enableStateReflection) {
                    this.initStateReflection();
                } else if (this.stateReflector) {
                    this.stateReflector.start();
                }
                break;
                
            case 'stop':
                this.stopStateReflection();
                break;
                
            case 'configure':
                if (this.stateReflector && message.data.options) {
                    // Yapılandırma ayarlarını güncelle
                    if (message.data.options.pollInterval && typeof message.data.options.pollInterval === 'number') {
                        this.stateReflector.pollInterval = message.data.options.pollInterval;
                        
                        // Çalışıyorsa yeniden başlat
                        if (this.stateReflector.isRunning) {
                            this.stateReflector.stop();
                            this.stateReflector.start();
                        }
                    }
                }
                break;
                
            case 'snapshot':
                // Anlık durum özeti talebi
                if (this.stateReflector) {
                    const snapshot = this.stateReflector.getStateSnapshot();
                    this.sendMessage('FACE1_STATE_SNAPSHOT', snapshot);
                }
                break;
        }
    }
}

// Global olarak erişilebilir yap
window.IFrameBridge = IFrameBridge;