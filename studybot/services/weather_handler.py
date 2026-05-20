import requests
from django.conf import settings
from bot.services.base_handler import BaseHandler


class WeatherHandler(BaseHandler):
    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

    def handle(self, message):
        parts = message.text.strip().split(maxsplit=1)
        if len(parts) < 2:
            self._bot.reply_to(message, '❗ Укажи город: /weather Almaty')
            return
        result = self._get_weather(parts[1].strip())
        if 'error' in result:
            self._bot.reply_to(message, f'❌ {result["error"]}')
        else:
            text = (
                f'🌤 *Погода в {result["city"]}:*\n\n'
                f'🌡 Температура: {result["temp"]}°C\n'
                f'🤔 Ощущается: {result["feels_like"]}°C\n'
                f'💧 Влажность: {result["humidity"]}%\n'
                f'💨 Ветер: {result["wind"]} м/с\n'
                f'☁️ {result["description"].capitalize()}\n\n'
                f'_📡 OpenWeather API_'
            )
            self._bot.reply_to(message, text, parse_mode='Markdown')

    def _get_weather(self, city):
        api_key = settings.OPENWEATHER_API_KEY
        if not api_key:
            return {'error': 'API ключ не задан в .env'}
        params = {'q': city, 'appid': api_key, 'units': 'metric', 'lang': 'ru'}
        try:
            r = requests.get(self.BASE_URL, params=params, timeout=6)
        except requests.exceptions.ConnectionError:
            return {'error': 'Нет соединения с интернетом'}
        except requests.exceptions.Timeout:
            return {'error': 'Сервер не ответил'}
        if r.status_code == 401:
            return {'error': 'Неверный API ключ (401)'}
        if r.status_code == 404:
            return {'error': f'Город "{city}" не найден'}
        if r.status_code != 200:
            return {'error': f'Ошибка сервера: {r.status_code}'}
        d = r.json()
        return {
            'city':        d.get('name', city),
            'temp':        d['main']['temp'],
            'feels_like':  d['main']['feels_like'],
            'humidity':    d['main']['humidity'],
            'wind':        d['wind']['speed'],
            'description': d['weather'][0]['description'],
        }
