from config import keys
import requests
import json


class MyException(Exception):
    pass

class APIException(MyException):
    def __str__(self):
        return f'Неправильный формат ввода валюты.\nДоступные валюты /values'


class Convert:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if base == quote:
            raise MyException('Одинаковые валюты')

        try:
            base_ticker = keys[base]
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException()

        try:
            amount = float(amount)
        except ValueError:
            raise MyException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://api.fastforex.io/fetch-one?from={base_ticker}&to={quote_ticker}&api_key=4ce6fa65d7-b3f5d0bcc1-qzwtaj')
        d = json.loads(r.content)['result']
        price_per_one = d[keys[quote]]
        price = round((price_per_one * amount), 2)
        return price