import os
import time
import phonenumbers
from phonenumbers import geocoder, carrier
from opencage.geocoder import OpenCageGeocode
from googlemaps import Client
import folium
from dotenv import load_dotenv
from pathlib import Path
from colorama import Fore, Style, init
from geopy.geocoders import Nominatim

# Terminali temizle (Linux/Windows/macOS uyumlu)
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Renkleri ve terminali başlat
init(autoreset=True)
clear_terminal()

# PeGaSuS Özel Banner
BANNER = f"""
{Fore.BLUE}
██████╗ ███████╗ ██████╗  █████╗ ███████╗██╗   ██╗███████╗
██╔══██╗██╔════╝██╔════╝ ██╔══██╗██╔════╝██║   ██║██╔════╝
██████╔╝█████╗  ██║  ███╗███████║███████╗██║   ██║███████╗
██╔═══╝ ██╔══╝  ██║   ██║██╔══██║╚════██║██║   ██║╚════██║
██║     ███████╗╚██████╔╝██║  ██║███████║╚██████╔╝███████║
╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝
{Fore.CYAN}
► Developed by {Fore.MAGENTA}PeGaSuS{Fore.CYAN} ◄
{Fore.YELLOW}══════════════════════════════════════════════════════
{Fore.GREEN}🌐 Website: {Fore.WHITE}https://about.me/pegasus/
{Fore.RED}▶ YouTube: {Fore.WHITE}https://youtube.com/@RzaSAHIN
{Fore.YELLOW}══════════════════════════════════════════════════════
{Style.RESET_ALL}
"""

def print_banner():
    """Özelleştirilmiş PeGaSuS banner'ını göster"""
    print(BANNER)

def get_api_key(service: str) -> str:
    """API anahtarını çevresel değişkenlerden al"""
    key = os.getenv(f"{service}_API_KEY")
    if not key:
        raise ValueError(f"{service} API anahtarı bulunamadı!")
    return key

def parse_phone_number(number: str) -> phonenumbers.PhoneNumber:
    """Telefon numarasını doğrula ve ayrıştır"""
    try:
        parsed_num = phonenumbers.parse(number, None)
        if not phonenumbers.is_valid_number(parsed_num):
            raise ValueError("Geçersiz telefon numarası")
        return parsed_num
    except phonenumbers.NumberParseException as e:
        raise ValueError(f"Numara ayrıştırma hatası: {str(e)}")

def get_location_details(parsed_num: phonenumbers.PhoneNumber) -> tuple[str, str]:
    """Konum ve operatör bilgilerini al"""
    try:
        location = geocoder.description_for_number(parsed_num, "en")  # Ülke bilgisini al
        operator = carrier.name_for_number(parsed_num, "en")
        return location, operator
    except Exception as e:
        raise RuntimeError(f"Konum bilgisi alınamadı: {str(e)}")

def get_country_coordinates(country_name: str) -> tuple[float, float]:
    """Ülke adından ülkenin merkez koordinatlarını al"""
    geolocator = Nominatim(user_agent="phone_tracker")
    location = geolocator.geocode(country_name, exactly_one=True)
    if location:
        return (location.latitude, location.longitude)
    else:
        raise ValueError(f"{country_name} için koordinat bulunamadı.")

def generate_map(lat: float, lng: float, operator: str, address: str) -> str:
    """Folium ile interaktif harita oluştur"""
    try:
        output_dir = Path(__file__).resolve().parent.parent / "output"
        output_dir.mkdir(exist_ok=True)
        
        harita = folium.Map(location=[lat, lng], zoom_start=5)
        popup_text = f"<b>Operatör:</b> {operator}<br><b>Adres:</b> {address}"
        folium.Marker([lat, lng], popup=popup_text, tooltip="Ülke Merkezi").add_to(harita)
        
        file_path = output_dir / "konum.html"
        harita.save(file_path)
        return str(file_path)
    except Exception as e:
        raise RuntimeError(f"Harita oluşturulamadı: {str(e)}")

def real_time_tracking():
    """Anlık konum takibi yapar"""
    try:
        print(f"{Fore.YELLOW}Anlık Konum Takibi Başlatıldı...{Style.RESET_ALL}")
        while True:
            # Örnek olarak sabit bir konum kullanıyoruz.
            # Gerçek bir uygulamada, bu bilgi mobil cihazdan veya IoT cihazından alınır.
            lat, lng = 41.0082, 28.9784  # İstanbul koordinatları
            address = get_detailed_address(lat, lng)
            print(f"{Fore.GREEN}Anlık Konum:{Style.RESET_ALL} Enlem = {lat}, Boylam = {lng}")
            print(f"{Fore.GREEN}Adres:{Style.RESET_ALL} {address}")
            
            # Haritayı güncelle
            map_path = generate_map(lat, lng, "Operatör Bilgisi", address)
            print(f"{Fore.MAGENTA}Harita güncellendi:{Style.RESET_ALL} {Fore.BLUE}{map_path}{Style.RESET_ALL}")
            
            time.sleep(10)  # Her 10 saniyede bir konumu güncelle
    except KeyboardInterrupt:
        print(f"{Fore.RED}Anlık Konum Takibi Durduruldu.{Style.RESET_ALL}")

def single_location_query():
    """Tek seferlik konum sorgulama yapar"""
    try:
        clear_terminal()
        print_banner()
        numara = input(f"{Fore.CYAN}[?]{Style.RESET_ALL} Telefon numarasını ülke koduyla girin (+905551234567): ").strip()
        
        parsed_num = parse_phone_number(numara)
        location, operator = get_location_details(parsed_num)
        
        # Ülke merkez koordinatlarını al
        lat, lng = get_country_coordinates(location)
        
        # Detaylı adres bilgisini al
        detailed_address = f"{location} (Ülke Merkezi)"
        
        print(f"\n{Fore.GREEN}{'═'*40}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📱 Operatör:{Style.RESET_ALL} {Fore.CYAN}{operator}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📍 Bölge:{Style.RESET_ALL} {Fore.CYAN}{location}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🏠 Detaylı Adres:{Style.RESET_ALL} {Fore.GREEN}{detailed_address}{Style.RESET_ALL}")
        
        # Harita oluştur ve kaydet
        map_path = generate_map(lat, lng, operator, detailed_address)
        print(f"\n{Fore.MAGENTA}🗺️ Harita kaydedildi:{Style.RESET_ALL} {Fore.BLUE}{map_path}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'═'*40}{Style.RESET_ALL}")

    except Exception as e:
        print(f"\n{Fore.RED}❌ Hata:{Style.RESET_ALL} {Fore.YELLOW}{str(e)}{Style.RESET_ALL}")

def main():
    """Ana menüyü gösterir ve kullanıcı seçimine göre işlem yapar"""
    try:
        clear_terminal()
        print_banner()
        print(f"{Fore.CYAN}[1]{Style.RESET_ALL} Tek Seferlik Konum Sorgulama")
        print(f"{Fore.CYAN}[2]{Style.RESET_ALL} Anlık Konum Takibi")
        secim = input(f"{Fore.CYAN}[?]{Style.RESET_ALL} Seçiminizi yapın (1/2): ").strip()
        
        if secim == "1":
            single_location_query()
        elif secim == "2":
            real_time_tracking()
        else:
            print(f"{Fore.RED}Geçersiz seçim!{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}❌ Hata:{Style.RESET_ALL} {Fore.YELLOW}{str(e)}{Style.RESET_ALL}")

if __name__ == "__main__":
    load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    main()
