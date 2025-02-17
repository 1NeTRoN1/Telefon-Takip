import folium
from folium.plugins import HeatMap
from typing import List, Tuple
from pathlib import Path

def generate_heatmap(locations: List[Tuple[float, float]]) -> str:
    """
    Verilen konum listesini kullanarak bir ısı haritası oluşturur.
    
    :param locations: (enlem, boylam) şeklinde konum listesi.
    :return: Oluşturulan haritanın dosya yolu.
    """
    if not locations:
        raise ValueError("Konum verisi bulunamadı!")
    
    try:
        # Çıktı klasörünü oluştur
        output_dir = Path(__file__).resolve().parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        # Türkiye merkezli bir harita oluştur
        m = folium.Map(location=[39.925533, 32.866287], zoom_start=6)
        
        # Isı haritasını ekle
        HeatMap(locations).add_to(m)
        
        # Haritayı kaydet
        file_path = output_dir / "heatmap.html"
        m.save(file_path)
        
        print(f"{Fore.GREEN}Isı haritası başarıyla oluşturuldu: {file_path}{Style.RESET_ALL}")
        return str(file_path)
    except Exception as e:
        raise RuntimeError(f"Isı haritası oluşturulamadı: {str(e)}")