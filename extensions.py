import requests
import json

from config import exchanges

class ApiException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote, base, amount):
        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise ApiException(f"Валюта {base} не найдена!")

        try:
            quote_key = exchanges[quote.lower()]
        except KeyError:
            raise ApiException(f"Валюта {quote} не найдена!")

        if base_key == quote_key:
            raise ApiException(f'Невозможно перевести одинаковые валюты {base}!')

        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise ApiException(f'Не удалось обработать количество {amount}!')

        # url = f"https://api.apilayer.com/exchangerates_data/convert?to={exchanges[base]}&from={exchanges[quote]}&amount={amount}"
        url = f"https://api.apilayer.com/exchangerates_data/convert?to={base_key}&from={quote_key}&amount={amount}"

        headers = {"apikey": "***********"}
        response = requests.request("GET", url, headers=headers)
        total_base = json.loads(response.content)['result']
        text = f'Стоимость {amount} {quote} в {base} - {total_base}'
        return text