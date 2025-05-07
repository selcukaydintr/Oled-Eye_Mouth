/**
 * FACE1 Yüz İfadesi Kontrolü Widget'ı
 * Duygu durumunu kontrol etmek için kullanılır
 */
(function() {
    // Widget tanımı
    const ExpressionControlWidget = {
        // Varsayılan yapılandırma
        config: {
            emotions: [
                { id: 'neutral', name: 'Nötr' },
                { id: 'happy', name: 'Mutlu' },
                { id: 'sad', name: 'Üzgün' },
                { id: 'angry', name: 'Kızgın' },
                { id: 'surprised', name: 'Şaşkın' },
                { id: 'fearful', name: 'Korkmuş' },
                { id: 'disgusted', name: 'İğrenmiş' },
                { id: 'calm', name: 'Sakin' }
            ]
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
                expressionItems: widgetElement.querySelectorAll('.expression-item'),
                intensitySlider: widgetElement.querySelector('.expression-intensity'),
                intensityValue: widgetElement.querySelector('.intensity-value'),
                durationSlider: widgetElement.querySelector('.expression-duration'),
                durationValue: widgetElement.querySelector('.duration-value'),
                microCheckbox: widgetElement.querySelector('.expression-micro'),
                currentEmotionName: widgetElement.querySelector('.current-emotion-name'),
                previewFace: widgetElement.querySelector('.preview-face')
            };
            
            // Mevcut durumu izleme
            this.state = {
                currentEmotion: 'neutral',
                intensity: 1.0,
                duration: 1.0,
                isMicro: false
            };
            
            // Olay dinleyicileri ekle
            this._setupEventListeners();
            
            // WebSocket üzerinden mevcut duygu durumunu al
            this._getCurrentEmotionState();
            
            console.log(`ExpressionControlWidget başlatıldı: ${this.widgetId}`);
        },
        
        /**
         * Olay dinleyicilerini ayarlar
         */
        _setupEventListeners: function() {
            const self = this;
            
            // İfadelere tıklama olayları
            this.elements.expressionItems.forEach(item => {
                item.addEventListener('click', function() {
                    const emotion = this.dataset.emotion;
                    self._setActiveEmotion(emotion);
                    self._applyEmotionChange();
                });
            });
            
            // Yoğunluk kaydırıcısı değişikliği
            this.elements.intensitySlider.addEventListener('input', function() {
                const value = parseFloat(this.value).toFixed(1);
                self.elements.intensityValue.textContent = value;
                self.state.intensity = parseFloat(value);
                self._updatePreviewFace();
            });
            
            // Süre kaydırıcısı değişikliği
            this.elements.durationSlider.addEventListener('input', function() {
                const value = parseFloat(this.value).toFixed(1);
                self.elements.durationValue.textContent = value;
                self.state.duration = parseFloat(value);
            });
            
            // Mikro ifade onay kutusu değişikliği
            this.elements.microCheckbox.addEventListener('change', function() {
                self.state.isMicro = this.checked;
            });
            
            // WebSocket mesaj dinleyicisi ekle
            if (window.socket) {
                window.socket.addEventListener('message', function(event) {
                    const data = JSON.parse(event.data);
                    if (data.type === 'emotion_changed') {
                        self._updateCurrentEmotion(data.emotion.state, data.emotion.intensity);
                    }
                });
            }
        },
        
        /**
         * Aktif duygu durumunu ayarlar
         * @param {string} emotion - Duygu ID'si
         */
        _setActiveEmotion: function(emotion) {
            // Önceki aktif ifadeyi temizle
            this.elements.expressionItems.forEach(item => {
                item.classList.remove('active');
            });
            
            // Yeni aktif ifadeyi belirle
            const activeItem = Array.from(this.elements.expressionItems).find(
                item => item.dataset.emotion === emotion
            );
            
            if (activeItem) {
                activeItem.classList.add('active');
                this.state.currentEmotion = emotion;
                this._updatePreviewFace();
            }
        },
        
        /**
         * Önizleme yüzünü günceller
         */
        _updatePreviewFace: function() {
            // Tüm ifade sınıflarını kaldır
            const previewFace = this.elements.previewFace;
            previewFace.classList.remove('neutral', 'happy', 'sad', 'angry', 
                                          'surprised', 'fearful', 'disgusted', 'calm');
            
            // Geçerli ifade sınıfını ekle
            previewFace.classList.add(this.state.currentEmotion);
            
            // İfade adını güncelle
            const emotionName = this.config.emotions.find(
                e => e.id === this.state.currentEmotion
            )?.name || 'Nötr';
            
            this.elements.currentEmotionName.textContent = emotionName;
            
            // Yoğunluğu yansıt
            const intensity = this.state.intensity;
            const eyes = previewFace.querySelectorAll('.eye');
            const mouth = previewFace.querySelector('.mouth');
            
            // İfadeye özgü stil ayarlamaları
            switch(this.state.currentEmotion) {
                case 'happy':
                    mouth.style.height = `${20 * intensity}px`;
                    mouth.style.borderBottom = 'none';
                    mouth.style.borderRadius = '0 0 20px 20px';
                    mouth.style.backgroundColor = '#333';
                    break;
                case 'sad':
                    mouth.style.height = '3px';
                    mouth.style.borderBottom = 'none';
                    mouth.style.borderTop = '3px solid #333';
                    mouth.style.borderRadius = '20px 20px 0 0';
                    mouth.style.backgroundColor = 'transparent';
                    break;
                case 'angry':
                    eyes.forEach(eye => {
                        eye.style.transform = `rotate(${15 * intensity}deg)`;
                        eye.style.height = `${18 * intensity}px`;
                    });
                    mouth.style.width = '40px';
                    mouth.style.height = '3px';
                    mouth.style.borderBottom = '3px solid #333';
                    mouth.style.borderTop = 'none';
                    mouth.style.borderRadius = '0';
                    mouth.style.backgroundColor = 'transparent';
                    break;
                case 'surprised':
                    eyes.forEach(eye => {
                        eye.style.height = `${24 * intensity}px`;
                        eye.style.transform = 'rotate(0)';
                    });
                    mouth.style.height = `${20 * intensity}px`;
                    mouth.style.width = `${20 * intensity}px`;
                    mouth.style.border = '3px solid #333';
                    mouth.style.borderRadius = '50%';
                    mouth.style.backgroundColor = 'transparent';
                    break;
                default:
                    eyes.forEach(eye => {
                        eye.style.transform = 'rotate(0)';
                        eye.style.height = '24px';
                    });
                    mouth.style.height = '20px';
                    mouth.style.width = '50px';
                    mouth.style.borderBottom = '3px solid #333';
                    mouth.style.borderTop = 'none';
                    mouth.style.borderRadius = '0';
                    mouth.style.backgroundColor = 'transparent';
            }
        },
        
        /**
         * Duygu değişikliğini API'ye gönderir
         */
        _applyEmotionChange: function() {
            const payload = {
                emotion: this.state.currentEmotion,
                intensity: this.state.intensity,
                duration: this.state.duration,
                is_micro: this.state.isMicro
            };
            
            // WebSocket kullanarak duygu değişikliği gönder
            if (window.socket && window.socket.readyState === WebSocket.OPEN) {
                window.socket.send(JSON.stringify({
                    action: this.state.isMicro ? 'show_micro_expression' : 'set_emotion',
                    ...payload
                }));
                
                console.log('Duygu değişikliği gönderildi:', payload);
            } else {
                console.error('WebSocket bağlantısı kapalı!');
                return;
            }
            
            // Önizlemeyi güncelle
            this._updatePreviewFace();
        },
        
        /**
         * Mevcut duygu durumunu WebSocket üzerinden alır
         */
        _getCurrentEmotionState: function() {
            if (window.socket && window.socket.readyState === WebSocket.OPEN) {
                window.socket.send(JSON.stringify({
                    action: 'get_emotion_state'
                }));
                console.log('Mevcut duygu durumu istendi');
            }
        },
        
        /**
         * Widget verilerini günceller
         * @param {HTMLElement} widgetEl - Widget elementi 
         * @param {Object} data - Güncel veriler
         */
        updateData: function(widgetEl, data) {
            if (data.emotion) {
                this._updateCurrentEmotion(data.emotion.state, data.emotion.intensity);
            }
        },
        
        /**
         * Aktif duygu durumunu günceller
         * @param {string} emotion - Duygu ID'si
         * @param {number} intensity - Duygu yoğunluğu
         */
        _updateCurrentEmotion: function(emotion, intensity) {
            this.state.currentEmotion = emotion;
            this.state.intensity = intensity;
            
            // UI öğelerini güncelle
            this._setActiveEmotion(emotion);
            this.elements.intensitySlider.value = intensity;
            this.elements.intensityValue.textContent = intensity.toFixed(1);
            
            // Önizlemeyi güncelle
            this._updatePreviewFace();
        }
    };
    
    // Widget'ı kaydet
    if (!window.FACE1Widgets) {
        window.FACE1Widgets = {};
    }
    window.FACE1Widgets.expression_control = ExpressionControlWidget;
})();