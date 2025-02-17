from twilio.rest import Client
from config import get_api_key, ConfigError

def send_location_request(target_number: str) -> str:
    """
    Belirtilen telefon numarasına konum isteği SMS'i gönderir.
    
    :param target_number: SMS gönderilecek telefon numarası (ülke koduyla birlikte).
    :return: Gönderilen SMS'in SID'si.
    """
    try:
        # Twilio hesap bilgilerini al
        account_sid = get_api_key("twilio_sid")
        auth_token = get_api_key("twilio_token")
        twilio_number = get_api_key("twilio_phone")
        
        # Twilio istemcisini oluştur
        client = Client(account_sid, auth_token)
        
        # SMS gönder
        message = client.messages.create(
            body="Konumunuzu paylaşın: http://bit.ly/3xYzabc",  # Örnek bir bağlantı
            from_=twilio_number,
            to=target_number
        )
        
        print(f"{Fore.GREEN}SMS başarıyla gönderildi! SID: {message.sid}{Style.RESET_ALL}")
        return message.sid
    except ConfigError as e:
        raise RuntimeError(f"Twilio API anahtarı bulunamadı: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Twilio SMS gönderilemedi: {str(e)}")