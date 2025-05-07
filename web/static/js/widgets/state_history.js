/**
 * FACE1 Durum İzleme ve Tarihçe Widget'ı
 * Sistem durumunu ve durum geçmişini izlemek için kullanılır
 */
(function() {
    // Widget tanımı
    const StateHistoryWidget = {
        // Varsayılan yapılandırma
        config: {
            historyLimit: 50,      // Gösterilecek maksimum tarihçe öğesi
            pollInterval: 10000,   // Güncel veri için sorgulama aralığı (ms)
            chartHours: 24         // Grafik için gösterilecek saat sayısı
        },
        
        // Durum ikonları
        icons: {
            system: "🖥️",
            emotion: "😀",
            speaking: "🗣️",
            animation: "🎭",
            error: "⚠️"
        },
        
        /**
         * Widget'ı başlatır
         * @param {HTMLElement} widgetElement - Widget HTML elementi
         */
        init: function(widgetElement) {
            this.widgetEl = widgetElement;
            this.widgetId = widgetElement.dataset.widgetId;
            
            // Referansları saklama
            this.elements = {
                systemState: widgetElement.querySelector(`#system-state-${this.widgetId}`),
                emotionState: widgetElement.querySelector(`#emotion-state-${this.widgetId}`),
                speakingState: widgetElement.querySelector(`#speaking-state-${this.widgetId}`),
                animationState: widgetElement.querySelector(`#animation-state-${this.widgetId}`),
                cpuUsage: widgetElement.querySelector(`#cpu-usage-${this.widgetId}`),
                memoryUsage: widgetElement.querySelector(`#memory-usage-${this.widgetId}`),
                temperature: widgetElement.querySelector(`#temperature-${this.widgetId}`),
                uptime: widgetElement.querySelector(`#uptime-${this.widgetId}`),
                historyFilter: widgetElement.querySelector(`#history-filter-${this.widgetId}`),
                historyTimeline: widgetElement.querySelector(`#history-timeline-${this.widgetId}`),
                activityChart: widgetElement.querySelector(`#activity-chart-${this.widgetId}`)
            };
            
            // Veriler
            this.state = {
                system: "unknown",
                emotion: "neutral",
                emotionIntensity: 1.0,
                speaking: false,
                animation: null,
                metrics: {
                    cpu: 0,
                    memory: 0,
                    temperature: 0,
                    uptime: 0
                },
                history: []
            };
            
            // Olay dinleyicileri ekle
            this._setupEventListeners();
            
            // Verilerinizi başlatma
            this._fetchInitialData();
            
            // Etkinlik grafiğini başlatma
            this._initActivityChart();
            
            // Periyodik yenileme
            this._startPolling();
            
            console.log(`StateHistoryWidget başlatıldı: ${this.widgetId}`);
        },
        
        /**
         * Olay dinleyicilerini ayarlar
         */
        _setupEventListeners: function() {
            const self = this;
            
            // Tarihçe filtresi değişikliği
            if (this.elements.historyFilter) {
                this.elements.historyFilter.addEventListener('change', function() {
                    self._filterHistory(this.value);
                });
            }
            
            // WebSocket mesaj dinleyicisi ekle
            if (window.socket) {
                window.socket.addEventListener('message', function(event) {
                    const data = JSON.parse(event.data);
                    self._handleSocketMessage(data);
                });
            }
        },
        
        /**
         * WebSocket mesajını işler
         * @param {Object} data - WebSocket mesajı
         */
        _handleSocketMessage: function(data) {
            if (!data || !data.type) return;
            
            switch (data.type) {
                case 'stats':
                    this._updateMetrics(data.data);
                    break;
                case 'emotion_changed':
                    this._updateEmotion(data.emotion.state, data.emotion.intensity);
                    this._addHistoryEntry('emotion', `Duygu durumu değişti: ${data.emotion.state} (${data.emotion.intensity.toFixed(1)})`);
                    break;
                case 'animation_started':
                    this._updateAnimation(data.animation, true);
                    this._addHistoryEntry('animation', `Animasyon başladı: ${data.animation}`);
                    break;
                case 'animation_stopped':
                    this._updateAnimation(null, false);
                    this._addHistoryEntry('animation', `Animasyon bitti: ${data.animation}`);
                    break;
                case 'speaking_update':
                    this._updateSpeaking(data.speaking);
                    this._addHistoryEntry('speaking', `Konuşma durumu: ${data.speaking ? 'başladı' : 'bitti'}`);
                    break;
                case 'system_state':
                    this._updateSystemState(data.state);
                    this._addHistoryEntry('system', `Sistem durumu: ${data.state}`);
                    break;
                case 'error':
                    this._addHistoryEntry('error', `Hata: ${data.message}`);
                    break;
            }
        },
        
        /**
         * Başlangıç verilerini getirir
         */
        _fetchInitialData: function() {
            const self = this;
            
            // Sistem durumu ve metrikleri al
            fetch('/api/system/status')
                .then(response => response.json())
                .then(data => {
                    self._updateSystemState(data.state);
                    self._updateMetrics(data.metrics);
                })
                .catch(error => {
                    console.error('Sistem durumu alınamadı:', error);
                });
                
            // Tarihçe verilerini al
            fetch('/api/system/history')
                .then(response => response.json())
                .then(data => {
                    if (Array.isArray(data.entries)) {
                        self.state.history = data.entries.map(entry => ({
                            type: entry.type,
                            message: entry.message,
                            timestamp: new Date(entry.timestamp),
                            icon: self.icons[entry.type] || "📝"
                        }));
                        self._renderHistory();
                    }
                })
                .catch(error => {
                    console.error('Tarihçe verileri alınamadı:', error);
                });
                
            // Etkinlik grafik verilerini al
            fetch('/api/system/activity')
                .then(response => response.json())
                .then(data => {
                    if (data.points) {
                        self._updateActivityChart(data.points);
                    }
                })
                .catch(error => {
                    console.error('Etkinlik verileri alınamadı:', error);
                });
        },
        
        /**
         * Düzenli sorgulamayı başlatır
         */
        _startPolling: function() {
            const self = this;
            this.pollTimer = setInterval(function() {
                self._fetchLatestData();
            }, this.config.pollInterval);
        },
        
        /**
         * En son verileri getirir
         */
        _fetchLatestData: function() {
            const self = this;
            
            // Sadece websocket bağlantısı yoksa HTTP üzerinden getir
            if (!window.socket || window.socket.readyState !== WebSocket.OPEN) {
                fetch('/api/system/status')
                    .then(response => response.json())
                    .then(data => {
                        self._updateSystemState(data.state);
                        self._updateMetrics(data.metrics);
                    })
                    .catch(error => {
                        console.error('Sistem durumu alınamadı:', error);
                    });
            }
        },
        
        /**
         * Sistem durumunu günceller
         * @param {string} state - Sistem durumu
         */
        _updateSystemState: function(state) {
            if (!this.elements.systemState) return;
            
            this.state.system = state;
            this.elements.systemState.textContent = state;
            
            // CSS sınıfları temizle
            this.elements.systemState.classList.remove('running', 'paused', 'error', 'maintenance', 'stopped');
            
            // Duruma göre CSS sınıfı ekle
            if (['running', 'paused', 'error', 'maintenance', 'stopped'].includes(state)) {
                this.elements.systemState.classList.add(state);
            }
        },
        
        /**
         * Duygu durumunu günceller
         * @param {string} emotion - Duygu durumu
         * @param {number} intensity - Duygu yoğunluğu
         */
        _updateEmotion: function(emotion, intensity) {
            if (!this.elements.emotionState) return;
            
            this.state.emotion = emotion;
            this.state.emotionIntensity = intensity;
            
            this.elements.emotionState.textContent = `${emotion} (${intensity.toFixed(1)})`;
        },
        
        /**
         * Konuşma durumunu günceller
         * @param {boolean} isSpeaking - Konuşma durumu
         */
        _updateSpeaking: function(isSpeaking) {
            if (!this.elements.speakingState) return;
            
            this.state.speaking = isSpeaking;
            this.elements.speakingState.textContent = isSpeaking ? 'Konuşuyor' : 'Sessiz';
        },
        
        /**
         * Animasyon durumunu günceller
         * @param {string} animation - Animasyon adı
         * @param {boolean} isPlaying - Çalma durumu
         */
        _updateAnimation: function(animation, isPlaying) {
            if (!this.elements.animationState) return;
            
            this.state.animation = isPlaying ? animation : null;
            this.elements.animationState.textContent = isPlaying ? animation : 'Yok';
        },
        
        /**
         * Metrikleri günceller
         * @param {Object} metrics - Sistem metrikleri
         */
        _updateMetrics: function(metrics) {
            if (!metrics) return;
            
            this.state.metrics = { ...this.state.metrics, ...metrics };
            
            if (this.elements.cpuUsage) {
                this.elements.cpuUsage.textContent = `${metrics.cpu.toFixed(1)}%`;
            }
            
            if (this.elements.memoryUsage) {
                this.elements.memoryUsage.textContent = `${metrics.memory.toFixed(1)}%`;
            }
            
            if (this.elements.temperature) {
                this.elements.temperature.textContent = `${metrics.temperature.toFixed(1)}°C`;
            }
            
            if (this.elements.uptime) {
                this.elements.uptime.textContent = this._formatUptime(metrics.uptime);
            }
        },
        
        /**
         * Çalışma süresini biçimlendirir
         * @param {number} seconds - Saniye cinsinden süre
         * @returns {string} - Biçimlendirilmiş süre
         */
        _formatUptime: function(seconds) {
            const hours = Math.floor(seconds / 3600);
            const minutes = Math.floor((seconds % 3600) / 60);
            const secs = Math.floor(seconds % 60);
            
            if (hours > 0) {
                return `${hours}sa ${minutes}dk ${secs}sn`;
            } else {
                return `${minutes}dk ${secs}sn`;
            }
        },
        
        /**
         * Tarihçeye yeni giriş ekler
         * @param {string} type - Giriş tipi
         * @param {string} message - Giriş mesajı
         */
        _addHistoryEntry: function(type, message) {
            const entry = {
                type: type,
                message: message,
                timestamp: new Date(),
                icon: this.icons[type] || "📝"
            };
            
            // Başa ekle
            this.state.history.unshift(entry);
            
            // Limiti aşan girişleri temizle
            if (this.state.history.length > this.config.historyLimit) {
                this.state.history = this.state.history.slice(0, this.config.historyLimit);
            }
            
            // Tarihçeyi yeniden oluştur
            this._renderHistory();
            
            // Etkinlik grafiğine nokta ekle
            this._addActivityPoint(type);
        },
        
        /**
         * Tarihçe listesini oluşturur
         */
        _renderHistory: function() {
            if (!this.elements.historyTimeline) return;
            
            const filter = this.elements.historyFilter ? this.elements.historyFilter.value : 'all';
            this._filterHistory(filter);
        },
        
        /**
         * Tarihçe filtresi
         * @param {string} filter - Filtre tipi
         */
        _filterHistory: function(filter) {
            if (!this.elements.historyTimeline) return;
            
            const filteredEntries = filter === 'all' 
                ? this.state.history 
                : this.state.history.filter(entry => entry.type === filter);
                
            this.elements.historyTimeline.innerHTML = '';
            
            filteredEntries.forEach(entry => {
                const entryEl = document.createElement('div');
                entryEl.className = `history-entry ${entry.type}`;
                
                const timeStr = this._formatTimestamp(entry.timestamp);
                
                entryEl.innerHTML = `
                    <div class="entry-icon">
                        <span class="icon">${entry.icon}</span>
                    </div>
                    <div class="entry-content">
                        <div class="entry-time">${timeStr}</div>
                        <div class="entry-message">${entry.message}</div>
                    </div>
                `;
                
                this.elements.historyTimeline.appendChild(entryEl);
            });
        },
        
        /**
         * Zaman damgasını biçimlendirir
         * @param {Date} timestamp - Zaman damgası
         * @returns {string} - Biçimlendirilmiş zaman
         */
        _formatTimestamp: function(timestamp) {
            const now = new Date();
            const diffMs = now - timestamp;
            const diffSec = Math.floor(diffMs / 1000);
            
            if (diffSec < 60) {
                return `${diffSec} saniye önce`;
            } else if (diffSec < 3600) {
                return `${Math.floor(diffSec / 60)} dakika önce`;
            } else if (diffSec < 86400) {
                return `${Math.floor(diffSec / 3600)} saat önce`;
            } else {
                return timestamp.toLocaleTimeString() + ' ' + timestamp.toLocaleDateString();
            }
        },
        
        /**
         * Etkinlik grafiğini başlatır
         */
        _initActivityChart: function() {
            if (!this.elements.activityChart) return;
            
            // Izgarayı çiz
            const chartWidth = this.elements.activityChart.offsetWidth;
            const chartHeight = this.elements.activityChart.offsetHeight;
            
            // X ekseni (saat)
            const xAxis = document.createElement('div');
            xAxis.className = 'chart-x-axis';
            xAxis.style.cssText = `
                position: absolute;
                left: 0;
                bottom: 20px;
                width: ${chartWidth}px;
                height: 1px;
                background-color: rgba(0, 0, 0, 0.1);
            `;
            this.elements.activityChart.appendChild(xAxis);
            
            // Y ekseni
            const yAxis = document.createElement('div');
            yAxis.className = 'chart-y-axis';
            yAxis.style.cssText = `
                position: absolute;
                left: 40px;
                top: 0;
                width: 1px;
                height: ${chartHeight}px;
                background-color: rgba(0, 0, 0, 0.1);
            `;
            this.elements.activityChart.appendChild(yAxis);
            
            // Görsel haznesi
            this.chartContainer = document.createElement('div');
            this.chartContainer.className = 'chart-points-container';
            this.chartContainer.style.cssText = `
                position: absolute;
                left: 40px;
                top: 10px;
                right: 10px;
                bottom: 20px;
            `;
            this.elements.activityChart.appendChild(this.chartContainer);
        },
        
        /**
         * Etkinlik grafiğini günceller
         * @param {Array} points - Etkinlik noktaları
         */
        _updateActivityChart: function(points) {
            if (!this.chartContainer) return;
            
            this.chartContainer.innerHTML = '';
            
            const containerWidth = this.chartContainer.offsetWidth;
            const containerHeight = this.chartContainer.offsetHeight;
            
            points.forEach(point => {
                const pointEl = document.createElement('div');
                pointEl.className = `chart-point ${point.type}`;
                
                // Nokta konumu
                const timestamp = new Date(point.timestamp);
                const now = new Date();
                const hoursDiff = (now - timestamp) / 3600000;  // saat farkı
                
                if (hoursDiff > this.config.chartHours) return; // Çok eski noktaları gösterme
                
                const xPos = containerWidth - (hoursDiff / this.config.chartHours) * containerWidth;
                const yPos = Math.random() * (containerHeight - 20) + 10; // Rastgele Y konumu
                
                pointEl.style.left = `${xPos}px`;
                pointEl.style.top = `${yPos}px`;
                
                this.chartContainer.appendChild(pointEl);
            });
        },
        
        /**
         * Etkinlik grafiğine nokta ekler
         * @param {string} type - Nokta tipi
         */
        _addActivityPoint: function(type) {
            if (!this.chartContainer) return;
            
            const pointEl = document.createElement('div');
            pointEl.className = `chart-point ${type}`;
            
            const containerWidth = this.chartContainer.offsetWidth;
            const containerHeight = this.chartContainer.offsetHeight;
            
            // Yeni nokta sağ tarafta olacak
            const xPos = containerWidth;
            const yPos = Math.random() * (containerHeight - 20) + 10;
            
            pointEl.style.left = `${xPos}px`;
            pointEl.style.top = `${yPos}px`;
            
            this.chartContainer.appendChild(pointEl);
            
            // Tüm noktaları sola kaydır
            const allPoints = this.chartContainer.querySelectorAll('.chart-point');
            allPoints.forEach(point => {
                const currentLeft = parseFloat(point.style.left);
                point.style.left = `${currentLeft - 5}px`; // Her yeni noktada 5px sola kaydır
                
                // Görünüm alanından çıkan noktaları kaldır
                if (currentLeft < 0) {
                    point.remove();
                }
            });
        },
        
        /**
         * Widget verilerini günceller
         * @param {HTMLElement} widgetEl - Widget elementi 
         * @param {Object} data - Güncel veriler
         */
        updateData: function(widgetEl, data) {
            if (data.system) {
                this._updateSystemState(data.system);
            }
            
            if (data.emotion) {
                this._updateEmotion(data.emotion.state, data.emotion.intensity);
            }
            
            if (data.speaking !== undefined) {
                this._updateSpeaking(data.speaking);
            }
            
            if (data.animation !== undefined) {
                this._updateAnimation(data.animation.current, data.animation.playing);
            }
            
            if (data.metrics) {
                this._updateMetrics(data.metrics);
            }
            
            if (data.historyEntry) {
                this._addHistoryEntry(data.historyEntry.type, data.historyEntry.message);
            }
        }
    };
    
    // Widget'ı kaydet
    if (!window.FACE1Widgets) {
        window.FACE1Widgets = {};
    }
    window.FACE1Widgets.state_history = StateHistoryWidget;
})();