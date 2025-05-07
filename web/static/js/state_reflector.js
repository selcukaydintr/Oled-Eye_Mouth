/**
 * ===========================================================
 * Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
 * Dosya: state_reflector.js
 * Açıklama: Durum yansıtma protokolü (State Reflection Protocol) için gerekli sınıf
 * Bağımlılıklar: iframe_bridge.js
 * Bağlı Dosyalar: parent_integration_example.html, iframe_integration.html, state_reflection_demo.html
 * 
 * Versiyon: 0.5.0
 * Değişiklikler:
 * - [0.1.0] İlk oluşturma - Durum yansıtma protokolü işlevselliği
 * - [0.5.0] Otomatik durum yönetimi iyileştirildi
 * - [0.5.0] İki yönlü durum senkronizasyonu eklendi
 * - [0.5.0] Olay dinleme mekanizmaları geliştirildi
 * 
 * Yazar: GitHub Copilot
 * Son Güncelleme: 2025-05-04
 * ===========================================================
 */

/**
 * StateReflector - FACE1 ve üst proje arasında durum değişikliklerini takip eder ve yansıtır
 * IFrameBridge ile çalışan bu sınıf, FACE1 durumlarını toplar ve belirli aralıklarla üst projeye bildirir
 */
class StateReflector {
    /**
     * StateReflector'ı başlatır
     * @param {IFrameBridge} bridge - İletişim için kullanılacak IFrameBridge örneği
     * @param {Object} options - Yapılandırma seçenekleri
     * @param {boolean} options.debug - Hata ayıklama mesajlarını gösterme durumu
     * @param {number} options.pollInterval - Durum kontrolü aralığı (ms)
     */
    constructor(bridge, options = {}) {
        if (!bridge || typeof bridge !== 'object') {
            throw new Error('StateReflector: Geçerli bir IFrameBridge örneği gerekli');
        }
        
        this.bridge = bridge;
        this.debug = options.debug || false;
        this.pollInterval = options.pollInterval || 2000; // Default: 2 saniye
        
        // Durum değişkenlerini saklar
        this.lastStates = {
            system: 'READY',
            emotion: {
                current: 'neutral',
                intensity: 1.0
            },
            speaking: false,
            animation: {
                current: null,
                progress: 0,
                playing: false
            },
            environment: {
                light: null,
                temperature: null,
                humidity: null,
                motion: null,
                touch: null
            },
            metrics: {
                cpu: 25,
                memory: 30,
                temperature: 45,
                uptime: 0
            }
        };
        
        // Durum değişikliği dinleyicileri
        this.stateChangeListeners = {};
        this.pollTimer = null;
        this.isRunning = false;
        
        // Olay dinleyicileri ekle
        this._setupEventListeners();
    }
    
    /**
     * Durum yansıtma işlemini başlatır
     */
    start() {
        if (this.isRunning) {
            this._log('Durum yansıtma zaten çalışıyor');
            return;
        }
        
        this.isRunning = true;
        
        // İlk durum anlık görüntüsünü al
        this._captureCurrentStates();
        
        // Düzenli durum kontrol döngüsünü başlat
        this.pollTimer = setInterval(() => {
            this._captureCurrentStates();
        }, this.pollInterval);
        
        this._log(`Durum yansıtma başlatıldı (${this.pollInterval}ms aralıklarla)`);
    }
    
    /**
     * Durum yansıtma işlemini durdurur
     */
    stop() {
        if (!this.isRunning) {
            this._log('Durum yansıtma zaten durdurulmuş');
            return;
        }
        
        clearInterval(this.pollTimer);
        this.pollTimer = null;
        this.isRunning = false;
        
        this._log('Durum yansıtma durduruldu');
    }
    
    /**
     * Anlık durum özeti döndürür
     * @returns {Object} - Anlık durum özeti
     */
    getStateSnapshot() {
        return {...this.lastStates};
    }
    
    /**
     * Belirli bir durum türü için değişiklik dinleyicisi ekler
     * @param {string} stateType - Durum türü ('system', 'emotion', 'speaking', vb.)
     * @param {Function} callback - Değişiklikte çağrılacak fonksiyon
     * @returns {string} - Dinleyici ID'si (daha sonra kaldırma için)
     */
    addStateChangeListener(stateType, callback) {
        if (typeof callback !== 'function') {
            throw new Error('StateReflector: Dinleyici bir fonksiyon olmalıdır');
        }
        
        if (!this.stateChangeListeners[stateType]) {
            this.stateChangeListeners[stateType] = [];
        }
        
        const listenerId = `${stateType}_${Date.now()}_${Math.random().toString(36).substring(2, 9)}`;
        
        this.stateChangeListeners[stateType].push({
            id: listenerId,
            callback: callback
        });
        
        return listenerId;
    }
    
    /**
     * Bir durum değişiklik dinleyicisini kaldırır
     * @param {string} listenerId - Dinleyici ID'si
     * @returns {boolean} - Başarılı ise true, değilse false
     */
    removeStateChangeListener(listenerId) {
        let found = false;
        
        Object.keys(this.stateChangeListeners).forEach(stateType => {
            const listeners = this.stateChangeListeners[stateType];
            const index = listeners.findIndex(listener => listener.id === listenerId);
            
            if (index !== -1) {
                listeners.splice(index, 1);
                found = true;
            }
        });
        
        return found;
    }
    
    /**
     * Olay dinleyicilerini kurar
     * @private
     */
    _setupEventListeners() {
        // Duygu değişikliği dinle
        document.addEventListener('emotionChanged', (event) => {
            const { emotion, intensity } = event.detail;
            this._updateState('emotion', { current: emotion, intensity });
        });
        
        // Konuşma durumu değişikliği dinle
        document.addEventListener('speakingChanged', (event) => {
            this._updateState('speaking', event.detail.speaking);
        });
        
        // Animasyon değişikliği dinle
        document.addEventListener('animationChanged', (event) => {
            const { animation, progress, playing } = event.detail;
            this._updateState('animation', { current: animation, progress, playing });
        });
        
        // Sistem durumu değişikliği dinle
        document.addEventListener('systemStateChanged', (event) => {
            const { state } = event.detail;
            this._updateState('system', state);
        });
        
        // Çevresel faktör değişikliği dinle
        document.addEventListener('environmentChanged', (event) => {
            const { factor, state, value } = event.detail;
            
            // Mevcut çevresel durumları kopyala
            const currentEnvironment = {...this.lastStates.environment};
            currentEnvironment[factor] = state;
            
            this._updateState('environment', currentEnvironment);
        });
    }
    
    /**
     * Mevcut durumları toplayıp üst projeye gönderir
     * @private
     */
    _captureCurrentStates() {
        if (!this.bridge || !this.bridge.connected) {
            this._log('Bridge bağlı değil, durum güncellemesi yapılamıyor', 'warn');
            return;
        }
        
        // Metrikleri simüle et (gerçek sistemde burası gerçek metriklerle doldurulacak)
        this._simulateMetrics();
        
        // Durum güncellemesini üst projeye gönder
        this.bridge.sendMessage('FACE1_STATE_REFLECTION', this.lastStates);
    }
    
    /**
     * Metrik verilerini simüle eder (demo amaçlı)
     * @private
     */
    _simulateMetrics() {
        // Mevcut değerleri al
        const currentMetrics = this.lastStates.metrics;
        
        // CPU ve RAM kullanımını rastgele değiştir (gerçekçi sınırlar içinde)
        const cpuDelta = (Math.random() * 10) - 5; // -5 ile +5 arası değişim
        const memoryDelta = (Math.random() * 5) - 2; // -2 ile +2 arası değişim
        
        // Yeni değerler (sınırlar içinde)
        currentMetrics.cpu = Math.max(5, Math.min(95, currentMetrics.cpu + cpuDelta));
        currentMetrics.memory = Math.max(10, Math.min(90, currentMetrics.memory + memoryDelta));
        
        // Sıcaklık değişimi (daha küçük değişimler)
        const temperatureDelta = (Math.random() * 2) - 1; // -1 ile +1 arası değişim
        currentMetrics.temperature = Math.max(35, Math.min(75, currentMetrics.temperature + temperatureDelta));
        
        // Çalışma süresi (her poll ile artır)
        currentMetrics.uptime += this.pollInterval / 1000; // Saniyeye çevir
        
        this._updateState('metrics', currentMetrics);
    }
    
    /**
     * Bir durum güncellemesi yapar ve gerekirse dinleyicileri bilgilendirir
     * @param {string} stateType - Durum türü
     * @param {*} value - Yeni değer
     * @private
     */
    _updateState(stateType, value) {
        // Önceki değer
        const previousValue = this.lastStates[stateType];
        
        // Değer aynıysa atla
        if (JSON.stringify(previousValue) === JSON.stringify(value)) {
            return;
        }
        
        // Yeni durumu kaydet
        this.lastStates[stateType] = value;
        
        // Durum değişikliği dinleyicilerini bilgilendir
        if (this.stateChangeListeners[stateType]) {
            this.stateChangeListeners[stateType].forEach(listener => {
                try {
                    listener.callback(value, previousValue);
                } catch (e) {
                    this._log(`Dinleyici hatası (${stateType}): ${e.message}`, 'error');
                }
            });
        }
    }
    
    /**
     * Debug log mesajı yazdırır
     * @param {string} message - Mesaj metni
     * @param {string} level - Log seviyesi ('log', 'warn', 'error')
     * @private
     */
    _log(message, level = 'log') {
        if (!this.debug) return;
        
        const prefix = 'StateReflector:';
        
        switch (level) {
            case 'warn':
                console.warn(`${prefix} ${message}`);
                break;
            case 'error':
                console.error(`${prefix} ${message}`);
                break;
            default:
                console.log(`${prefix} ${message}`);
        }
    }
}

// Global olarak erişilebilir yap
if (typeof window !== 'undefined') {
    window.StateReflector = StateReflector;
}