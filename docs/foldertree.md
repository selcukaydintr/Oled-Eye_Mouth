Haklısınız, dosyaları tekrar tekrar oluşturmak yerine, var olan dosyaları kullanmam veya sadece değişiklik yapmam gerekiyordu. Özür dilerim bu karışıklık için.

Dosyaları tekrar oluşturmak yerine, önce varlıklarını kontrol etmeliydim ve eğer varsa içeriklerini güncellemem gerekiyordu.

Bundan sonra şu adımları izleyeceğim:

1. Önce bir dosyanın var olup olmadığını kontrol edeceğim
2. Dosya varsa, güncellemem gereken kısmı güncelleyeceğim
3. Dosya yoksa yeni bir dosya oluşturacağım

Bu yaklaşımla gereksiz tekrarları önleyeceğim. Teşekkür ederim uyarınız için.

# FACE1 Projesi Dosya Yapısı

/face1/
│── docs/
│   ├── changes.md               # Değişiklik kaydı
│   ├── talimatlar.md            # Proje talimatları
│   ├── plugin_roadmap.md        # Plugin geliştirme yol haritası
│   ├── roadmap.md               # Genel proje yol haritası
│   ├── foldertree.md            # Bu dosya (proje dizin yapısı)
│   ├── fonsiyon_listesi.md      # Fonksiyonların listesi ve açıklamaları
│   ├── notlar.md                # Geliştirme notları ve ipuçları
│   ├── devam.md                 # Projeye devam hatırlatıcısı
│   ├── dosya_bolme_talimati.md  # Dosya bölme talimatları
│   ├── animation_system.md      # Animasyon sistemi dokümantasyonu
│   ├── sound_processor.md       # Ses işleme modülü dokümantasyonu
│   ├── state_reflector_guide.md # Durum Yansıtma Protokolü kılavuzu
│   ├── iframe_bridge_integration.md # IFrame Köprüsü entegrasyon kılavuzu
│   ├── widget_system.md         # Widget sistemi kullanım kılavuzu
│   └── sorgu_hatası.md          # Sorgu hatası kayıtları
│
│── src/
│   ├── face_plugin.py           # Ana kontrol sınıfı
│   ├── modules/
│   │   ├── face1_plugin.py           # Yüz eklentisi yaşam döngüsü kontrolü
│   │   ├── face_plugin_config.py     # Plugin yapılandırma yönetimi
│   │   ├── face_plugin_metrics.py    # Plugin performans metrikleri
│   │   ├── face_plugin_environment.py # Plugin çevresel faktör yönetimi
│   │   ├── face_plugin_lifecycle.py  # Plugin yaşam döngüsü yöneticisi
│   │   │
│   │   ├── sound_processor.py        # Ses işleme ve reaktif ifade modülü
│   │   ├── state_reflector.py        # Durum yansıtma protokolü
│   │   ├── iframe_bridge.py          # IFrame iletişim köprüsü
│   │   ├── api_bridge.py             # API köprüsü ve yönlendirici
│   │   │
│   │   ├── performance_optimizer.py  # Performans optimizasyon modülü
│   │
│   │   ├── oled_controller.py           # OLED ekran kontrolcüsü (ana sınıf)
│   │   ├── oled_controller_base.py      # OLED temel sınıfı
│   │   ├── oled_controller_display.py   # OLED gösterge sınıfı
│   │   ├── oled_controller_animations.py # OLED animasyon sınıfı
│   │
│   │   ├── emotion_engine.py            # Duygu işleme motoru (ana sınıf)
│   │   ├── emotion_engine_base.py       # Duygu motoru temel sınıfı
│   │   ├── emotion_engine_expressions.py # Duygu ifadeleri modülü
│   │   ├── emotion_engine_memory.py     # Duygu hafızası modülü
│   │   ├── emotion_engine_transitions.py # Duygu geçişleri modülü
│   │   ├── emotion_states.py            # Duygu durumları tanımlamaları
│   │
│   │   ├── led_controller.py            # WS2812 LED kontrolcüsü (ana sınıf)
│   │   ├── led_controller_base.py       # LED kontrolcü temel sınıfı
│   │   ├── led_controller_animations.py # LED animasyonları modülü
│   │   ├── led_controller_colors.py     # LED renk işlemleri modülü
│   │   ├── led_controller_patterns.py   # LED desen yönetimi modülü
│   │
│   │   ├── theme_manager.py             # Ana tema yöneticisi
│   │   ├── theme/                       # Tema alt modülleri
│   │   │   ├── theme_manager_assets.py  # Tema varlıkları yöneticisi
│   │   │   ├── theme_manager_cache.py   # Tema önbellek yöneticisi
│   │   │   ├── theme_manager_operations.py # Tema işlemleri yöneticisi
│   │   │   └── theme_manager_templates.py # Tema şablonları yöneticisi
│   │
│   │   ├── io_manager.py                # Giriş/çıkış yöneticisi
│   │
│   │   ├── dashboard_server.py          # Web paneli sunucusu (ana sınıf)
│   │   ├── dashboard_routes.py          # Dashboard API yönlendirmeleri
│   │   ├── dashboard_websocket.py       # Dashboard WebSocket işleyicisi
│   │   ├── dashboard_templates.py       # Dashboard şablon yöneticisi
│   │   ├── dashboard_stats.py           # Dashboard istatistik toplayıcısı
│   │   │
│   │   ├── dashboard_widgets/           # Widget sistemi
│   │   │   ├── __init__.py              # Widget paketi tanımı
│   │   │   ├── widget_base.py           # Temel widget sınıfı
│   │   │   ├── expression_control.py    # İfade kontrol widget'ı
│   │   │   ├── state_history.py         # Durum takip widget'ı
│   │   │   └── emotion_transitions.py   # Duygu geçişleri widget'ı
│   │
│   │   ├── animation_engine.py          # Animasyon motoru
│   │
│   │   ├── face/                        # Yüz kontrol modülleri
│   │   │   └── __init__.py              # Paket tanımlama dosyası
│   │
│   │   ├── sensor_manager.py            # [GELECEK] Sensör entegrasyonu yöneticisi
│   │
│   └── plugins/                 # Eklenti sistemi
│       ├── __init__.py          # Eklenti paketi tanımı
│       ├── plugin_isolation.py  # Eklenti izolasyonu
│       ├── config_standardizer.py # Yapılandırma standardizasyonu
│       └── default_plugins/     # [GELECEK] Varsayılan eklentiler
│
│── include/
│   ├── hardware_defines.py      # Donanım sabitleri
│   └── constants.py             # [GELECEK] Genel program sabitleri
│
│── config/
│   ├── config.json              # Ana yapılandırma dosyası
│   ├── default_config.json      # Varsayılan yapılandırma
│   ├── hardware_profiles/       # Donanıma özgü ayarlar
│   │   ├── rpi5.json            # Raspberry Pi 5 için ayarlar
│   │   ├── rpi4.json            # Raspberry Pi 4 için ayarlar
│   │   └── custom_hw.json       # [GELECEK] Özel donanım profili
│   ├── user_config.json         # Kullanıcı özelleştirmeleri
│   ├── backups/                 # Yapılandırma yedekleri
│   └── plugin_config/           # [GELECEK] Eklenti yapılandırmaları
│
│── logs/
│   ├── face_plugin.log          # Sistem kayıtları
│   ├── errors.log               # Hata kayıtları
│   └── performance.log          # Performans ölçümleri
│
│── simulation/                  # Simülasyon çıktı klasörü
│   ├── display_left_eye_*.png   # Sol göz simülasyon görüntüleri
│   ├── display_right_eye_*.png  # Sağ göz simülasyon görüntüleri 
│   ├── display_mouth_*.png      # Ağız simülasyon görüntüleri
│   ├── leds_*.png               # LED simülasyon görüntüleri
│   └── replay/                  # [GELECEK] Simülasyon tekrar oynatma kayıtları
│
│── themes/
│   ├── default/                 # Varsayılan tema
│   │   ├── eyes/                # Göz ifadeleri
│   │   ├── mouth/               # Ağız ifadeleri
│   │   └── theme.json           # Tema tanımlamaları
│   ├── pixel/                   # Pixel stili tema
│   │   ├── eyes/                # Pixel stil göz ifadeleri
│   │   ├── mouth/               # Pixel stil ağız ifadeleri
│   │   └── theme.json           # Pixel tema tanımlamaları
│   ├── minimal/                 # Minimal tema
│   │   ├── eyes/                # Minimal göz ifadeleri
│   │   ├── mouth/               # Minimal ağız ifadeleri
│   │   └── theme.json           # Minimal tema tanımlamaları
│   ├── realistic/               # Gerçekçi tema
│   │   ├── eyes/                # Gerçekçi göz ifadeleri
│   │   ├── mouth/               # Gerçekçi ağız ifadeleri
│   │   └── theme.json           # Gerçekçi tema tanımlamaları
│   ├── fonts/                   # Tema fontları
│   └── custom_themes/           # [GELECEK] Kullanıcı temaları
│
│── animation/
│   ├── standard/                # Standart animasyonlar
│   │   ├── startup_animation.json      # Başlangıç animasyonu
│   │   ├── emotion_transition.json     # Duygu geçişi animasyonu
│   │   ├── speaking.json               # Konuşma animasyonu
│   │   ├── happy_dance.json            # Mutlu duygu animasyonu
│   │   └── surprise_reaction.json      # Şaşkınlık tepkisi animasyonu
│   ├── custom/                  # Özel animasyonlar
│   └── templates/               # [GELECEK] Animasyon şablonları
│
│── web/
│   ├── static/                  # Statik web dosyaları
│   │   ├── css/                 # CSS stil dosyaları
│   │   │   ├── main.css         # Ana stil dosyası
│   │   │   ├── dashboard.css    # Dashboard stilleri
│   │   │   ├── widgets/         # Widget stil dosyaları
│   │   │   │   ├── widget_base.css            # Temel widget stilleri
│   │   │   │   ├── expression_control.css     # İfade kontrolü widget stilleri
│   │   │   │   ├── state_history.css          # Durum widget stilleri 
│   │   │   │   └── emotion_transitions.css    # Duygu geçişi widget stilleri
│   │   │   └── iframe.css       # IFrame entegrasyon stilleri
│   │   ├── js/                  # JavaScript dosyaları
│   │   │   ├── main.js          # Ana JavaScript dosyası
│   │   │   ├── websocket.js     # WebSocket bağlantı yöneticisi
│   │   │   ├── state_sync.js    # Durum senkronizasyonu
│   │   │   ├── iframe_bridge.js # IFrame köprüsü
│   │   │   ├── widgets/         # Widget JavaScript dosyaları
│   │   │   │   ├── widget_loader.js           # Widget yükleme sistemi
│   │   │   │   ├── expression_control.js      # İfade kontrolü widget kodu
│   │   │   │   ├── state_history.js           # Durum widget kodu
│   │   │   │   └── emotion_transitions.js     # Duygu geçişi widget kodu
│   │   │   └── parent_api.js    # Üst proje API entegrasyonu
│   │   ├── images/              # Web arayüzü için görseller
│   │   └── fonts/               # Web fontları
│   ├── templates/               # Web şablonları
│   │   ├── index.html           # Ana sayfa şablonu
│   │   ├── dashboard.html       # Kontrol paneli şablonu
│   │   ├── theme_editor.html    # Tema düzenleme şablonu
│   │   ├── animation_editor.html # Animasyon düzenleme şablonu
│   │   ├── configuration_editor.html # Yapılandırma düzenleme şablonu
│   │   ├── lifecycle_dashboard.html # Plugin yaşam döngüsü paneli
│   │   ├── iframe_integration.html # IFrame entegrasyon örneği
│   │   ├── parent_integration_example.html # Üst proje entegrasyon örneği
│   │   ├── error.html           # Hata sayfası şablonu
│   │   ├── widgets/             # Widget şablonları
│   │   │   ├── widget_base.html               # Temel widget şablonu
│   │   │   ├── expression_control_widget.html # İfade kontrolü widget şablonu
│   │   │   ├── state_history_widget.html      # Durum widget şablonu
│   │   │   └── emotion_transitions_widget.html # Duygu geçişi widget şablonu
│   │   └── components/          # Yeniden kullanılabilir bileşenler
│   ├── api/                     # RESTful API
│   │   ├── routes.py            # API yönlendirmeleri
│   │   └── controllers.py       # API denetleyicileri
│   └── websocket/               # WebSocket desteği
│       ├── handlers.py          # WebSocket işleyicileri
│       └── state_broadcaster.py # Durum yayın sistemi
│
│── utils/
│   ├── diagnostics.py           # Sistem tanılama araçları
│   ├── calibration.py           # Kalibrasyon araçları
│   ├── simulator.py             # Çevrimdışı simülasyon aracı
│   ├── integration_tester.py    # Entegrasyon test aracı
│   ├── backup.py                # Yedekleme aracı
│   ├── converter.py             # Format dönüştürücü
│   └── debug_tools/             # Hata ayıklama araçları
│       ├── profiler.py          # Performans ölçümü
│       └── logger.py            # Gelişmiş günlükleme
│
│── tests/                       # [GELECEK] Test dizini
│   ├── unit/                    # [GELECEK] Birim testleri
│   ├── integration/             # [GELECEK] Entegrasyon testleri
│   └── fixtures/                # [GELECEK] Test sabitleri
│
│── scripts/                     # [GELECEK] Yardımcı scriptler
│   ├── install.sh               # [GELECEK] Kurulum scripti
│   ├── update.sh                # [GELECEK] Güncelleme scripti
│   └── maintenance.sh           # [GELECEK] Bakım scripti
│
│── README.md                    # Proje tanıtımı ve kullanım kılavuzu
│── oled_talimatlar.md           # OLED ekran talimatları
│── create_venv.py               # Sanal ortam oluşturma scripti
│── run_face.sh                  # Çalıştırma scripti
│── dashboard.sh                 # Web paneli başlatma scripti
│── test_drivers.py              # Test sürücüleri
│── function_list.md             # Fonksiyon listesi
│── function_scanner.py          # Fonksiyon tarama aracı
│── setup.py                     # [GELECEK] Kurulum konfigürasyonu
└── requirements.txt             # Bağımlılıklar listesi

# Not: [GELECEK] etiketi, henüz eklenmemiş ancak planlanan dosya ve dizinleri belirtir.
# Son güncelleme: 05.05.2025
