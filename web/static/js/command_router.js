/**
 * ===========================================================
 * Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
 * Dosya: command_router.js
 * Açıklama: Komut yönlendirme mekanizması - üst projeden gelen komutları yönetir
 * 
 * Versiyon: 0.5.0
 * Değişiklikler:
 * - [0.5.0] İlk oluşturma - Komut yönlendirme mekanizması
 * Son Güncelleme : 2025-05-04
 * ===========================================================
 */

/**
 * CommandRouter - Üst projeden gelen komutları yönetir ve çeşitli hedeflere yönlendirir
 * EventDelegator ile entegre çalışır ve komut işleme yetenekleri ekler:
 * - Komut geçmişi ve geri alma/yineleme
 * - Komut doğrulama ve onay
 * - Toplu komut işleme
 * - Komut önceliklendirme
 * - Asenkron komut işleme
 */
class CommandRouter {
    /**
     * CommandRouter'ı başlatır
     * @param {EventDelegator} delegator - Event delegator bağlantısı
     * @param {Object} options - Yapılandırma seçenekleri
     * @param {boolean} options.debug - Debug modunu etkinleştir (varsayılan: false)
     * @param {boolean} options.enableHistory - Komut geçmişini etkinleştir (varsayılan: true)
     * @param {number} options.historyLimit - Geçmişte saklanacak maksimum komut sayısı (varsayılan: 50)
     * @param {boolean} options.strictValidation - Katı komut doğrulaması (varsayılan: true)
     */
    constructor(delegator = null, options = {}) {
        this.delegator = delegator;
        this.debug = options.debug || false;
        this.enableHistory = options.enableHistory !== undefined ? options.enableHistory : true;
        this.historyLimit = options.historyLimit || 50;
        this.strictValidation = options.strictValidation !== undefined ? options.strictValidation : true;
        
        // Komut işleyicileri
        this.commandHandlers = {};
        
        // Komut geçmişi
        this.commandHistory = [];
        this.historyIndex = -1;
        
        // Sistem komutları için özel işleyiciler (otomatik kaydedilir)
        this.systemCommandHandlers = {
            // Temel sistem komutları
            'SYSTEM_PING': this.handleSystemPing.bind(this),
            'SYSTEM_GET_STATUS': this.handleSystemGetStatus.bind(this),
            'SYSTEM_RESET': this.handleSystemReset.bind(this)
        };
        
        // Varsayılan komut şemaları
        this.commandSchemas = {
            // Duygu komutları
            'SET_EMOTION': {
                requiredParams: ['emotion'],
                optionalParams: ['intensity', 'duration', 'transition'],
                validateParams: (params) => {
                    const validEmotions = ['happy', 'sad', 'angry', 'surprised', 'neutral', 'confused', 'fear'];
                    if (!validEmotions.includes(params.emotion)) {
                        return { valid: false, error: `Geçersiz duygu: ${params.emotion}` };
                    }
                    if (params.intensity !== undefined && (params.intensity < 0 || params.intensity > 1)) {
                        return { valid: false, error: 'Yoğunluk 0-1 aralığında olmalıdır' };
                    }
                    return { valid: true };
                }
            },
            // Animasyon komutları
            'PLAY_ANIMATION': {
                requiredParams: ['animation'],
                optionalParams: ['speed', 'repeat', 'onComplete'],
                validateParams: (params) => {
                    if (typeof params.animation !== 'string') {
                        return { valid: false, error: 'Animasyon adı bir string olmalıdır' };
                    }
                    return { valid: true };
                }
            },
            // LED komutları
            'LED_CONTROL': {
                requiredParams: ['action'],
                optionalParams: ['color', 'speed', 'brightness', 'zone'],
                validateParams: (params) => {
                    const validActions = ['pulse', 'rainbow', 'breathe', 'solid', 'off'];
                    if (!validActions.includes(params.action)) {
                        return { valid: false, error: `Geçersiz LED aksiyonu: ${params.action}` };
                    }
                    return { valid: true };
                }
            },
            // Yaşam döngüsü komutları
            'PLUGIN_CONTROL': {
                requiredParams: ['command'],
                optionalParams: ['params'],
                validateParams: (params) => {
                    const validCommands = ['restart', 'maintenance', 'exit_maintenance', 'pause', 'resume'];
                    if (!validCommands.includes(params.command)) {
                        return { valid: false, error: `Geçersiz plugin komutu: ${params.command}` };
                    }
                    return { valid: true };
                }
            },
            // Tema komutları
            'SET_THEME': {
                requiredParams: ['theme'], 
                optionalParams: ['applyToParent'],
                validateParams: (params) => {
                    return { valid: true }; // Tema adı valide edilmeyecek, çünkü özel temalar olabilir
                }
            }
        };
        
        // Event Delegator bağlı ise, mesaj dinleyiciler ekle
        if (this.delegator) {
            this.connectDelegator();
        }
        
        // Sistem komut işleyicilerini kaydet
        this.registerSystemCommandHandlers();
        
        this.log('CommandRouter başlatıldı');
    }
    
    /**
     * EventDelegator bağlantısını kurar
     * @param {EventDelegator} delegator - Bağlanılacak event delegator
     */
    connectDelegator(delegator) {
        if (delegator) {
            this.delegator = delegator;
        }
        
        if (!this.delegator) {
            this.log('Geçerli bir EventDelegator bağlantısı gerekli', 'error');
            return false;
        }
        
        // EventDelegator event'lerine abone ol
        this.delegator.subscribeToEvent('message:FACE1_COMMAND', this.handleCommand.bind(this));
        this.delegator.subscribeToEvent('message:FACE1_BATCH_COMMAND', this.handleBatchCommand.bind(this));
        
        // Özel komut olayları için dinleyiciler
        this.delegator.subscribeToEvent('message:FACE1_SET_EMOTION', event => {
            this.executeCommand('SET_EMOTION', event.detail); 
        });
        
        this.delegator.subscribeToEvent('message:FACE1_PLAY_ANIMATION', event => {
            this.executeCommand('PLAY_ANIMATION', event.detail);
        });
        
        this.delegator.subscribeToEvent('message:FACE1_LED_CONTROL', event => {
            this.executeCommand('LED_CONTROL', event.detail);
        });
        
        this.delegator.subscribeToEvent('message:FACE1_PLUGIN_CONTROL', event => {
            this.executeCommand('PLUGIN_CONTROL', event.detail);
        });
        
        this.delegator.subscribeToEvent('message:FACE1_SET_THEME', event => {
            this.executeCommand('SET_THEME', event.detail);
        });
        
        this.log('EventDelegator bağlantısı kuruldu');
        return true;
    }
    
    /**
     * Sistem komut işleyicilerini kaydeder
     */
    registerSystemCommandHandlers() {
        for (const commandName in this.systemCommandHandlers) {
            this.registerCommand(commandName, this.systemCommandHandlers[commandName], { system: true });
        }
    }
    
    /**
     * Yeni bir komut işleyicisi kaydeder
     * @param {string} commandName - Komut adı
     * @param {Function} handler - Komut işleyici fonksiyon
     * @param {Object} options - Komut seçenekleri
     * @param {boolean} options.system - Sistem komutu mu? (varsayılan: false)
     * @param {boolean} options.overwrite - Mevcut komutu üzerine yaz (varsayılan: false)
     * @param {Object} options.schema - Komut şeması (varsayılan: null)
     * @returns {boolean} - Kayıt başarılı mı?
     */
    registerCommand(commandName, handler, options = {}) {
        const isSystem = options.system || false;
        const overwrite = options.overwrite || false;
        
        // Komut adını standardize et
        commandName = commandName.toUpperCase();
        
        // Mevcut komutu kontrol et
        if (this.commandHandlers[commandName] && !overwrite) {
            this.log(`"${commandName}" komutu zaten kayıtlı, üzerine yazmak için overwrite seçeneğini kullanın`, 'warn');
            return false;
        }
        
        // Komut şemasını ayarla
        if (options.schema) {
            this.commandSchemas[commandName] = options.schema;
        }
        
        // Komutu kaydet
        this.commandHandlers[commandName] = {
            handler: handler,
            system: isSystem,
            timestamp: Date.now()
        };
        
        this.log(`"${commandName}" komutu kaydedildi${isSystem ? ' (sistem komutu)' : ''}`);
        return true;
    }
    
    /**
     * Komut kaydını kaldırır
     * @param {string} commandName - Kaldırılacak komutun adı
     * @returns {boolean} - Kaldırma başarılı mı?
     */
    unregisterCommand(commandName) {
        commandName = commandName.toUpperCase();
        
        if (!this.commandHandlers[commandName]) {
            this.log(`"${commandName}" komutu bulunamadı`, 'warn');
            return false;
        }
        
        // Sistem komutlarını silmeye karşı koruma
        if (this.commandHandlers[commandName].system) {
            this.log(`"${commandName}" sistem komutunu silemezsiniz`, 'error');
            return false;
        }
        
        delete this.commandHandlers[commandName];
        this.log(`"${commandName}" komutu kaldırıldı`);
        return true;
    }
    
    /**
     * Bir komutu çalıştırır
     * @param {string} commandName - Çalıştırılacak komut adı
     * @param {Object} params - Komut parametreleri
     * @param {Object} options - Çalıştırma seçenekleri
     * @param {boolean} options.addToHistory - Geçmişe ekle (varsayılan: true)
     * @param {boolean} options.validate - Komut validasyonu yap (varsayılan: true)
     * @param {number} options.priority - Komut önceliği (varsayılan: 0)
     * @returns {Promise<Object>} - Komut çalıştırma sonucu
     */
    async executeCommand(commandName, params = {}, options = {}) {
        commandName = commandName.toUpperCase();
        
        const addToHistory = options.addToHistory !== undefined ? options.addToHistory : this.enableHistory;
        const validate = options.validate !== undefined ? options.validate : this.strictValidation;
        const priority = options.priority || 0;
        
        this.log(`"${commandName}" komutu çalıştırılıyor, parametreler:`, 'info');
        this.log(params, 'debug');
        
        // Komut işleyicisini bul
        if (!this.commandHandlers[commandName]) {
            const error = `"${commandName}" komutu için işleyici bulunamadı`;
            this.log(error, 'error');
            return { success: false, error };
        }
        
        // Validasyon
        if (validate && this.commandSchemas[commandName]) {
            const validationResult = this.validateCommand(commandName, params);
            if (!validationResult.valid) {
                this.log(`"${commandName}" komutu validasyon hatası: ${validationResult.error}`, 'error');
                return { success: false, error: validationResult.error };
            }
        }
        
        try {
            // Komutu tarihçeye ekle
            if (addToHistory) {
                this.addToHistory(commandName, params, options);
            }
            
            // Komutu çalıştır
            const handler = this.commandHandlers[commandName].handler;
            const result = await Promise.resolve(handler(params));
            
            this.log(`"${commandName}" komutu başarıyla çalıştırıldı`, 'info');
            return { success: true, result };
        } catch (error) {
            this.log(`"${commandName}" komutu çalıştırılırken hata: ${error.message}`, 'error');
            return { success: false, error: error.message };
        }
    }
    
    /**
     * Toplu komut çalıştırır
     * @param {Array<Object>} commands - Komutlar dizisi
     * @param {Object} options - Çalıştırma seçenekleri
     * @param {boolean} options.stopOnError - Hata durumunda dur (varsayılan: false)
     * @returns {Promise<Array<Object>>} - Komut çalıştırma sonuçları
     */
    async executeBatch(commands, options = {}) {
        const stopOnError = options.stopOnError || false;
        const results = [];
        
        this.log(`${commands.length} komutluk batch işlemi başlatılıyor`, 'info');
        
        for (let i = 0; i < commands.length; i++) {
            const cmd = commands[i];
            
            if (!cmd.command || typeof cmd.command !== 'string') {
                const error = 'Geçersiz komut formatı: "command" alanı gerekli ve string olmalı';
                results.push({ success: false, index: i, error });
                
                if (stopOnError) {
                    this.log('Hata nedeniyle batch işlemi durduruldu', 'error');
                    return results;
                }
                
                continue;
            }
            
            const result = await this.executeCommand(
                cmd.command,
                cmd.params || {},
                { 
                    addToHistory: cmd.addToHistory !== undefined ? cmd.addToHistory : true,
                    validate: cmd.validate !== undefined ? cmd.validate : true,
                    priority: cmd.priority || 0
                }
            );
            
            results.push({
                ...result,
                index: i,
                command: cmd.command
            });
            
            if (!result.success && stopOnError) {
                this.log('Hata nedeniyle batch işlemi durduruldu', 'error');
                return results;
            }
        }
        
        this.log(`Batch işlemi tamamlandı: ${results.filter(r => r.success).length}/${commands.length} başarılı`, 'info');
        return results;
    }
    
    /**
     * Komutu geçmişe ekler
     * @param {string} commandName - Komut adı
     * @param {Object} params - Komut parametreleri
     * @param {Object} options - Komut seçenekleri
     */
    addToHistory(commandName, params, options = {}) {
        if (!this.enableHistory) return;
        
        // Geçmiş limiti kontrol
        if (this.commandHistory.length >= this.historyLimit) {
            this.commandHistory.shift(); // En eski komutu çıkar
        }
        
        // Yeni komutu geçmişe ekle
        const historyItem = {
            command: commandName,
            params: JSON.parse(JSON.stringify(params)), // Derin kopya
            timestamp: Date.now(),
            options
        };
        
        // Eğer geçmişte ileri gitmişsek, sonrasını sil
        if (this.historyIndex < this.commandHistory.length - 1) {
            this.commandHistory = this.commandHistory.slice(0, this.historyIndex + 1);
        }
        
        this.commandHistory.push(historyItem);
        this.historyIndex = this.commandHistory.length - 1;
    }
    
    /**
     * Komut geçmişinde geri gider
     * @returns {Object|null} - Önceki komut veya geçmiş başındaysa null
     */
    undoCommand() {
        if (!this.enableHistory || this.commandHistory.length === 0 || this.historyIndex < 0) {
            this.log('Geri alınacak komut yok', 'warn');
            return null;
        }
        
        const currentCommand = this.commandHistory[this.historyIndex];
        this.historyIndex--;
        
        this.log(`"${currentCommand.command}" komutu geri alındı`, 'info');
        return currentCommand;
    }
    
    /**
     * Komut geçmişinde ileri gider
     * @returns {Object|null} - Sonraki komut veya geçmiş sonundaysa null
     */
    redoCommand() {
        if (!this.enableHistory || this.historyIndex >= this.commandHistory.length - 1) {
            this.log('Yinelenecek komut yok', 'warn');
            return null;
        }
        
        this.historyIndex++;
        const nextCommand = this.commandHistory[this.historyIndex];
        
        this.log(`"${nextCommand.command}" komutu yinelendi`, 'info');
        return nextCommand;
    }
    
    /**
     * Komut parametrelerini validasyon şemasına göre doğrular
     * @param {string} commandName - Doğrulanacak komut
     * @param {Object} params - Komut parametreleri
     * @returns {Object} - Validasyon sonucu {valid: boolean, error: string}
     */
    validateCommand(commandName, params) {
        const schema = this.commandSchemas[commandName];
        if (!schema) {
            return { valid: true }; // Şema yoksa validasyon atlanır
        }
        
        // Gerekli parametreleri kontrol et
        if (schema.requiredParams) {
            for (const required of schema.requiredParams) {
                if (params[required] === undefined) {
                    return {
                        valid: false,
                        error: `"${required}" parametresi gerekli`
                    };
                }
            }
        }
        
        // Özel validasyon fonksiyonu varsa çalıştır
        if (schema.validateParams && typeof schema.validateParams === 'function') {
            return schema.validateParams(params);
        }
        
        return { valid: true };
    }
    
    /**
     * Komut olayını işler (delegator aracılığıyla)
     * @param {CustomEvent} event - Event detayları
     */
    handleCommand(event) {
        const data = event.detail;
        
        if (!data || !data.command) {
            this.log('Geçersiz komut formatı: "command" alanı eksik', 'error');
            return;
        }
        
        this.executeCommand(data.command, data.params || {}, data.options || {})
            .then(result => {
                // Sonucu üst projeye bildir
                if (this.delegator) {
                    this.delegator.sendToParent('FACE1_COMMAND_RESULT', {
                        command: data.command,
                        result: result,
                        requestId: data.requestId
                    });
                }
            });
    }
    
    /**
     * Toplu komut olayını işler
     * @param {CustomEvent} event - Event detayları
     */
    handleBatchCommand(event) {
        const data = event.detail;
        
        if (!data || !Array.isArray(data.commands)) {
            this.log('Geçersiz batch komut formatı: "commands" array alanı eksik', 'error');
            return;
        }
        
        this.executeBatch(data.commands, data.options || {})
            .then(results => {
                // Sonucu üst projeye bildir
                if (this.delegator) {
                    this.delegator.sendToParent('FACE1_BATCH_RESULT', {
                        results: results,
                        requestId: data.requestId
                    });
                }
            });
    }
    
    /**
     * SYSTEM_PING komutunu işler
     * @param {Object} params - Komut parametreleri
     * @returns {Object} - Ping yanıtı
     */
    handleSystemPing(params) {
        return {
            pong: true,
            timestamp: Date.now(),
            echo: params.echo,
            uptime: this.getUptime(),
            registeredCommands: Object.keys(this.commandHandlers).length
        };
    }
    
    /**
     * SYSTEM_GET_STATUS komutunu işler
     * @returns {Object} - Sistem durumu
     */
    handleSystemGetStatus() {
        return {
            commands: {
                registered: Object.keys(this.commandHandlers).length,
                history: {
                    enabled: this.enableHistory,
                    count: this.commandHistory.length,
                    currentIndex: this.historyIndex
                }
            },
            router: {
                version: '0.5.0',
                debugMode: this.debug,
                strictValidation: this.strictValidation,
                delegatorConnected: !!this.delegator
            },
            uptime: this.getUptime()
        };
    }
    
    /**
     * SYSTEM_RESET komutunu işler
     * @param {Object} params - Komut parametreleri
     * @returns {Object} - Sıfırlama sonucu
     */
    handleSystemReset(params = {}) {
        const resetHistory = params.resetHistory !== undefined ? params.resetHistory : true;
        const resetCustomCommands = params.resetCustomCommands !== undefined ? params.resetCustomCommands : false;
        
        if (resetHistory) {
            this.commandHistory = [];
            this.historyIndex = -1;
            this.log('Komut geçmişi sıfırlandı', 'info');
        }
        
        if (resetCustomCommands) {
            // Sadece özel komutları sil, sistem komutlarını koru
            const systemCommands = {};
            for (const command in this.commandHandlers) {
                if (this.commandHandlers[command].system) {
                    systemCommands[command] = this.commandHandlers[command];
                }
            }
            
            this.commandHandlers = systemCommands;
            this.log('Özel komutlar sıfırlandı', 'info');
        }
        
        return {
            resetPerformed: true,
            historyReset: resetHistory,
            customCommandsReset: resetCustomCommands
        };
    }
    
    /**
     * Uygulamanın çalışma süresini hesaplar
     * @returns {number} - Çalışma süresi (milisaniye)
     */
    getUptime() {
        // Burada gerçek bir uptime değeri döndürmek için, başlangıç zamanı tutulabilir
        // Ancak browser yeniden yüklendiğinde kaybolacağından, şimdilik sabit değer
        return 60000; // Örnek olarak 1 dakika
    }
    
    /**
     * Debug ve log işlemleri için
     * @param {string|Object} message - Log mesajı
     * @param {string} level - Log seviyesi (log, info, warn, error, debug)
     */
    log(message, level = 'log') {
        if (!this.debug && level !== 'error' && level !== 'warn') {
            return;
        }
        
        const prefix = '[CommandRouter]';
        
        // Object log işleme
        if (typeof message === 'object' && message !== null) {
            switch (level) {
                case 'info':
                    console.info(prefix, message);
                    break;
                case 'warn':
                    console.warn(prefix, message);
                    break;
                case 'error':
                    console.error(prefix, message);
                    break;
                case 'debug':
                    console.debug(prefix, message);
                    break;
                default:
                    console.log(prefix, message);
            }
            return;
        }
        
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
            case 'debug':
                console.debug(`${prefix} ${message}`);
                break;
            default:
                console.log(`${prefix} ${message}`);
        }
    }
}

// Global erişim için
window.CommandRouter = CommandRouter;