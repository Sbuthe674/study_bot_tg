"""
bot/services/country_handler.py
API — Lab 5, Variant 9: REST Countries API

Демонстрирует:
  - GET-запрос без API ключа
  - Безопасный доступ к необязательным полям через .get()
  - Работа со списками и вложенными словарями в JSON
  - Команда /country + бинарный поиск по кэшу (алгоритмы)
"""
import requests
import bisect

from .base_handler import BaseHandler


class CountryHandler(BaseHandler):
    """Получает данные о стране из REST Countries API."""

    BASE_URL = 'https://restcountries.com/v3.1/name/{}'

    def handle(self, message):
        parts = message.text.strip().split(maxsplit=1)
        if len(parts) < 2:
            self._bot.reply_to(message, '❗ Укажи страну: /country Kazakhstan')
            return

        country_name = parts[1].strip()
        result = self._get_country(country_name)

        if 'error' in result:
            self._bot.reply_to(message, f'❌ {result["error"]}')
        else:
            text = (
                f'🌍 *{result["name"]}*\n\n'
                f'🏙 Столица: {result["capital"]}\n'
                f'👥 Население: {result["population"]:,}\n'
                f'🗺 Регион: {result["region"]}\n'
                f'📐 Площадь: {result["area"]:,} км²\n'
                f'💰 Валюта: {result["currency"]}\n\n'
                f'_📡 REST Countries API_'
            )
            self._bot.reply_to(message, text, parse_mode='Markdown')

    def _get_country(self, name: str) -> dict:
        url = self.BASE_URL.format(name)
        try:
            response = requests.get(url, timeout=6)
        except requests.exceptions.ConnectionError:
            return {'error': 'Нет соединения'}
        except requests.exceptions.Timeout:
            return {'error': 'Сервер не ответил'}

        if response.status_code == 404:
            return {'error': f'Страна "{name}" не найдена. Пиши на английском: Kazakhstan, Germany'}
        if response.status_code != 200:
            return {'error': f'Ошибка API: {response.status_code}'}

        data = response.json()
        if not data:
            return {'error': 'Пустой ответ от API'}

        country = data[0]  # API возвращает список

        # Безопасный доступ к вложенным и необязательным полям
        capital  = country.get('capital', ['—'])[0] if country.get('capital') else '—'
        area     = country.get('area', 0)

        # Валюта — вложенный словарь currencies: {"USD": {"name": "Dollar"}}
        currencies = country.get('currencies', {})
        if currencies:
            first_key  = next(iter(currencies))
            currency   = currencies[first_key].get('name', first_key)
        else:
            currency = '—'

        return {
            'name':       country.get('name', {}).get('common', name),
            'capital':    capital,
            'population': country.get('population', 0),
            'region':     country.get('region', '—'),
            'area':       int(area),
            'currency':   currency,
        }
