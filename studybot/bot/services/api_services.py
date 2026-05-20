import requests
from bs4 import BeautifulSoup


def get_weather(city: str, api_key: str) -> dict:
    if not api_key:
        return {'error': 'API ключ не задан. Добавь OPENWEATHER_API_KEY в .env'}

    url = 'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric',
        'lang': 'ru',
    }

    try:
        response = requests.get(url, params=params, timeout=6)
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
    return {
        'city': data.get('name', city),
        'temp': data['main']['temp'],
        'feels_like': data['main']['feels_like'],
        'humidity': data['main']['humidity'],
        'wind': data['wind']['speed'],
        'description': data['weather'][0]['description'],
    }


def get_country(name: str) -> dict:
    url = f'https://restcountries.com/v3.1/name/{name}'

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

    country = data[0]
    capital = country.get('capital', ['—'])[0] if country.get('capital') else '—'
    area = country.get('area', 0)
    currencies = country.get('currencies', {})
    if currencies:
        first_key = next(iter(currencies))
        currency = currencies[first_key].get('name', first_key)
    else:
        currency = '—'

    return {
        'name': country.get('name', {}).get('common', name),
        'capital': capital,
        'population': country.get('population', 0),
        'region': country.get('region', '—'),
        'area': int(area),
        'currency': currency,
    }


def get_jobs() -> list:
    url = 'https://realpython.github.io/fake-jobs/'

    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
    except requests.exceptions.Timeout:
        return []
    except requests.exceptions.RequestException:
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    cards = soup.select('.card-content')
    jobs = []

    for card in cards:
        title = card.select_one('h2.title')
        company = card.select_one('h3.company')
        link_tag = card.select_one('a[href]')

        jobs.append({
            'title': title.text.strip() if title else 'Без названия',
            'company': company.text.strip() if company else 'Без компании',
            'link': link_tag['href'] if link_tag else '',
        })

    return jobs
