#By PeGaSuS

# Alt paket başlatma mesajı
print("data_analysis alt paketi yüklendi!")

# Modülleri otomatik olarak import et
from .heatmap import generate_heatmap

# Alt paket içindeki fonksiyonları dışarıya aç
__all__ = [
    "generate_heatmap",  # heatmap.py'deki fonksiyon
]