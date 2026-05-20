# StudyBot — учебный Telegram-бот

Это учебный проект на Python и Django, который делает Telegram-бота для учебных лабораторных.

Проект собрал разные темы:
- API-запросы и парсинг
- регулярные выражения
- алгоритмы и сортировки
- Django-модели и админку
- Telegram inline-кнопки

## Что умеет бот

- `/start` — приветствие и меню
- `/help` — помощь по командам
- `/progress` — показывает пройденные уроки
- Погода через OpenWeather
- Данные о странах через REST Countries
- Вакансии с сайта через парсинг
- Проверка email/телефона/URL/IP/HEX-цвета
- Тесты скорости алгоритмов и сортировки

## Как запустить

1. Открой папку проекта:

```bash
cd studybot
```

2. Создай виртуальное окружение и активируй его:

```bash
python -m venv venv
venv\Scripts\activate
```

3. Установи зависимости:

```bash
pip install -r requirements.txt
```

4. Скопируй пример `.env` и заполни его:

```bash
copy .env.example .env
```

В `.env` нужно прописать:

```text
TELEGRAM_TOKEN=токен_бота_от_BotFather
OPENWEATHER_API_KEY=ключ_openweathermap
```

5. Создай базу данных и применяй миграции:

```bash
python manage.py migrate
```

6. Запусти бот:

```bash
python manage.py runbot
```

7. Если хочешь, можешь ещё запустить веб-сервер:

```bash
python manage.py runserver
```

И открыть в браузере:
- `http://127.0.0.1:8000/admin/` — админка Django
- `http://127.0.0.1:8000/history/` — история запросов

## Структура проекта

```
studybot/
├── manage.py
├── requirements.txt
├── .env.example
├── studybot/               # Django настройки
│   ├── settings.py
│   └── urls.py
├── bot/                    # логика бота
│   ├── models.py
│   ├── admin.py
│   ├── telegram_bot.py
│   ├── services/
│   │   ├── base_handler.py
│   │   ├── weather_handler.py
│   │   ├── country_handler.py
│   │   ├── job_parser.py
│   │   ├── validator_handler.py
│   │   ├── benchmark_handler.py
│   │   └── api_services.py
│   └── utils/
│       ├── regex_helpers.py
│       └── sort_utils.py
└── templates/bot/history.html
```

## Важно

- Для бота нужен `TELEGRAM_TOKEN`.
- Для погоды нужен `OPENWEATHER_API_KEY`.
- Если бот не запускается из-за `409 Conflict`, закрой другие копии и перезапусти.

## Советы

- Первым делом протестируй `/start` в Telegram.
- Если хочешь посмотреть данные в базе, зайди в админку.
- Код написан так, чтобы можно было смотреть, как связаны лабораторные в одном проекте.

