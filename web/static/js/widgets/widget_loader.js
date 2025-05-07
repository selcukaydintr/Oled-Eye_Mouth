/**
 * FACE1 Widget Yükleyici
 * Dashboard widget'larını yüklemek ve yönetmek için kullanılır
 */
class WidgetLoader {
    constructor(options = {}) {
        this.options = {
            widgetContainer: options.widgetContainer || '.widgets-grid',
            refreshInterval: options.refreshInterval || 30000, // 30 saniye
            socket: options.socket || null  // WebSocket bağlantısı
        };
        
        this.widgets = new Map();
        this.initialized = false;
        
        // Desteklenen widget tipleri
        this.widgetTypes = [
            {id: 'expression-control', name: 'İfade Kontrolü'},
            {id: 'state-history', name: 'Durum İzleme'},
            {id: 'emotion-transitions', name: 'Duygu Geçişleri'}
        ];
    }
    
    /**
     * Widget yükleyiciyi başlatır
     */
    init() {
        if (this.initialized) return;
        
        this._setupEventListeners();
        this._initializeWidgetContainers();
        
        this.initialized = true;
        console.log('FACE1 Widget Yükleyici başlatıldı');
    }
    
    /**
     * Widget container'ları başlat
     */
    _initializeWidgetContainers() {
        // Her bir widget tipi için
        this.widgetTypes.forEach(widget => {
            const containerId = `${widget.id}-widget-container`;
            const container = document.getElementById(containerId);
            
            if (!container) {
                console.warn(`Widget container bulunamadı: ${containerId}`);
                return;
            }
            
            // Widget container'ın içini temizle
            container.innerHTML = '';
            
            // API'den widget içeriğini yükle
            this._loadWidgetContent(widget.id, container);
        });
    }
    
    /**
     * Widget içeriğini API'den yükle
     */
    _loadWidgetContent(widgetId, container) {
        // Yükleniyor göstergesini göster
        container.innerHTML = '<div class="widget-loading">Widget yükleniyor...</div>';
        
        // Widget HTML'ini API'den al
        fetch(`/api/widgets/${widgetId}/render`)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`Widget yüklenemedi: ${response.status}`);
                }
                return response.text();
            })
            .then(html => {
                // Widget HTML'ini container'a yerleştir
                container.innerHTML = html;
                
                // Widget JS kodunu yükle
                return this._loadWidgetScript(widgetId);
            })
            .then(() => {
                const widgetEl = container.querySelector('.face1-widget');
                
                // Yüklenen script içinde window.FACE1Widgets[widgetId] olmalı
                if (window.FACE1Widgets && window.FACE1Widgets[widgetId]) {
                    const widget = window.FACE1Widgets[widgetId];
                    this.widgets.set(widgetId, widget);
                    
                    // Widget'ı başlat
                    if (typeof widget.init === 'function' && widgetEl) {
                        widget.init(widgetEl);
                    }
                }
            })
            .catch(error => {
                console.error(`Widget yüklenemedi: ${widgetId}`, error);
                container.innerHTML = `<div class="widget-error">Widget yüklenemedi: ${error.message}</div>`;
            });
    }
    
    /**
     * Tüm olay dinleyicilerini ayarlar
     */
    _setupEventListeners() {
        // Widget içindeki butonların davranışlarını ekle
        document.addEventListener('click', (e) => {
            // Widget küçültme/genişletme butonu
            if (e.target.closest('.widget-collapse-btn')) {
                const widgetEl = e.target.closest('.face1-widget');
                if (widgetEl) {
                    this._toggleWidgetCollapse(widgetEl);
                }
            }
            
            // Widget yenileme butonu
            if (e.target.closest('.widget-refresh-btn')) {
                const widgetEl = e.target.closest('.face1-widget');
                if (widgetEl) {
                    this._refreshWidget(widgetEl);
                }
            }
        });
        
        // WebSocket mesajlarını dinle
        if (this.options.socket) {
            this.options.socket.addEventListener('message', (event) => {
                try {
                    const data = JSON.parse(event.data);
                    this._handleSocketMessage(data);
                } catch (e) {
                    console.error('WebSocket mesaj işleme hatası:', e);
                }
            });
        } else {
            // Socket mevcut değilse global WebSocket nesnesini kontrol et
            if (window.socket) {
                this.options.socket = window.socket;
                window.socket.addEventListener('message', (event) => {
                    try {
                        const data = JSON.parse(event.data);
                        this._handleSocketMessage(data);
                    } catch (e) {
                        console.error('WebSocket mesaj işleme hatası:', e);
                    }
                });
            } else {
                console.warn('WebSocket bağlantısı mevcut değil, widget güncellemeleri devre dışı.');
            }
        }
    }
    
    /**
     * WebSocket mesajı işleme
     */
    _handleSocketMessage(data) {
        if (!data || !data.type) return;
        
        // Widget veri güncellemesi
        if (data.type === 'widget_update') {
            const { widgetId, data: widgetData } = data;
            this._updateWidgetData(widgetId, widgetData);
        }
    }
    
    /**
     * Widget durumunu değiştirir (küçültme/genişletme)
     */
    _toggleWidgetCollapse(widgetEl) {
        widgetEl.classList.toggle('widget-collapsed');
        
        const button = widgetEl.querySelector('.widget-collapse-btn .icon');
        if (button) {
            button.textContent = widgetEl.classList.contains('widget-collapsed') ? '▶' : '▼';
        }
    }
    
    /**
     * Widget verilerini yeniler
     */
    _refreshWidget(widgetEl) {
        const widgetId = widgetEl.dataset.widgetId;
        
        if (!widgetId) return;
        
        // Widget'ın yükleniyor durumunu göster
        this._setWidgetStatus(widgetEl, 'Yenileniyor...', 'loading');
        
        // Widget verilerini API'den yeniden yükle
        fetch(`/api/widgets/${widgetId}/data`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Widget verisi yüklenemedi');
                }
                return response.json();
            })
            .then(data => {
                this._updateWidgetData(widgetId, data);
                this._setWidgetStatus(widgetEl, 'Güncellendi', 'success');
                
                // 3 saniye sonra durumu sıfırla
                setTimeout(() => {
                    this._setWidgetStatus(widgetEl, 'Hazır');
                }, 3000);
            })
            .catch(error => {
                console.error('Widget yenilenemedi:', error);
                this._setWidgetStatus(widgetEl, 'Hata oluştu', 'error');
            });
    }
    
    /**
     * Widget durumunu ayarlar
     */
    _setWidgetStatus(widgetEl, message, statusClass = '') {
        const statusEl = widgetEl.querySelector('.widget-status');
        if (statusEl) {
            statusEl.textContent = message;
            
            // Tüm durum sınıflarını kaldır
            statusEl.classList.remove('loading', 'success', 'error', 'warning');
            
            if (statusClass) {
                statusEl.classList.add(statusClass);
            }
        }
        
        // Zaman damgası güncelle
        const timestampEl = widgetEl.querySelector('.widget-timestamp time');
        if (timestampEl) {
            const now = new Date();
            timestampEl.textContent = now.toLocaleTimeString();
            timestampEl.setAttribute('datetime', now.toISOString());
        }
    }
    
    /**
     * Widget verisini günceller
     */
    _updateWidgetData(widgetId, data) {
        const widgetEl = document.querySelector(`.face1-widget[data-widget-id="${widgetId}"]`);
        if (!widgetEl) return;
        
        // Widget tipine göre güncelleme fonksiyonu çağır
        if (this.widgets.has(widgetId)) {
            const widget = this.widgets.get(widgetId);
            if (typeof widget.updateData === 'function') {
                widget.updateData(widgetEl, data);
            }
        }
    }
    
    /**
     * Widget script dosyasını yükler
     */
    _loadWidgetScript(widgetId) {
        return new Promise((resolve, reject) => {
            // Script zaten yüklüyse tekrar yükleme
            if (document.querySelector(`script[data-widget="${widgetId}"]`)) {
                resolve();
                return;
            }
            
            const script = document.createElement('script');
            script.src = `/static/js/widgets/${widgetId.replace('-', '_')}.js`;
            script.dataset.widget = widgetId;
            
            script.onload = resolve;
            script.onerror = reject;
            
            document.head.appendChild(script);
        });
    }
    
    /**
     * Yeni bir widget kaydeder
     */
    registerWidget(widgetId, widgetImplementation) {
        if (!window.FACE1Widgets) {
            window.FACE1Widgets = {};
        }
        
        window.FACE1Widgets[widgetId] = widgetImplementation;
        this.widgets.set(widgetId, widgetImplementation);
    }
}

// Global widget yükleyici örneği
window.widgetLoader = new WidgetLoader({
    socket: window.socket // dashboard.js'de tanımlanmış olan WebSocket bağlantısı
});

// Sayfa yüklendiğinde başlat
document.addEventListener('DOMContentLoaded', () => {
    window.widgetLoader.init();
});