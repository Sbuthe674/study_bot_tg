"""
bot/services/weather_handler.py
API — Lab 5, Variant 13: OpenWeather API

Демонстрирует:
  - GET-запрос с параметрами через params={}
  - Обработка ошибок: 401 (неверный ключ), 404 (город не найден)
  - Извлечение вложенных JSON-полей
  - ООП: наследование от BaseHandler
"""
import requests
from django.conf import settings

from .base_handler import BaseHandler


class WeatherHandler(BaseHandler):
    """Получает погоду через OpenWeather API."""

    BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'

    def handle(self, message):
        """Парсит город из сообщения и возвращает погоду."""
        parts = message.text.strip().split(maxsplit=1)
        if len(parts) < 2:
            self._bot.reply_to(
                message,
                '❗ Укажи город: /weather Almaty'
            )
            return

        city = parts[1].strip()
        result = self._get_weather(city)

        if 'error' in result:
            self._bot.reply_to(message, f'❌ {result["error"]}')
        else:
            text = (
                f'🌤 *Погода в {result["city"]}:*\n\n'
                f'🌡 Температура: {result["temp"]}°C\n'
                f'🤔 Ощущается как: {result["feels_like"]}°C\n'
                f'💧 Влажность: {result["humidity"]}%\n'
                f'💨 Ветер: {result["wind"]} м/с\n'
                f'☁️ {result["description"].capitalize()}\n\n'
                f'_📡 OpenWeather API_'
            )
            self._bot.reply_to(message, text, parse_mode='Markdown')

    def _get_weather(self, city: str) -> dict:
        """
        Выполняет GET-запрос к OpenWeather.
        Обрабатывает основные ошибки API.
        """
        api_key = settings.OPENWEATHER_API_KEY
        if not api_key:
            return {'error': 'API ключ не задан. Добавь OPENWEATHER_API_KEY в .env'}

        params = {
            'q':     city,
            'appid': api_key,
            'units': 'metric',   # градусы Цельсия
            'lang':  'ru',
        }

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=6)
        except requests.exceptions.ConnectionError:
            return {'error': 'Нет соединения с интернетом'}
        except requests.exceptions.Timeout:
            return {'error': 'Сервер не ответил вовремя'}

        if response.status_code == 401:
            return {'error': 'Неверный API ключ (401). Проверь OPENWEATHER_API_KEY'}
        if response.status_code == 404:
            return {'error': f'Город "{city}" не найден. Попробуй на английском: Almaty, Moscow'}
        if response.status_code != 200:
            return {'error': f'Ошибка сервера: {response.status_code}'}

        data = response.json()

        # Извлечение вложенных полей JSON (Lab 5 — часть 2)
        return {
            'city':        data.get('name', city),
            'temp':        data['main']['temp'],
            'feels_like':  data['main']['feels_like'],
            'humidity':    data['main']['humidity'],
            'wind':        data['wind']['speed'],
            'description': data['weather'][0]['description'],
        }
