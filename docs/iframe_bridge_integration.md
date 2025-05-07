# FACE1 IFrame Entegrasyon Kılavuzu

## İçindekiler

- [Genel Bakış](#genel-bakış)
- [Entegrasyon Adımları](#entegrasyon-adımları)
- [Mesaj Protokolü](#mesaj-protokolü)
- [API Referansı](#api-referansı)
- [Olay Dinleyicileri](#olay-dinleyicileri)
- [Güvenlik Hususları](#güvenlik-hususları)
- [İleri Düzey Kullanım](#i̇leri-düzey-kullanım)
- [Sorun Giderme](#sorun-giderme)
- [Örnek Kodlar](#örnek-kodlar)

## Genel Bakış

FACE1, üst projelere kolayca entegre edilebilmesi için IFrame tabanlı bir entegrasyon mekanizması sunar. Bu entegrasyon, FACE1'in kendi arayüzünü ve işlevselliğini korurken, üst projenin kendi arayüzü içinde FACE1'i gömülü olarak kullanmasına ve kontrol etmesine olanak tanır.

### IFrame Entegrasyonu Nedir?

IFrame (Inline Frame) entegrasyonu, bir web sayfasının başka bir web sayfasını kendi içinde göstermesine olanak tanıyan bir HTML öğesidir. FACE1 IFrame köprüsü, bu standart HTML özelliğini genişleterek üst projenin ve FACE1'in karşılıklı iletişim kurabilmesini sağlar.

### Avantajları

- **İzolasyon**: FACE1'in kodu ve işlevselliği üst projeden izole edilir
- **Kolay Entegrasyon**: Minimum kod değişikliği gerektirir
- **Güvenlik**: Kontrollü bir iletişim kanalı sağlar
- **Esneklik**: Üst proje, FACE1'i ihtiyaca göre özelleştirebilir
- **Çift Yönlü İletişim**: Hem üst projeden FACE1'e, hem de FACE1'den üst projeye iletişim mümkündür

## Entegrasyon Adımları

### 1. HTML Sayfanıza IFrame Ekleme

Üst projenizin HTML sayfasına FACE1 için bir IFrame ekleyin:

```html
<iframe 
  id="face1-frame" 
  src="http://localhost:8000/embed" 
  width="800" 
  height="600"
  scrolling="no"
  allowtransparency="true"
  style="border: none; overflow: hidden;">
</iframe>
```

### 2. IFrame İletişim Kodunu Ekleme

Üst projenizde JavaScript dosyanıza şu kodu ekleyin:

```javascript
// FACE1 IFrame Köprüsü
class Face1Bridge {
  constructor(iframeId, targetOrigin = 'http://localhost:8000') {
    this.iframe = document.getElementById(iframeId);
    this.targetOrigin = targetOrigin;
    this.eventHandlers = {};
    this.isConnected = false;
    this.messageQueue = [];
    this.setupMessageListener();
    this.connect();
  }

  // Mesaj dinleyici kurulumu
  setupMessageListener() {
    window.addEventListener('message', (event) => {
      if (event.origin !== this.targetOrigin) return;
      
      const message = event.data;
      
      // Bağlantı yanıtını işle
      if (message.type === 'FACE1_CONNECT_RESPONSE') {
        this.isConnected = true;
        console.log('FACE1 ile bağlantı kuruldu');
        this.processMessageQueue();
        return;
      }
      
      // Kayıtlı olay işleyicilerini çağır
      if (this.eventHandlers[message.type]) {
        this.eventHandlers[message.type].forEach(handler => handler(message.data));
      }
      
      // Genel olay işleyicilerini çağır
      if (this.eventHandlers['*']) {
        this.eventHandlers['*'].forEach(handler => handler(message));
      }
    });
  }

  // Bağlantı kurma
  connect() {
    this.sendMessage('FACE1_CONNECT_REQUEST', {
      version: '1.0',
      clientName: 'ParentApp'
    });
  }

  // Mesaj kuyruğunu işleme
  processMessageQueue() {
    while (this.messageQueue.length > 0) {
      const { type, data } = this.messageQueue.shift();
      this.sendMessage(type, data);
    }
  }

  // Mesaj gönderimi
  sendMessage(type, data) {
    if (!this.isConnected && type !== 'FACE1_CONNECT_REQUEST') {
      this.messageQueue.push({ type, data });
      return;
    }

    this.iframe.contentWindow.postMessage({
      type: type,
      data: data,
      timestamp: Date.now()
    }, this.targetOrigin);
  }

  // Olay dinleyici ekleme
  on(eventType, handler) {
    if (!this.eventHandlers[eventType]) {
      this.eventHandlers[eventType] = [];
    }
    this.eventHandlers[eventType].push(handler);
    return this;
  }

  // Olay dinleyici kaldırma
  off(eventType, handler) {
    if (!this.eventHandlers[eventType]) return this;
    
    if (!handler) {
      delete this.eventHandlers[eventType];
    } else {
      this.eventHandlers[eventType] = this.eventHandlers[eventType]
        .filter(h => h !== handler);
    }
    return this;
  }

  // Duygu ayarlama
  setEmotion(emotion, intensity = 1.0) {
    this.sendMessage('FACE1_SET_EMOTION', { 
      emotion: emotion, 
      intensity: intensity 
    });
  }

  // Animasyon oynatma
  playAnimation(animationName) {
    this.sendMessage('FACE1_PLAY_ANIMATION', { 
      animation: animationName 
    });
  }

  // Animasyonu durdurma
  stopAnimation() {
    this.sendMessage('FACE1_STOP_ANIMATION', {});
  }

  // Tema değiştirme
  setTheme(themeName) {
    this.sendMessage('FACE1_SET_THEME', { 
      theme: themeName 
    });
  }

  // Ses tepkimeli mod kontrolü
  setSoundReactive(enabled) {
    this.sendMessage('FACE1_SET_SOUND_REACTIVE', { 
      enabled: enabled 
    });
  }

  // Simülasyon modu kontrolü
  setSimulationMode(enabled) {
    this.sendMessage('FACE1_SET_SIMULATION', { 
      enabled: enabled 
    });
  }
}

// FACE1 Köprüsünü başlat
const face1 = new Face1Bridge('face1-frame');

// Örnekler:
// Olay dinleyicisi ekle
face1.on('FACE1_EMOTION_CHANGE', (data) => {
  console.log('Duygu değişti:', data.emotion, data.intensity);
});

// Duygu ayarla
// face1.setEmotion('happy', 0.8);

// Animasyon oynat
// face1.playAnimation('hello_animation');
```

### 3. Üst Proje Kontrollerini Bağlama

Üst projenizin kullanıcı arayüzü elemanlarını FACE1 kontrollerine bağlayın:

```javascript
// Örnek duygu butonları
document.getElementById('btn-happy').addEventListener('click', function() {
  face1.setEmotion('happy', 0.8);
});

document.getElementById('btn-sad').addEventListener('click', function() {
  face1.setEmotion('sad', 0.7);
});

// Animasyon kontrolleri
document.getElementById('btn-play-greeting').addEventListener('click', function() {
  face1.playAnimation('hello_animation');
});

// Tema değiştirme
document.getElementById('theme-selector').addEventListener('change', function() {
  face1.setTheme(this.value);
});
```

### 4. Olayları Dinleme

FACE1'den gelecek olayları dinleyin ve üst projenizde işleyin:

```javascript
// Duygu değişikliklerini dinle
face1.on('FACE1_EMOTION_CHANGE', (data) => {
  updateEmotionUI(data.emotion, data.intensity);
});

// Animasyon durumunu dinle
face1.on('FACE1_ANIMATION_UPDATE', (data) => {
  updateAnimationProgressBar(data.progress);
  if (data.playing === false) {
    animationCompleted(data.animation);
  }
});

// Sistem durumunu dinle
face1.on('FACE1_SYSTEM_STATUS', (data) => {
  updateSystemStatus(data.status, data.uptime);
});
```

## Mesaj Protokolü

FACE1 IFrame entegrasyonu, JSON tabanlı bir mesaj protokolü kullanır. Her mesaj aşağıdaki formattadır:

```json
{
  "type": "MESAJ_TİPİ",
  "data": {
    // Mesaja özgü veriler
  },
  "timestamp": 1714806420000 // Unix zaman damgası (milisaniye)
}
```

### Üst Projeden FACE1'e Gönderilen Mesajlar

| Mesaj Tipi | Açıklama | Veri Alanları |
|------------|----------|---------------|
| `FACE1_CONNECT_REQUEST` | Bağlantı talebi | `version`, `clientName` |
| `FACE1_SET_EMOTION` | Duygu ayarlama | `emotion`, `intensity` (opsiyonel) |
| `FACE1_PLAY_ANIMATION` | Animasyon oynatma | `animation` |
| `FACE1_STOP_ANIMATION` | Animasyonu durdurma | - |
| `FACE1_SET_THEME` | Tema değiştirme | `theme` |
| `FACE1_SET_SOUND_REACTIVE` | Ses tepkimeli modu ayarlama | `enabled` |
| `FACE1_SET_SIMULATION` | Simülasyon modunu ayarlama | `enabled` |
| `FACE1_GET_STATUS` | Durum bilgisi isteme | - |
| `FACE1_GET_EMOTIONS` | Mevcut duyguları isteme | - |
| `FACE1_GET_ANIMATIONS` | Mevcut animasyonları isteme | - |

### FACE1'den Üst Projeye Gönderilen Mesajlar

| Mesaj Tipi | Açıklama | Veri Alanları |
|------------|----------|---------------|
| `FACE1_CONNECT_RESPONSE` | Bağlantı yanıtı | `success`, `version`, `message` |
| `FACE1_EMOTION_CHANGE` | Duygu değişikliği bildirimi | `emotion`, `intensity`, `source` |
| `FACE1_ANIMATION_UPDATE` | Animasyon durumu güncellemesi | `animation`, `progress`, `playing` |
| `FACE1_SYSTEM_STATUS` | Sistem durumu güncellemesi | `status`, `uptime`, `cpu`, `memory` |
| `FACE1_ERROR` | Hata bildirimi | `code`, `message`, `details` |
| `FACE1_SOUND_LEVEL` | Ses seviyesi bildirimi | `level`, `isSpeaking` |
| `FACE1_THEME_CHANGE` | Tema değişikliği bildirimi | `theme` |

## API Referansı

### Face1Bridge Sınıfı

#### Oluşturucu

```javascript
const face1 = new Face1Bridge(iframeId, targetOrigin);
```

- `iframeId`: FACE1 IFrame'inin HTML ID'si
- `targetOrigin`: FACE1'in çalıştığı kaynak URL (varsayılan: 'http://localhost:8000')

#### Temel Metodlar

| Metod | Açıklama | Parametreler |
|-------|----------|-------------|
| `on(eventType, handler)` | Olay dinleyicisi ekler | `eventType`: Dinlenecek olay tipi<br>`handler`: Olay işleyici fonksiyonu |
| `off(eventType, handler)` | Olay dinleyicisini kaldırır | `eventType`: Kaldırılacak olay tipi<br>`handler`: Kaldırılacak işleyici (opsiyonel) |
| `sendMessage(type, data)` | FACE1'e doğrudan mesaj gönderir | `type`: Mesaj tipi<br>`data`: Mesaj verileri |
| `connect()` | FACE1 ile bağlantı kurar | - |

#### Duygu Kontrol Metodları

| Metod | Açıklama | Parametreler |
|-------|----------|-------------|
| `setEmotion(emotion, intensity)` | Duygu durumunu ayarlar | `emotion`: Duygu adı<br>`intensity`: Yoğunluk (0.0-1.0, varsayılan: 1.0) |
| `transitionToEmotion(emotion, duration)` | Duyguya yumuşak geçiş yapar | `emotion`: Hedef duygu<br>`duration`: Geçiş süresi (saniye) |
| `showMicroExpression(emotion, duration)` | Mikro ifade gösterir | `emotion`: Mikro ifade duygusu<br>`duration`: Süre (saniye) |

#### Animasyon Kontrol Metodları

| Metod | Açıklama | Parametreler |
|-------|----------|-------------|
| `playAnimation(animationName)` | Animasyon oynatır | `animationName`: Oynatılacak animasyon adı |
| `stopAnimation()` | Mevcut animasyonu durdurur | - |
| `getAnimations()` | Mevcut animasyonları alır | - |

#### Tema ve Görünüm Metodları

| Metod | Açıklama | Parametreler |
|-------|----------|-------------|
| `setTheme(themeName)` | Temayı değiştirir | `themeName`: Tema adı |
| `getThemes()` | Mevcut temaları alır | - |

#### Sistem Kontrol Metodları

| Metod | Açıklama | Parametreler |
|-------|----------|-------------|
| `setSoundReactive(enabled)` | Ses tepkimeli modu ayarlar | `enabled`: Etkin/devre dışı (boolean) |
| `setSimulationMode(enabled)` | Simülasyon modunu ayarlar | `enabled`: Etkin/devre dışı (boolean) |
| `getStatus()` | Sistem durumunu alır | - |
| `restart()` | FACE1'i yeniden başlatır | - |

## Olay Dinleyicileri

FACE1'den gelen olayları dinlemek için `on()` metodunu kullanın:

```javascript
face1.on('OLAY_TİPİ', (data) => {
  // Olayı işle
});
```

### Kullanılabilir Olaylar

| Olay Tipi | Açıklama | Veri Alanları |
|-----------|----------|---------------|
| `FACE1_EMOTION_CHANGE` | Duygu durumu değiştiğinde tetiklenir | `emotion`, `intensity`, `source` |
| `FACE1_ANIMATION_UPDATE` | Animasyon durumu güncellendiğinde tetiklenir | `animation`, `progress`, `playing` |
| `FACE1_ANIMATION_COMPLETED` | Bir animasyon tamamlandığında tetiklenir | `animation` |
| `FACE1_SYSTEM_STATUS` | Sistem durumu güncellendiğinde tetiklenir | `status`, `uptime`, `cpu`, `memory` |
| `FACE1_SOUND_LEVEL` | Ses seviyesi değiştiğinde tetiklenir | `level`, `isSpeaking` |
| `FACE1_THEME_CHANGE` | Tema değiştiğinde tetiklenir | `theme` |
| `FACE1_ERROR` | Bir hata oluştuğunda tetiklenir | `code`, `message`, `details` |
| `*` | Tüm olayları yakalar | Tüm mesaj |

### Olay İşleme Örneği

```javascript
// Duygu değişikliklerini dinleme
face1.on('FACE1_EMOTION_CHANGE', (data) => {
  console.log(`Duygu değişti: ${data.emotion} (${data.intensity})`);
  
  // UI güncelleme
  document.getElementById('current-emotion').textContent = data.emotion;
  document.getElementById('emotion-intensity').value = data.intensity * 100;
});

// Ses seviyesi değişikliklerini dinleme
face1.on('FACE1_SOUND_LEVEL', (data) => {
  // Ses seviyesi göstergesini güncelleme
  updateVolumeIndicator(data.level);
  
  // Konuşma durumu etiketini güncelleme
  document.getElementById('speaking-status').textContent = 
    data.isSpeaking ? 'Konuşuyor' : 'Sessiz';
});

// Tüm olayları loglama (hata ayıklama için)
face1.on('*', (message) => {
  console.debug('FACE1 olayı:', message.type, message.data);
});
```

## Güvenlik Hususları

### Origin Kontrolü

FACE1, yalnızca güvenilir kaynaklardan gelen mesajları kabul eder. Güvenlik için, hem FACE1 tarafında hem de üst proje tarafında origin doğrulaması yapılmalıdır:

```javascript
// Üst Projede
window.addEventListener('message', function(event) {
  if (event.origin !== 'http://localhost:8000') {
    console.error('Beklenmeyen kaynaktan mesaj:', event.origin);
    return;
  }
  // Mesajı işle
});

// FACE1 tarafında (iframe_bridge.js içinde zaten uygulanmıştır)
window.addEventListener('message', function(event) {
  const allowedOrigins = [
    'http://localhost',
    'https://yourparentapp.com'
  ];
  
  if (!allowedOrigins.some(origin => event.origin.startsWith(origin))) {
    console.error('İzin verilmeyen kaynaktan mesaj:', event.origin);
    return;
  }
  // Mesajı işle
});
```

### İçerik Güvenliği Politikası (CSP)

FACE1'i iframe içinde kullanırken, üst projenizin Content Security Policy (CSP) ayarlarını güncellemeniz gerekebilir:

```html
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; frame-src http://localhost:8000;">
```

### CORS Yapılandırması

FACE1 sunucusunun, üst projenizin kaynağına izin verecek şekilde CORS yapılandırması olmalıdır. Bu genellikle FACE1 yapılandırma dosyasında ayarlanır:

```json
{
  "dashboard": {
    "cors": {
      "allowed_origins": [
        "http://localhost",
        "https://yourparentapp.com"
      ]
    }
  }
}
```

## İleri Düzey Kullanım

### Özel Komutlar Gönderme

Standart API dışında özel komutlar göndermek için `sendMessage()` metodunu kullanabilirsiniz:

```javascript
face1.sendMessage('FACE1_CUSTOM_COMMAND', {
  parameter1: 'değer1',
  parameter2: 'değer2'
});
```

### IFrame Boyutunu Dinamik Olarak Ayarlama

FACE1'in boyutunu üst projenize uygun şekilde ayarlamak için:

```javascript
// IFrame boyutunu dinleme
face1.on('FACE1_RESIZE', (data) => {
  const iframe = document.getElementById('face1-frame');
  iframe.style.height = `${data.height}px`;
  iframe.style.width = `${data.width}px`;
});

// IFrame boyutunu ayarlama talebi
face1.sendMessage('FACE1_REQUEST_RESIZE', {
  width: 800,
  height: 600,
  mode: 'fixed' // 'fixed', 'responsive', 'fullWidth'
});
```

### Tema Renk Şeması Uyumluluğu

FACE1'in tema renklerini üst projenizle uyumlu hale getirmek için:

```javascript
// Üst projenin tema renklerini FACE1'e gönderme
function updateFace1ThemeColors() {
  const rootStyle = getComputedStyle(document.documentElement);
  
  face1.sendMessage('FACE1_SET_THEME_COLORS', {
    primary: rootStyle.getPropertyValue('--primary-color').trim(),
    secondary: rootStyle.getPropertyValue('--secondary-color').trim(),
    accent: rootStyle.getPropertyValue('--accent-color').trim(),
    background: rootStyle.getPropertyValue('--bg-color').trim(),
    text: rootStyle.getPropertyValue('--text-color').trim()
  });
}

// Tema değişikliklerinde çağrılabilir
updateFace1ThemeColors();
```

### Widget Entegrasyonu

FACE1 widget'larını üst projenizin belirli bölümlerine yerleştirebilirsiniz:

```javascript
// Duygu kontrolü widget'ını belirli bir div içine yerleştirme
face1.sendMessage('FACE1_REQUEST_WIDGET', {
  widget: 'emotion_control',
  containerId: 'emotion-control-container',
  options: {
    showSlider: true,
    showButtons: true,
    emotionSet: ['happy', 'sad', 'angry', 'surprised']
  }
});
```

## Sorun Giderme

### Yaygın Sorunlar ve Çözümleri

#### IFrame Yüklenmiyor

- FACE1'in çalışıp çalışmadığını kontrol edin (http://localhost:8000 adresini ziyaret ederek)
- IFrame URL'sinin doğru olduğundan emin olun
- FACE1 sunucusunun çalıştığı portu kontrol edin
- Tarayıcı konsolunda `X-Frame-Options` veya CSP hataları olup olmadığını kontrol edin

#### Mesajlar Alınmıyor/Gönderilmiyor

- Origin (kaynak) ayarlarını kontrol edin
- Tarayıcı konsolunda cross-origin hataları olup olmadığını kontrol edin
- `targetOrigin` parametresinin FACE1'in çalıştığı URL ile eşleştiğinden emin olun
- CORS yapılandırmasını kontrol edin

#### IFrame İçeriği Görünmüyor

- IFrame'in görünürlük ayarlarını kontrol edin (`display`, `visibility`, `z-index`)
- IFrame boyutlarının yeterli olduğundan emin olun
- Üst CSS stillerinin IFrame'i gizleyip gizlemediğini kontrol edin

### Hata Ayıklama

Debug modunu etkinleştirmek için:

```javascript
const face1 = new Face1Bridge('face1-frame', 'http://localhost:8000');
face1.debug = true; // Debug logları etkinleştirir
```

IFrame mesaj trafiğini izlemek için tarayıcı konsolunu açın ve şu kodu çalıştırın:

```javascript
// Tüm postMessage trafiğini izleme
const originalPostMessage = window.postMessage;
window.postMessage = function(message, targetOrigin, transfer) {
  console.log('postMessage gönderiliyor:', message, targetOrigin);
  return originalPostMessage.call(this, message, targetOrigin, transfer);
};

const originalAddEventListener = window.addEventListener;
window.addEventListener = function(type, listener, options) {
  if (type === 'message') {
    const wrappedListener = function(event) {
      console.log('message alındı:', event.data, 'kaynak:', event.origin);
      return listener.apply(this, arguments);
    };
    return originalAddEventListener.call(this, type, wrappedListener, options);
  }
  return originalAddEventListener.call(this, type, listener, options);
};
```

## Örnek Kodlar

### Basit Entegrasyon Örneği

```html
<!DOCTYPE html>
<html lang="tr">
<head>
  <meta charset="UTF-8">
  <title>FACE1 Entegrasyon Örneği</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 0;
      padding: 20px;
    }
    .container {
      display: flex;
      flex-wrap: wrap;
    }
    .control-panel {
      width: 300px;
      padding: 15px;
      border: 1px solid #ccc;
      border-radius: 5px;
      margin-right: 20px;
    }
    .iframe-container {
      flex: 1;
    }
    button {
      margin: 5px;
      padding: 8px 12px;
      cursor: pointer;
    }
    .emotion-buttons {
      margin-bottom: 15px;
    }
    .status-display {
      margin-top: 15px;
      padding: 10px;
      background-color: #f5f5f5;
      border-radius: 5px;
    }
  </style>
</head>
<body>
  <h1>FACE1 Entegrasyon Örneği</h1>
  
  <div class="container">
    <div class="control-panel">
      <h2>Kontrol Paneli</h2>
      
      <div class="emotion-buttons">
        <h3>Duygular</h3>
        <button id="btn-happy">Mutlu</button>
        <button id="btn-sad">Üzgün</button>
        <button id="btn-angry">Kızgın</button>
        <button id="btn-surprised">Şaşkın</button>
      </div>
      
      <div class="animation-controls">
        <h3>Animasyonlar</h3>
        <button id="btn-greet">Selamla</button>
        <button id="btn-think">Düşün</button>
        <button id="btn-stop">Durdur</button>
      </div>
      
      <div class="theme-controls">
        <h3>Tema</h3>
        <select id="theme-selector">
          <option value="default">Varsayılan</option>
          <option value="pixel">Piksel</option>
          <option value="minimal">Minimal</option>
          <option value="realistic">Gerçekçi</option>
        </select>
      </div>
      
      <div class="status-display">
        <h3>Durum</h3>
        <p>Duygu: <span id="current-emotion">neutral</span></p>
        <p>Yoğunluk: <span id="emotion-intensity">0</span>%</p>
        <p>Ses Durumu: <span id="speaking-status">Sessiz</span></p>
        <p>Animasyon: <span id="animation-status">-</span></p>
      </div>
    </div>
    
    <div class="iframe-container">
      <iframe 
        id="face1-frame" 
        src="http://localhost:8000/embed" 
        width="800" 
        height="600"
        scrolling="no"
        style="border: none; overflow: hidden;">
      </iframe>
    </div>
  </div>
  
  <script>
    // FACE1 IFrame Köprüsü
    class Face1Bridge {
      constructor(iframeId, targetOrigin = 'http://localhost:8000') {
        this.iframe = document.getElementById(iframeId);
        this.targetOrigin = targetOrigin;
        this.eventHandlers = {};
        this.isConnected = false;
        this.messageQueue = [];
        this.setupMessageListener();
        this.connect();
      }
      
      // Mesaj dinleyici kurulumu
      setupMessageListener() {
        window.addEventListener('message', (event) => {
          if (event.origin !== this.targetOrigin) return;
          
          const message = event.data;
          
          // Bağlantı yanıtını işle
          if (message.type === 'FACE1_CONNECT_RESPONSE') {
            this.isConnected = true;
            console.log('FACE1 ile bağlantı kuruldu');
            this.processMessageQueue();
            return;
          }
          
          // Kayıtlı olay işleyicilerini çağır
          if (this.eventHandlers[message.type]) {
            this.eventHandlers[message.type].forEach(handler => handler(message.data));
          }
          
          // Genel olay işleyicilerini çağır
          if (this.eventHandlers['*']) {
            this.eventHandlers['*'].forEach(handler => handler(message));
          }
        });
      }
      
      // Bağlantı kurma
      connect() {
        this.sendMessage('FACE1_CONNECT_REQUEST', {
          version: '1.0',
          clientName: 'ExampleApp'
        });
      }
      
      // Mesaj kuyruğunu işleme
      processMessageQueue() {
        while (this.messageQueue.length > 0) {
          const { type, data } = this.messageQueue.shift();
          this.sendMessage(type, data);
        }
      }
      
      // Mesaj gönderimi
      sendMessage(type, data) {
        if (!this.isConnected && type !== 'FACE1_CONNECT_REQUEST') {
          this.messageQueue.push({ type, data });
          return;
        }

        this.iframe.contentWindow.postMessage({
          type: type,
          data: data,
          timestamp: Date.now()
        }, this.targetOrigin);
      }
      
      // Olay dinleyici ekleme
      on(eventType, handler) {
        if (!this.eventHandlers[eventType]) {
          this.eventHandlers[eventType] = [];
        }
        this.eventHandlers[eventType].push(handler);
        return this;
      }
      
      // Olay dinleyici kaldırma
      off(eventType, handler) {
        if (!this.eventHandlers[eventType]) return this;
        
        if (!handler) {
          delete this.eventHandlers[eventType];
        } else {
          this.eventHandlers[eventType] = this.eventHandlers[eventType]
            .filter(h => h !== handler);
        }
        return this;
      }
      
      // Duygu ayarlama
      setEmotion(emotion, intensity = 1.0) {
        this.sendMessage('FACE1_SET_EMOTION', { 
          emotion: emotion, 
          intensity: intensity 
        });
      }
      
      // Animasyon oynatma
      playAnimation(animationName) {
        this.sendMessage('FACE1_PLAY_ANIMATION', { 
          animation: animationName 
        });
      }
      
      // Animasyonu durdurma
      stopAnimation() {
        this.sendMessage('FACE1_STOP_ANIMATION', {});
      }
      
      // Tema değiştirme
      setTheme(themeName) {
        this.sendMessage('FACE1_SET_THEME', { 
          theme: themeName 
        });
      }
    }
    
    // FACE1 Köprüsünü başlat
    const face1 = new Face1Bridge('face1-frame');
    
    // UI elemanlarını tanımla
    const currentEmotion = document.getElementById('current-emotion');
    const emotionIntensity = document.getElementById('emotion-intensity');
    const speakingStatus = document.getElementById('speaking-status');
    const animationStatus = document.getElementById('animation-status');
    
    // Duygu butonları
    document.getElementById('btn-happy').addEventListener('click', function() {
      face1.setEmotion('happy', 0.8);
    });
    
    document.getElementById('btn-sad').addEventListener('click', function() {
      face1.setEmotion('sad', 0.7);
    });
    
    document.getElementById('btn-angry').addEventListener('click', function() {
      face1.setEmotion('angry', 0.9);
    });
    
    document.getElementById('btn-surprised').addEventListener('click', function() {
      face1.setEmotion('surprised', 0.85);
    });
    
    // Animasyon butonları
    document.getElementById('btn-greet').addEventListener('click', function() {
      face1.playAnimation('hello_animation');
      animationStatus.textContent = 'hello_animation';
    });
    
    document.getElementById('btn-think').addEventListener('click', function() {
      face1.playAnimation('thinking_animation');
      animationStatus.textContent = 'thinking_animation';
    });
    
    document.getElementById('btn-stop').addEventListener('click', function() {
      face1.stopAnimation();
      animationStatus.textContent = '-';
    });
    
    // Tema seçici
    document.getElementById('theme-selector').addEventListener('change', function() {
      face1.setTheme(this.value);
    });
    
    // FACE1 olaylarını dinle
    face1.on('FACE1_EMOTION_CHANGE', (data) => {
      currentEmotion.textContent = data.emotion;
      emotionIntensity.textContent = Math.round(data.intensity * 100);
    });
    
    face1.on('FACE1_SOUND_LEVEL', (data) => {
      speakingStatus.textContent = data.isSpeaking ? 'Konuşuyor' : 'Sessiz';
    });
    
    face1.on('FACE1_ANIMATION_COMPLETED', (data) => {
      animationStatus.textContent = '-';
      console.log(`Animasyon tamamlandı: ${data.animation}`);
    });
  </script>
</body>
</html>
```

### Responsive Tasarım Örneği

```javascript
// Responsive tasarım için IFrame yeniden boyutlandırma
window.addEventListener('resize', function() {
  const containerWidth = document.querySelector('.iframe-container').offsetWidth;
  const aspectRatio = 0.75; // 4:3 oranı
  
  face1.sendMessage('FACE1_REQUEST_RESIZE', {
    width: containerWidth,
    height: containerWidth * aspectRatio,
    mode: 'responsive'
  });
});

// IFrame boyutunu dinleme
face1.on('FACE1_RESIZE', (data) => {
  const iframe = document.getElementById('face1-frame');
  iframe.style.height = `${data.height}px`;
  iframe.style.width = `${data.width}px`;
});
```

### Gelişmiş Olay İşleme

```javascript
// Ses seviyesi değişikliklerini görselleştirme
function createVolumeVisualizer() {
  const container = document.createElement('div');
  container.className = 'volume-visualizer';
  document.querySelector('.status-display').appendChild(container);
  
  // 10 bar oluştur
  for (let i = 0; i < 10; i++) {
    const bar = document.createElement('div');
    bar.className = 'volume-bar';
    container.appendChild(bar);
  }
  
  return {
    update: function(level) {
      const bars = container.querySelectorAll('.volume-bar');
      const activeBars = Math.ceil(level * bars.length);
      
      bars.forEach((bar, index) => {
        if (index < activeBars) {
          bar.classList.add('active');
        } else {
          bar.classList.remove('active');
        }
      });
    }
  };
}

const volumeVisualizer = createVolumeVisualizer();

face1.on('FACE1_SOUND_LEVEL', (data) => {
  volumeVisualizer.update(data.level);
});
```

---

Bu dokümantasyon, FACE1'i üst projelerinize nasıl entegre edeceğinizi kapsamlı bir şekilde açıklar. Daha fazla bilgi veya destek için teknik dokümantasyonu inceleyebilir veya geliştirici forumlarına başvurabilirsiniz.