/**
 * FACE1 Tema Yöneticisi
 * 
 * Versiyon: 0.5.1
 * Tarih: 06.05.2025
 * 
 * Bu dosya, dinamik tema değişikliklerini yönetmek,
 * üst projeden tema verilerini almak ve tema tercihlerini
 * saklamak için işlevler içerir.
 */

class F1ThemeManager {
    constructor(options = {}) {
        // Varsayılan ayarlar
        this.settings = {
            defaultTheme: 'light',
            storageKey: 'f1-theme-preference',
            parentThemeEnabled: false,
            themeDataAttribute: 'data-theme',
            parentThemeDataAttribute: 'data-parent-theme',
            debug: false,
            ...options
        };
        
        // Mevcut tema durumu
        this.currentTheme = null;
        this.usingParentTheme = false;
        
        // Tema değişikliklerini dinle
        this.setupEventListeners();
        
        // İlk tema tercihini ayarla
        this.initialize();
    }
    
    /**
     * Tema yöneticisini başlatır ve mevcut temayı ayarlar
     */
    initialize() {
        // Üst projeden gelen tema ayarlarını kontrol et
        if (window.parent !== window && this.settings.parentThemeEnabled) {
            this.log('Üst projeden tema ayarları kontrol ediliyor...');
            this.checkParentTheme();
        } else {
            // Yerel depolamadan veya varsayılan temadan yükle
            this.loadThemePreference();
        }
    }
    
    /**
     * Tema tercihi için yerel depolamayı kontrol eder
     */
    loadThemePreference() {
        try {
            const savedTheme = localStorage.getItem(this.settings.storageKey);
            
            if (savedTheme) {
                this.log(`Kaydedilmiş tema bulundu: ${savedTheme}`);
                this.applyTheme(savedTheme);
            } else {
                this.log(`Kaydedilmiş tema bulunamadı, sistem tercihini kontrol et`);
                this.checkSystemPreference();
            }
        } catch (error) {
            this.log('Yerel depolamaya erişim hatası, sistem tercihini kontrol et', error);
            this.checkSystemPreference();
        }
    }
    
    /**
     * Sistem renk şeması tercihini kontrol eder
     */
    checkSystemPreference() {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            this.log('Sistem tercihi: koyu tema');
            this.applyTheme('dark');
        } else {
            this.log(`Sistem tercihi bulunamadı, varsayılan temaya dön: ${this.settings.defaultTheme}`);
            this.applyTheme(this.settings.defaultTheme);
        }
        
        // Sistem tercihi değişikliklerini dinle
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
            if (!this.usingParentTheme && !localStorage.getItem(this.settings.storageKey)) {
                this.log('Sistem tercihi değişti');
                this.applyTheme(e.matches ? 'dark' : 'light');
            }
        });
    }
    
    /**
     * Üst projeyi tema değişiklikleri için kontrol eder
     */
    checkParentTheme() {
        this.log('Üst projeden tema değişiklikleri dinleniyor');
        
        // Üst projeden gelen mesajları dinle
        window.addEventListener('message', (event) => {
            // Uygun mesaj olup olmadığını kontrol et
            try {
                const message = event.data;
                
                // Tema değişikliği mesajlarını kontrol et
                if (message && (message.type === 'FACE1_SET_THEME' || message.type === 'FACE1_SET_THEME_NAME')) {
                    const themeName = message.data && message.data.themeName;
                    
                    if (themeName) {
                        this.log(`Üst projeden tema değişikliği: ${themeName}`);
                        this.applyTheme(themeName, true);
                    }
                }
                
                // CSS değişkenleri mesajını kontrol et
                if (message && message.type === 'FACE1_SET_CSS_VARS') {
                    if (message.data && message.data.variables) {
                        this.log('Üst projeden CSS değişkenleri alındı');
                        this.applyCSSVariables(message.data.variables);
                    }
                }
            } catch (error) {
                this.log('Üst proje mesajı işlenirken hata oluştu', error);
            }
        });
        
        // Üst projeye hazır olduğumuzu bildir
        this.sendMessageToParent('FACE1_THEME_READY', {});
        
        // İlk durumda kaydedilmiş temaya geri dön
        this.loadThemePreference();
    }
    
    /**
     * Temayı belge ve yerel depolamaya uygular
     * @param {string} theme - Tema adı ('light', 'dark', 'high-contrast', vb.)
     * @param {boolean} fromParent - Tema değişikliği üst projeden mi geldi
     */
    applyTheme(theme, fromParent = false) {
        // Geçerli temayı güncelle
        this.currentTheme = theme;
        this.usingParentTheme = fromParent;
        
        // HTML elementine tema özelliğini uygula
        document.documentElement.setAttribute(this.settings.themeDataAttribute, theme);
        
        // Üst tema bayrağını ayarla veya kaldır
        if (fromParent) {
            document.documentElement.setAttribute(this.settings.parentThemeDataAttribute, 'true');
        } else {
            document.documentElement.removeAttribute(this.settings.parentThemeDataAttribute);
        }
        
        // Yerel tercihi kaydet (eğer üst temadan gelmiyorsa)
        if (!fromParent) {
            try {
                localStorage.setItem(this.settings.storageKey, theme);
                this.log(`Tema tercihi kaydedildi: ${theme}`);
            } catch (error) {
                this.log('Tema tercihi kaydedilirken hata oluştu', error);
            }
        }
        
        // Tema değişikliği olayını tetikle
        this.dispatchThemeChangeEvent(theme, fromParent);
        
        this.log(`Tema uygulandı: ${theme} (${fromParent ? 'üst' : 'yerel'})`);
    }
    
    /**
     * Üst projeden alınan CSS değişkenlerini uygular
     * @param {Object} variables - CSS değişkenleri nesnesi
     */
    applyCSSVariables(variables) {
        for (const [key, value] of Object.entries(variables)) {
            // Değişken adını yeniden düzenle
            const varName = key.startsWith('--') ? key : `--parent-${key}`;
            
            // CSS değişkenini kök belgeye uygula
            document.documentElement.style.setProperty(varName, value);
        }
        
        this.log(`${Object.keys(variables).length} CSS değişkeni uygulandı`);
    }
    
    /**
     * Tema değişkliklerini dinlemek için olay dinleyicileri ekler
     */
    setupEventListeners() {
        // Tema değiştirme düğmelerini dinle
        document.addEventListener('click', (event) => {
            // data-theme-toggle özniteliği olan her element
            if (event.target.hasAttribute('data-theme-toggle')) {
                const newTheme = event.target.getAttribute('data-theme-toggle');
                this.applyTheme(newTheme);
            }
        });
        
        // Üst proje tema değişikliklerini dinle
        if (window.parent !== window && this.settings.parentThemeEnabled) {
            this.log('Üst pencere tema değişiklikleri için dinleniyor');
        }
        
        this.log('Tema olayları dinleyicileri kuruldu');
    }
    
    /**
     * Özel tema değişikliği olayını tetikler
     * @param {string} theme - Yeni tema
     * @param {boolean} fromParent - Üst projeden mi geldi
     */
    dispatchThemeChangeEvent(theme, fromParent) {
        const event = new CustomEvent('f1ThemeChange', {
            detail: {
                theme,
                fromParent,
                timestamp: new Date().getTime()
            }
        });
        
        document.dispatchEvent(event);
    }
    
    /**
     * Üst projeye mesaj gönderir (iframe içindeyken)
     * @param {string} type - Mesaj tipi
     * @param {Object} data - Mesaj verileri
     */
    sendMessageToParent(type, data) {
        if (window.parent !== window) {
            window.parent.postMessage({
                type,
                data,
                timestamp: new Date().getTime()
            }, '*');
        }
    }
    
    /**
     * Debug günlüğü oluşturur
     * @param {string} message - Günlük mesajı
     * @param {Error} [error] - Opsiyonel hata nesnesi 
     */
    log(message, error = null) {
        if (this.settings.debug) {
            console.log(`[F1ThemeManager] ${message}`);
            if (error) {
                console.error(error);
            }
        }
    }
    
    /**
     * Mevcut temayı döndürür
     * @returns {string} Mevcut tema
     */
    getCurrentTheme() {
        return this.currentTheme;
    }
    
    /**
     * Mevcut tema üst projeden mi geldi
     * @returns {boolean} Üst projeden tema kullanılıyorsa true
     */
    isUsingParentTheme() {
        return this.usingParentTheme;
    }
}

// Global nesneyi oluştur
window.f1ThemeManager = null;

// Sayfa yüklendiğinde tema yöneticisini başlat
document.addEventListener('DOMContentLoaded', () => {
    window.f1ThemeManager = new F1ThemeManager({
        defaultTheme: 'light',
        parentThemeEnabled: true,
        debug: false
    });
});