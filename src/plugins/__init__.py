#!/usr/bin/env python3
"""
===========================================================
# Proje: FACE1 - Raspberry Pi 5 Robot AI için Yüz Eklentisi
# Dosya: __init__.py (plugins paketi)
# Açıklama: Plugin sistemi ve üst proje entegrasyon araçlarını içe aktarır
# Bağımlılıklar: -
# Bağlı Dosyalar: 
#   - src/plugins/plugin_isolation.py
#   - src/plugins/config_standardizer.py

# Versiyon: 0.4.3
# Değişiklikler:
# - [0.4.3] Plugin sistemi ve üst proje entegrasyon araçları eklendi
#
# Yazar: GitHub Copilot
# Tarih: 2025-05-04
===========================================================
"""

# Plugin izolasyon katmanı ve yapılandırma standardizasyonunu dışa aktar
from .plugin_isolation import PluginIsolation
from .config_standardizer import ConfigStandardizer

# Dışa aktarılan sınıflar
__all__ = ['PluginIsolation', 'ConfigStandardizer']