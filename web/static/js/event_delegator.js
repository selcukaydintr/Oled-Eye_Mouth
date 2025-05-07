/**
 * ===========================================================
 * Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
 * Dosya: event_delegator.js
 * Açıklama: IFrameBridge üzerinden olay delegasyonu sağlayan yardımcı sınıf
 * Bağımlılıklar: iframe_bridge.js
 * Bağlı Dosyalar: state_reflector.js, iframe_integration.html
 * 
 * Versiyon: 0.5.0
 * Değişiklikler:
 * - [0.1.0] İlk sürüm oluşturuldu
 * - [0.3.0] Komponent kayıt sistemi eklendi
 * - [0.5.0] Durum Yansıtma Protokolü ile entegrasyon tamamlandı
 * - [0.5.0] Dinamik olay güvenlik kontrolü güçlendirildi
 * 
 * Yazar: GitHub Copilot
 * Son Güncelleme: 2025-05-04
 * ===========================================================
 */

/**
 * EventDelegator - IFrameBridge üzerinden olay delegasyonu sağlayan ve 
 * bileşenler arası iletişimi kolaylaştıran yardımcı sınıf 
 */
class EventDelegator {
    /**
     * EventDelegator'u başlatır
     * @param {IFrameBridge} bridge - IFrameBridge bağlantısı (isteğe bağlı)
     * @param {Object} options - Delegasyon seçenekleri
     * @param {boolean} options.debug - Debug modunu etkinleştirir (varsayılan: false)
     * @param {boolean} options.useCommandRouter - Komut yönlendirmeyi etkinleştirir (varsayılan: true)
     */
    constructor(bridge = null, options = {}) {
        this.bridge = bridge;
        this.debug = options.debug || false;
        this.useCommandRouter = options.useCommandRouter !== undefined ? options.useCommandRouter : true;
        
        // Bileşen türleri
        this.componentTypes = {
            EMOTION: 'emotion',
            ANIMATION: 'animation',
            THEME: 'theme',
            LIFECYCLE: 'lifecycle',
            LED: 'led',
            SOUND: 'sound',
            METRICS: 'metrics',
            UI: 'ui',
            COMMAND: 'command' // Yeni komut bileşen türü
        };
        
        // Kayıtlı bileşenler
        this.registeredComponents = {};
        
        // Mesaj-Bileşen eşleştirme haritası
        this.messageToComponentMap = {
            // Üst projeden gelen mesajları bileşen türleriyle eşleştir
            'FACE1_SET_EMOTION': this.componentTypes.EMOTION,
            'FACE1_PLAY_ANIMATION': this.componentTypes.ANIMATION,
            'FACE1_SET_THEME': this.componentTypes.THEME,
            'FACE1_SET_THEME_NAME': this.componentTypes.THEME,
            'FACE1_PLUGIN_CONTROL': this.componentTypes.LIFECYCLE,
            'FACE1_REQUEST_METRICS': this.componentTypes.METRICS,
            'FACE1_LED_CONTROL': this.componentTypes.LED,
            'FACE1_SOUND_CONTROL': this.componentTypes.SOUND,
            'FACE1_SET_CONFIGURATION': this.componentTypes.UI,
            'FACE1_COMMAND': this.componentTypes.COMMAND, // Yeni: Genel komut
            'FACE1_BATCH_COMMAND': this.componentTypes.COMMAND // Yeni: Toplu komut işleme
        };
        
        // Event bus'ı oluştur (bileşenler arası haberleşme için)
        this.eventBus = document.createElement('div');
        
        // Komut yönlendirme mekanizması
        if (this.useCommandRouter && typeof CommandRouter !== 'undefined') {
            this.commandRouter = new CommandRouter(this, { debug: this.debug });
            this.log('CommandRouter başlatıldı ve bağlandı');
        }
        
        // Köprü bridge verilmişse bağlantı kur
        if (this.bridge) {
            this.connectBridge();
        }
        
        this.log('EventDelegator başlatıldı');
    }
    
    /**
     * IFrameBridge bağlantısını ayarlar
     * @param {IFrameBridge} bridge - Bağlanılacak IFrameBridge nesnesi
     */
    connectBridge(bridge) {
        if (bridge) {
            this.bridge = bridge;
        }
        
        if (!this.bridge) {
            console.error('EventDelegator: Geçerli bir IFrameBridge bağlantısı gerekiyor');
            return;
        }
        
        // Köprüden gelen mesajları dinle
        this.bridge.onMessageCallback = this.handleBridgeMessage.bind(this);
        
        // Özel mesaj işleyicilerini ekle
        this.addBridgeMessageHandlers();
        
        this.log('IFrameBridge bağlantısı kuruldu');
    }
    
    /**
     * Köprü mesaj işleyicileri ekler
     */
    addBridgeMessageHandlers() {
        if (!this.bridge) return;
        
        // Tüm eşleştirilen mesaj türleri için işleyiciler ekle
        for (const messageType in this.messageToComponentMap) {
            this.bridge.addMessageHandler(messageType, this.handleBridgeMessage.bind(this));
        }
    }
    
    /**
     * Bridge'den gelen mesajları işler ve ilgili bileşenlere dağıtır
     * @param {Object} message - Gelen mesaj
     * @param {string} origin - Mesaj kaynağı (origin)
     */
    handleBridgeMessage(message, origin) {
        const messageType = message.type;
        const componentType = this.messageToComponentMap[messageType];
        
        if (!componentType) {
            this.log(`Belirtilmemiş mesaj türü: ${messageType}`, 'warn');
            return;
        }
        
        // İlgili bileşen türüne kayıtlı tüm bileşenlere mesajı ilet
        const components = this.registeredComponents[componentType] || [];
        
        if (components.length === 0) {
            this.log(`'${componentType}' türünde kayıtlı bileşen bulunamadı`, 'warn');
            return;
        }
        
        components.forEach(component => {
            if (typeof component.handleMessage === 'function') {
                component.handleMessage(messageType, message.data);
            } else {
                this.log(`Bileşen '${component.name || 'isimsiz'}' handleMessage metodunu uygulamıyor`, 'warn');
            }
        });
        
        // Olay olarak da dağıt (DOM event dispatching)
        this.dispatchComponentEvent(componentType, messageType, message.data);
        
        this.log(`Mesaj dağıtıldı: ${messageType} -> ${componentType} (${components.length} bileşen)`, 'info');
    }
    
    /**
     * Bileşen kaydeder
     * @param {string} componentType - Bileşen türü
     * @param {Object} component - Kaydedilecek bileşen
     * @param {string} component.name - Bileşen adı (isteğe bağlı)
     * @param {Function} component.handleMessage - Mesaj işleme metodu
     */
    registerComponent(componentType, component) {
        if (!this.componentTypes[componentType.toUpperCase()]) {
            this.log(`Geçersiz bileşen türü: ${componentType}`, 'error');
            return false;
        }
        
        const actualType = this.componentTypes[componentType.toUpperCase()];
        
        if (!this.registeredComponents[actualType]) {
            this.registeredComponents[actualType] = [];
        }
        
        // Aynı bileşen daha önce eklenmiş mi kontrol et
        const existingIndex = this.registeredComponents[actualType].findIndex(
            c => c === component || (component.name && c.name === component.name)
        );
        
        if (existingIndex >= 0) {
            this.log(`Bileşen '${component.name || 'isimsiz'}' zaten ${actualType} türüne kayıtlı`, 'warn');
            return false;
        }
        
        this.registeredComponents[actualType].push(component);
        this.log(`Bileşen '${component.name || 'isimsiz'}' ${actualType} türüne kaydedildi`);
        return true;
    }
    
    /**
     * Bileşen kaydını kaldırır
     * @param {string} componentType - Bileşen türü
     * @param {Object} component - Kaydı silinecek bileşen
     */
    unregisterComponent(componentType, component) {
        if (!this.componentTypes[componentType.toUpperCase()]) {
            this.log(`Geçersiz bileşen türü: ${componentType}`, 'error');
            return false;
        }
        
        const actualType = this.componentTypes[componentType.toUpperCase()];
        
        if (!this.registeredComponents[actualType]) {
            return false;
        }
        
        const index = this.registeredComponents[actualType].findIndex(
            c => c === component || (component.name && c.name === component.name)
        );
        
        if (index >= 0) {
            this.registeredComponents[actualType].splice(index, 1);
            this.log(`Bileşen '${component.name || 'isimsiz'}' ${actualType} türünden kaldırıldı`);
            return true;
        }
        
        return false;
    }
    
    /**
     * Bileşenler arası olay yayınlar
     * @param {string} eventType - Olay türü
     * @param {Object} data - Olay verileri
     */
    publishEvent(eventType, data = {}) {
        const event = new CustomEvent(eventType, {
            detail: data,
            bubbles: true,
            cancelable: true
        });
        
        this.eventBus.dispatchEvent(event);
        this.log(`Olay yayınlandı: ${eventType}`);
        
        return event;
    }
    
    /**
     * Bileşenler arası olayları dinler
     * @param {string} eventType - Olay türü
     * @param {Function} callback - Olay gerçekleştiğinde çağrılacak fonksiyon
     */
    subscribeToEvent(eventType, callback) {
        if (typeof callback !== 'function') {
            this.log('Event callback bir fonksiyon olmalıdır', 'error');
            return false;
        }
        
        this.eventBus.addEventListener(eventType, callback);
        this.log(`Olay dinleyici eklendi: ${eventType}`);
        return true;
    }
    
    /**
     * Bileşenler arası olay dinleyiciyi kaldırır
     * @param {string} eventType - Olay türü
     * @param {Function} callback - Kaldırılacak callback fonksiyonu
     */
    unsubscribeFromEvent(eventType, callback) {
        this.eventBus.removeEventListener(eventType, callback);
        this.log(`Olay dinleyici kaldırıldı: ${eventType}`);
    }
    
    /**
     * Bileşen olayı dağıtır
     * @param {string} componentType - Bileşen türü
     * @param {string} messageType - Mesaj türü
     * @param {Object} data - Olay verileri
     */
    dispatchComponentEvent(componentType, messageType, data) {
        // Bileşen tipine özgü olayları yayınla
        const componentEvent = this.publishEvent(`${componentType}:message`, {
            messageType,
            data
        });
        
        // Belirli mesaj tipine özgü olayları yayınla 
        const specificEvent = this.publishEvent(`message:${messageType}`, data);
        
        return {
            componentEvent,
            specificEvent
        };
    }
    
    /**
     * Üst projeye mesaj gönderir
     * @param {string} messageType - Mesaj türü
     * @param {Object} data - Mesaj verileri
     */
    sendToParent(messageType, data = {}) {
        if (!this.bridge || !this.bridge.connected) {
            this.log('IFrameBridge bağlantısı yok veya bağlı değil', 'error');
            return false;
        }
        
        return this.bridge.sendMessage(messageType, data);
    }
    
    /**
     * Komut Yönlendiriciye erişim sağlar
     * @returns {CommandRouter} - Komut yönlendirici
     */
    getCommandRouter() {
        if (!this.commandRouter) {
            this.log('CommandRouter etkinleştirilmemiş veya yüklenemedi', 'warn');
            return null;
        }
        return this.commandRouter;
    }
    
    /**
     * Bir komut çalıştırır (CommandRouter aracılığıyla)
     * @param {string} commandName - Çalıştırılacak komut adı
     * @param {Object} params - Komut parametreleri
     * @param {Object} options - Çalıştırma seçenekleri
     * @returns {Promise<Object>} - Komut çalıştırma sonucu
     */
    executeCommand(commandName, params = {}, options = {}) {
        if (!this.commandRouter) {
            this.log('CommandRouter etkinleştirilmemiş, komut çalıştırılamıyor', 'error');
            return Promise.resolve({ success: false, error: 'Komut Router mevcut değil' });
        }
        
        return this.commandRouter.executeCommand(commandName, params, options);
    }
    
    /**
     * Toplu komut çalıştırır (CommandRouter aracılığıyla)
     * @param {Array<Object>} commands - Komutlar dizisi
     * @param {Object} options - Çalıştırma seçenekleri
     * @returns {Promise<Array<Object>>} - Komut çalıştırma sonuçları
     */
    executeBatchCommands(commands, options = {}) {
        if (!this.commandRouter) {
            this.log('CommandRouter etkinleştirilmemiş, toplu komut çalıştırılamıyor', 'error');
            return Promise.resolve([{ success: false, error: 'Komut Router mevcut değil' }]);
        }
        
        return this.commandRouter.executeBatch(commands, options);
    }
    
    /**
     * Debug ve log işlemleri için
     * @param {string} message - Log mesajı
     * @param {string} level - Log seviyesi (log, info, warn, error)
     */
    log(message, level = 'log') {
        if (!this.debug && level !== 'error') {
            return;
        }
        
        const prefix = '[EventDelegator]';
        
        switch (level) {
            case 'info':
                console.info(`${prefix} ${message}`);
                break;
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

// Global erişim için
window.EventDelegator = EventDelegator;