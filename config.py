import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class ConfigError(Exception):
    """Özel hata sınıfı API anahtarları için"""
    pass

def get_api_key(service: str) -> str:
    """
    Belirtilen servis için API anahtarını döndürür.
    
    :param service: API anahtarı istenen servis (örneğin, "opencage", "google").
    :return: API anahtarı.
    """
    keys = {
        "opencage": os.getenv("OPENCAGE_API_KEY"),
        "google": os.getenv("GOOGLE_MAPS_API_KEY"),
        "twilio_sid": os.getenv("TWILIO_ACCOUNT_SID"),
        "twilio_token": os.getenv("TWILIO_AUTH_TOKEN"),
        "twilio_phone": os.getenv("TWILIO_PHONE_NUMBER")
    }
    
    if not keys.get(service):
        raise ConfigError(f"{service.upper()} API anahtarı bulunamadı!")
    return keys[service]