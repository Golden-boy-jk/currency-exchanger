import requests
import json

class APIException(Exception):
    """Класс для собственных исключений"""
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        # Пример API для получения курса валют
        url = f'https://min-api.cryptocompare.com/data/price?fsym={quote.upper()}&tsyms={base.upper()}'

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Неверное количество валюты: {amount}")

        response = requests.get(url)
        if response.status_code != 200:
            raise APIException(f"Ошибка при запросе API: {response.status_code}")

        try:
            data = response.json()
            rate = data[base.upper()]
        except KeyError:
            raise APIException(f"Не удалось найти валюту {base} или {quote} в данных API.")

        return rate * amount
