/**
 * FACE1 Robot Animasyon Editörü
 * 
 * Bu JavaScript dosyası, animasyon editörü işlevselliğini sağlar:
 * - Mevcut animasyonları listeleme
 * - Yeni animasyon oluşturma
 * - Animasyonları düzenleme ve kaydetme
 * - Adım eklemek, silmek ve düzenlemek
 * - Zaman çizelgesi görselleştirme
 * - JSON olarak dışa/içe aktarma
 */

// Animasyon verilerini tutacak ana değişkenler
let animations = [];             // Tüm animasyonlar
let currentAnimation = null;     // Şu anda düzenlenen animasyon
let currentStep = null;          // Seçili adım
let isPlaying = false;           // Oynatma durumu
let animationSteps = [];         // Animasyon adımları
let timelineItems = [];          // Zaman çizelgesi öğeleri
let simulationConnection = null; // WebSocket bağlantısı

// DOM Elementleri
const animationSelect = document.getElementById('animation-select');
const stepSelect = document.getElementById('step-select');
const playButton = document.getElementById('play-animation');
const stopButton = document.getElementById('stop-animation');
const animationDescription = document.getElementById('animation-description');
const animationDuration = document.getElementById('animation-duration');
const timelineContainer = document.querySelector('.timeline-items');
const timelineMarker = document.querySelector('.timeline-marker');
const timelineRuler = document.querySelector('.timeline-ruler');

// Form Elementleri
const animationNameInput = document.getElementById('animation-name');
const animationFileInput = document.getElementById('animation-file');
const animationDescInput = document.getElementById('animation-description-input');
const animationDurationInput = document.getElementById('animation-duration-input');
const stepTimeInput = document.getElementById('step-time');

// Eylem sekmeleri ve parametre konteynerları
const eyesAction = document.getElementById('eyes-action');
const mouthAction = document.getElementById('mouth-action');
const ledsAction = document.getElementById('leds-action');
const emotionAction = document.getElementById('emotion-action');
const eyesParams = document.getElementById('eyes-params');
const mouthParams = document.getElementById('mouth-params');
const ledsParams = document.getElementById('leds-params');
const emotionParams = document.getElementById('emotion-params');

// Butonlar
const newAnimationBtn = document.getElementById('new-animation');
const loadAnimationBtn = document.getElementById('load-animation');
const deleteAnimationBtn = document.getElementById('delete-animation');
const addStepBtn = document.getElementById('add-step');
const duplicateStepBtn = document.getElementById('duplicate-step');
const deleteStepBtn = document.getElementById('delete-step');
const saveAnimationBtn = document.getElementById('save-animation');
const exportAnimationBtn = document.getElementById('export-animation');
const importAnimationBtn = document.getElementById('import-animation');

// Tab Butonları
const tabButtons = document.querySelectorAll('.tab-button');
const tabPanes = document.querySelectorAll('.tab-pane');

// Modal Elementleri
const modal = document.getElementById('modal');
const modalTitle = document.getElementById('modal-title');
const modalBody = document.getElementById('modal-body');
const modalConfirm = document.getElementById('modal-confirm');
const modalCancel = document.getElementById('modal-cancel');
const closeModal = document.querySelector('.close-modal');

// Bildirim Elementleri
const notification = document.getElementById('notification');

// Sayfa yüklendiğinde
document.addEventListener('DOMContentLoaded', () => {
    initializeEditor();
    loadAnimations();
    setupEventListeners();
    setupWebSocketConnection();
});

/**
 * Editörü başlatır
 */
function initializeEditor() {
    // Zaman çizelgesi cetvelini oluştur
    createTimelineRuler(10); // 10 saniyelik varsayılan zaman çizelgesi
    
    // Tab işlevselliğini ayarla
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            tabButtons.forEach(b => b.classList.remove('active'));
            tabPanes.forEach(p => p.classList.remove('active'));
            
            button.classList.add('active');
            const tabId = `tab-${button.getAttribute('data-tab')}`;
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Eylem seçici değişikliklerini izle
    eyesAction.addEventListener('change', updateEyesParams);
    mouthAction.addEventListener('change', updateMouthParams);
    ledsAction.addEventListener('change', updateLedsParams);
    emotionAction.addEventListener('change', updateEmotionParams);
    
    // İlk parametre alanlarını oluştur
    updateEyesParams();
    updateMouthParams();
    updateLedsParams();
    updateEmotionParams();
    
    // Modal kapatma işlevselliği
    closeModal.addEventListener('click', () => modal.style.display = 'none');
    modalCancel.addEventListener('click', () => modal.style.display = 'none');
    window.addEventListener('click', (e) => {
        if (e.target === modal) modal.style.display = 'none';
    });
}

/**
 * Tüm olay dinleyicilerini ayarlar
 */
function setupEventListeners() {
    // Animasyon listesi değiştiğinde
    animationSelect.addEventListener('change', onAnimationSelected);
    
    // Adım listesi değiştiğinde
    stepSelect.addEventListener('change', onStepSelected);
    
    // Adımın zamanı değiştiğinde
    stepTimeInput.addEventListener('change', () => {
        if (!currentStep) return;
        const newTime = parseFloat(stepTimeInput.value);
        if (isNaN(newTime) || newTime < 0) return;
        
        currentStep.time = newTime;
        updateStepList();
        updateTimeline();
    });
    
    // Oynat/Durdur butonları
    playButton.addEventListener('click', playCurrentAnimation);
    stopButton.addEventListener('click', stopCurrentAnimation);
    
    // Yeni animasyon butonu
    newAnimationBtn.addEventListener('click', createNewAnimation);
    
    // Animasyon yükleme butonu
    loadAnimationBtn.addEventListener('click', () => {
        if (!animationSelect.value) return;
        loadAnimationDetails(animationSelect.value);
    });
    
    // Animasyon silme butonu
    deleteAnimationBtn.addEventListener('click', deleteSelectedAnimation);
    
    // Adım butonları
    addStepBtn.addEventListener('click', addNewStep);
    duplicateStepBtn.addEventListener('click', duplicateSelectedStep);
    deleteStepBtn.addEventListener('click', deleteSelectedStep);
    
    // Kaydetme butonları
    saveAnimationBtn.addEventListener('click', saveCurrentAnimation);
    exportAnimationBtn.addEventListener('click', exportAnimationToJSON);
    importAnimationBtn.addEventListener('click', importAnimationFromJSON);
}

/**
 * WebSocket bağlantısını kurar
 */
function setupWebSocketConnection() {
    // WebSocket bağlantısı kur
    const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${protocol}//${location.host}/ws/simulation`;
    
    simulationConnection = new WebSocket(wsUrl);
    
    simulationConnection.onopen = () => {
        console.log('WebSocket bağlantısı kuruldu');
    };
    
    simulationConnection.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'simulation') {
            updateSimulationImages(data.data.images);
        } else if (data.type === 'animation_status') {
            updateAnimationStatus(data.data);
        }
    };
    
    simulationConnection.onerror = (error) => {
        console.error('WebSocket hatası:', error);
    };
    
    simulationConnection.onclose = () => {
        console.log('WebSocket bağlantısı kapatıldı');
        // Bağlantıyı yeniden kurmayı dene
        setTimeout(setupWebSocketConnection, 2000);
    };
}

/**
 * Simülasyon görüntülerini günceller
 */
function updateSimulationImages(images) {
    if (images.left_eye) {
        document.querySelector('.simulation-images .left-eye').style.backgroundImage = 
            `url('/simulation/${images.left_eye}')`;
    }
    
    if (images.right_eye) {
        document.querySelector('.simulation-images .right-eye').style.backgroundImage = 
            `url('/simulation/${images.right_eye}')`;
    }
    
    if (images.mouth) {
        document.querySelector('.simulation-images .mouth').style.backgroundImage = 
            `url('/simulation/${images.mouth}')`;
    }
    
    if (images.leds) {
        document.querySelector('.simulation-images .leds').style.backgroundImage = 
            `url('/simulation/${images.leds}')`;
    }
}

/**
 * Animasyon durumunu günceller
 */
function updateAnimationStatus(status) {
    isPlaying = status.playing;
    playButton.disabled = isPlaying;
    stopButton.disabled = !isPlaying;
    
    if (isPlaying) {
        // Zaman çizelgesindeki işaretçiyi güncelle
        const progress = status.progress || 0;
        const duration = currentAnimation?.metadata?.duration || 10;
        const position = (progress / duration) * 100;
        timelineMarker.style.left = `${position}%`;
    }
}

/**
 * Mevcut animasyonları yükler
 */
async function loadAnimations() {
    try {
        const response = await fetch('/api/animations');
        const data = await response.json();
        
        animations = data.animations || [];
        
        // Animasyon seçiciyi doldur
        animationSelect.innerHTML = '';
        animations.forEach(anim => {
            const option = document.createElement('option');
            option.value = anim.name;
            option.textContent = anim.display_name;
            animationSelect.appendChild(option);
        });
        
        if (animations.length > 0) {
            playButton.disabled = false;
        } else {
            animationDescription.textContent = 'Henüz animasyon yok';
        }
        
    } catch (error) {
        console.error('Animasyon yüklenirken hata:', error);
        showNotification('Animasyonlar yüklenemedi: ' + error.message, 'error');
    }
}

/**
 * Seçilen animasyonun detaylarını yükler
 */
async function loadAnimationDetails(animationName) {
    try {
        // Animasyon dosyasının içeriğini al
        const response = await fetch(`/api/animations/${animationName}/details`);
        const animationData = await response.json();
        
        if (!animationData) {
            showNotification('Animasyon yüklenemedi', 'error');
            return;
        }
        
        currentAnimation = animationData;
        
        // Meta bilgileri doldur
        animationNameInput.value = animationData.metadata.name || '';
        animationFileInput.value = animationName || '';
        animationDescInput.value = animationData.metadata.description || '';
        animationDurationInput.value = animationData.metadata.duration || 3.0;
        
        // Adım listesini doldur
        animationSteps = animationData.sequence || [];
        updateStepList();
        
        // Zaman çizelgesini güncelle
        updateTimeline();
        
        // Önizleme bilgilerini güncelle
        animationDescription.textContent = animationData.metadata.description;
        animationDuration.textContent = `Süre: ${animationData.metadata.duration} saniye`;
        
        // Butonları etkinleştir
        playButton.disabled = false;
        
        showNotification('Animasyon yüklendi: ' + animationName);
    } catch (error) {
        console.error('Animasyon detayları yüklenirken hata:', error);
        showNotification('Animasyon detayları yüklenemedi: ' + error.message, 'error');
    }
}

/**
 * Seçilen animasyonu oynatır
 */
async function playCurrentAnimation() {
    if (!animationSelect.value) return;
    
    try {
        const response = await fetch(`/api/animations/${animationSelect.value}/play`, {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            isPlaying = true;
            playButton.disabled = true;
            stopButton.disabled = false;
            showNotification('Animasyon oynatılıyor: ' + animationSelect.value);
        } else {
            showNotification('Animasyon oynatılamadı', 'error');
        }
    } catch (error) {
        console.error('Animasyon oynatılırken hata:', error);
        showNotification('Animasyon oynatılamadı: ' + error.message, 'error');
    }
}

/**
 * Çalan animasyonu durdurur
 */
async function stopCurrentAnimation() {
    try {
        const response = await fetch('/api/animations/stop', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (data.success) {
            isPlaying = false;
            playButton.disabled = false;
            stopButton.disabled = true;
            timelineMarker.style.left = '0';
            showNotification('Animasyon durduruldu');
        }
    } catch (error) {
        console.error('Animasyon durdurulurken hata:', error);
        showNotification('Animasyon durdurulamadı: ' + error.message, 'error');
    }
}

/**
 * Bir animasyon seçildiğinde
 */
function onAnimationSelected() {
    const selectedAnimation = animationSelect.value;
    
    if (!selectedAnimation) {
        animationDescription.textContent = 'Bir animasyon seçin';
        animationDuration.textContent = '';
        playButton.disabled = true;
        return;
    }
    
    // Seçilen animasyonun bilgilerini bul
    const animation = animations.find(a => a.name === selectedAnimation);
    
    if (animation) {
        animationDescription.textContent = animation.description;
        animationDuration.textContent = `Süre: ${animation.duration} saniye`;
        playButton.disabled = false;
    }
}

/**
 * Yeni bir animasyon oluşturur
 */
function createNewAnimation() {
    currentAnimation = {
        metadata: {
            name: "Yeni Animasyon",
            description: "Yeni bir animasyon açıklaması",
            duration: 3.0,
            version: "1.0.0",
            author: "FACE1 Animasyon Editörü",
            date: new Date().toISOString().split('T')[0]
        },
        sequence: []
    };
    
    // Form alanlarını doldur
    animationNameInput.value = currentAnimation.metadata.name;
    animationFileInput.value = "";
    animationDescInput.value = currentAnimation.metadata.description;
    animationDurationInput.value = currentAnimation.metadata.duration;
    
    // Adım listesini temizle
    animationSteps = [];
    updateStepList();
    
    // Zaman çizelgesini güncelle
    updateTimeline();
    
    showNotification('Yeni animasyon oluşturuldu');
}

/**
 * Seçili animasyonu siler
 */
function deleteSelectedAnimation() {
    if (!animationSelect.value) return;
    
    const animationToDelete = animationSelect.value;
    
    // Onay modalını göster
    showModal(
        'Animasyon Sil',
        `<p>"${animationToDelete}" animasyonunu silmek istediğinizden emin misiniz?</p>
         <p>Bu işlem geri alınamaz.</p>`,
        async () => {
            try {
                const response = await fetch(`/api/animations/${animationToDelete}/delete`, {
                    method: 'DELETE'
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showNotification(`"${animationToDelete}" animasyonu silindi`);
                    loadAnimations(); // Listeyi yenile
                } else {
                    showNotification('Animasyon silinemedi', 'error');
                }
            } catch (error) {
                console.error('Animasyon silinirken hata:', error);
                showNotification('Animasyon silinemedi: ' + error.message, 'error');
            }
        }
    );
}

/**
 * Yeni bir adım ekler
 */
function addNewStep() {
    if (!currentAnimation) return;
    
    const newStep = {
        time: animationSteps.length > 0 ? Math.max(...animationSteps.map(step => step.time)) + 0.5 : 0,
        eyes: {
            action: "clear",
            params: {}
        }
    };
    
    animationSteps.push(newStep);
    updateStepList();
    updateTimeline();
    
    // Yeni adımı seç
    stepSelect.value = animationSteps.length - 1;
    onStepSelected();
}

/**
 * Seçili adımı kopyalar
 */
function duplicateSelectedStep() {
    if (!currentStep) return;
    
    // Derin kopya oluştur
    const newStep = JSON.parse(JSON.stringify(currentStep));
    newStep.time += 0.2; // Biraz sonra başlasın
    
    animationSteps.push(newStep);
    updateStepList();
    updateTimeline();
    
    // Yeni adımı seç
    stepSelect.value = animationSteps.length - 1;
    onStepSelected();
}

/**
 * Seçili adımı siler
 */
function deleteSelectedStep() {
    if (!currentStep) return;
    
    const index = animationSteps.indexOf(currentStep);
    if (index === -1) return;
    
    animationSteps.splice(index, 1);
    currentStep = null;
    
    updateStepList();
    updateTimeline();
}

/**
 * Bir adım seçildiğinde çağrılır
 */
function onStepSelected() {
    const index = parseInt(stepSelect.value);
    if (isNaN(index) || index < 0 || index >= animationSteps.length) {
        currentStep = null;
        return;
    }
    
    currentStep = animationSteps[index];
    
    // Zaman alanını güncelle
    stepTimeInput.value = currentStep.time || 0;
    
    // Gözler
    if (currentStep.eyes) {
        eyesAction.value = currentStep.eyes.action;
        updateEyesParams();
        fillEyesParams(currentStep.eyes.params);
    }
    
    // Ağız
    if (currentStep.mouth) {
        mouthAction.value = currentStep.mouth.action;
        updateMouthParams();
        fillMouthParams(currentStep.mouth.params);
    }
    
    // LED'ler
    if (currentStep.leds) {
        ledsAction.value = currentStep.leds.action;
        updateLedsParams();
        fillLedsParams(currentStep.leds.params);
    }
    
    // Duygu
    if (currentStep.emotion) {
        emotionAction.value = currentStep.emotion.action;
        updateEmotionParams();
        fillEmotionParams(currentStep.emotion.params);
    }
}

/**
 * Göz parametrelerini günceller
 */
function updateEyesParams() {
    eyesParams.innerHTML = '';
    
    const action = eyesAction.value;
    
    if (action === 'clear') {
        // Clear eylemi için parametre yok
    } else if (action === 'blink') {
        eyesParams.innerHTML = `
            <div class="form-group">
                <label for="eyes-blink-duration">Kırpma Süresi (sn):</label>
                <input type="number" id="eyes-blink-duration" min="0.1" step="0.1" value="0.2">
            </div>
        `;
    } else if (action === 'look_around') {
        eyesParams.innerHTML = `
            <div class="form-group">
                <label for="eyes-duration">Süre (sn):</label>
                <input type="number" id="eyes-duration" min="0.1" step="0.1" value="1.0">
            </div>
            <div class="form-group">
                <label for="eyes-points">Bakış Noktaları (x,y çiftleri):</label>
                <textarea id="eyes-points">[-0.5, 0], [0.5, 0], [0, 0]</textarea>
                <small>Format: [x1, y1], [x2, y2], ... (-1 ile 1 arası değerler)</small>
            </div>
        `;
    } else if (action === 'growing_circle') {
        eyesParams.innerHTML = `
            <div class="form-group">
                <label for="eyes-circle-duration">Büyüme Süresi (sn):</label>
                <input type="number" id="eyes-circle-duration" min="0.1" step="0.1" value="1.0">
            </div>
        `;
    }
    
    if (currentStep && currentStep.eyes && currentStep.eyes.action === action) {
        fillEyesParams(currentStep.eyes.params);
    }
}

/**
 * Ağız parametrelerini günceller
 */
function updateMouthParams() {
    mouthParams.innerHTML = '';
    
    const action = mouthAction.value;
    
    if (action === 'clear') {
        // Clear eylemi için parametre yok
    } else if (action === 'smile') {
        mouthParams.innerHTML = `
            <div class="form-group">
                <label for="mouth-emotion">Duygu:</label>
                <select id="mouth-emotion">
                    <option value="happy">Mutlu</option>
                    <option value="sad">Üzgün</option>
                    <option value="neutral">Nötr</option>
                    <option value="surprised">Şaşkın</option>
                </select>
            </div>
            <div class="form-group">
                <label for="mouth-intensity">Yoğunluk:</label>
                <input type="range" id="mouth-intensity" min="0" max="1" step="0.1" value="0.7">
                <span id="mouth-intensity-value">0.7</span>
            </div>
        `;
        
        const intensitySlider = document.getElementById('mouth-intensity');
        const intensityValue = document.getElementById('mouth-intensity-value');
        
        intensitySlider.addEventListener('input', () => {
            intensityValue.textContent = intensitySlider.value;
        });
    } else if (action === 'speak') {
        mouthParams.innerHTML = `
            <div class="form-group">
                <label for="mouth-speak-duration">Konuşma Süresi (sn):</label>
                <input type="number" id="mouth-speak-duration" min="0.1" step="0.1" value="1.0">
            </div>
            <div class="form-group">
                <label for="mouth-speak-pattern">Konuşma Deseni:</label>
                <select id="mouth-speak-pattern">
                    <option value="default">Varsayılan</option>
                    <option value="excited">Heyecanlı</option>
                    <option value="slow">Yavaş</option>
                </select>
            </div>
        `;
    }
    
    if (currentStep && currentStep.mouth && currentStep.mouth.action === action) {
        fillMouthParams(currentStep.mouth.params);
    }
}

/**
 * LED parametrelerini günceller
 */
function updateLedsParams() {
    ledsParams.innerHTML = '';
    
    const action = ledsAction.value;
    
    if (action === 'off') {
        // Off eylemi için parametre yok
    } else if (action === 'pulse') {
        ledsParams.innerHTML = `
            <div class="form-group">
                <label for="leds-color">Renk:</label>
                <div class="color-picker">
                    <div class="color-preview" id="led-color-preview"></div>
                    <input type="text" id="leds-color" placeholder="0,0,255">
                    <small>RGB formatı: R,G,B (0-255)</small>
                </div>
            </div>
            <div class="form-group">
                <label for="leds-speed">Hız:</label>
                <input type="range" id="leds-speed" min="10" max="100" step="5" value="50">
                <span id="leds-speed-value">50</span>
            </div>
        `;
        
        const speedSlider = document.getElementById('leds-speed');
        const speedValue = document.getElementById('leds-speed-value');
        const colorInput = document.getElementById('leds-color');
        const colorPreview = document.getElementById('led-color-preview');
        
        speedSlider.addEventListener('input', () => {
            speedValue.textContent = speedSlider.value;
        });
        
        colorInput.addEventListener('input', () => {
            try {
                const rgb = colorInput.value.split(',').map(v => parseInt(v.trim()));
                if (rgb.length === 3) {
                    colorPreview.style.backgroundColor = `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
                }
            } catch (e) {
                console.error('Geçersiz renk formatı');
            }
        });
    } else if (action === 'rainbow') {
        ledsParams.innerHTML = `
            <div class="form-group">
                <label for="leds-rainbow-speed">Hız:</label>
                <input type="range" id="leds-rainbow-speed" min="10" max="100" step="5" value="30">
                <span id="leds-rainbow-speed-value">30</span>
            </div>
        `;
        
        const speedSlider = document.getElementById('leds-rainbow-speed');
        const speedValue = document.getElementById('leds-rainbow-speed-value');
        
        speedSlider.addEventListener('input', () => {
            speedValue.textContent = speedSlider.value;
        });
    }
    
    if (currentStep && currentStep.leds && currentStep.leds.action === action) {
        fillLedsParams(currentStep.leds.params);
    }
}

/**
 * Duygu parametrelerini günceller
 */
function updateEmotionParams() {
    emotionParams.innerHTML = '';
    
    const action = emotionAction.value;
    
    if (action === 'set_emotion') {
        emotionParams.innerHTML = `
            <div class="form-group">
                <label for="emotion-name">Duygu:</label>
                <select id="emotion-name">
                    <option value="happy">Mutlu</option>
                    <option value="sad">Üzgün</option>
                    <option value="angry">Kızgın</option>
                    <option value="surprised">Şaşkın</option>
                    <option value="fearful">Korkmuş</option>
                    <option value="disgusted">İğrenmiş</option>
                    <option value="calm">Sakin</option>
                    <option value="neutral">Nötr</option>
                </select>
            </div>
            <div class="form-group">
                <label for="emotion-transition">Geçiş Süresi (sn):</label>
                <input type="number" id="emotion-transition" min="0.1" step="0.1" value="0.5">
            </div>
            <div class="form-group">
                <label for="emotion-intensity">Yoğunluk:</label>
                <input type="range" id="emotion-intensity" min="0" max="1" step="0.1" value="0.7">
                <span id="emotion-intensity-value">0.7</span>
            </div>
        `;
        
        const intensitySlider = document.getElementById('emotion-intensity');
        const intensityValue = document.getElementById('emotion-intensity-value');
        
        intensitySlider.addEventListener('input', () => {
            intensityValue.textContent = intensitySlider.value;
        });
    }
    
    if (currentStep && currentStep.emotion && currentStep.emotion.action === action) {
        fillEmotionParams(currentStep.emotion.params);
    }
}

/**
 * Göz parametrelerini doldurur
 */
function fillEyesParams(params) {
    if (!params) return;
    
    const action = eyesAction.value;
    
    if (action === 'blink') {
        const durationInput = document.getElementById('eyes-blink-duration');
        if (durationInput) durationInput.value = params.duration || 0.2;
    } else if (action === 'look_around') {
        const durationInput = document.getElementById('eyes-duration');
        const pointsInput = document.getElementById('eyes-points');
        
        if (durationInput) durationInput.value = params.duration || 1.0;
        if (pointsInput && params.points) {
            pointsInput.value = JSON.stringify(params.points).slice(1, -1);
        }
    } else if (action === 'growing_circle') {
        const durationInput = document.getElementById('eyes-circle-duration');
        if (durationInput) durationInput.value = params.duration || 1.0;
    }
}

/**
 * Ağız parametrelerini doldurur
 */
function fillMouthParams(params) {
    if (!params) return;
    
    const action = mouthAction.value;
    
    if (action === 'smile') {
        const emotionSelect = document.getElementById('mouth-emotion');
        const intensitySlider = document.getElementById('mouth-intensity');
        const intensityValue = document.getElementById('mouth-intensity-value');
        
        if (emotionSelect) emotionSelect.value = params.emotion || 'happy';
        if (intensitySlider) {
            intensitySlider.value = params.intensity || 0.7;
            if (intensityValue) intensityValue.textContent = intensitySlider.value;
        }
    } else if (action === 'speak') {
        const durationInput = document.getElementById('mouth-speak-duration');
        const patternSelect = document.getElementById('mouth-speak-pattern');
        
        if (durationInput) durationInput.value = params.duration || 1.0;
        if (patternSelect) patternSelect.value = params.pattern || 'default';
    }
}

/**
 * LED parametrelerini doldurur
 */
function fillLedsParams(params) {
    if (!params) return;
    
    const action = ledsAction.value;
    
    if (action === 'pulse') {
        const colorInput = document.getElementById('leds-color');
        const colorPreview = document.getElementById('led-color-preview');
        const speedSlider = document.getElementById('leds-speed');
        const speedValue = document.getElementById('leds-speed-value');
        
        if (colorInput && params.color) {
            colorInput.value = params.color.join(',');
            if (colorPreview) {
                const [r, g, b] = params.color;
                colorPreview.style.backgroundColor = `rgb(${r}, ${g}, ${b})`;
            }
        }
        
        if (speedSlider) {
            speedSlider.value = params.speed || 50;
            if (speedValue) speedValue.textContent = speedSlider.value;
        }
    } else if (action === 'rainbow') {
        const speedSlider = document.getElementById('leds-rainbow-speed');
        const speedValue = document.getElementById('leds-rainbow-speed-value');
        
        if (speedSlider) {
            speedSlider.value = params.speed || 30;
            if (speedValue) speedValue.textContent = speedSlider.value;
        }
    }
}

/**
 * Duygu parametrelerini doldurur
 */
function fillEmotionParams(params) {
    if (!params) return;
    
    const emotionSelect = document.getElementById('emotion-name');
    const transitionInput = document.getElementById('emotion-transition');
    const intensitySlider = document.getElementById('emotion-intensity');
    const intensityValue = document.getElementById('emotion-intensity-value');
    
    if (emotionSelect) emotionSelect.value = params.emotion || 'calm';
    if (transitionInput) transitionInput.value = params.transition || 0.5;
    if (intensitySlider) {
        intensitySlider.value = params.intensity || 0.7;
        if (intensityValue) intensityValue.textContent = intensitySlider.value;
    }
}

/**
 * Adım listesini günceller
 */
function updateStepList() {
    stepSelect.innerHTML = '';
    
    // Adımları zamana göre sırala
    const sortedSteps = [...animationSteps].sort((a, b) => a.time - b.time);
    
    sortedSteps.forEach((step, index) => {
        const option = document.createElement('option');
        option.value = animationSteps.indexOf(step);
        
        let description = `Adım ${index + 1} (${step.time}s):`;
        
        if (step.eyes) description += ` Göz: ${step.eyes.action}`;
        if (step.mouth) description += ` Ağız: ${step.mouth.action}`;
        if (step.leds) description += ` LED: ${step.leds.action}`;
        if (step.emotion) description += ` Duygu: ${step.emotion.action}`;
        
        option.textContent = description;
        stepSelect.appendChild(option);
    });
}

/**
 * Zaman çizelgesini günceller
 */
function updateTimeline() {
    if (!currentAnimation) return;
    
    // Maksimum süreye göre cetvel oluştur
    const duration = parseFloat(animationDurationInput.value) || 10;
    createTimelineRuler(duration);
    
    // Zaman çizelgesi öğelerini temizle
    timelineItems.forEach(item => item.remove());
    timelineItems = [];
    
    timelineContainer.innerHTML = '';
    
    // Her adım için zaman çizelgesi öğesi oluştur
    animationSteps.forEach(step => {
        const position = (step.time / duration) * 100;
        
        if (step.eyes) {
            const item = document.createElement('div');
            item.className = 'timeline-item eyes';
            item.style.left = `${position}%`;
            item.title = `Göz: ${step.eyes.action} (${step.time}s)`;
            timelineContainer.appendChild(item);
            timelineItems.push(item);
        }
        
        if (step.mouth) {
            const item = document.createElement('div');
            item.className = 'timeline-item mouth';
            item.style.left = `${position}%`;
            item.title = `Ağız: ${step.mouth.action} (${step.time}s)`;
            timelineContainer.appendChild(item);
            timelineItems.push(item);
        }
        
        if (step.leds) {
            const item = document.createElement('div');
            item.className = 'timeline-item leds';
            item.style.left = `${position}%`;
            item.title = `LED: ${step.leds.action} (${step.time}s)`;
            timelineContainer.appendChild(item);
            timelineItems.push(item);
        }
    });
}

/**
 * Zaman çizelgesi cetveli oluşturur
 */
function createTimelineRuler(duration) {
    timelineRuler.innerHTML = '';
    
    // Her saniye için bir işaret oluştur
    for (let i = 0; i <= duration; i++) {
        const marker = document.createElement('div');
        marker.className = 'ruler-marker';
        marker.textContent = `${i}s`;
        timelineRuler.appendChild(marker);
    }
}

/**
 * Mevcut adımı günceller
 */
function updateCurrentStep() {
    if (!currentStep) return;
    
    const action = eyesAction.value;
    
    // Gözler
    currentStep.eyes = {
        action: eyesAction.value,
        params: {}
    };
    
    if (action === 'blink') {
        const duration = parseFloat(document.getElementById('eyes-blink-duration').value);
        currentStep.eyes.params = { duration };
    } else if (action === 'look_around') {
        const duration = parseFloat(document.getElementById('eyes-duration').value);
        const pointsStr = document.getElementById('eyes-points').value;
        let points = [];
        
        try {
            points = JSON.parse(`[${pointsStr}]`);
        } catch (e) {
            console.error('Geçersiz bakış noktaları formatı', e);
        }
        
        currentStep.eyes.params = { duration, points };
    } else if (action === 'growing_circle') {
        const duration = parseFloat(document.getElementById('eyes-circle-duration').value);
        currentStep.eyes.params = { duration };
    }
    
    // Ağız
    if (mouthAction.value !== 'none') {
        currentStep.mouth = {
            action: mouthAction.value,
            params: {}
        };
        
        if (mouthAction.value === 'smile') {
            const emotion = document.getElementById('mouth-emotion').value;
            const intensity = parseFloat(document.getElementById('mouth-intensity').value);
            currentStep.mouth.params = { emotion, intensity };
        } else if (mouthAction.value === 'speak') {
            const duration = parseFloat(document.getElementById('mouth-speak-duration').value);
            const pattern = document.getElementById('mouth-speak-pattern').value;
            currentStep.mouth.params = { duration, pattern };
        }
    } else {
        delete currentStep.mouth;
    }
    
    // LED'ler
    if (ledsAction.value !== 'none') {
        currentStep.leds = {
            action: ledsAction.value,
            params: {}
        };
        
        if (ledsAction.value === 'pulse') {
            const speedValue = parseInt(document.getElementById('leds-speed').value);
            let colorValue = [0, 0, 255]; // Varsayılan mavi
            
            try {
                colorValue = document.getElementById('leds-color').value
                    .split(',')
                    .map(v => parseInt(v.trim()));
            } catch (e) {
                console.error('Geçersiz renk formatı');
            }
            
            currentStep.leds.params = { speed: speedValue, color: colorValue };
        } else if (ledsAction.value === 'rainbow') {
            const speedValue = parseInt(document.getElementById('leds-rainbow-speed').value);
            currentStep.leds.params = { speed: speedValue };
        }
    } else {
        delete currentStep.leds;
    }
    
    // Duygu
    if (emotionAction.value !== 'none') {
        currentStep.emotion = {
            action: emotionAction.value,
            params: {}
        };
        
        if (emotionAction.value === 'set_emotion') {
            const emotion = document.getElementById('emotion-name').value;
            const transition = parseFloat(document.getElementById('emotion-transition').value);
            const intensity = parseFloat(document.getElementById('emotion-intensity').value);
            currentStep.emotion.params = { emotion, transition, intensity };
        }
    } else {
        delete currentStep.emotion;
    }
    
    updateStepList();
    updateTimeline();
}

/**
 * Mevcut animasyonu kaydeder
 */
async function saveCurrentAnimation() {
    if (!currentAnimation) return;
    
    // Form verileri
    const name = animationNameInput.value.trim();
    const description = animationDescInput.value.trim();
    const duration = parseFloat(animationDurationInput.value);
    let fileName = animationFileInput.value.trim();
    
    // Doğrulama
    if (!name) {
        showNotification('Lütfen animasyon adını girin', 'error');
        return;
    }
    
    if (!fileName) {
        // İsimden dosya adı oluştur
        fileName = name.toLowerCase().replace(/\s+/g, '_');
    }
    
    // Uzantıyı kaldır (otomatik olarak eklenecek)
    if (fileName.endsWith('.json')) {
        fileName = fileName.slice(0, -5);
    }
    
    // Adım olmadan animasyon kaydedemeyiz
    if (animationSteps.length === 0) {
        showNotification('En az bir adım ekleyin', 'error');
        return;
    }
    
    // Metadata güncelle
    currentAnimation.metadata = {
        name,
        description,
        duration,
        version: currentAnimation.metadata.version || "1.0.0",
        author: currentAnimation.metadata.author || "FACE1 Animasyon Editörü",
        date: new Date().toISOString().split('T')[0]
    };
    
    // Adımları zamana göre sırala
    currentAnimation.sequence = [...animationSteps].sort((a, b) => a.time - b.time);
    
    try {
        // Animasyonu kaydet
        const response = await fetch(`/api/animations/${fileName}/save`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(currentAnimation)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification(`Animasyon kaydedildi: ${fileName}`);
            loadAnimations(); // Listeyi yenile
            
            // Yeni oluşturulan animasyonu seç
            setTimeout(() => {
                animationSelect.value = fileName;
                onAnimationSelected();
            }, 500);
        } else {
            showNotification('Animasyon kaydedilemedi: ' + data.message, 'error');
        }
    } catch (error) {
        console.error('Animasyon kaydedilirken hata:', error);
        showNotification('Animasyon kaydedilemedi: ' + error.message, 'error');
    }
}

/**
 * Animasyon verilerini JSON olarak dışa aktarır
 */
function exportAnimationToJSON() {
    if (!currentAnimation) return;
    
    // Adımları zamana göre sırala
    currentAnimation.sequence = [...animationSteps].sort((a, b) => a.time - b.time);
    
    // JSON formatına dönüştür
    const jsonString = JSON.stringify(currentAnimation, null, 2);
    
    // JSON içeriğini modalda göster
    showModal(
        'JSON Olarak Dışa Aktar',
        `<div class="form-group">
            <textarea style="width:100%; height:300px; font-family:monospace; white-space:pre;">${jsonString}</textarea>
         </div>
         <p>JSON verisini kopyalayın veya kaydedin.</p>`,
        null,
        'Kapat'
    );
}

/**
 * JSON verilerinden animasyon içe aktarır
 */
function importAnimationFromJSON() {
    showModal(
        'JSON İçe Aktar',
        `<div class="form-group">
            <textarea id="import-json" style="width:100%; height:300px; font-family:monospace; white-space:pre;" placeholder="JSON verilerini buraya yapıştırın..."></textarea>
         </div>`,
        () => {
            const jsonText = document.getElementById('import-json').value;
            
            try {
                const animationData = JSON.parse(jsonText);
                
                // Temel doğrulama
                if (!animationData.metadata || !animationData.sequence) {
                    throw new Error('Geçersiz animasyon formatı');
                }
                
                // Animasyon verilerini ayarla
                currentAnimation = animationData;
                animationSteps = [...animationData.sequence];
                
                // Form alanlarını doldur
                animationNameInput.value = animationData.metadata.name || '';
                animationFileInput.value = '';
                animationDescInput.value = animationData.metadata.description || '';
                animationDurationInput.value = animationData.metadata.duration || 3.0;
                
                // UI güncelle
                updateStepList();
                updateTimeline();
                
                showNotification('Animasyon içe aktarıldı');
            } catch (error) {
                console.error('JSON ayrıştırılırken hata:', error);
                showNotification('Geçersiz JSON formatı: ' + error.message, 'error');
            }
        },
        'İçe Aktar'
    );
}

/**
 * Bildirim gösterir
 * 
 * @param {string} message - Gösterilecek mesaj
 * @param {string} type - Bildirim tipi ('success', 'error', 'warning', 'info')
 * @param {number} duration - Bildirimin otomatik kapanma süresi (ms)
 * @param {boolean} autoHide - Otomatik kaybolsun mu?
 */
function showNotification(message, type = 'success', duration = 5000, autoHide = true) {
    // Önceki bildirimleri temizle
    clearTimeout(notification.dataset.timer);
    
    // Bildirim içeriğini ayarla
    let iconHtml = '';
    switch(type) {
        case 'error':
            iconHtml = '<span style="margin-right:10px;">❌</span>';
            break;
        case 'warning':
            iconHtml = '<span style="margin-right:10px;">⚠️</span>';
            break;
        case 'info':
            iconHtml = '<span style="margin-right:10px;">ℹ️</span>';
            break;
        case 'success':
        default:
            iconHtml = '<span style="margin-right:10px;">✅</span>';
            break;
    }
    
    // Bildirim içeriği 
    notification.innerHTML = `
        ${iconHtml}
        <div style="flex: 1">${message}</div>
        <span class="notification-close" onclick="document.getElementById('notification').style.display='none'">&times;</span>
    `;
    
    // Bildirim stilini ayarla
    notification.className = 'notification';
    notification.classList.add(type);
    notification.style.display = 'flex';
    notification.style.alignItems = 'center';
    notification.style.justifyContent = 'space-between';
    
    // Animasyon ile bildirimi göster
    notification.style.opacity = '0';
    setTimeout(() => {
        notification.style.opacity = '1';
    }, 10);
    
    // Otomatik kapanma
    if (autoHide) {
        const timer = setTimeout(() => {
            notification.style.opacity = '0';
            setTimeout(() => {
                notification.style.display = 'none';
            }, 300);
        }, duration);
        notification.dataset.timer = timer;
    }
    
    // Tıklandığında kapat (dokunmatik ekranlar için)
    notification.addEventListener('click', function(e) {
        // Kapatma düğmesine tıklanmadıysa bildirimi kapat
        if (!e.target.classList.contains('notification-close')) {
            notification.style.opacity = '0';
            setTimeout(() => {
                notification.style.display = 'none';
            }, 300);
        }
    });
    
    // Konsola da yaz
    console.log(`[${type.toUpperCase()}] ${message}`);
}

/**
 * Hata bildirimini gösterir
 * 
 * @param {string} message - Hata mesajı
 * @param {number} code - Hata kodu (opsiyonel)
 * @param {boolean} recoverable - Hatanın düzeltilebilir olup olmadığı
 */
function showErrorNotification(message, code = null, recoverable = true) {
    const codeText = code ? `[Kod: ${code}] ` : '';
    const recoveryText = recoverable ? '' : ' (Düzeltilemez)';
    showNotification(`${codeText}${message}${recoveryText}`, 'error', recoverable ? 5000 : 8000, recoverable);
}

/**
 * Onay modalı gösterir
 */
function showModal(title, content, onConfirm, confirmText = 'Tamam') {
    modalTitle.textContent = title;
    modalBody.innerHTML = content;
    modalConfirm.textContent = confirmText;
    
    if (onConfirm) {
        modalConfirm.onclick = () => {
            onConfirm();
            modal.style.display = 'none';
        };
        modalConfirm.style.display = 'block';
    } else {
        modalConfirm.style.display = 'none';
    }
    
    modal.style.display = 'block';
}