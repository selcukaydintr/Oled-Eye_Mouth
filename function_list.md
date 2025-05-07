# FACE1 Projesi Fonksiyon Listesi

Bu liste, FACE1 projesi içindeki tüm fonksiyon ve sınıfları içerir.

Oluşturulma Tarihi: 2025-05-05 01:17:36

| Fonksiyon | Bulunduğu Dosya | Versiyon | Değiştirme Tarihi | İşlevi ve Amacı |
|-----------|----------------|----------|-------------------|----------------|
| `check_python_version` | create_venv.py | Belirtilmemiş | 2025-04-28 | Python sürümünü kontrol eder |
| `check_rpi_specific_packages` | create_venv.py | Belirtilmemiş | 2025-04-28 | Raspberry Pi'ye özgü paketlerin kullanılabilirliğini kontrol eder |
| `create_virtual_environment` | create_venv.py | Belirtilmemiş | 2025-04-28 | Python sanal ortamını oluşturur |
| `install_requirements` | create_venv.py | Belirtilmemiş | 2025-04-28 | Gerekli paketleri sanal ortama yükler |
| `main` | create_venv.py | Belirtilmemiş | 2025-04-28 | Ana fonksiyon |
| `extract_purpose_from_docstring` | function_scanner.py | Belirtilmemiş | 2025-05-02 | Docstring içinden fonksiyonun amacını çıkarır. |
| `extract_version_from_docstring` | function_scanner.py | Belirtilmemiş | 2025-05-02 | Docstring içinden versiyon bilgisini çıkarır. |
| `generate_markdown` | function_scanner.py | Belirtilmemiş | 2025-05-02 | Fonksiyon listesinden markdown çıktısı oluşturur |
| `get_git_last_modified_date` | function_scanner.py | Belirtilmemiş | 2025-05-02 | Git log kullanarak bir dosyanın son değiştirilme tarihini alır. |
| `main` | function_scanner.py | Belirtilmemiş | 2025-05-02 | Ana fonksiyon. |
| `parse_python_file` | function_scanner.py | Belirtilmemiş | 2025-05-02 | Python dosyasını ayrıştırarak fonksiyonları ve sınıfları çıkarır. |
| `scan_directory` | function_scanner.py | Belirtilmemiş | 2025-05-02 | Belirtilen dizini ve alt dizinlerini tarayarak Python dosyalarını bulur. |
| `🔶 SMBus` | include/hardware_defines.py | Belirtilmemiş | 2025-04-28 | SMBus modülü import edilemediğinde tip kontrolü için yer tutucu sınıf |
| `cleanup` | include/hardware_defines.py | Belirtilmemiş | 2025-04-28 | Donanım kaynaklarını serbest bırakır |
| `detect_platform` | include/hardware_defines.py | Belirtilmemiş | 2025-04-28 | Çalışılan platformu tespit eder |
| `get_cpu_temperature` | include/hardware_defines.py | Belirtilmemiş | 2025-04-28 | CPU sıcaklığını okur (sadece Raspberry Pi için çalışır) |
| `get_platform_i2c` | include/hardware_defines.py | Belirtilmemiş | 2025-04-28 | Platform için uygun I2C nesnesini döndürür |
| `get_platform_info` | include/hardware_defines.py | Belirtilmemiş | 2025-04-28 | Platform hakkında detaylı bilgi sağlar |
| `get_raspberry_pi_model` | include/hardware_defines.py | Belirtilmemiş | 2025-04-28 | Raspberry Pi modelini tespit eder |
| `init_gpio` | include/hardware_defines.py | Belirtilmemiş | 2025-04-28 | GPIO pinlerini başlatır |
| `init_i2c` | include/hardware_defines.py | Belirtilmemiş | 2025-04-28 | I2C veri yolunu başlatır |
| `init_i2c_multiplexer` | include/hardware_defines.py | Belirtilmemiş | 2025-04-28 | TCA9548A I2C çoğaltıcısını başlatır |
| `scan_i2c_devices` | include/hardware_defines.py | Belirtilmemiş | 2025-04-28 | I2C veri yolundaki cihazları tarar |
| `🔶 AnimationEngine` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon sekanslarını yöneten ve oynatmaya yarayan motor sınıfı |
| `↪ AnimationEngine.__init__` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon motorunu başlatır |
| `↪ AnimationEngine._action_eyes_blink` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Göz kırpma |
| `↪ AnimationEngine._action_eyes_clear` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Gözleri temizler |
| `↪ AnimationEngine._action_eyes_growing_circle` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Büyüyen çember |
| `↪ AnimationEngine._action_eyes_look_around` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Etrafı izleme |
| `↪ AnimationEngine._action_leds_off` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | LED'leri kapatır |
| `↪ AnimationEngine._action_leds_pulse` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | LED'leri yanıp söndürür |
| `↪ AnimationEngine._action_leds_rainbow` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | LED'lerde gökkuşağı efekti |
| `↪ AnimationEngine._action_mouth_clear` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Ağzı temizler |
| `↪ AnimationEngine._action_mouth_smile` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Gülümseme |
| `↪ AnimationEngine._action_mouth_speak` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Konuşma animasyonu |
| `↪ AnimationEngine._action_set_emotion` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Duygu durumunu ayarlar |
| `↪ AnimationEngine._ease_transition` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Geçiş ilerlemesini yumuşatmak için easing fonksiyonu uygular |
| `↪ AnimationEngine._execute_step` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon adımını yürütür |
| `↪ AnimationEngine._load_animations_from_dir` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Belirtilen dizindeki tüm JSON animasyonlarını yükler |
| `↪ AnimationEngine._play_transition_animation` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Geçiş animasyonunu oynatır |
| `↪ AnimationEngine._run_animation` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon sekansını çalıştırır |
| `↪ AnimationEngine._run_transition_animation` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Geçiş animasyonunu çalıştırır ve tamamlandığında temizlik yapar |
| `↪ AnimationEngine._transition_led_effect` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Geçiş anında LED efekti uygular |
| `↪ AnimationEngine._trigger_animation_event` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon olayını tetikler ve callback'leri çağırır |
| `↪ AnimationEngine._update_emotion_blend` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | İki duygu durumu arasında karışım uygula |
| `↪ AnimationEngine._validate_animation` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon verilerini doğrular |
| `↪ AnimationEngine.delete_animation` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyonu siler |
| `↪ AnimationEngine.get_animation_details` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon detaylarını döndürür (tam içerik) |
| `↪ AnimationEngine.get_animation_info` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon meta bilgilerini döndürür |
| `↪ AnimationEngine.get_animation_names` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Mevcut animasyon adlarını döndürür |
| `↪ AnimationEngine.get_animation_status` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Mevcut animasyon durumunu döndürür |
| `↪ AnimationEngine.load_animations` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Tüm animasyon dosyalarını yükler |
| `↪ AnimationEngine.play_animation` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Belirtilen animasyonu oynatır |
| `↪ AnimationEngine.save_animation` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyonu dosyaya kaydeder |
| `↪ AnimationEngine.set_emotion` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Duygu durumunu ayarlar |
| `↪ AnimationEngine.set_theme` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Temayı değiştirir |
| `↪ AnimationEngine.show_micro_expression` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Mikro ifade gösterir |
| `↪ AnimationEngine.show_startup_animation` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Başlangıç animasyonunu oynatır |
| `↪ AnimationEngine.start` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon motorunu başlatır |
| `↪ AnimationEngine.stop` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon motorunu durdurur |
| `↪ AnimationEngine.stop_current_animation` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Çalışan animasyonu durdurur |
| `↪ AnimationEngine.transition_emotion` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | İki duygu arasında geçiş için animasyon yapar |
| `__init__` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon motorunu başlatır |
| `_action_eyes_blink` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Göz kırpma |
| `_action_eyes_clear` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Gözleri temizler |
| `_action_eyes_growing_circle` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Büyüyen çember |
| `_action_eyes_look_around` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Etrafı izleme |
| `_action_leds_off` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | LED'leri kapatır |
| `_action_leds_pulse` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | LED'leri yanıp söndürür |
| `_action_leds_rainbow` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | LED'lerde gökkuşağı efekti |
| `_action_mouth_clear` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Ağzı temizler |
| `_action_mouth_smile` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Gülümseme |
| `_action_mouth_speak` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Konuşma animasyonu |
| `_action_set_emotion` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Duygu durumunu ayarlar |
| `_ease_transition` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Geçiş ilerlemesini yumuşatmak için easing fonksiyonu uygular |
| `_execute_step` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon adımını yürütür |
| `_load_animations_from_dir` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Belirtilen dizindeki tüm JSON animasyonlarını yükler |
| `_play_transition_animation` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Geçiş animasyonunu oynatır |
| `_run_animation` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon sekansını çalıştırır |
| `_run_transition_animation` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Geçiş animasyonunu çalıştırır ve tamamlandığında temizlik yapar |
| `_transition_led_effect` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Geçiş anında LED efekti uygular |
| `_trigger_animation_event` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon olayını tetikler ve callback'leri çağırır |
| `_update_emotion_blend` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | İki duygu durumu arasında karışım uygula |
| `_validate_animation` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon verilerini doğrular |
| `delete_animation` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyonu siler |
| `get_action_func` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `get_animation_details` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon detaylarını döndürür (tam içerik) |
| `get_animation_info` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon meta bilgilerini döndürür |
| `get_animation_names` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Mevcut animasyon adlarını döndürür |
| `get_animation_status` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Mevcut animasyon durumunu döndürür |
| `load_animations` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Tüm animasyon dosyalarını yükler |
| `play_animation` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Belirtilen animasyonu oynatır |
| `save_animation` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyonu dosyaya kaydeder |
| `set_emotion` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Duygu durumunu ayarlar |
| `set_theme` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Temayı değiştirir |
| `show_micro_expression` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Mikro ifade gösterir |
| `show_startup_animation` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Başlangıç animasyonunu oynatır |
| `start` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon motorunu başlatır |
| `stop` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Animasyon motorunu durdurur |
| `stop_current_animation` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | Çalışan animasyonu durdurur |
| `transition_emotion` | src/modules/animation_engine.py | Belirtilmemiş | 2025-05-04 | İki duygu arasında geçiş için animasyon yapar |
| `🔶 RoutesManager` | src/modules/dashboard_routes.py | Belirtilmemiş | 2025-05-05 | Dashboard rotalarını yöneten sınıf |
| `↪ RoutesManager.__init__` | src/modules/dashboard_routes.py | Belirtilmemiş | 2025-05-05 | Routes Manager'ı başlatır |
| `↪ RoutesManager._deep_merge_dict` | src/modules/dashboard_routes.py | Belirtilmemiş | 2025-05-05 | İki sözlüğü derin birleştirir, iç içe yapıları korur |
| `↪ RoutesManager._register_widget_endpoints` | src/modules/dashboard_routes.py | Belirtilmemiş | 2025-05-05 | Widget endpoint'lerini kaydeder |
| `↪ RoutesManager.register_routes` | src/modules/dashboard_routes.py | Belirtilmemiş | 2025-05-05 | API rotalarını kaydeder |
| `↪ RoutesManager.set_config` | src/modules/dashboard_routes.py | Belirtilmemiş | 2025-05-05 | Yapılandırma ayarlarını ayarlar |
| `↪ RoutesManager.set_face_plugin` | src/modules/dashboard_routes.py | Belirtilmemiş | 2025-05-05 | Face Plugin referansını ayarlar |
| `__init__` | src/modules/dashboard_routes.py | Belirtilmemiş | 2025-05-05 | Routes Manager'ı başlatır |
| `_deep_merge_dict` | src/modules/dashboard_routes.py | Belirtilmemiş | 2025-05-05 | İki sözlüğü derin birleştirir, iç içe yapıları korur |
| `_register_widget_endpoints` | src/modules/dashboard_routes.py | Belirtilmemiş | 2025-05-05 | Widget endpoint'lerini kaydeder |
| `register_routes` | src/modules/dashboard_routes.py | Belirtilmemiş | 2025-05-05 | API rotalarını kaydeder |
| `set_config` | src/modules/dashboard_routes.py | Belirtilmemiş | 2025-05-05 | Yapılandırma ayarlarını ayarlar |
| `set_face_plugin` | src/modules/dashboard_routes.py | Belirtilmemiş | 2025-05-05 | Face Plugin referansını ayarlar |
| `🔶 DashboardServer` | src/modules/dashboard_server.py | Belirtilmemiş | 2025-05-05 | Dashboard sunucu sınıfı |
| `↪ DashboardServer.__init__` | src/modules/dashboard_server.py | Belirtilmemiş | 2025-05-05 | Dashboard sunucusunu başlatır |
| `↪ DashboardServer._run_server` | src/modules/dashboard_server.py | Belirtilmemiş | 2025-05-05 | FastAPI sunucusunu başlatır |
| `↪ DashboardServer._system_stats_loop` | src/modules/dashboard_server.py | Belirtilmemiş | 2025-05-05 | Sistem istatistiklerini düzenli aralıklarla toplar ve istemcilere gönderir |
| `↪ DashboardServer.create_app` | src/modules/dashboard_server.py | Belirtilmemiş | 2025-05-05 | FastAPI uygulamasını oluşturur ve yapılandırır |
| `↪ DashboardServer.set_face_plugin` | src/modules/dashboard_server.py | Belirtilmemiş | 2025-05-05 | Face Plugin referansını ayarlar |
| `↪ DashboardServer.start` | src/modules/dashboard_server.py | Belirtilmemiş | 2025-05-05 | Dashboard sunucusunu başlatır |
| `↪ DashboardServer.stop` | src/modules/dashboard_server.py | Belirtilmemiş | 2025-05-05 | Dashboard sunucusunu durdurur |
| `__init__` | src/modules/dashboard_server.py | Belirtilmemiş | 2025-05-05 | Dashboard sunucusunu başlatır |
| `_run_server` | src/modules/dashboard_server.py | Belirtilmemiş | 2025-05-05 | FastAPI sunucusunu başlatır |
| `_system_stats_loop` | src/modules/dashboard_server.py | Belirtilmemiş | 2025-05-05 | Sistem istatistiklerini düzenli aralıklarla toplar ve istemcilere gönderir |
| `create_app` | src/modules/dashboard_server.py | Belirtilmemiş | 2025-05-05 | FastAPI uygulamasını oluşturur ve yapılandırır |
| `set_face_plugin` | src/modules/dashboard_server.py | Belirtilmemiş | 2025-05-05 | Face Plugin referansını ayarlar |
| `start` | src/modules/dashboard_server.py | Belirtilmemiş | 2025-05-05 | Dashboard sunucusunu başlatır |
| `stop` | src/modules/dashboard_server.py | Belirtilmemiş | 2025-05-05 | Dashboard sunucusunu durdurur |
| `get_system_stats` | src/modules/dashboard_stats.py | Belirtilmemiş | 2025-05-02 | Sistem istatistiklerini alır |
| `🔶 TemplateManager` | src/modules/dashboard_templates.py | Belirtilmemiş | 2025-05-02 | Dashboard şablonlarını ve varsayılan içerikleri yöneten sınıf |
| `↪ TemplateManager.__init__` | src/modules/dashboard_templates.py | Belirtilmemiş | 2025-05-02 | Template Manager'ı başlatır |
| `↪ TemplateManager.ensure_templates` | src/modules/dashboard_templates.py | Belirtilmemiş | 2025-05-02 | Temel şablonların varlığını kontrol eder ve yoksa oluşturur |
| `↪ TemplateManager.get_default_css` | src/modules/dashboard_templates.py | Belirtilmemiş | 2025-05-02 | Varsayılan CSS stilini döndürür |
| `↪ TemplateManager.get_default_dashboard_template` | src/modules/dashboard_templates.py | Belirtilmemiş | 2025-05-02 | Varsayılan dashboard şablonunu döndürür |
| `↪ TemplateManager.get_default_error_template` | src/modules/dashboard_templates.py | Belirtilmemiş | 2025-05-02 | Varsayılan hata şablonunu döndürür |
| `↪ TemplateManager.get_default_html` | src/modules/dashboard_templates.py | Belirtilmemiş | 2025-05-02 | Varsayılan HTML içeriğini döndürür |
| `↪ TemplateManager.get_default_js` | src/modules/dashboard_templates.py | Belirtilmemiş | 2025-05-02 | Varsayılan JavaScript kodunu döndürür |
| `__init__` | src/modules/dashboard_templates.py | Belirtilmemiş | 2025-05-02 | Template Manager'ı başlatır |
| `ensure_templates` | src/modules/dashboard_templates.py | Belirtilmemiş | 2025-05-02 | Temel şablonların varlığını kontrol eder ve yoksa oluşturur |
| `get_default_css` | src/modules/dashboard_templates.py | Belirtilmemiş | 2025-05-02 | Varsayılan CSS stilini döndürür |
| `get_default_dashboard_template` | src/modules/dashboard_templates.py | Belirtilmemiş | 2025-05-02 | Varsayılan dashboard şablonunu döndürür |
| `get_default_error_template` | src/modules/dashboard_templates.py | Belirtilmemiş | 2025-05-02 | Varsayılan hata şablonunu döndürür |
| `get_default_html` | src/modules/dashboard_templates.py | Belirtilmemiş | 2025-05-02 | Varsayılan HTML içeriğini döndürür |
| `get_default_js` | src/modules/dashboard_templates.py | Belirtilmemiş | 2025-05-02 | Varsayılan JavaScript kodunu döndürür |
| `🔶 WebSocketManager` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | WebSocket bağlantı yönetim sınıfı |
| `↪ WebSocketManager.__init__` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `↪ WebSocketManager._ease_progress` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | İlerleme değerini yumuşatmak için easing fonksiyonu |
| `↪ WebSocketManager.handle_speaking_change` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | Konuşma durumu değiştiğinde çağrılır |
| `↪ WebSocketManager.handle_volume_change` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | Ses seviyesi değiştiğinde çağrılır |
| `↪ WebSocketManager.notify_animation_error` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | Animasyon hatalarını bildirir |
| `↪ WebSocketManager.notify_animation_event` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | Animasyon olaylarını bildirir ve WebSocket üzerinden istemcilere iletir |
| `↪ WebSocketManager.notify_animation_transition` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | Duygu durumları arasındaki geçiş animasyonlarını bildirir |
| `↪ WebSocketManager.register_animation_callbacks` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | Animasyon olayları için callback'leri kaydeder |
| `↪ WebSocketManager.register_sound_callbacks` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | Ses olayları için callback'leri kaydeder |
| `↪ WebSocketManager.set_face_plugin` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | Face Plugin referansını ayarlar |
| `__init__` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `_ease_progress` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | İlerleme değerini yumuşatmak için easing fonksiyonu |
| `handle_speaking_change` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | Konuşma durumu değiştiğinde çağrılır |
| `handle_volume_change` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | Ses seviyesi değiştiğinde çağrılır |
| `notify_animation_error` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | Animasyon hatalarını bildirir |
| `notify_animation_event` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | Animasyon olaylarını bildirir ve WebSocket üzerinden istemcilere iletir |
| `notify_animation_transition` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | Duygu durumları arasındaki geçiş animasyonlarını bildirir |
| `register_animation_callbacks` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | Animasyon olayları için callback'leri kaydeder |
| `register_sound_callbacks` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | Ses olayları için callback'leri kaydeder |
| `set_face_plugin` | src/modules/dashboard_websocket.py | Belirtilmemiş | 2025-05-04 | Face Plugin referansını ayarlar |
| `🔶 EmotionTransitionsWidget` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Hızlı Duygu Geçişleri Widget Sınıfı |
| `↪ EmotionTransitionsWidget.__init__` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Widget'ı başlatır |
| `↪ EmotionTransitionsWidget._add_to_recent_transitions` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Son kullanılanlar listesine bir geçiş ekler |
| `↪ EmotionTransitionsWidget._create_default_transitions` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Varsayılan duygu geçişleri oluşturur |
| `↪ EmotionTransitionsWidget._handle_delete_transition` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Duygu geçişi silme mesajını işler |
| `↪ EmotionTransitionsWidget._handle_play_transition` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Duygu geçişi oynatma mesajını işler |
| `↪ EmotionTransitionsWidget._handle_save_transition` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Duygu geçişi kaydetme mesajını işler |
| `↪ EmotionTransitionsWidget._handle_update_recent` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Son kullanılanlar listesini güncelleme mesajını işler |
| `↪ EmotionTransitionsWidget._load_transitions` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Duygu geçişlerini ve son kullanılanları yükler |
| `↪ EmotionTransitionsWidget._save_transitions` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Duygu geçişlerini ve son kullanılanları kaydeder |
| `↪ EmotionTransitionsWidget.get_widget_data` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Widget tarafından ihtiyaç duyulan verileri döndürür |
| `↪ EmotionTransitionsWidget.handle_websocket_message` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | WebSocket mesajını işler |
| `↪ EmotionTransitionsWidget.render` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Widget HTML içeriğini oluşturur |
| `↪ EmotionTransitionsWidget.set_emotion_engine` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Duygu motoru referansını ayarlar |
| `__init__` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Widget'ı başlatır |
| `_add_to_recent_transitions` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Son kullanılanlar listesine bir geçiş ekler |
| `_create_default_transitions` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Varsayılan duygu geçişleri oluşturur |
| `_handle_delete_transition` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Duygu geçişi silme mesajını işler |
| `_handle_play_transition` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Duygu geçişi oynatma mesajını işler |
| `_handle_save_transition` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Duygu geçişi kaydetme mesajını işler |
| `_handle_update_recent` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Son kullanılanlar listesini güncelleme mesajını işler |
| `_load_transitions` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Duygu geçişlerini ve son kullanılanları yükler |
| `_save_transitions` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Duygu geçişlerini ve son kullanılanları kaydeder |
| `get_widget_data` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Widget tarafından ihtiyaç duyulan verileri döndürür |
| `handle_websocket_message` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | WebSocket mesajını işler |
| `render` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Widget HTML içeriğini oluşturur |
| `set_emotion_engine` | src/modules/dashboard_widgets/emotion_transitions_widget.py | Belirtilmemiş | 2025-05-05 | Duygu motoru referansını ayarlar |
| `🔶 ExpressionWidget` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | Yüz İfadesi Kontrolü Widget'ı |
| `↪ ExpressionWidget.__init__` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | Widget'ı başlat |
| `↪ ExpressionWidget._get_current_emotion` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | Mevcut duygu durumunu alır |
| `↪ ExpressionWidget._handle_get_emotion_state` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | Mevcut duygu durumu sorgulama mesajını işler |
| `↪ ExpressionWidget._handle_micro_expression` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | Mikro ifade gösterme mesajını işler |
| `↪ ExpressionWidget._handle_set_emotion` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | Duygu durumu değiştirme mesajını işler |
| `↪ ExpressionWidget.get_widget_data` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | Widget tarafından ihtiyaç duyulan verileri döndürür |
| `↪ ExpressionWidget.handle_websocket_message` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | WebSocket mesajını işler |
| `↪ ExpressionWidget.render` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | Widget HTML içeriğini oluşturur |
| `↪ ExpressionWidget.set_emotion_engine` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | Duygu motoru referansını ayarlar |
| `__init__` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | Widget'ı başlat |
| `_get_current_emotion` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | Mevcut duygu durumunu alır |
| `_handle_get_emotion_state` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | Mevcut duygu durumu sorgulama mesajını işler |
| `_handle_micro_expression` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | Mikro ifade gösterme mesajını işler |
| `_handle_set_emotion` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | Duygu durumu değiştirme mesajını işler |
| `get_widget_data` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | Widget tarafından ihtiyaç duyulan verileri döndürür |
| `handle_websocket_message` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | WebSocket mesajını işler |
| `render` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | Widget HTML içeriğini oluşturur |
| `set_emotion_engine` | src/modules/dashboard_widgets/expression_widget.py | Belirtilmemiş | 2025-05-04 | Duygu motoru referansını ayarlar |
| `🔶 StateHistoryWidget` | src/modules/dashboard_widgets/state_history_widget.py | Belirtilmemiş | 2025-05-04 | Sistem durumu ve durum tarihçesi widget sınıfı |
| `↪ StateHistoryWidget.__init__` | src/modules/dashboard_widgets/state_history_widget.py | Belirtilmemiş | 2025-05-04 | StateHistoryWidget sınıfını başlatır |
| `↪ StateHistoryWidget._format_relative_time` | src/modules/dashboard_widgets/state_history_widget.py | Belirtilmemiş | 2025-05-04 | Bir zaman damgasını göreceli bir zaman ifadesine dönüştürür |
| `↪ StateHistoryWidget._format_uptime` | src/modules/dashboard_widgets/state_history_widget.py | Belirtilmemiş | 2025-05-04 | Çalışma süresini okunabilir bir formata dönüştürür |
| `↪ StateHistoryWidget.add_history_entry` | src/modules/dashboard_widgets/state_history_widget.py | Belirtilmemiş | 2025-05-04 | Tarihçeye yeni bir giriş ekler |
| `↪ StateHistoryWidget.get_activity_data` | src/modules/dashboard_widgets/state_history_widget.py | Belirtilmemiş | 2025-05-04 | Etkinlik grafiği için gerekli verileri döndürür |
| `↪ StateHistoryWidget.get_history_entries` | src/modules/dashboard_widgets/state_history_widget.py | Belirtilmemiş | 2025-05-04 | Durum tarihçesi girişlerini döndürür |
| `↪ StateHistoryWidget.get_widget_data` | src/modules/dashboard_widgets/state_history_widget.py | Belirtilmemiş | 2025-05-04 | Widget'ın şablon verilerini döndürür |
| `↪ StateHistoryWidget.update_state` | src/modules/dashboard_widgets/state_history_widget.py | Belirtilmemiş | 2025-05-04 | Belirli bir durum tipinin değerini günceller |
| `__init__` | src/modules/dashboard_widgets/state_history_widget.py | Belirtilmemiş | 2025-05-04 | StateHistoryWidget sınıfını başlatır |
| `_format_relative_time` | src/modules/dashboard_widgets/state_history_widget.py | Belirtilmemiş | 2025-05-04 | Bir zaman damgasını göreceli bir zaman ifadesine dönüştürür |
| `_format_uptime` | src/modules/dashboard_widgets/state_history_widget.py | Belirtilmemiş | 2025-05-04 | Çalışma süresini okunabilir bir formata dönüştürür |
| `add_history_entry` | src/modules/dashboard_widgets/state_history_widget.py | Belirtilmemiş | 2025-05-04 | Tarihçeye yeni bir giriş ekler |
| `get_activity_data` | src/modules/dashboard_widgets/state_history_widget.py | Belirtilmemiş | 2025-05-04 | Etkinlik grafiği için gerekli verileri döndürür |
| `get_history_entries` | src/modules/dashboard_widgets/state_history_widget.py | Belirtilmemiş | 2025-05-04 | Durum tarihçesi girişlerini döndürür |
| `get_widget_data` | src/modules/dashboard_widgets/state_history_widget.py | Belirtilmemiş | 2025-05-04 | Widget'ın şablon verilerini döndürür |
| `update_state` | src/modules/dashboard_widgets/state_history_widget.py | Belirtilmemiş | 2025-05-04 | Belirli bir durum tipinin değerini günceller |
| `🔶 WidgetManager` | src/modules/dashboard_widgets/widget_manager.py | Belirtilmemiş | 2025-05-05 | Dashboard widget'larını yöneten sınıf |
| `↪ WidgetManager.__init__` | src/modules/dashboard_widgets/widget_manager.py | Belirtilmemiş | 2025-05-05 | Widget Manager'ı başlatır |
| `↪ WidgetManager.get_all_widgets` | src/modules/dashboard_widgets/widget_manager.py | Belirtilmemiş | 2025-05-05 | Tüm yüklü widget'ların listesini döndürür |
| `↪ WidgetManager.get_widget_data` | src/modules/dashboard_widgets/widget_manager.py | Belirtilmemiş | 2025-05-05 | Belirtilen widget'ın veri güncellemesi için gerekli verileri döndürür |
| `↪ WidgetManager.handle_websocket_message` | src/modules/dashboard_widgets/widget_manager.py | Belirtilmemiş | 2025-05-05 | WebSocket mesajını ilgili widget'a yönlendirir |
| `↪ WidgetManager.load_widgets` | src/modules/dashboard_widgets/widget_manager.py | Belirtilmemiş | 2025-05-05 | Tüm widget modüllerini dinamik olarak yükler |
| `↪ WidgetManager.render_widget` | src/modules/dashboard_widgets/widget_manager.py | Belirtilmemiş | 2025-05-05 | Belirtilen widget'ın HTML içeriğini oluşturur |
| `↪ WidgetManager.set_face_plugin` | src/modules/dashboard_widgets/widget_manager.py | Belirtilmemiş | 2025-05-05 | Face Plugin referansını ayarlar ve tüm widget'lara iletir |
| `__init__` | src/modules/dashboard_widgets/widget_manager.py | Belirtilmemiş | 2025-05-05 | Widget Manager'ı başlatır |
| `get_all_widgets` | src/modules/dashboard_widgets/widget_manager.py | Belirtilmemiş | 2025-05-05 | Tüm yüklü widget'ların listesini döndürür |
| `get_widget_data` | src/modules/dashboard_widgets/widget_manager.py | Belirtilmemiş | 2025-05-05 | Belirtilen widget'ın veri güncellemesi için gerekli verileri döndürür |
| `handle_websocket_message` | src/modules/dashboard_widgets/widget_manager.py | Belirtilmemiş | 2025-05-05 | WebSocket mesajını ilgili widget'a yönlendirir |
| `load_widgets` | src/modules/dashboard_widgets/widget_manager.py | Belirtilmemiş | 2025-05-05 | Tüm widget modüllerini dinamik olarak yükler |
| `render_widget` | src/modules/dashboard_widgets/widget_manager.py | Belirtilmemiş | 2025-05-05 | Belirtilen widget'ın HTML içeriğini oluşturur |
| `set_face_plugin` | src/modules/dashboard_widgets/widget_manager.py | Belirtilmemiş | 2025-05-05 | Face Plugin referansını ayarlar ve tüm widget'lara iletir |
| `🔶 EmotionEngine` | src/modules/emotion_engine.py | Belirtilmemiş | 2025-05-02 | Duygu motoru ana sınıfı |
| `↪ EmotionEngine.__init__` | src/modules/emotion_engine.py | Belirtilmemiş | 2025-05-02 | Duygu motoru sınıfını başlatır |
| `↪ EmotionEngine._load_personality` | src/modules/emotion_engine.py | Belirtilmemiş | 2025-05-02 | Kişilik matrisini yükler |
| `↪ EmotionEngine._update_loop` | src/modules/emotion_engine.py | Belirtilmemiş | 2025-05-02 | Duygu güncelleme döngüsü |
| `↪ EmotionEngine.load_state` | src/modules/emotion_engine.py | Belirtilmemiş | 2025-05-02 | Duygu motoru durumunu dosyadan yükler |
| `↪ EmotionEngine.save_state` | src/modules/emotion_engine.py | Belirtilmemiş | 2025-05-02 | Duygu motoru durumunu dosyaya kaydeder |
| `__init__` | src/modules/emotion_engine.py | Belirtilmemiş | 2025-05-02 | Duygu motoru sınıfını başlatır |
| `_load_personality` | src/modules/emotion_engine.py | Belirtilmemiş | 2025-05-02 | Kişilik matrisini yükler |
| `_update_loop` | src/modules/emotion_engine.py | Belirtilmemiş | 2025-05-02 | Duygu güncelleme döngüsü |
| `load_state` | src/modules/emotion_engine.py | Belirtilmemiş | 2025-05-02 | Duygu motoru durumunu dosyadan yükler |
| `on_emotion_changed` | src/modules/emotion_engine.py | Belirtilmemiş | 2025-05-02 | Belirtilmemiş |
| `on_emotion_update` | src/modules/emotion_engine.py | Belirtilmemiş | 2025-05-02 | Belirtilmemiş |
| `save_state` | src/modules/emotion_engine.py | Belirtilmemiş | 2025-05-02 | Duygu motoru durumunu dosyaya kaydeder |
| `🔶 EmotionEngineBase` | src/modules/emotion_engine_base.py | Belirtilmemiş | 2025-05-02 | Duygu motoru temel sınıfı |
| `↪ EmotionEngineBase.__init__` | src/modules/emotion_engine_base.py | Belirtilmemiş | 2025-05-02 | Duygu motoru temel sınıfını başlatır |
| `↪ EmotionEngineBase._trigger_callbacks` | src/modules/emotion_engine_base.py | Belirtilmemiş | 2025-05-02 | Belirtilen olay tipindeki tüm geri çağrıları tetikler |
| `↪ EmotionEngineBase._update_loop` | src/modules/emotion_engine_base.py | Belirtilmemiş | 2025-05-02 | Duygu güncelleme döngüsü - alt sınıflar tarafından uygulanacak |
| `↪ EmotionEngineBase.register_callback` | src/modules/emotion_engine_base.py | Belirtilmemiş | 2025-05-02 | Olay geri çağrısı kaydeder |
| `↪ EmotionEngineBase.start` | src/modules/emotion_engine_base.py | Belirtilmemiş | 2025-05-02 | Duygu motorunu başlatır |
| `↪ EmotionEngineBase.stop` | src/modules/emotion_engine_base.py | Belirtilmemiş | 2025-05-02 | Duygu motorunu durdurur |
| `↪ EmotionEngineBase.unregister_callback` | src/modules/emotion_engine_base.py | Belirtilmemiş | 2025-05-02 | Olay geri çağrısı kaydını siler |
| `__init__` | src/modules/emotion_engine_base.py | Belirtilmemiş | 2025-05-02 | Duygu motoru temel sınıfını başlatır |
| `_trigger_callbacks` | src/modules/emotion_engine_base.py | Belirtilmemiş | 2025-05-02 | Belirtilen olay tipindeki tüm geri çağrıları tetikler |
| `_update_loop` | src/modules/emotion_engine_base.py | Belirtilmemiş | 2025-05-02 | Duygu güncelleme döngüsü - alt sınıflar tarafından uygulanacak |
| `register_callback` | src/modules/emotion_engine_base.py | Belirtilmemiş | 2025-05-02 | Olay geri çağrısı kaydeder |
| `start` | src/modules/emotion_engine_base.py | Belirtilmemiş | 2025-05-02 | Duygu motorunu başlatır |
| `stop` | src/modules/emotion_engine_base.py | Belirtilmemiş | 2025-05-02 | Duygu motorunu durdurur |
| `unregister_callback` | src/modules/emotion_engine_base.py | Belirtilmemiş | 2025-05-02 | Olay geri çağrısı kaydını siler |
| `🔶 EmotionExpressionsMixin` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Duygu ifadeleri mixin sınıfı |
| `↪ EmotionExpressionsMixin.__init_expressions` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Duygu ifade değişkenlerini başlatır. |
| `↪ EmotionExpressionsMixin._clean_expired_micro_expressions` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Süresi dolmuş mikro ifadeleri temizler |
| `↪ EmotionExpressionsMixin._generate_spontaneous_micro_expression` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Rastgele bir spontane mikro ifade oluşturur |
| `↪ EmotionExpressionsMixin._process_emotion_decay` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Duygu yoğunluğu zamanla azalma işlemini gerçekleştirir |
| `↪ EmotionExpressionsMixin._process_micro_expressions` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Mikro ifadeleri işler |
| `↪ EmotionExpressionsMixin.add_micro_expression` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Bir mikro ifade ekler |
| `↪ EmotionExpressionsMixin.get_current_emotion` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Mevcut duygu durumunu döndürür |
| `↪ EmotionExpressionsMixin.get_emotional_description` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Mevcut duygu durumunun metin açıklamasını oluşturur |
| `↪ EmotionExpressionsMixin.set_emotion` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Duygu durumunu ayarlar |
| `__init_expressions` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Duygu ifade değişkenlerini başlatır. |
| `_clean_expired_micro_expressions` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Süresi dolmuş mikro ifadeleri temizler |
| `_generate_spontaneous_micro_expression` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Rastgele bir spontane mikro ifade oluşturur |
| `_process_emotion_decay` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Duygu yoğunluğu zamanla azalma işlemini gerçekleştirir |
| `_process_micro_expressions` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Mikro ifadeleri işler |
| `add_micro_expression` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Bir mikro ifade ekler |
| `get_current_emotion` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Mevcut duygu durumunu döndürür |
| `get_emotional_description` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Mevcut duygu durumunun metin açıklamasını oluşturur |
| `set_emotion` | src/modules/emotion_engine_expressions.py | Belirtilmemiş | 2025-05-02 | Duygu durumunu ayarlar |
| `🔶 EmotionMemoryMixin` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Duygu hafızası mixin sınıfı |
| `↪ EmotionMemoryMixin.__init_memory` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Duygu hafıza ve istatistik değişkenlerini başlatır. |
| `↪ EmotionMemoryMixin._calculate_stability` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Duygu dengesini hesaplar (0.0-1.0) |
| `↪ EmotionMemoryMixin._update_emotion_memory` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Duygu hafızasını günceller |
| `↪ EmotionMemoryMixin._update_emotion_stats` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Duygu istatistiklerini günceller |
| `↪ EmotionMemoryMixin._update_memory_tiers` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Hafıza katmanlarını günceller - kısa, orta ve uzun vadeli hafızalar |
| `↪ EmotionMemoryMixin.generate_emotional_summary` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Duygu durumunun özet bilgisini oluşturur |
| `↪ EmotionMemoryMixin.get_dominant_emotion` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Belirli bir zaman diliminde baskın duyguyu döndürür |
| `↪ EmotionMemoryMixin.get_emotion_memory` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Duygu hafızasını döndürür |
| `↪ EmotionMemoryMixin.get_emotion_trend` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Duygu trendini hesaplar ve döndürür |
| `__init_memory` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Duygu hafıza ve istatistik değişkenlerini başlatır. |
| `_calculate_stability` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Duygu dengesini hesaplar (0.0-1.0) |
| `_update_emotion_memory` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Duygu hafızasını günceller |
| `_update_emotion_stats` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Duygu istatistiklerini günceller |
| `_update_memory_tiers` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Hafıza katmanlarını günceller - kısa, orta ve uzun vadeli hafızalar |
| `generate_emotional_summary` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Duygu durumunun özet bilgisini oluşturur |
| `get_dominant_emotion` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Belirli bir zaman diliminde baskın duyguyu döndürür |
| `get_emotion_memory` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Duygu hafızasını döndürür |
| `get_emotion_trend` | src/modules/emotion_engine_memory.py | Belirtilmemiş | 2025-05-02 | Duygu trendini hesaplar ve döndürür |
| `🔶 EmotionTransitionsMixin` | src/modules/emotion_engine_transitions.py | Belirtilmemiş | 2025-05-02 | Duygu geçişleri mixin sınıfı |
| `↪ EmotionTransitionsMixin.__init_transitions` | src/modules/emotion_engine_transitions.py | Belirtilmemiş | 2025-05-02 | Duygu geçiş değişkenlerini başlatır. |
| `↪ EmotionTransitionsMixin._add_transition_micro_expressions` | src/modules/emotion_engine_transitions.py | Belirtilmemiş | 2025-05-02 | Duygu geçişine uygun mikro ifadeler ekler |
| `↪ EmotionTransitionsMixin._complete_main_transition` | src/modules/emotion_engine_transitions.py | Belirtilmemiş | 2025-05-02 | Ana duygu geçişini tamamlar |
| `↪ EmotionTransitionsMixin._get_response_curve_value` | src/modules/emotion_engine_transitions.py | Belirtilmemiş | 2025-05-02 | Bir duygu için tepki eğrisindeki değeri hesaplar (zamanın bir fonksiyonu olarak) |
| `↪ EmotionTransitionsMixin._process_single_transition` | src/modules/emotion_engine_transitions.py | Belirtilmemiş | 2025-05-02 | Tek bir duygu geçişini işler |
| `↪ EmotionTransitionsMixin._update_emotion_transition` | src/modules/emotion_engine_transitions.py | Belirtilmemiş | 2025-05-02 | Duygu geçiş durumunu günceller |
| `↪ EmotionTransitionsMixin.transition_to` | src/modules/emotion_engine_transitions.py | Belirtilmemiş | 2025-05-02 | Belirtilen duyguya geçiş yapar |
| `__init_transitions` | src/modules/emotion_engine_transitions.py | Belirtilmemiş | 2025-05-02 | Duygu geçiş değişkenlerini başlatır. |
| `_add_transition_micro_expressions` | src/modules/emotion_engine_transitions.py | Belirtilmemiş | 2025-05-02 | Duygu geçişine uygun mikro ifadeler ekler |
| `_complete_main_transition` | src/modules/emotion_engine_transitions.py | Belirtilmemiş | 2025-05-02 | Ana duygu geçişini tamamlar |
| `_get_response_curve_value` | src/modules/emotion_engine_transitions.py | Belirtilmemiş | 2025-05-02 | Bir duygu için tepki eğrisindeki değeri hesaplar (zamanın bir fonksiyonu olarak) |
| `_process_single_transition` | src/modules/emotion_engine_transitions.py | Belirtilmemiş | 2025-05-02 | Tek bir duygu geçişini işler |
| `_update_emotion_transition` | src/modules/emotion_engine_transitions.py | Belirtilmemiş | 2025-05-02 | Duygu geçiş durumunu günceller |
| `transition_to` | src/modules/emotion_engine_transitions.py | Belirtilmemiş | 2025-05-02 | Belirtilen duyguya geçiş yapar |
| `🔶 EmotionState` | src/modules/emotion_states.py | Belirtilmemiş | 2025-05-02 | Duygu durumları için enum |
| `get_all_emotions` | src/modules/emotion_states.py | Belirtilmemiş | 2025-05-02 | Tüm duygu durumlarını liste olarak döndürür |
| `get_emotion_state` | src/modules/emotion_states.py | Belirtilmemiş | 2025-05-02 | Duygu adından EmotionState nesnesini döndürür |
| `get_emotion_subtype` | src/modules/emotion_states.py | Belirtilmemiş | 2025-05-02 | Belirli bir duygu ve yoğunluğa göre alt tür seçer |
| `get_intensity_label` | src/modules/emotion_states.py | Belirtilmemiş | 2025-05-02 | Belirli bir yoğunluk için etiket döndürür |
| `is_valid_emotion` | src/modules/emotion_states.py | Belirtilmemiş | 2025-05-02 | Duygu adının geçerli olup olmadığını kontrol eder |
| `🔶 FacePluginAPI` | src/modules/face/face_plugin_api.py | Belirtilmemiş | 2025-05-03 | FacePlugin API sınıfı |
| `↪ FacePluginAPI._notify_websocket_clients` | src/modules/face/face_plugin_api.py | Belirtilmemiş | 2025-05-03 | WebSocket istemcilerine bildirim gönderir |
| `↪ FacePluginAPI._setup_api` | src/modules/face/face_plugin_api.py | Belirtilmemiş | 2025-05-03 | REST API'yi ayarlar ve başlatır |
| `↪ FacePluginAPI._stop_api` | src/modules/face/face_plugin_api.py | Belirtilmemiş | 2025-05-03 | API sunucusunu durdurur |
| `_notify_websocket_clients` | src/modules/face/face_plugin_api.py | Belirtilmemiş | 2025-05-03 | WebSocket istemcilerine bildirim gönderir |
| `_setup_api` | src/modules/face/face_plugin_api.py | Belirtilmemiş | 2025-05-03 | REST API'yi ayarlar ve başlatır |
| `_stop_api` | src/modules/face/face_plugin_api.py | Belirtilmemiş | 2025-05-03 | API sunucusunu durdurur |
| `run_api` | src/modules/face/face_plugin_api.py | Belirtilmemiş | 2025-05-03 | Belirtilmemiş |
| `🔶 FacePluginBase` | src/modules/face/face_plugin_base.py | Belirtilmemiş | 2025-05-04 | FacePlugin temel sınıfı |
| `↪ FacePluginBase.__init__` | src/modules/face/face_plugin_base.py | Belirtilmemiş | 2025-05-04 | FacePluginBase sınıfını başlatır |
| `↪ FacePluginBase._create_default_config` | src/modules/face/face_plugin_base.py | Belirtilmemiş | 2025-05-04 | Varsayılan yapılandırma ayarlarını oluşturur |
| `↪ FacePluginBase._load_config` | src/modules/face/face_plugin_base.py | Belirtilmemiş | 2025-05-04 | Yapılandırma dosyasını yükler |
| `↪ FacePluginBase._on_state_changed` | src/modules/face/face_plugin_base.py | Belirtilmemiş | 2025-05-04 | Durum değişikliği olaylarını işler |
| `↪ FacePluginBase._setup_logging` | src/modules/face/face_plugin_base.py | Belirtilmemiş | 2025-05-04 | Loglama yapılandırmasını ayarlar |
| `↪ FacePluginBase.update_config` | src/modules/face/face_plugin_base.py | Belirtilmemiş | 2025-05-04 | Yeni yapılandırmayı uygular ve yapılandırma dosyasına kaydeder |
| `__init__` | src/modules/face/face_plugin_base.py | Belirtilmemiş | 2025-05-04 | FacePluginBase sınıfını başlatır |
| `_create_default_config` | src/modules/face/face_plugin_base.py | Belirtilmemiş | 2025-05-04 | Varsayılan yapılandırma ayarlarını oluşturur |
| `_load_config` | src/modules/face/face_plugin_base.py | Belirtilmemiş | 2025-05-04 | Yapılandırma dosyasını yükler |
| `_on_state_changed` | src/modules/face/face_plugin_base.py | Belirtilmemiş | 2025-05-04 | Durum değişikliği olaylarını işler |
| `_setup_logging` | src/modules/face/face_plugin_base.py | Belirtilmemiş | 2025-05-04 | Loglama yapılandırmasını ayarlar |
| `update_config` | src/modules/face/face_plugin_base.py | Belirtilmemiş | 2025-05-04 | Yeni yapılandırmayı uygular ve yapılandırma dosyasına kaydeder |
| `🔶 FacePluginCallbacks` | src/modules/face/face_plugin_callbacks.py | Belirtilmemiş | 2025-05-02 | FacePlugin callback sınıfı |
| `↪ FacePluginCallbacks._on_emotion_changed` | src/modules/face/face_plugin_callbacks.py | Belirtilmemiş | 2025-05-02 | Duygu değiştiğinde çağrılan fonksiyon |
| `↪ FacePluginCallbacks._on_emotion_transition` | src/modules/face/face_plugin_callbacks.py | Belirtilmemiş | 2025-05-02 | Duygu geçişi sürecinde çağrılan fonksiyon |
| `↪ FacePluginCallbacks._on_micro_expression` | src/modules/face/face_plugin_callbacks.py | Belirtilmemiş | 2025-05-02 | Mikro ifade tetiklendiğinde çağrılan fonksiyon |
| `↪ FacePluginCallbacks._on_theme_changed` | src/modules/face/face_plugin_callbacks.py | Belirtilmemiş | 2025-05-02 | Tema değiştiğinde çağrılan fonksiyon |
| `↪ FacePluginCallbacks._register_callbacks` | src/modules/face/face_plugin_callbacks.py | Belirtilmemiş | 2025-05-02 | Duygu motoru için geri çağrı fonksiyonlarını kaydeder |
| `↪ FacePluginCallbacks._run_startup_sequence` | src/modules/face/face_plugin_callbacks.py | Belirtilmemiş | 2025-05-02 | Başlangıç animasyon dizisini çalıştırır |
| `_on_emotion_changed` | src/modules/face/face_plugin_callbacks.py | Belirtilmemiş | 2025-05-02 | Duygu değiştiğinde çağrılan fonksiyon |
| `_on_emotion_transition` | src/modules/face/face_plugin_callbacks.py | Belirtilmemiş | 2025-05-02 | Duygu geçişi sürecinde çağrılan fonksiyon |
| `_on_micro_expression` | src/modules/face/face_plugin_callbacks.py | Belirtilmemiş | 2025-05-02 | Mikro ifade tetiklendiğinde çağrılan fonksiyon |
| `_on_theme_changed` | src/modules/face/face_plugin_callbacks.py | Belirtilmemiş | 2025-05-02 | Tema değiştiğinde çağrılan fonksiyon |
| `_register_callbacks` | src/modules/face/face_plugin_callbacks.py | Belirtilmemiş | 2025-05-02 | Duygu motoru için geri çağrı fonksiyonlarını kaydeder |
| `_run_startup_sequence` | src/modules/face/face_plugin_callbacks.py | Belirtilmemiş | 2025-05-02 | Başlangıç animasyon dizisini çalıştırır |
| `🔶 FacePluginConfigMixin` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | FacePlugin yapılandırma yönetimi mixin sınıfı |
| `↪ FacePluginConfigMixin._create_default_config` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Varsayılan yapılandırmayı oluşturur |
| `↪ FacePluginConfigMixin._load_config` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Yapılandırma dosyasını yükler |
| `↪ FacePluginConfigMixin._save_config` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Yapılandırmayı dosyaya kaydeder |
| `↪ FacePluginConfigMixin.get_config_value` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Yapılandırmadan değer alır (nokta ayrılmış yol ile) |
| `↪ FacePluginConfigMixin.notify_config_changed` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Modülleri yapılandırma değişikliğinden haberdar eder |
| `↪ FacePluginConfigMixin.reset_config` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Yapılandırmayı varsayılan değerlere sıfırlar |
| `↪ FacePluginConfigMixin.set_config_value` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Yapılandırmada değer ayarlar (nokta ayrılmış yol ile) |
| `↪ FacePluginConfigMixin.track_config_changes` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Yapılandırma değişikliklerini takip eder ve loglar |
| `↪ FacePluginConfigMixin.update_config` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Yeni yapılandırmayı uygular ve isteğe bağlı olarak dosyaya kaydeder |
| `_create_default_config` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Varsayılan yapılandırmayı oluşturur |
| `_load_config` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Yapılandırma dosyasını yükler |
| `_save_config` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Yapılandırmayı dosyaya kaydeder |
| `get_config_value` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Yapılandırmadan değer alır (nokta ayrılmış yol ile) |
| `notify_config_changed` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Modülleri yapılandırma değişikliğinden haberdar eder |
| `reset_config` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Yapılandırmayı varsayılan değerlere sıfırlar |
| `set_config_value` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Yapılandırmada değer ayarlar (nokta ayrılmış yol ile) |
| `track_config_changes` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Yapılandırma değişikliklerini takip eder ve loglar |
| `traverse_and_compare` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `update_config` | src/modules/face/face_plugin_config.py | Belirtilmemiş | 2025-05-04 | Yeni yapılandırmayı uygular ve isteğe bağlı olarak dosyaya kaydeder |
| `🔶 FacePluginEnvironmentMixin` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | FacePlugin çevresel faktör yönetimi mixin sınıfı |
| `↪ FacePluginEnvironmentMixin.__init_environment__` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel faktör sistemini başlatır - ana __init__ metodundan sonra çağrılmalıdır |
| `↪ FacePluginEnvironmentMixin._environment_monitoring_loop` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel faktör izleme döngüsünün ana işlevi |
| `↪ FacePluginEnvironmentMixin._handle_special_environmental_cases` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Özel çevresel durumlara tepki verir (özel kullanım durumları için) |
| `↪ FacePluginEnvironmentMixin.cleanup_environment_resources` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel faktör kaynaklarını temizler (program sonlandırılırken) |
| `↪ FacePluginEnvironmentMixin.get_environment_data` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Güncel çevresel faktör verilerini döndürür |
| `↪ FacePluginEnvironmentMixin.on_environment_change` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel faktör değişikliklerini işler |
| `↪ FacePluginEnvironmentMixin.process_environmental_reactions` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel faktörlere göre tepkiler oluşturur |
| `↪ FacePluginEnvironmentMixin.read_light_level` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Işık seviyesini okur |
| `↪ FacePluginEnvironmentMixin.read_motion_sensor` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Hareket sensörünü okur |
| `↪ FacePluginEnvironmentMixin.read_temperature_humidity` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Sıcaklık ve nem değerlerini okur |
| `↪ FacePluginEnvironmentMixin.read_touch_sensors` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Dokunmatik sensörleri okur |
| `↪ FacePluginEnvironmentMixin.register_environment_callback` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel faktör değişiklikleri için geri çağırma işlevi kaydeder |
| `↪ FacePluginEnvironmentMixin.setup_environment_sensors` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel sensörleri yapılandırır |
| `↪ FacePluginEnvironmentMixin.start_environment_monitoring` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel faktör izleme döngüsünü başlatır |
| `↪ FacePluginEnvironmentMixin.stop_environment_monitoring` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel faktör izleme döngüsünü durdurur |
| `↪ FacePluginEnvironmentMixin.unregister_environment_callback` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel faktör geri çağırma işlevini kaldırır |
| `__init_environment__` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel faktör sistemini başlatır - ana __init__ metodundan sonra çağrılmalıdır |
| `_environment_monitoring_loop` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel faktör izleme döngüsünün ana işlevi |
| `_handle_special_environmental_cases` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Özel çevresel durumlara tepki verir (özel kullanım durumları için) |
| `cleanup_environment_resources` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel faktör kaynaklarını temizler (program sonlandırılırken) |
| `get_environment_data` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Güncel çevresel faktör verilerini döndürür |
| `on_environment_change` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel faktör değişikliklerini işler |
| `process_environmental_reactions` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel faktörlere göre tepkiler oluşturur |
| `read_light_level` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Işık seviyesini okur |
| `read_motion_sensor` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Hareket sensörünü okur |
| `read_temperature_humidity` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Sıcaklık ve nem değerlerini okur |
| `read_touch_sensors` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Dokunmatik sensörleri okur |
| `register_environment_callback` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel faktör değişiklikleri için geri çağırma işlevi kaydeder |
| `setup_environment_sensors` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel sensörleri yapılandırır |
| `start_environment_monitoring` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel faktör izleme döngüsünü başlatır |
| `stop_environment_monitoring` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel faktör izleme döngüsünü durdurur |
| `unregister_environment_callback` | src/modules/face/face_plugin_environment.py | Belirtilmemiş | 2025-05-04 | Çevresel faktör geri çağırma işlevini kaldırır |
| `🔶 FacePluginLifecycle` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | FacePlugin yaşam döngüsü sınıfı |
| `↪ FacePluginLifecycle.__init__` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | FacePluginLifecycle sınıfını başlatır |
| `↪ FacePluginLifecycle._notify_state_changed` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Durum değişikliği bildirimlerini gönderir |
| `↪ FacePluginLifecycle.can_transition_to` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Belirtilen duruma geçişin mümkün olup olmadığını kontrol eder |
| `↪ FacePluginLifecycle.enter_maintenance_mode` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Plugin'i bakım moduna alır |
| `↪ FacePluginLifecycle.exit_maintenance_mode` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Plugin'i bakım modundan çıkarır |
| `↪ FacePluginLifecycle.get_error_rate` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Hata oranını döndürür |
| `↪ FacePluginLifecycle.get_state_duration` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Belirli bir durumda toplam geçirilen süreyi döndürür |
| `↪ FacePluginLifecycle.get_state_history` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Durum geçiş tarihçesini döndürür |
| `↪ FacePluginLifecycle.get_status_report` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Plugin durumunun detaylı raporunu döndürür |
| `↪ FacePluginLifecycle.get_uptime` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Plugin'in toplam çalışma süresini döndürür |
| `↪ FacePluginLifecycle.pause` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Plugin'i duraklatır |
| `↪ FacePluginLifecycle.perform_maintenance` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Bakım işlemlerini gerçekleştirir |
| `↪ FacePluginLifecycle.register_state_change_callback` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Durum değişikliği olayları için callback kaydeder |
| `↪ FacePluginLifecycle.resume` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Duraklatılmış plugin'i devam ettirir |
| `↪ FacePluginLifecycle.should_enter_maintenance` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Bakım moduna geçilmesi gerekip gerekmediğini kontrol eder |
| `↪ FacePluginLifecycle.shutdown` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Plugin'i tamamen kapatır (shutdown) |
| `↪ FacePluginLifecycle.start_maintenance_cycle` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Periyodik bakım döngüsünü başlatır |
| `↪ FacePluginLifecycle.state` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Plugin'in mevcut durumunu döndürür |
| `↪ FacePluginLifecycle.state_name` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Plugin'in mevcut durum adını döndürür |
| `↪ FacePluginLifecycle.stop_maintenance_cycle` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Periyodik bakım döngüsünü durdurur |
| `↪ FacePluginLifecycle.transition_to` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Belirtilen duruma geçiş yapar |
| `↪ FacePluginLifecycle.unregister_state_change_callback` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Durum değişikliği callback'ini kaldırır |
| `🔶 PluginState` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Plugin durumlarını tanımlayan enum sınıfı |
| `__init__` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | FacePluginLifecycle sınıfını başlatır |
| `_notify_state_changed` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Durum değişikliği bildirimlerini gönderir |
| `can_transition_to` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Belirtilen duruma geçişin mümkün olup olmadığını kontrol eder |
| `enter_maintenance_mode` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Plugin'i bakım moduna alır |
| `exit_maintenance_mode` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Plugin'i bakım modundan çıkarır |
| `get_error_rate` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Hata oranını döndürür |
| `get_state_duration` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Belirli bir durumda toplam geçirilen süreyi döndürür |
| `get_state_history` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Durum geçiş tarihçesini döndürür |
| `get_status_report` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Plugin durumunun detaylı raporunu döndürür |
| `get_uptime` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Plugin'in toplam çalışma süresini döndürür |
| `maintenance_loop` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Belirtilmemiş |
| `pause` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Plugin'i duraklatır |
| `perform_maintenance` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Bakım işlemlerini gerçekleştirir |
| `register_state_change_callback` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Durum değişikliği olayları için callback kaydeder |
| `resume` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Duraklatılmış plugin'i devam ettirir |
| `should_enter_maintenance` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Bakım moduna geçilmesi gerekip gerekmediğini kontrol eder |
| `shutdown` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Plugin'i tamamen kapatır (shutdown) |
| `start_maintenance_cycle` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Periyodik bakım döngüsünü başlatır |
| `state` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Plugin'in mevcut durumunu döndürür |
| `state_name` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Plugin'in mevcut durum adını döndürür |
| `stop_maintenance_cycle` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Periyodik bakım döngüsünü durdurur |
| `transition_to` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Belirtilen duruma geçiş yapar |
| `unregister_state_change_callback` | src/modules/face/face_plugin_lifecycle.py | Belirtilmemiş | 2025-05-03 | Durum değişikliği callback'ini kaldırır |
| `🔶 FacePluginMetricsMixin` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | FacePlugin metrik toplama mixin sınıfı |
| `↪ FacePluginMetricsMixin.__init_metrics__` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Metrik sistemini başlatır - ana __init__ metodundan sonra çağrılmalıdır |
| `↪ FacePluginMetricsMixin._get_system_temperature` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Sistem sıcaklığını alır (Raspberry Pi'de çalışır) |
| `↪ FacePluginMetricsMixin._metrics_collection_loop` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Metrik toplama döngüsünün ana işlevi |
| `↪ FacePluginMetricsMixin._update_metric_history` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Metrik geçmişini günceller |
| `↪ FacePluginMetricsMixin.collect_module_metrics` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Modül metriklerini toplar |
| `↪ FacePluginMetricsMixin.collect_system_metrics` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Sistem metriklerini toplar |
| `↪ FacePluginMetricsMixin.get_health_status` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Sistem sağlık durumu raporu oluşturur |
| `↪ FacePluginMetricsMixin.get_metric_history` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Metrik geçmişini döndürür |
| `↪ FacePluginMetricsMixin.get_metrics` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Tüm metrikleri toplar ve döndürür |
| `↪ FacePluginMetricsMixin.save_metrics_to_file` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Metrikleri dosyaya kaydeder |
| `↪ FacePluginMetricsMixin.start_metric_collection` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Metrik toplama döngüsünü başlatır |
| `↪ FacePluginMetricsMixin.stop_metric_collection` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Metrik toplama döngüsünü durdurur |
| `↪ FacePluginMetricsMixin.update_api_metrics` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | API metriklerini günceller |
| `↪ FacePluginMetricsMixin.update_performance_metrics` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Performans metriklerini günceller |
| `__init_metrics__` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Metrik sistemini başlatır - ana __init__ metodundan sonra çağrılmalıdır |
| `_get_system_temperature` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Sistem sıcaklığını alır (Raspberry Pi'de çalışır) |
| `_metrics_collection_loop` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Metrik toplama döngüsünün ana işlevi |
| `_update_metric_history` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Metrik geçmişini günceller |
| `collect_module_metrics` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Modül metriklerini toplar |
| `collect_system_metrics` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Sistem metriklerini toplar |
| `get_health_status` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Sistem sağlık durumu raporu oluşturur |
| `get_metric_history` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Metrik geçmişini döndürür |
| `get_metrics` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Tüm metrikleri toplar ve döndürür |
| `save_metrics_to_file` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Metrikleri dosyaya kaydeder |
| `start_metric_collection` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Metrik toplama döngüsünü başlatır |
| `stop_metric_collection` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Metrik toplama döngüsünü durdurur |
| `update_api_metrics` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | API metriklerini günceller |
| `update_performance_metrics` | src/modules/face/face_plugin_metrics.py | Belirtilmemiş | 2025-05-04 | Performans metriklerini günceller |
| `🔶 FacePluginSystem` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | FacePlugin sistem sınıfı |
| `↪ FacePluginSystem._run_startup_sequence` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Başlangıç animasyon sekansını çalıştırır |
| `↪ FacePluginSystem._start_watchdog` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Watchdog zamanlayıcısını başlatır |
| `↪ FacePluginSystem.heartbeat` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Watchdog kalp atışını günceller |
| `↪ FacePluginSystem.initialize` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Yüz eklentisini ve tüm modüllerini başlatır |
| `↪ FacePluginSystem.load_state` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Eklenti durumunu yükler |
| `↪ FacePluginSystem.notify_state_change` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Durum değişikliğini istemcilere bildirir |
| `↪ FacePluginSystem.perform_maintenance` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Bakım işlemlerini gerçekleştirir - FacePluginLifecycle'dan override edildi |
| `↪ FacePluginSystem.restart` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Yüz eklentisini yeniden başlatır |
| `↪ FacePluginSystem.save_state` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Eklenti durumunu kaydeder |
| `↪ FacePluginSystem.start` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Yüz eklentisini çalıştırmaya başlar |
| `↪ FacePluginSystem.stop` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Yüz eklentisini durdurur |
| `_run_startup_sequence` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Başlangıç animasyon sekansını çalıştırır |
| `_start_watchdog` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Watchdog zamanlayıcısını başlatır |
| `heartbeat` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Watchdog kalp atışını günceller |
| `initialize` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Yüz eklentisini ve tüm modüllerini başlatır |
| `load_state` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Eklenti durumunu yükler |
| `notify_state_change` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Durum değişikliğini istemcilere bildirir |
| `perform_maintenance` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Bakım işlemlerini gerçekleştirir - FacePluginLifecycle'dan override edildi |
| `restart` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Yüz eklentisini yeniden başlatır |
| `save_state` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Eklenti durumunu kaydeder |
| `start` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Yüz eklentisini çalıştırmaya başlar |
| `stop` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Yüz eklentisini durdurur |
| `watchdog_check` | src/modules/face/face_plugin_system.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `🔶 FacePlugin` | src/modules/face1_plugin.py | 0.4.4 | 2025-05-04 | FACE1 yüz eklentisi ana sınıf |
| `↪ FacePlugin.__init__` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | FACE1 yüz eklentisini başlatır |
| `↪ FacePlugin._init_animation_engine` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Animasyon motoru modülünü başlatır |
| `↪ FacePlugin._init_emotion_engine` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Duygu motoru modülünü başlatır |
| `↪ FacePlugin._init_led_controller` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | LED kontrolcü modülünü başlatır |
| `↪ FacePlugin._init_modules` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Tüm modülleri başlatır |
| `↪ FacePlugin._init_oled_controller` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | OLED kontrolcü modülünü başlatır |
| `↪ FacePlugin._init_sound_processor` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Ses işleme modülünü başlatır |
| `↪ FacePlugin._init_theme_manager` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Tema yöneticisi modülünü başlatır |
| `↪ FacePlugin.export_to_parent_config` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | FACE1 yapılandırmasını üst proje formatına dönüştürür |
| `↪ FacePlugin.get_current_emotion` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Mevcut duygu durumu bilgisini döndürür |
| `↪ FacePlugin.get_metrics` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Plugin metriklerini döndürür |
| `↪ FacePlugin.get_plugin_status` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Plugin durumunu döndürür |
| `↪ FacePlugin.handle_environment_change` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Çevresel faktör değişikliklerini işler ve websocket üzerinden istemcilere bildirir |
| `↪ FacePlugin.initialize_modules` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Tüm modülleri başlatır ve aralarındaki bağlantıları kurar |
| `↪ FacePlugin.migrate_parent_config` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Üst proje yapılandırmasını FACE1'e uygun formata dönüştürür |
| `↪ FacePlugin.pause` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Yüz eklentisini duraklatır (ancak durdurma yerine kısmi işlevsellik sürdürür) |
| `↪ FacePlugin.resume` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Duraklatılmış yüz eklentisini devam ettirir |
| `↪ FacePlugin.run_forever` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Eklentiyi başlatır ve sonsuza kadar çalıştırır |
| `↪ FacePlugin.set_emotion` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Duygu durumunu ayarlar |
| `↪ FacePlugin.start` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Yüz eklentisini başlatır |
| `↪ FacePlugin.stop` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Yüz eklentisini durdurur |
| `↪ FacePlugin.transition_to_emotion` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Belirli bir duyguya yumuşak geçiş yapar |
| `__init__` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | FACE1 yüz eklentisini başlatır |
| `_init_animation_engine` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Animasyon motoru modülünü başlatır |
| `_init_emotion_engine` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Duygu motoru modülünü başlatır |
| `_init_led_controller` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | LED kontrolcü modülünü başlatır |
| `_init_modules` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Tüm modülleri başlatır |
| `_init_oled_controller` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | OLED kontrolcü modülünü başlatır |
| `_init_sound_processor` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Ses işleme modülünü başlatır |
| `_init_theme_manager` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Tema yöneticisi modülünü başlatır |
| `export_to_parent_config` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | FACE1 yapılandırmasını üst proje formatına dönüştürür |
| `get_current_emotion` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Mevcut duygu durumu bilgisini döndürür |
| `get_metrics` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Plugin metriklerini döndürür |
| `get_plugin_status` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Plugin durumunu döndürür |
| `handle_environment_change` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Çevresel faktör değişikliklerini işler ve websocket üzerinden istemcilere bildirir |
| `initialize_modules` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Tüm modülleri başlatır ve aralarındaki bağlantıları kurar |
| `main` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Ana fonksiyon |
| `migrate_parent_config` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Üst proje yapılandırmasını FACE1'e uygun formata dönüştürür |
| `pause` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Yüz eklentisini duraklatır (ancak durdurma yerine kısmi işlevsellik sürdürür) |
| `resume` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Duraklatılmış yüz eklentisini devam ettirir |
| `run_forever` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Eklentiyi başlatır ve sonsuza kadar çalıştırır |
| `set_emotion` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Duygu durumunu ayarlar |
| `signal_handler` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `start` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Yüz eklentisini başlatır |
| `stop` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Yüz eklentisini durdurur |
| `transition_to_emotion` | src/modules/face1_plugin.py | Belirtilmemiş | 2025-05-04 | Belirli bir duyguya yumuşak geçiş yapar |
| `🔶 IOManager` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | I/O yöneticisi sınıfı |
| `↪ IOManager.__init__` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | I/O yöneticisini başlatır |
| `↪ IOManager._check_rate_limit` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | Hız sınırı kontrolü yapar |
| `↪ IOManager._init_mqtt_client` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | MQTT istemcisini başlatır |
| `↪ IOManager._on_mqtt_connect` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | MQTT bağlantı geri çağrısı |
| `↪ IOManager._on_mqtt_disconnect` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | MQTT bağlantı kesme geri çağrısı |
| `↪ IOManager._on_mqtt_message` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | MQTT mesaj geri çağrısı |
| `↪ IOManager._start_websocket_server` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | WebSocket sunucusunu başlatır |
| `↪ IOManager.register_callback` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | Olay geri çağrısı kaydeder |
| `↪ IOManager.register_command_handler` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | Komut işleyici kaydeder |
| `↪ IOManager.send_event` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | Olay gönderir |
| `↪ IOManager.start` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | I/O yöneticisini başlatır |
| `↪ IOManager.stop` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | I/O yöneticisini durdurur |
| `↪ IOManager.unregister_callback` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | Olay geri çağrı kaydını siler |
| `↪ IOManager.unregister_command_handler` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | Komut işleyici kaydını siler |
| `🔶 MessageType` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | Mesaj türleri için enum sınıfı |
| `__init__` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | I/O yöneticisini başlatır |
| `_check_rate_limit` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | Hız sınırı kontrolü yapar |
| `_init_mqtt_client` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | MQTT istemcisini başlatır |
| `_on_mqtt_connect` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | MQTT bağlantı geri çağrısı |
| `_on_mqtt_disconnect` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | MQTT bağlantı kesme geri çağrısı |
| `_on_mqtt_message` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | MQTT mesaj geri çağrısı |
| `_start_websocket_server` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | WebSocket sunucusunu başlatır |
| `handle_test_command` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | Belirtilmemiş |
| `on_test_event` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | Belirtilmemiş |
| `register_callback` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | Olay geri çağrısı kaydeder |
| `register_command_handler` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | Komut işleyici kaydeder |
| `send_event` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | Olay gönderir |
| `start` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | I/O yöneticisini başlatır |
| `stop` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | I/O yöneticisini durdurur |
| `unregister_callback` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | Olay geri çağrı kaydını siler |
| `unregister_command_handler` | src/modules/io_manager.py | Belirtilmemiş | 2025-04-30 | Komut işleyici kaydını siler |
| `🔶 LEDController` | src/modules/led_controller.py | Belirtilmemiş | 2025-05-02 | WS2812B LED şeritlerini kontrol etmek için ana sınıf |
| `↪ LEDController.__init__` | src/modules/led_controller.py | Belirtilmemiş | 2025-05-02 | LED kontrolcüsünü başlatır |
| `↪ LEDController.get_state` | src/modules/led_controller.py | Belirtilmemiş | 2025-05-02 | LED kontrolcünün mevcut durumunu döndürür |
| `↪ LEDController.on_emotion_changed` | src/modules/led_controller.py | Belirtilmemiş | 2025-05-02 | Duygu değişikliğinde çağrılan metod |
| `__init__` | src/modules/led_controller.py | Belirtilmemiş | 2025-05-02 | LED kontrolcüsünü başlatır |
| `get_state` | src/modules/led_controller.py | Belirtilmemiş | 2025-05-02 | LED kontrolcünün mevcut durumunu döndürür |
| `on_emotion_changed` | src/modules/led_controller.py | Belirtilmemiş | 2025-05-02 | Duygu değişikliğinde çağrılan metod |
| `🔶 LEDControllerAnimations` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | LED animasyonları için karışım (mixin) sınıfı |
| `↪ LEDControllerAnimations._animate_breathe` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Nefes alma animasyonu - Yumuşak geçişlerle parlama ve sönme |
| `↪ LEDControllerAnimations._animate_breathe` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Nefes alma animasyonu - Yumuşak geçişli parlama/sönme |
| `↪ LEDControllerAnimations._animate_chase` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Takip animasyonu - Renk noktası şeridi dolaşır |
| `↪ LEDControllerAnimations._animate_color_fade` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Renkler arası geçiş animasyonu |
| `↪ LEDControllerAnimations._animate_fade` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Solma animasyonu - Tam renkten siyaha doğru geçiş |
| `↪ LEDControllerAnimations._animate_pulse` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Nabız animasyonu - Parlayıp sönme |
| `↪ LEDControllerAnimations._animate_pulse` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Nabız animasyonu - Parlayıp sönme |
| `↪ LEDControllerAnimations._animate_rainbow` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Gökkuşağı animasyonu - Renk spektrumu boyunca hareket |
| `↪ LEDControllerAnimations._animate_rainbow` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Gökkuşağı animasyonu - Spektrum rengi geçişleri |
| `↪ LEDControllerAnimations._animate_scan` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Tarama animasyonu - Işık soldan sağa, sonra sağdan sola hareket eder |
| `↪ LEDControllerAnimations._animate_sparkle` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Pırıltı animasyonu - Rastgele LEDler yanıp söner |
| `↪ LEDControllerAnimations._animate_static` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Sabit renk animasyonu |
| `↪ LEDControllerAnimations._animate_theater_chase` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Tiyatro takip animasyonu - Sırayla yanıp sönen gruplar |
| `↪ LEDControllerAnimations._animate_twinkle` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Yıldız parıltısı animasyonu - Rastgele LEDler yanıp söner, farklı parlaklık düzeylerinde |
| `↪ LEDControllerAnimations._animate_wave` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Dalga animasyonu - sinüs dalgası şeklinde renk dalgalanması |
| `↪ LEDControllerAnimations._animate_wipe` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Silme animasyonu - Renk bir uçtan diğerine doğru yayılır |
| `↪ LEDControllerAnimations._precompute_fire_values` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Ateş efekti için önceden rastgele değerler üretir |
| `↪ LEDControllerAnimations._precompute_rainbow_cycles` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Gökkuşağı döngülerini önceden hesaplar |
| `↪ LEDControllerAnimations._run_animation` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Animasyon döngüsünü çalıştırır |
| `↪ LEDControllerAnimations._set_zone_multiple_colors` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Bir bölgedeki birden çok LED'i farklı renklerle ayarlar |
| `↪ LEDControllerAnimations._wheel` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Renk tekerleği - 0-255 arası bir pozisyon değerini RGB rengine dönüştürür |
| `↪ LEDControllerAnimations.animate` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Animasyon başlatır |
| `_animate_breathe` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Nefes alma animasyonu - Yumuşak geçişlerle parlama ve sönme |
| `_animate_breathe` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Nefes alma animasyonu - Yumuşak geçişli parlama/sönme |
| `_animate_chase` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Takip animasyonu - Renk noktası şeridi dolaşır |
| `_animate_color_fade` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Renkler arası geçiş animasyonu |
| `_animate_fade` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Solma animasyonu - Tam renkten siyaha doğru geçiş |
| `_animate_pulse` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Nabız animasyonu - Parlayıp sönme |
| `_animate_pulse` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Nabız animasyonu - Parlayıp sönme |
| `_animate_rainbow` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Gökkuşağı animasyonu - Renk spektrumu boyunca hareket |
| `_animate_rainbow` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Gökkuşağı animasyonu - Spektrum rengi geçişleri |
| `_animate_scan` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Tarama animasyonu - Işık soldan sağa, sonra sağdan sola hareket eder |
| `_animate_sparkle` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Pırıltı animasyonu - Rastgele LEDler yanıp söner |
| `_animate_static` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Sabit renk animasyonu |
| `_animate_theater_chase` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Tiyatro takip animasyonu - Sırayla yanıp sönen gruplar |
| `_animate_twinkle` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Yıldız parıltısı animasyonu - Rastgele LEDler yanıp söner, farklı parlaklık düzeylerinde |
| `_animate_wave` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Dalga animasyonu - sinüs dalgası şeklinde renk dalgalanması |
| `_animate_wipe` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Silme animasyonu - Renk bir uçtan diğerine doğru yayılır |
| `_precompute_fire_values` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Ateş efekti için önceden rastgele değerler üretir |
| `_precompute_rainbow_cycles` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Gökkuşağı döngülerini önceden hesaplar |
| `_run_animation` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Animasyon döngüsünü çalıştırır |
| `_set_zone_multiple_colors` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Bir bölgedeki birden çok LED'i farklı renklerle ayarlar |
| `_wheel` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Renk tekerleği - 0-255 arası bir pozisyon değerini RGB rengine dönüştürür |
| `animate` | src/modules/led_controller_animations.py | Belirtilmemiş | 2025-05-03 | Animasyon başlatır |
| `🔶 AnimationPattern` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | LED animasyon desenleri için enum |
| `🔶 LEDControllerBase` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | WS2812B LED şeritlerini kontrol eden temel sınıf |
| `↪ LEDControllerBase.__init__` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | LED kontrolcüsünü başlatır |
| `↪ LEDControllerBase._create_default_zones` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Varsayılan LED bölgelerini oluşturur |
| `↪ LEDControllerBase._save_simulation_image` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Simülasyon modunda LED durumunu bir görüntü dosyasına kaydeder |
| `↪ LEDControllerBase._set_pixel_color` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Bir LED'in rengini ayarlar |
| `↪ LEDControllerBase._set_zone_color` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Bir bölgenin rengini ayarlar |
| `↪ LEDControllerBase.clear` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Tüm LEDleri kapatır (siyah yapar) |
| `↪ LEDControllerBase.get_state` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | LED kontrolcünün mevcut durumunu döndürür |
| `↪ LEDControllerBase.register_theme_callback` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Tema değişikliği için callback kaydeder |
| `↪ LEDControllerBase.reset_activity_timer` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Aktivite zamanlayıcısını sıfırlar |
| `↪ LEDControllerBase.set_brightness` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | LED parlaklığını ayarlar |
| `↪ LEDControllerBase.set_color` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Belirli bir bölgenin rengini ayarlar |
| `↪ LEDControllerBase.start` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | LED kontrolcüsünü başlatır |
| `↪ LEDControllerBase.stop` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Animasyonu durdurur ve LEDleri kapatır |
| `🔶 LEDZone` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | LED şeritlerinin bölgesi için yardımcı sınıf |
| `↪ LEDZone.__init__` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | LED bölgesi oluşturur |
| `↪ LEDZone.__str__` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Belirtilmemiş |
| `__init__` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | LED bölgesi oluşturur |
| `__init__` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | LED kontrolcüsünü başlatır |
| `__str__` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Belirtilmemiş |
| `_create_default_zones` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Varsayılan LED bölgelerini oluşturur |
| `_save_simulation_image` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Simülasyon modunda LED durumunu bir görüntü dosyasına kaydeder |
| `_set_pixel_color` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Bir LED'in rengini ayarlar |
| `_set_zone_color` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Bir bölgenin rengini ayarlar |
| `clear` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Tüm LEDleri kapatır (siyah yapar) |
| `get_state` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | LED kontrolcünün mevcut durumunu döndürür |
| `register_theme_callback` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Tema değişikliği için callback kaydeder |
| `reset_activity_timer` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Aktivite zamanlayıcısını sıfırlar |
| `set_brightness` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | LED parlaklığını ayarlar |
| `set_color` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Belirli bir bölgenin rengini ayarlar |
| `start` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | LED kontrolcüsünü başlatır |
| `stop` | src/modules/led_controller_base.py | Belirtilmemiş | 2025-05-02 | Animasyonu durdurur ve LEDleri kapatır |
| `🔶 LEDControllerColors` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | LED renk işlemleri için karışım (mixin) sınıfı |
| `↪ LEDControllerColors.__init__` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | Renk modülünün başlatıcısı |
| `↪ LEDControllerColors._adjust_brightness` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | Rengin parlaklığını ayarlar |
| `↪ LEDControllerColors._complement_color` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | Rengin tamamlayıcısını (complementary) döndürür |
| `↪ LEDControllerColors._generate_harmony_colors` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | Temel bir renkten, seçilen harmoni tipine göre bir dizi uyumlu renk oluşturur |
| `↪ LEDControllerColors._rotate_hue` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | Rengin tonunu belirli bir derece döndürür |
| `↪ LEDControllerColors.get_color_for_emotion` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | Duygu durumuna göre renk döndürür |
| `↪ LEDControllerColors.on_theme_changed` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | Tema değiştiğinde çağrılan fonksiyon |
| `↪ LEDControllerColors.set_color_harmony` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | Renk harmonisi tipini ayarlar |
| `↪ LEDControllerColors.set_emotion_color` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | Duygu durumuna göre renk ayarlar |
| `__init__` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | Renk modülünün başlatıcısı |
| `_adjust_brightness` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | Rengin parlaklığını ayarlar |
| `_complement_color` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | Rengin tamamlayıcısını (complementary) döndürür |
| `_generate_harmony_colors` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | Temel bir renkten, seçilen harmoni tipine göre bir dizi uyumlu renk oluşturur |
| `_rotate_hue` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | Rengin tonunu belirli bir derece döndürür |
| `get_color_for_emotion` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | Duygu durumuna göre renk döndürür |
| `on_theme_changed` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | Tema değiştiğinde çağrılan fonksiyon |
| `set_color_harmony` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | Renk harmonisi tipini ayarlar |
| `set_emotion_color` | src/modules/led_controller_colors.py | Belirtilmemiş | 2025-05-02 | Duygu durumuna göre renk ayarlar |
| `🔶 LEDControllerPatterns` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | LED ışık desenleri için karışım (mixin) sınıfı |
| `↪ LEDControllerPatterns._enter_power_save_mode` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Enerji tasarrufu moduna girer |
| `↪ LEDControllerPatterns._run_alternate_pattern` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Dönüşümlü renk desenini çalıştırır |
| `↪ LEDControllerPatterns._run_chase_pattern` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Takip ışık desenini çalıştırır |
| `↪ LEDControllerPatterns._run_custom_pattern` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Özel bir deseni çalıştırır |
| `↪ LEDControllerPatterns._run_sequence_pattern` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Renk sırası desenini çalıştırır |
| `↪ LEDControllerPatterns.animate_emotion` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Duygu durumuna göre animasyon başlatır |
| `↪ LEDControllerPatterns.create_pattern` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Özel bir desen yapılandırması oluşturur |
| `↪ LEDControllerPatterns.run_pattern` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Bir deseni çalıştırır |
| `↪ LEDControllerPatterns.run_startup_animation` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Başlangıç animasyonunu çalıştırır |
| `↪ LEDControllerPatterns.start_power_save_timer` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Enerji tasarrufu zamanlayıcısını başlatır |
| `_enter_power_save_mode` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Enerji tasarrufu moduna girer |
| `_run_alternate_pattern` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Dönüşümlü renk desenini çalıştırır |
| `_run_chase_pattern` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Takip ışık desenini çalıştırır |
| `_run_custom_pattern` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Özel bir deseni çalıştırır |
| `_run_sequence_pattern` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Renk sırası desenini çalıştırır |
| `animate_emotion` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Duygu durumuna göre animasyon başlatır |
| `create_pattern` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Özel bir desen yapılandırması oluşturur |
| `run_pattern` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Bir deseni çalıştırır |
| `run_startup_animation` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Başlangıç animasyonunu çalıştırır |
| `start_power_save_timer` | src/modules/led_controller_patterns.py | Belirtilmemiş | 2025-05-02 | Enerji tasarrufu zamanlayıcısını başlatır |
| `🔶 OLEDController` | src/modules/oled_controller.py | Belirtilmemiş | 2025-04-30 | OLED ekranları kontrol eden ana sınıf |
| `↪ OLEDController.__init__` | src/modules/oled_controller.py | Belirtilmemiş | 2025-04-30 | OLED kontrolcü sınıfını başlatır |
| `↪ OLEDController._extended_animation_loop` | src/modules/oled_controller.py | Belirtilmemiş | 2025-04-30 | Genişletilmiş animasyon döngüsü (duygu geçişlerini destekler) |
| `__init__` | src/modules/oled_controller.py | Belirtilmemiş | 2025-04-30 | OLED kontrolcü sınıfını başlatır |
| `_extended_animation_loop` | src/modules/oled_controller.py | Belirtilmemiş | 2025-04-30 | Genişletilmiş animasyon döngüsü (duygu geçişlerini destekler) |
| `🔶 OLEDAnimationsMixin` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | OLED ekranlar için animasyon ve duygu geçiş işlevlerini içeren mixin sınıfı. |
| `↪ OLEDAnimationsMixin._get_optimized_reaction_plan` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Çevresel tepki türüne göre optimize edilmiş tepki planı döndürür |
| `↪ OLEDAnimationsMixin.animate_blink` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Göz kırpma animasyonu başlatır |
| `↪ OLEDAnimationsMixin.blend_emotions` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | İki duygu arasında yumuşak geçiş sağlar. |
| `↪ OLEDAnimationsMixin.enable_random_eye_movement` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Rastgele göz hareketlerini etkinleştirir veya devre dışı bırakır |
| `↪ OLEDAnimationsMixin.look_at` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Göz bebeklerinin belirli bir noktaya bakmasını sağlar |
| `↪ OLEDAnimationsMixin.react_to_environmental_factors` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Çevresel faktörlere göre ifadeyi ayarlar. |
| `↪ OLEDAnimationsMixin.set_emotion` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Ekranları belirtilen duygu durumuna göre günceller |
| `↪ OLEDAnimationsMixin.show_environmental_reaction` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Çevresel faktörlere göre tepki gösterir |
| `↪ OLEDAnimationsMixin.show_micro_expression` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Kısa süreli mikro ifade gösterir |
| `↪ OLEDAnimationsMixin.start_emotion_transition` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Bir duygu durumundan diğerine yumuşak geçiş başlatır |
| `↪ OLEDAnimationsMixin.update_emotion_transition` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Duygu geçiş durumunu günceller |
| `_get_optimized_reaction_plan` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Çevresel tepki türüne göre optimize edilmiş tepki planı döndürür |
| `animate_blink` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Göz kırpma animasyonu başlatır |
| `blend_emotions` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | İki duygu arasında yumuşak geçiş sağlar. |
| `enable_random_eye_movement` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Rastgele göz hareketlerini etkinleştirir veya devre dışı bırakır |
| `look_at` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Göz bebeklerinin belirli bir noktaya bakmasını sağlar |
| `react_to_environmental_factors` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Çevresel faktörlere göre ifadeyi ayarlar. |
| `set_emotion` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Ekranları belirtilen duygu durumuna göre günceller |
| `show_environmental_reaction` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Çevresel faktörlere göre tepki gösterir |
| `show_micro_expression` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Kısa süreli mikro ifade gösterir |
| `start_emotion_transition` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Bir duygu durumundan diğerine yumuşak geçiş başlatır |
| `update_emotion_transition` | src/modules/oled_controller_animations.py | Belirtilmemiş | 2025-05-03 | Duygu geçiş durumunu günceller |
| `🔶 OLEDController` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | OLED ekranları kontrol eden temel sınıf |
| `↪ OLEDController.__init__` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | OLED kontrolcü sınıfını başlatır |
| `↪ OLEDController._animation_loop` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Ana animasyon döngüsü |
| `↪ OLEDController._check_environmental_factors` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Çevresel faktörleri kontrol eder ve günceller |
| `↪ OLEDController._check_power_saving_mode` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Güç tasarrufu modunu kontrol eder ve günceller |
| `↪ OLEDController._get_random_blink_interval` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Rastgele göz kırpma aralığı oluşturur |
| `↪ OLEDController._init_displays` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | OLED ekranları başlatır |
| `↪ OLEDController._init_sensors` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Çevresel sensörleri başlatır |
| `↪ OLEDController._load_fonts` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Kullanılacak fontları yükler |
| `↪ OLEDController._update_blink_state` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Göz kırpma durumunu günceller |
| `↪ OLEDController._update_eye_position` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Göz pozisyonunu günceller (göz bebeklerinin hareketi için) |
| `↪ OLEDController._update_micro_expression` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Mikro ifadeyi günceller |
| `↪ OLEDController.clear_displays` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Tüm ekranları temizler |
| `↪ OLEDController.reset_activity_timer` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Aktivite zamanlayıcısını sıfırlar (güç tasarrufu modu için) |
| `↪ OLEDController.set_brightness` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | OLED ekranların parlaklığını ayarlar |
| `↪ OLEDController.set_power_mode` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | OLED ekranların güç modunu ayarlar |
| `↪ OLEDController.start` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | OLED ekranları başlatır ve animasyon döngüsünü çalıştırır |
| `↪ OLEDController.stop` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Animasyon döngüsünü durdurur ve ekranları temizler |
| `↪ OLEDController.update_display` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Tüm ekranları günceller (tamponları ekranlara gönderir) |
| `🔶 SimulatedDisplay` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | SSD1306 ekranı simüle eden sınıf |
| `↪ SimulatedDisplay.__init__` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Belirtilmemiş |
| `↪ SimulatedDisplay.contrast` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Kontrast ayarı (0-255) |
| `↪ SimulatedDisplay.fill` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Ekranı belirtilen renkle doldurur |
| `↪ SimulatedDisplay.image` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Görüntüyü tampona yükler |
| `↪ SimulatedDisplay.poweroff` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Ekranı kapatır |
| `↪ SimulatedDisplay.poweron` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Ekranı açar |
| `↪ SimulatedDisplay.save_frame` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Güncel ekran görüntüsünü kaydeder |
| `↪ SimulatedDisplay.show` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Tamponu ekrana çizer (simüle edilen) |
| `__init__` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Belirtilmemiş |
| `__init__` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | OLED kontrolcü sınıfını başlatır |
| `_animation_loop` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Ana animasyon döngüsü |
| `_check_environmental_factors` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Çevresel faktörleri kontrol eder ve günceller |
| `_check_power_saving_mode` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Güç tasarrufu modunu kontrol eder ve günceller |
| `_get_random_blink_interval` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Rastgele göz kırpma aralığı oluşturur |
| `_init_displays` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | OLED ekranları başlatır |
| `_init_sensors` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Çevresel sensörleri başlatır |
| `_load_fonts` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Kullanılacak fontları yükler |
| `_update_blink_state` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Göz kırpma durumunu günceller |
| `_update_eye_position` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Göz pozisyonunu günceller (göz bebeklerinin hareketi için) |
| `_update_micro_expression` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Mikro ifadeyi günceller |
| `clear_displays` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Tüm ekranları temizler |
| `contrast` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Kontrast ayarı (0-255) |
| `fill` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Ekranı belirtilen renkle doldurur |
| `image` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Görüntüyü tampona yükler |
| `poweroff` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Ekranı kapatır |
| `poweron` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Ekranı açar |
| `reset_activity_timer` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Aktivite zamanlayıcısını sıfırlar (güç tasarrufu modu için) |
| `save_frame` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Güncel ekran görüntüsünü kaydeder |
| `set_brightness` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | OLED ekranların parlaklığını ayarlar |
| `set_power_mode` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | OLED ekranların güç modunu ayarlar |
| `show` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Tamponu ekrana çizer (simüle edilen) |
| `start` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | OLED ekranları başlatır ve animasyon döngüsünü çalıştırır |
| `stop` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Animasyon döngüsünü durdurur ve ekranları temizler |
| `update_display` | src/modules/oled_controller_base.py | Belirtilmemiş | 2025-05-05 | Tüm ekranları günceller (tamponları ekranlara gönderir) |
| `🔶 OLEDDisplayMixin` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | OLED ekranlar için çizim işlevlerini içeren mixin sınıfı. |
| `↪ OLEDDisplayMixin._draw_all_displays` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Tüm ekranlara mevcut duygu durumuna göre çizim yapar |
| `↪ OLEDDisplayMixin._draw_startup_eye_animation` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Göz için başlangıç animasyonu çizer |
| `↪ OLEDDisplayMixin._draw_startup_mouth_animation` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Ağız için başlangıç animasyonu çizer |
| `↪ OLEDDisplayMixin.animate_mouth_speaking` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Konuşma animasyonuyla ağzın hareket etmesini sağlar |
| `↪ OLEDDisplayMixin.blink` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Göz kırpma animasyonu gösterir |
| `↪ OLEDDisplayMixin.clear_eyes` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Göz ekranlarını temizler |
| `↪ OLEDDisplayMixin.clear_mouth` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Ağız ekranını temizler |
| `↪ OLEDDisplayMixin.draw_eyes` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Göz ekranlarına çizim yapar |
| `↪ OLEDDisplayMixin.draw_mouth` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Ağız ekranına çizim yapar |
| `↪ OLEDDisplayMixin.show_eyes_growing_circle` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Gözlerde büyüyen çember animasyonu gösterir |
| `↪ OLEDDisplayMixin.show_mouth_expression` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Belirli bir duyguya göre ağız ifadesi gösterir |
| `↪ OLEDDisplayMixin.show_startup_animation` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Başlangıç animasyonunu gösterir |
| `_draw_all_displays` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Tüm ekranlara mevcut duygu durumuna göre çizim yapar |
| `_draw_startup_eye_animation` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Göz için başlangıç animasyonu çizer |
| `_draw_startup_mouth_animation` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Ağız için başlangıç animasyonu çizer |
| `animate_mouth_speaking` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Konuşma animasyonuyla ağzın hareket etmesini sağlar |
| `blink` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Göz kırpma animasyonu gösterir |
| `clear_eyes` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Göz ekranlarını temizler |
| `clear_mouth` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Ağız ekranını temizler |
| `draw_eyes` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Göz ekranlarına çizim yapar |
| `draw_mouth` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Ağız ekranına çizim yapar |
| `show_eyes_growing_circle` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Gözlerde büyüyen çember animasyonu gösterir |
| `show_mouth_expression` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Belirli bir duyguya göre ağız ifadesi gösterir |
| `show_startup_animation` | src/modules/oled_controller_display.py | Belirtilmemiş | 2025-05-04 | Başlangıç animasyonunu gösterir |
| `🔶 MockController` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `↪ MockController.get_brightness` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `↪ MockController.get_fps` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `↪ MockController.set_brightness` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `↪ MockController.set_fps` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `🔶 PerformanceOptimizer` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | FACE1 için performans optimizasyon modülü |
| `↪ PerformanceOptimizer.__init__` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | PerformanceOptimizer sınıfını başlatır |
| `↪ PerformanceOptimizer._adjust_performance` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Performansı sistem yüküne göre ayarlar |
| `↪ PerformanceOptimizer._check_battery_available` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Sistemde pil olup olmadığını kontrol eder |
| `↪ PerformanceOptimizer._check_battery_status` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Pil seviyesini kontrol eder ve düşük pil durumunda önlem alır |
| `↪ PerformanceOptimizer._get_battery_level` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Pil seviyesini döndürür |
| `↪ PerformanceOptimizer._get_cpu_temperature` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | CPU sıcaklığını döndürür |
| `↪ PerformanceOptimizer._get_performance_tier` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | CPU kullanım oranına göre uygun performans kademesini döndürür |
| `↪ PerformanceOptimizer._monitor_loop` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Sistem kaynaklarını izleme döngüsü |
| `↪ PerformanceOptimizer._update_system_metrics` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Sistem metriklerini günceller (CPU, bellek, sıcaklık, pil) |
| `↪ PerformanceOptimizer.get_status` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Mevcut performans durumu bilgilerini döndürür |
| `↪ PerformanceOptimizer.set_controllers` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Controller referanslarını ayarlar |
| `↪ PerformanceOptimizer.start` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Performans optimize ediciyi başlatır |
| `↪ PerformanceOptimizer.stop` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Performans optimize ediciyi durdurur |
| `↪ PerformanceOptimizer.update_config` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Yapılandırmayı günceller |
| `__init__` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | PerformanceOptimizer sınıfını başlatır |
| `_adjust_performance` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Performansı sistem yüküne göre ayarlar |
| `_check_battery_available` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Sistemde pil olup olmadığını kontrol eder |
| `_check_battery_status` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Pil seviyesini kontrol eder ve düşük pil durumunda önlem alır |
| `_get_battery_level` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Pil seviyesini döndürür |
| `_get_cpu_temperature` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | CPU sıcaklığını döndürür |
| `_get_performance_tier` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | CPU kullanım oranına göre uygun performans kademesini döndürür |
| `_monitor_loop` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Sistem kaynaklarını izleme döngüsü |
| `_update_system_metrics` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Sistem metriklerini günceller (CPU, bellek, sıcaklık, pil) |
| `get_brightness` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `get_fps` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `get_status` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Mevcut performans durumu bilgilerini döndürür |
| `set_brightness` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `set_controllers` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Controller referanslarını ayarlar |
| `set_fps` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `start` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Performans optimize ediciyi başlatır |
| `stop` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Performans optimize ediciyi durdurur |
| `update_config` | src/modules/performance_optimizer.py | Belirtilmemiş | 2025-05-04 | Yapılandırmayı günceller |
| `🔶 SoundProcessor` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | FACE1 için ses işleme modülü |
| `↪ SoundProcessor.__init__` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Ses işleme modülünü başlatır |
| `↪ SoundProcessor._analyze_emotion` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Ses özelliklerine göre basit bir duygu analizi yapar |
| `↪ SoundProcessor._call_callbacks` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Tüm geri çağırma işlevlerini çağırır |
| `↪ SoundProcessor._call_volume_callbacks` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Ses seviyesi geri çağırma işlevlerini çağırır |
| `↪ SoundProcessor._process_audio_data` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Ham ses verilerini işler |
| `↪ SoundProcessor._processing_loop` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Ses verilerini sürekli işleyen ana döngü |
| `↪ SoundProcessor._simulation_loop` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Simülasyon modunda ses verilerini taklit eden döngü |
| `↪ SoundProcessor._update_measurements` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Ses ölçümlerini günceller ve konuşma algılama durumunu değiştirir |
| `↪ SoundProcessor.get_current_volume` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Mevcut ses seviyesini döndürür |
| `↪ SoundProcessor.get_frequency_distribution` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Mevcut frekans dağılımını döndürür |
| `↪ SoundProcessor.is_speaking` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Konuşma algılanıp algılanmadığını döndürür |
| `↪ SoundProcessor.register_emotion_callback` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Duygu değişikliği önerildiğinde çağrılacak geri çağırma işlevini kaydeder |
| `↪ SoundProcessor.register_speaking_callback` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Konuşma durumu değiştiğinde çağrılacak geri çağırma işlevini kaydeder |
| `↪ SoundProcessor.register_volume_callback` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Ses seviyesi değiştiğinde çağrılacak geri çağırma işlevini kaydeder |
| `↪ SoundProcessor.start` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Ses işleme modülünü başlatır |
| `↪ SoundProcessor.stop` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Ses işleme modülünü durdurur |
| `↪ SoundProcessor.update_config` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Yapılandırmayı günceller |
| `__init__` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Ses işleme modülünü başlatır |
| `_analyze_emotion` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Ses özelliklerine göre basit bir duygu analizi yapar |
| `_call_callbacks` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Tüm geri çağırma işlevlerini çağırır |
| `_call_volume_callbacks` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Ses seviyesi geri çağırma işlevlerini çağırır |
| `_process_audio_data` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Ham ses verilerini işler |
| `_processing_loop` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Ses verilerini sürekli işleyen ana döngü |
| `_simulation_loop` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Simülasyon modunda ses verilerini taklit eden döngü |
| `_update_measurements` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Ses ölçümlerini günceller ve konuşma algılama durumunu değiştirir |
| `get_current_volume` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Mevcut ses seviyesini döndürür |
| `get_frequency_distribution` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Mevcut frekans dağılımını döndürür |
| `is_speaking` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Konuşma algılanıp algılanmadığını döndürür |
| `print_emotion` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `print_speaking` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `print_volume` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `random_noise` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | 0 ile 1 arasında rastgele gürültü üretir (simülasyon için) |
| `register_emotion_callback` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Duygu değişikliği önerildiğinde çağrılacak geri çağırma işlevini kaydeder |
| `register_speaking_callback` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Konuşma durumu değiştiğinde çağrılacak geri çağırma işlevini kaydeder |
| `register_volume_callback` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Ses seviyesi değiştiğinde çağrılacak geri çağırma işlevini kaydeder |
| `start` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Ses işleme modülünü başlatır |
| `stop` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Ses işleme modülünü durdurur |
| `update_config` | src/modules/sound_processor.py | Belirtilmemiş | 2025-05-04 | Yapılandırmayı günceller |
| `🔶 StateHistoryManager` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | FACE1 durum tarihçesi yönetim sınıfı. |
| `↪ StateHistoryManager.__init__` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | StateHistoryManager sınıfını başlatır |
| `↪ StateHistoryManager._load_history` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Depodan tarihçe verilerini yükler |
| `↪ StateHistoryManager._save_entry_to_storage` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Bir girişi depoya kaydeder |
| `↪ StateHistoryManager._update_stats` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Belirli bir giriş tipi için istatistikleri günceller |
| `↪ StateHistoryManager.add_entry` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Tarihçeye yeni bir giriş ekler |
| `↪ StateHistoryManager.clear_history` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Tüm tarihçeyi temizler |
| `↪ StateHistoryManager.get_entries_by_type` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Belirli bir türdeki tarihçe girişlerini döndürür |
| `↪ StateHistoryManager.get_events_since` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Belirli bir zamandan sonraki tüm girişleri döndürür |
| `↪ StateHistoryManager.get_frequency` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Belirli bir zaman diliminde belirli tipte kaç giriş olduğunu hesaplar |
| `↪ StateHistoryManager.get_history` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Tarihçe girişlerini döndürür |
| `↪ StateHistoryManager.get_last_entry` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Son tarihçe girişini döndürür |
| `↪ StateHistoryManager.get_stats` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Tarihçe istatistiklerini döndürür |
| `↪ StateHistoryManager.set_storage_path` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Tarihçe depolama yolunu değiştirir |
| `__init__` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | StateHistoryManager sınıfını başlatır |
| `_load_history` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Depodan tarihçe verilerini yükler |
| `_save_entry_to_storage` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Bir girişi depoya kaydeder |
| `_update_stats` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Belirli bir giriş tipi için istatistikleri günceller |
| `add_entry` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Tarihçeye yeni bir giriş ekler |
| `clear_history` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Tüm tarihçeyi temizler |
| `get_entries_by_type` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Belirli bir türdeki tarihçe girişlerini döndürür |
| `get_events_since` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Belirli bir zamandan sonraki tüm girişleri döndürür |
| `get_frequency` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Belirli bir zaman diliminde belirli tipte kaç giriş olduğunu hesaplar |
| `get_history` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Tarihçe girişlerini döndürür |
| `get_last_entry` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Son tarihçe girişini döndürür |
| `get_stats` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Tarihçe istatistiklerini döndürür |
| `set_storage_path` | src/modules/state_history_manager.py | Belirtilmemiş | 2025-05-05 | Tarihçe depolama yolunu değiştirir |
| `🔶 ThemeAssetsMixin` | src/modules/theme/theme_manager_assets.py | Belirtilmemiş | 2025-05-02 | Tema varlıkları (assets) yönetimi için mixin sınıfı |
| `↪ ThemeAssetsMixin._clear_asset_cache` | src/modules/theme/theme_manager_assets.py | Belirtilmemiş | 2025-05-02 | Tema varlıkları önbelleğini temizler |
| `↪ ThemeAssetsMixin._copy_theme_assets` | src/modules/theme/theme_manager_assets.py | Belirtilmemiş | 2025-05-02 | Tema varlıklarını bir dizinden diğerine kopyalar |
| `↪ ThemeAssetsMixin.get_emotion_assets` | src/modules/theme/theme_manager_assets.py | Belirtilmemiş | 2025-05-02 | Belirli bir duygu için tema varlıklarını döndürür |
| `↪ ThemeAssetsMixin.get_emotion_subtype_assets` | src/modules/theme/theme_manager_assets.py | Belirtilmemiş | 2025-05-02 | Duygu alt tipi için tema varlıklarını döndürür |
| `↪ ThemeAssetsMixin.get_theme_preview` | src/modules/theme/theme_manager_assets.py | Belirtilmemiş | 2025-05-02 | Tema önizleme verileri oluşturur |
| `_clear_asset_cache` | src/modules/theme/theme_manager_assets.py | Belirtilmemiş | 2025-05-02 | Tema varlıkları önbelleğini temizler |
| `_copy_theme_assets` | src/modules/theme/theme_manager_assets.py | Belirtilmemiş | 2025-05-02 | Tema varlıklarını bir dizinden diğerine kopyalar |
| `get_emotion_assets` | src/modules/theme/theme_manager_assets.py | Belirtilmemiş | 2025-05-02 | Belirli bir duygu için tema varlıklarını döndürür |
| `get_emotion_subtype_assets` | src/modules/theme/theme_manager_assets.py | Belirtilmemiş | 2025-05-02 | Duygu alt tipi için tema varlıklarını döndürür |
| `get_theme_preview` | src/modules/theme/theme_manager_assets.py | Belirtilmemiş | 2025-05-02 | Tema önizleme verileri oluşturur |
| `🔶 BaseThemeManager` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Tema yöneticisi temel sınıfı |
| `↪ BaseThemeManager.__init__` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Tema yöneticisi temel sınıfını başlatır |
| `↪ BaseThemeManager._deep_merge_dict` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | İki sözlüğü derin birleştirir, iç içe yapıları korur |
| `↪ BaseThemeManager.get_current_theme` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Mevcut tema adını döndürür |
| `↪ BaseThemeManager.get_theme_list` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Mevcut temaların listesini döndürür |
| `↪ BaseThemeManager.load_theme` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Bir temayı yükler |
| `↪ BaseThemeManager.register_change_callback` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Tema değişikliği için geri çağrı fonksiyonu kaydeder |
| `↪ BaseThemeManager.set_theme` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Temayı değiştirir |
| `↪ BaseThemeManager.start` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Tema yöneticisini başlatır |
| `↪ BaseThemeManager.stop` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Tema yöneticisini durdurur |
| `↪ BaseThemeManager.unregister_change_callback` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Tema değişikliği için geri çağrı fonksiyonu kaydını siler |
| `__init__` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Tema yöneticisi temel sınıfını başlatır |
| `_deep_merge_dict` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | İki sözlüğü derin birleştirir, iç içe yapıları korur |
| `get_current_theme` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Mevcut tema adını döndürür |
| `get_theme_list` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Mevcut temaların listesini döndürür |
| `load_theme` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Bir temayı yükler |
| `register_change_callback` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Tema değişikliği için geri çağrı fonksiyonu kaydeder |
| `set_theme` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Temayı değiştirir |
| `start` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Tema yöneticisini başlatır |
| `stop` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Tema yöneticisini durdurur |
| `unregister_change_callback` | src/modules/theme/theme_manager_base.py | Belirtilmemiş | 2025-05-02 | Tema değişikliği için geri çağrı fonksiyonu kaydını siler |
| `🔶 ThemeCacheMixin` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Tema önbellek yönetimi için mixin sınıfı. |
| `↪ ThemeCacheMixin._cache_cleanup_thread` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Önbellek temizleme iş parçacığı |
| `↪ ThemeCacheMixin._cache_subtype_assets` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Alt tip varlıklarını önbelleğe alır |
| `↪ ThemeCacheMixin._cache_theme_preview` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Tema önizleme verilerini önbelleğe alır |
| `↪ ThemeCacheMixin._cleanup_expired_cache` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Süresi dolmuş önbellek öğelerini temizler |
| `↪ ThemeCacheMixin._deep_merge_dict` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | İki sözlüğü derin birleştirir, iç içe yapıları korur |
| `↪ ThemeCacheMixin._get_cached_subtype_assets` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Önbelleğe alınmış alt tip varlıklarını döndürür |
| `↪ ThemeCacheMixin._get_cached_theme_preview` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Önbelleğe alınmış tema önizleme verilerini döndürür |
| `↪ ThemeCacheMixin._load_theme_file` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Tema dosyasını disk üzerinden yükler |
| `↪ ThemeCacheMixin._save_theme_file` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Tema verilerini dosyaya kaydeder |
| `↪ ThemeCacheMixin._start_cache_cleanup_timer` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Önbellek temizleme zamanlayıcısını başlatır |
| `↪ ThemeCacheMixin._update_cache_access` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Tema erişim zamanını günceller (LRU için) |
| `↪ ThemeCacheMixin._update_theme_cache` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Tema önbelleğini günceller |
| `↪ ThemeCacheMixin.clear_cache` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Tüm önbellek verilerini temizler |
| `_cache_cleanup_thread` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Önbellek temizleme iş parçacığı |
| `_cache_subtype_assets` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Alt tip varlıklarını önbelleğe alır |
| `_cache_theme_preview` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Tema önizleme verilerini önbelleğe alır |
| `_cleanup_expired_cache` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Süresi dolmuş önbellek öğelerini temizler |
| `_deep_merge_dict` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | İki sözlüğü derin birleştirir, iç içe yapıları korur |
| `_get_cached_subtype_assets` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Önbelleğe alınmış alt tip varlıklarını döndürür |
| `_get_cached_theme_preview` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Önbelleğe alınmış tema önizleme verilerini döndürür |
| `_load_theme_file` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Tema dosyasını disk üzerinden yükler |
| `_save_theme_file` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Tema verilerini dosyaya kaydeder |
| `_start_cache_cleanup_timer` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Önbellek temizleme zamanlayıcısını başlatır |
| `_update_cache_access` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Tema erişim zamanını günceller (LRU için) |
| `_update_theme_cache` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Tema önbelleğini günceller |
| `clear_cache` | src/modules/theme/theme_manager_cache.py | Belirtilmemiş | 2025-05-02 | Tüm önbellek verilerini temizler |
| `🔶 ThemeOperationsMixin` | src/modules/theme/theme_manager_operations.py | Belirtilmemiş | 2025-05-02 | Tema işlemleri için mixin sınıfı. |
| `↪ ThemeOperationsMixin._copy_theme_assets` | src/modules/theme/theme_manager_operations.py | Belirtilmemiş | 2025-05-02 | Tema varlıklarını bir dizinden diğerine kopyalar |
| `↪ ThemeOperationsMixin._is_valid_theme_name` | src/modules/theme/theme_manager_operations.py | Belirtilmemiş | 2025-05-02 | Tema adının geçerli olup olmadığını kontrol eder |
| `↪ ThemeOperationsMixin.copy_theme` | src/modules/theme/theme_manager_operations.py | Belirtilmemiş | 2025-05-02 | Bir temayı başka bir isimle kopyalar |
| `↪ ThemeOperationsMixin.create_theme` | src/modules/theme/theme_manager_operations.py | Belirtilmemiş | 2025-05-02 | Yeni bir tema oluşturur |
| `↪ ThemeOperationsMixin.delete_theme` | src/modules/theme/theme_manager_operations.py | Belirtilmemiş | 2025-05-02 | Bir temayı siler |
| `↪ ThemeOperationsMixin.edit_theme` | src/modules/theme/theme_manager_operations.py | Belirtilmemiş | 2025-05-02 | Mevcut bir temayı düzenler |
| `↪ ThemeOperationsMixin.get_theme_details` | src/modules/theme/theme_manager_operations.py | Belirtilmemiş | 2025-05-02 | Bir tema hakkında detaylı bilgi döndürür |
| `↪ ThemeOperationsMixin.get_theme_preview` | src/modules/theme/theme_manager_operations.py | Belirtilmemiş | 2025-05-02 | Tema önizleme verileri oluşturur |
| `_copy_theme_assets` | src/modules/theme/theme_manager_operations.py | Belirtilmemiş | 2025-05-02 | Tema varlıklarını bir dizinden diğerine kopyalar |
| `_is_valid_theme_name` | src/modules/theme/theme_manager_operations.py | Belirtilmemiş | 2025-05-02 | Tema adının geçerli olup olmadığını kontrol eder |
| `copy_theme` | src/modules/theme/theme_manager_operations.py | Belirtilmemiş | 2025-05-02 | Bir temayı başka bir isimle kopyalar |
| `create_theme` | src/modules/theme/theme_manager_operations.py | Belirtilmemiş | 2025-05-02 | Yeni bir tema oluşturur |
| `delete_theme` | src/modules/theme/theme_manager_operations.py | Belirtilmemiş | 2025-05-02 | Bir temayı siler |
| `edit_theme` | src/modules/theme/theme_manager_operations.py | Belirtilmemiş | 2025-05-02 | Mevcut bir temayı düzenler |
| `get_theme_details` | src/modules/theme/theme_manager_operations.py | Belirtilmemiş | 2025-05-02 | Bir tema hakkında detaylı bilgi döndürür |
| `get_theme_preview` | src/modules/theme/theme_manager_operations.py | Belirtilmemiş | 2025-05-02 | Tema önizleme verileri oluşturur |
| `🔶 ThemeTemplatesMixin` | src/modules/theme/theme_manager_templates.py | Belirtilmemiş | 2025-05-02 | Tema şablonları için mixin sınıfı. |
| `↪ ThemeTemplatesMixin._create_default_theme_file` | src/modules/theme/theme_manager_templates.py | Belirtilmemiş | 2025-05-02 | Varsayılan tema tanımlama dosyasını oluşturur |
| `↪ ThemeTemplatesMixin._create_minimal_theme_file` | src/modules/theme/theme_manager_templates.py | Belirtilmemiş | 2025-05-02 | Minimal tema tanımlama dosyasını oluşturur |
| `↪ ThemeTemplatesMixin._create_pixel_theme_file` | src/modules/theme/theme_manager_templates.py | Belirtilmemiş | 2025-05-02 | Pixel tema dosyası oluşturur |
| `↪ ThemeTemplatesMixin._create_realistic_theme_file` | src/modules/theme/theme_manager_templates.py | Belirtilmemiş | 2025-05-02 | Gerçekçi tema dosyasını oluşturur |
| `_create_default_theme_file` | src/modules/theme/theme_manager_templates.py | Belirtilmemiş | 2025-05-02 | Varsayılan tema tanımlama dosyasını oluşturur |
| `_create_minimal_theme_file` | src/modules/theme/theme_manager_templates.py | Belirtilmemiş | 2025-05-02 | Minimal tema tanımlama dosyasını oluşturur |
| `_create_pixel_theme_file` | src/modules/theme/theme_manager_templates.py | Belirtilmemiş | 2025-05-02 | Pixel tema dosyası oluşturur |
| `_create_realistic_theme_file` | src/modules/theme/theme_manager_templates.py | Belirtilmemiş | 2025-05-02 | Gerçekçi tema dosyasını oluşturur |
| `🔶 ThemeManager` | src/modules/theme_manager.py | Belirtilmemiş | 2025-05-02 | Tema yöneticisi kompozit sınıfı |
| `🔶 ConfigStandardizer` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Plugin Yapılandırma Standardizasyonu |
| `↪ ConfigStandardizer.__init__` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Yapılandırma standardizasyonu başlatır |
| `↪ ConfigStandardizer._add_to_history` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Yapılandırmayı geçmiş bilgisine ekler |
| `↪ ConfigStandardizer._create_backup` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Mevcut yapılandırmanın yedeğini oluşturur |
| `↪ ConfigStandardizer._get_default_config` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Varsayılan yapılandırmayı döndürür |
| `↪ ConfigStandardizer._get_nested_value` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | İç içe sözlükten değer alır |
| `↪ ConfigStandardizer._load_config` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Yapılandırma dosyasını yükler |
| `↪ ConfigStandardizer._merge_with_defaults` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Yapılandırmayı varsayılanlar ile birleştirir |
| `↪ ConfigStandardizer._normalize_values` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Yapılandırma değerlerini normalleştirir |
| `↪ ConfigStandardizer._set_nested_value` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | İç içe sözlükte değer ayarlar |
| `↪ ConfigStandardizer._validate_schema` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Yapılandırmanın şema uygunluğunu doğrular |
| `↪ ConfigStandardizer.export_to_parent_format` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | FACE1 yapılandırmasını üst proje formatına dönüştürür |
| `↪ ConfigStandardizer.migrate_from_parent_config` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Üst projenin yapılandırmasından FACE1'e uygun yapılandırma oluşturur |
| `↪ ConfigStandardizer.restore_backup` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Yedekten yapılandırmayı geri yükler |
| `↪ ConfigStandardizer.save_config` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Yapılandırmayı kaydeder |
| `↪ ConfigStandardizer.standardize` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Yapılandırmayı standardize eder ve şema uygunluğunu doğrular |
| `__init__` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Yapılandırma standardizasyonu başlatır |
| `_add_to_history` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Yapılandırmayı geçmiş bilgisine ekler |
| `_create_backup` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Mevcut yapılandırmanın yedeğini oluşturur |
| `_get_default_config` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Varsayılan yapılandırmayı döndürür |
| `_get_nested_value` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | İç içe sözlükten değer alır |
| `_load_config` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Yapılandırma dosyasını yükler |
| `_merge_with_defaults` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Yapılandırmayı varsayılanlar ile birleştirir |
| `_normalize_values` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Yapılandırma değerlerini normalleştirir |
| `_set_nested_value` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | İç içe sözlükte değer ayarlar |
| `_validate_schema` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Yapılandırmanın şema uygunluğunu doğrular |
| `deep_merge` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `export_to_parent_format` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | FACE1 yapılandırmasını üst proje formatına dönüştürür |
| `migrate_from_parent_config` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Üst projenin yapılandırmasından FACE1'e uygun yapılandırma oluşturur |
| `normalize` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `restore_backup` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Yedekten yapılandırmayı geri yükler |
| `save_config` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Yapılandırmayı kaydeder |
| `standardize` | src/plugins/config_standardizer.py | Belirtilmemiş | 2025-05-04 | Yapılandırmayı standardize eder ve şema uygunluğunu doğrular |
| `🔶 PluginIsolation` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | Plugin İzolasyon Katmanı |
| `↪ PluginIsolation.__init__` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | Plugin izolasyon katmanını başlatır |
| `↪ PluginIsolation._get_cpu_usage` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | Mevcut CPU kullanımını ölçer |
| `↪ PluginIsolation._get_memory_usage` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | Mevcut bellek kullanımını ölçer |
| `↪ PluginIsolation._monitoring_loop` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | Kaynak kullanımını izleyen döngü |
| `↪ PluginIsolation._set_resource_limits` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | İşlem için kaynak sınırlarını ayarlar |
| `↪ PluginIsolation.get_metrics` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | İzolasyon katmanı metriklerini döndürür |
| `↪ PluginIsolation.start` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | İzolasyon katmanını başlatır |
| `↪ PluginIsolation.stop` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | İzolasyon katmanını durdurur |
| `↪ PluginIsolation.wrap_call` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | İşlev çağrısını izole edip hata yönetimi sağlar |
| `__init__` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | Plugin izolasyon katmanını başlatır |
| `_get_cpu_usage` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | Mevcut CPU kullanımını ölçer |
| `_get_memory_usage` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | Mevcut bellek kullanımını ölçer |
| `_monitoring_loop` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | Kaynak kullanımını izleyen döngü |
| `_set_resource_limits` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | İşlem için kaynak sınırlarını ayarlar |
| `error_func` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `get_metrics` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | İzolasyon katmanı metriklerini döndürür |
| `start` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | İzolasyon katmanını başlatır |
| `stop` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | İzolasyon katmanını durdurur |
| `test_func` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | Belirtilmemiş |
| `wrap_call` | src/plugins/plugin_isolation.py | Belirtilmemiş | 2025-05-04 | İşlev çağrısını izole edip hata yönetimi sağlar |
| `handle_test_command` | test_drivers.py | Belirtilmemiş | 2025-04-28 | Belirtilmemiş |
| `main` | test_drivers.py | Belirtilmemiş | 2025-04-28 | Ana fonksiyon |
| `on_test_event` | test_drivers.py | Belirtilmemiş | 2025-04-28 | Belirtilmemiş |
| `test_dashboard_server` | test_drivers.py | Belirtilmemiş | 2025-04-28 | Dashboard sunucusu testi |
| `test_i2c_scan` | test_drivers.py | Belirtilmemiş | 2025-04-28 | I2C tarama testi |
| `test_io_manager` | test_drivers.py | Belirtilmemiş | 2025-04-28 | I/O yöneticisi testi |
| `test_led_controller` | test_drivers.py | Belirtilmemiş | 2025-04-28 | LED kontrolcü testi |
| `test_oled_controller` | test_drivers.py | Belirtilmemiş | 2025-04-28 | OLED kontrolcü testi |
| `test_platform_info` | test_drivers.py | Belirtilmemiş | 2025-04-28 | Platform bilgileri testi |
| `test_theme_manager` | test_drivers.py | Belirtilmemiş | 2025-04-28 | Tema yöneticisi testi |
