import requests
from django.conf import settings
import os

def get_exchange_rate(currency_code, base_currency="UAH"):
    
    api_key = settings.EXCHANGE_API_KEY

    if not api_key:
        raise Exception("Exchange API key is not set in settings.")

    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{currency_code}/{base_currency}"

    response = requests.get(url)
    
    response.raise_for_status()
    
    data = response.json()
    if data.get('result') != 'success':
        raise Exception(f"API Error: {data.get('error-type')}")

    return data['conversion_rate']