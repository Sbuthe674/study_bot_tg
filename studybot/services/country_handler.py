import requests
from bot.services.base_handler import BaseHandler


class CountryHandler(BaseHandler):
    BASE_URL = 'https://restcountries.com/v3.1/name/{}'

    def handle(self, message):
        parts = message.text.strip().split(maxsplit=1)
        if len(parts) < 2:
            self._bot.reply_to(message, '❗ Укажи страну: /country Kazakhstan')
            return
        result = self._get_country(parts[1].strip())
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

    def _get_country(self, name):
        try:
            r = requests.get(self.BASE_URL.format(name), timeout=6)
        except Exception as e:
            return {'error': str(e)}
        if r.status_code == 404:
            return {'error': f'Страна "{name}" не найдена. Пиши на английском.'}
        if r.status_code != 200:
            return {'error': f'Ошибка API: {r.status_code}'}
        data = r.json()
        if not data:
            return {'error': 'Пустой ответ'}
        c = data[0]
        capital    = c.get('capital', ['—'])[0] if c.get('capital') else '—'
        currencies = c.get('currencies', {})
        currency   = next(iter(currencies.values()), {}).get('name', '—') if currencies else '—'
        return {
            'name':       c.get('name', {}).get('common', name),
            'capital':    capital,
            'population': c.get('population', 0),
            'region':     c.get('region', '—'),
            'area':       int(c.get('area', 0)),
            'currency':   currency,
        }
