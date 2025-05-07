/**
 * FACE1 Hızlı Duygu Geçişleri Widget'ı
 * Duygu durumu sekanslarını ve hızlı duygu değişimlerini yönetmek için kullanılır
 */
(function() {
    // Widget tanımı
    const EmotionTransitionsWidget = {
        // Varsayılan yapılandırma
        config: {
            recentLimit: 5,  // Son kullanılanlar listesindeki maksimum öğe sayısı
            emotions: [
                { id: 'neutral', name: 'Nötr', intensity: 1.0 },
                { id: 'happy', name: 'Mutlu', intensity: 0.8 },
                { id: 'sad', name: 'Üzgün', intensity: 0.7 },
                { id: 'angry', name: 'Kızgın', intensity: 0.8 },
                { id: 'surprised', name: 'Şaşkın', intensity: 0.9 },
                { id: 'fearful', name: 'Korkmuş', intensity: 0.7 }
            ],
            transitions: []  // Sunucudan yüklenecek
        },
        
        /**
         * Widget'ı başlatır
         * @param {HTMLElement} widgetElement - Widget HTML elementi
         */
        init: function(widgetElement) {
            this.widgetEl = widgetElement;
            this.widgetId = widgetElement.dataset.widgetId;
            
            // Modal elementlerini saklama
            this.modalEl = document.getElementById(`transition-modal-${this.widgetId}`);
            
            // Gerçekleştirilen son duygu sekanslarını izleme
            this.recentTransitions = [];
            
            // Duygu sekansları
            this.transitions = [];
            
            // Olay dinleyicilerini ekle
            this._setupEventListeners();
            
            // Duygu geçişlerini yükle
            this._loadTransitions();
            
            console.log(`EmotionTransitionsWidget başlatıldı: ${this.widgetId}`);
        },
        
        /**
         * Olay dinleyicilerini ayarlar
         */
        _setupEventListeners: function() {
            const self = this;
            
            // Duygu sekansı çalıştırma butonu
            this.widgetEl.querySelectorAll('.play-transition-btn').forEach(btn => {
                btn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    const item = this.closest('.transition-item');
                    if (item) {
                        const transitionId = item.dataset.transitionId;
                        self._playTransition(transitionId);
                    }
                });
            });
            
            // Son kullanılanlar tekrar oynatma butonları
            this.widgetEl.querySelectorAll('.replay-transition-btn').forEach(btn => {
                btn.addEventListener('click', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    const item = this.closest('.recent-transition-item');
                    if (item) {
                        const transitionId = item.dataset.transitionId;
                        self._playTransition(transitionId);
                    }
                });
            });
            
            // Son kullanılanlar öğelerine tıklamak
            this.widgetEl.querySelectorAll('.recent-transition-item').forEach(item => {
                item.addEventListener('click', function(e) {
                    if (!e.target.classList.contains('replay-transition-btn')) {
                        const transitionId = this.dataset.transitionId;
                        self._playTransition(transitionId);
                    }
                });
            });
            
            // Hızlı duygulara tıklamak
            this.widgetEl.querySelectorAll('.quick-emotion-item').forEach(item => {
                item.addEventListener('click', function() {
                    const emotion = this.dataset.emotion;
                    const intensity = parseFloat(this.dataset.intensity) || 1.0;
                    self._setEmotion(emotion, intensity);
                });
            });
            
            // Yeni sekans ekleme butonu
            const addTransitionBtn = this.widgetEl.querySelector(`#add-transition-btn-${this.widgetId}`);
            if (addTransitionBtn) {
                addTransitionBtn.addEventListener('click', function() {
                    self._showTransitionModal();
                });
            }
            
            // Düzenleme butonu
            const editTransitionsBtn = this.widgetEl.querySelector(`#edit-transitions-btn-${this.widgetId}`);
            if (editTransitionsBtn) {
                editTransitionsBtn.addEventListener('click', function() {
                    self._editTransitions();
                });
            }
            
            // Modal olayları
            if (this.modalEl) {
                // Modal kapatma butonu
                const closeBtn = this.modalEl.querySelector('.close-modal-btn');
                if (closeBtn) {
                    closeBtn.addEventListener('click', function() {
                        self._hideTransitionModal();
                    });
                }
                
                // İptal butonu
                const cancelBtn = this.modalEl.querySelector('.cancel-btn');
                if (cancelBtn) {
                    cancelBtn.addEventListener('click', function() {
                        self._hideTransitionModal();
                    });
                }
                
                // Form gönderilmesi
                const form = this.modalEl.querySelector(`#transition-form-${this.widgetId}`);
                if (form) {
                    form.addEventListener('submit', function(e) {
                        e.preventDefault();
                        self._saveTransition(this);
                    });
                }
                
                // Duygu adımı ekleme butonu
                const addStepBtn = this.modalEl.querySelector('.add-emotion-step-btn');
                if (addStepBtn) {
                    addStepBtn.addEventListener('click', function() {
                        self._addEmotionStep();
                    });
                }
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
            
            if (data.type === 'transition_updated' && data.transitions) {
                this.transitions = data.transitions;
                this._renderTransitionsList();
            }
        },
        
        /**
         * Geçişleri yükler
         */
        _loadTransitions: function() {
            const self = this;
            
            // Sunucudan geçişleri al
            fetch('/api/emotions/transitions')
                .then(response => response.json())
                .then(data => {
                    if (data.transitions) {
                        self.transitions = data.transitions;
                        self._renderTransitionsList();
                    }
                    
                    if (data.recent_transitions) {
                        self.recentTransitions = data.recent_transitions;
                        self._renderRecentTransitions();
                    }
                })
                .catch(error => {
                    console.error('Duygu geçişleri yüklenirken hata:', error);
                });
        },
        
        /**
         * Duygu sekansları listesini oluşturur
         */
        _renderTransitionsList: function() {
            const listEl = this.widgetEl.querySelector(`#transitions-list-${this.widgetId}`);
            if (!listEl) return;
            
            listEl.innerHTML = '';
            
            this.transitions.forEach(transition => {
                const li = document.createElement('li');
                li.className = 'transition-item';
                li.dataset.transitionId = transition.id;
                
                let emotionsHtml = '';
                transition.emotions.forEach(emotion => {
                    emotionsHtml += `
                        <div class="sequence-emotion ${emotion.id}" title="${emotion.name} (${emotion.intensity})">
                            <div class="mini-face-icon">
                                <div class="eye left"></div>
                                <div class="eye right"></div>
                                <div class="mouth"></div>
                            </div>
                        </div>
                    `;
                });
                
                li.innerHTML = `
                    <div class="transition-sequence">${emotionsHtml}</div>
                    <div class="transition-info">
                        <div class="transition-name">${transition.name}</div>
                        <div class="transition-description">${transition.description || ''}</div>
                    </div>
                    <div class="transition-actions">
                        <button class="play-transition-btn" title="Oynat">
                            <span class="icon">▶</span>
                        </button>
                    </div>
                `;
                
                // Oynat butonuna tıklama olayı ekle
                const playBtn = li.querySelector('.play-transition-btn');
                playBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    this._playTransition(transition.id);
                });
                
                listEl.appendChild(li);
            });
        },
        
        /**
         * Son kullanılan geçişleri oluşturur
         */
        _renderRecentTransitions: function() {
            const listEl = this.widgetEl.querySelector(`#recent-transitions-${this.widgetId}`);
            if (!listEl) return;
            
            listEl.innerHTML = '';
            
            this.recentTransitions.forEach(transition => {
                const li = document.createElement('li');
                li.className = 'recent-transition-item';
                li.dataset.transitionId = transition.id;
                
                let emotionsHtml = '';
                const displayedEmotions = transition.emotions.slice(0, 2);
                displayedEmotions.forEach(emotion => {
                    emotionsHtml += `<div class="mini-face-icon ${emotion.id}"></div>`;
                });
                
                const moreCount = transition.emotions.length - 2;
                const moreHtml = moreCount > 0 ? 
                    `<div class="more-emotions">+${moreCount}</div>` : '';
                
                li.innerHTML = `
                    <div class="recent-transition-icon">
                        ${emotionsHtml}
                        ${moreHtml}
                    </div>
                    <div class="recent-transition-name">${transition.name}</div>
                    <button class="replay-transition-btn" title="Tekrar Oynat">
                        <span class="icon">↻</span>
                    </button>
                `;
                
                // Öğeye tıklama olayı ekle
                li.addEventListener('click', function(e) {
                    if (!e.target.closest('.replay-transition-btn')) {
                        const transitionId = this.dataset.transitionId;
                        this._playTransition(transitionId);
                    }
                }.bind(this));
                
                // Tekrar oynat butonuna tıklama olayı ekle
                const replayBtn = li.querySelector('.replay-transition-btn');
                replayBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    this._playTransition(transition.id);
                });
                
                listEl.appendChild(li);
            });
        },
        
        /**
         * Bir duygu sekansını oynatır
         * @param {string} transitionId - Sekans ID'si
         */
        _playTransition: function(transitionId) {
            const transition = this.transitions.find(t => t.id === transitionId);
            if (!transition) return;
            
            console.log(`Duygu sekansı oynatılıyor: ${transition.name}`);
            
            // WebSocket üzerinden sekans oynatma isteği gönder
            if (window.socket && window.socket.readyState === WebSocket.OPEN) {
                window.socket.send(JSON.stringify({
                    action: 'play_emotion_transition',
                    transition_id: transitionId
                }));
            } else {
                console.error('WebSocket bağlantısı kapalı!');
                return;
            }
            
            // Son kullanılanlar listesine ekle
            this._addToRecentTransitions(transition);
        },
        
        /**
         * Tek bir duygu durumunu ayarlar
         * @param {string} emotion - Duygu ID'si
         * @param {number} intensity - Duygu yoğunluğu
         */
        _setEmotion: function(emotion, intensity) {
            console.log(`Duygu durumu ayarlanıyor: ${emotion} (${intensity})`);
            
            // WebSocket üzerinden duygu ayarlama isteği gönder
            if (window.socket && window.socket.readyState === WebSocket.OPEN) {
                window.socket.send(JSON.stringify({
                    action: 'set_emotion',
                    emotion: emotion,
                    intensity: intensity
                }));
            } else {
                console.error('WebSocket bağlantısı kapalı!');
            }
        },
        
        /**
         * Son kullanılanlar listesine bir geçiş ekler
         * @param {Object} transition - Eklenecek sekans
         */
        _addToRecentTransitions: function(transition) {
            // Önceden bu geçiş zaten listede var mı kontrol et
            const existingIndex = this.recentTransitions.findIndex(t => t.id === transition.id);
            if (existingIndex !== -1) {
                // Varsa, listeden kaldır (sonra başa ekleyeceğiz)
                this.recentTransitions.splice(existingIndex, 1);
            }
            
            // Başa ekle
            this.recentTransitions.unshift(transition);
            
            // Limit aşılmışsa sondan kırp
            if (this.recentTransitions.length > this.config.recentLimit) {
                this.recentTransitions = this.recentTransitions.slice(0, this.config.recentLimit);
            }
            
            // Son kullanılanları güncelle
            this._renderRecentTransitions();
            
            // Sunucuya da bildir
            if (window.socket && window.socket.readyState === WebSocket.OPEN) {
                window.socket.send(JSON.stringify({
                    action: 'update_recent_transitions',
                    transitions: this.recentTransitions.map(t => t.id)
                }));
            }
        },
        
        /**
         * Duygu sekansı oluşturmak/düzenlemek için modal pencereyi gösterir
         * @param {Object} transition - Düzenlenecek sekans (yeni oluşturma için boş bırakılabilir)
         */
        _showTransitionModal: function(transition = null) {
            if (!this.modalEl) return;
            
            const isEdit = transition !== null;
            const form = this.modalEl.querySelector(`#transition-form-${this.widgetId}`);
            const modalTitle = this.modalEl.querySelector(`#modal-title-${this.widgetId}`);
            const transitionIdInput = this.modalEl.querySelector(`#transition-id-${this.widgetId}`);
            const nameInput = this.modalEl.querySelector(`#transition-name-${this.widgetId}`);
            const descInput = this.modalEl.querySelector(`#transition-description-${this.widgetId}`);
            const stepsContainer = this.modalEl.querySelector(`#emotion-steps-${this.widgetId}`);
            
            // Modalı sıfırla
            transitionIdInput.value = '';
            nameInput.value = '';
            descInput.value = '';
            stepsContainer.innerHTML = '';
            
            // Başlık ayarla
            modalTitle.textContent = isEdit ? 'Duygu Sekansını Düzenle' : 'Yeni Duygu Sekansı Ekle';
            
            // Düzenleme modundaysa, mevcut değerleri forma doldur
            if (isEdit) {
                transitionIdInput.value = transition.id;
                nameInput.value = transition.name;
                descInput.value = transition.description || '';
                
                // Duygu adımlarını ekle
                transition.emotions.forEach(emotion => {
                    this._addEmotionStep(emotion);
                });
            } else {
                // Yeni oluşturma modunda varsayılan bir adım ekle
                this._addEmotionStep();
            }
            
            // Modalı göster
            this.modalEl.classList.remove('hidden');
        },
        
        /**
         * Modal pencereyi gizler
         */
        _hideTransitionModal: function() {
            if (this.modalEl) {
                this.modalEl.classList.add('hidden');
            }
        },
        
        /**
         * Duygu sekansı formunu kaydeder
         * @param {HTMLFormElement} form - Form elementi
         */
        _saveTransition: function(form) {
            const transitionId = form.querySelector(`#transition-id-${this.widgetId}`).value;
            const name = form.querySelector(`#transition-name-${this.widgetId}`).value;
            const description = form.querySelector(`#transition-description-${this.widgetId}`).value;
            
            // Duygu adımlarını topla
            const emotionSteps = Array.from(form.querySelectorAll('.emotion-step')).map(step => {
                const emotionSelect = step.querySelector('select[name="emotion"]');
                const intensityInput = step.querySelector('input[name="intensity"]');
                const durationInput = step.querySelector('input[name="duration"]');
                
                return {
                    id: emotionSelect.value,
                    name: emotionSelect.options[emotionSelect.selectedIndex].text,
                    intensity: parseFloat(intensityInput.value),
                    duration: parseFloat(durationInput.value)
                };
            });
            
            // Sekans verilerini oluştur
            const transitionData = {
                name: name,
                description: description,
                emotions: emotionSteps
            };
            
            // Düzenleme mi yoksa oluşturma mı?
            if (transitionId) {
                transitionData.id = transitionId;
            }
            
            // Sunucuya gönder
            const endpoint = transitionId ? 
                `/api/emotions/transitions/${transitionId}` : 
                '/api/emotions/transitions';
                
            const method = transitionId ? 'PUT' : 'POST';
            
            fetch(endpoint, {
                method: method,
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(transitionData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Geçişleri tekrar yükle
                    this._loadTransitions();
                    
                    // Modalı kapat
                    this._hideTransitionModal();
                } else {
                    console.error('Duygu sekansı kaydedilemedi:', data.message);
                    alert(`Hata: ${data.message}`);
                }
            })
            .catch(error => {
                console.error('Duygu sekansı kaydedilirken hata:', error);
                alert('Sekans kaydedilirken bir hata oluştu.');
            });
        },
        
        /**
         * Sekans düzenleme ekranını gösterir
         */
        _editTransitions: function() {
            // Şu an için basitçe bir uyarı göster
            alert('Bu özellik henüz geliştirme aşamasında. Sekansları tek tek düzenlemek için sekansın üzerine tıklayın.');
        },
        
        /**
         * Duygu sekansına yeni bir adım ekler
         * @param {Object} emotion - Eklenecek duygu verisi (varsa)
         */
        _addEmotionStep: function(emotion = null) {
            const stepsContainer = this.modalEl.querySelector(`#emotion-steps-${this.widgetId}`);
            if (!stepsContainer) return;
            
            const stepEl = document.createElement('div');
            stepEl.className = 'emotion-step';
            
            // Adımın varsayılan verileri
            const stepData = emotion || {
                id: 'neutral',
                intensity: 1.0,
                duration: 1.0
            };
            
            // Duygu seçme, yoğunluk ve süre inputları için HTML
            let emotionsOptionHtml = '';
            this.config.emotions.forEach(e => {
                const selected = e.id === stepData.id ? 'selected' : '';
                emotionsOptionHtml += `<option value="${e.id}" ${selected}>${e.name}</option>`;
            });
            
            stepEl.innerHTML = `
                <div class="step-header">
                    <span class="step-number">#${stepsContainer.children.length + 1}</span>
                    <button type="button" class="remove-step-btn">&times;</button>
                </div>
                <div class="step-content">
                    <div class="step-row">
                        <div class="step-field">
                            <label>Duygu:</label>
                            <select name="emotion" class="emotion-select">
                                ${emotionsOptionHtml}
                            </select>
                        </div>
                        
                        <div class="step-field">
                            <label>Yoğunluk:</label>
                            <input type="range" name="intensity" min="0" max="1" step="0.1" value="${stepData.intensity}" class="intensity-slider">
                            <span class="intensity-value">${stepData.intensity.toFixed(1)}</span>
                        </div>
                        
                        <div class="step-field">
                            <label>Süre (sn):</label>
                            <input type="number" name="duration" min="0.1" max="10" step="0.1" value="${stepData.duration}" class="duration-input">
                        </div>
                    </div>
                </div>
            `;
            
            // Adım silme butonu olayı
            const removeBtn = stepEl.querySelector('.remove-step-btn');
            removeBtn.addEventListener('click', function() {
                stepEl.remove();
                // Adım numaralarını güncelle
                Array.from(stepsContainer.querySelectorAll('.emotion-step')).forEach((step, index) => {
                    step.querySelector('.step-number').textContent = `#${index + 1}`;
                });
            });
            
            // Yoğunluk değeri güncellemesi
            const intensitySlider = stepEl.querySelector('.intensity-slider');
            const intensityValue = stepEl.querySelector('.intensity-value');
            intensitySlider.addEventListener('input', function() {
                intensityValue.textContent = parseFloat(this.value).toFixed(1);
            });
            
            stepsContainer.appendChild(stepEl);
        },
        
        /**
         * Widget verilerini günceller
         * @param {HTMLElement} widgetEl - Widget elementi 
         * @param {Object} data - Güncel veriler
         */
        updateData: function(widgetEl, data) {
            if (data.transitions) {
                this.transitions = data.transitions;
                this._renderTransitionsList();
            }
            
            if (data.recentTransitions) {
                this.recentTransitions = data.recentTransitions;
                this._renderRecentTransitions();
            }
        }
    };
    
    // Widget'ı kaydet
    if (!window.FACE1Widgets) {
        window.FACE1Widgets = {};
    }
    window.FACE1Widgets.emotion_transitions = EmotionTransitionsWidget;
})();