"""
bot/telegram_bot.py
Главный файл Telegram-бота.

Запуск: python manage.py runbot
  (или напрямую: python bot/telegram_bot.py из корня проекта)

Команды:
  /start      — приветствие и список команд
  /help       — справка
  /weather    — погода через OpenWeather API
  /country    — данные о стране через REST Countries
  /jobs       — парсинг вакансий с сайта
  /validate   — проверка текста по regex-паттерну
  /benchmark  — сравнение алгоритмов поиска/сортировки
"""
import os
import sys
import django

# Инициализируем Django перед импортом моделей
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studybot.settings')
django.setup()

import telebot
from django.conf import settings
from bot.models import UserQuery
from bot.services import (
    WeatherHandler,
    CountryHandler,
    ValidatorHandler,
    JobParser,
    BenchmarkHandler,
)

bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)

# Создаём обработчики — передаём им экземпляр бота
weather_h   = WeatherHandler(bot)
country_h   = CountryHandler(bot)
validator_h = ValidatorHandler(bot)
job_h       = JobParser(bot)
benchmark_h = BenchmarkHandler(bot)

COMMANDS_HELP = """
🤖 *StudyBot — команды:*

/weather <город> — погода сейчас
  Пример: /weather Almaty

/country <страна> — данные о стране
  Пример: /country Kazakhstan

/jobs — свежие вакансии (парсинг сайта)

/validate <тип> <текст> — проверка формата
  Типы: email, phone, url, ip, num, color
  Пример: /validate email test@mail.com

/benchmark [n] — сравнение алгоритмов
  Пример: /benchmark 10000
"""


def save_query(message, response_text: str):
    """Сохраняет запрос в Django БД."""
    try:
        UserQuery.objects.create(
            telegram_id   = message.from_user.id,
            username      = message.from_user.username or '',
            command       = message.text.split()[0],
            query_text    = message.text,
            response_text = response_text,
        )
    except Exception:
        pass  # не ломаем бота из-за ошибки БД


# ── Обработчики команд ────────────────────────────────────────

@bot.message_handler(commands=['start'])
def cmd_start(message):
    name = message.from_user.first_name or 'студент'
    text = (
        f'👋 Привет, {name}!\n\n'
        f'Я *StudyBot* — учебный бот, который показывает,\n'
        f'как Python-курс работает на практике.\n\n'
        + COMMANDS_HELP
    )
    bot.reply_to(message, text, parse_mode='Markdown')
    save_query(message, text)


@bot.message_handler(commands=['help'])
def cmd_help(message):
    bot.reply_to(message, COMMANDS_HELP, parse_mode='Markdown')
    save_query(message, COMMANDS_HELP)


@bot.message_handler(commands=['weather'])
def cmd_weather(message):
    weather_h.handle(message)
    save_query(message, 'weather response')


@bot.message_handler(commands=['country'])
def cmd_country(message):
    country_h.handle(message)
    save_query(message, 'country response')


@bot.message_handler(commands=['jobs'])
def cmd_jobs(message):
    bot.reply_to(message, '🔍 Парсю вакансии, подожди секунду...')
    job_h.handle(message)
    save_query(message, 'jobs response')


@bot.message_handler(commands=['validate'])
def cmd_validate(message):
    validator_h.handle(message)
    save_query(message, 'validate response')


@bot.message_handler(commands=['benchmark'])
def cmd_benchmark(message):
    bot.reply_to(message, '⚡ Запускаю тест алгоритмов...')
    benchmark_h.handle(message)
    save_query(message, 'benchmark response')


@bot.message_handler(func=lambda m: True)
def handle_unknown(message):
    bot.reply_to(
        message,
        '🤷 Не понял команду. Напиши /help чтобы увидеть список команд.'
    )


# ── Запуск ────────────────────────────────────────────────────

if __name__ == '__main__':
    print('🤖 StudyBot запущен. Нажми Ctrl+C для остановки.')
    print(f'   Токен: {settings.TELEGRAM_TOKEN[:10]}...')
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5, logger_level=None)
    except KeyboardInterrupt:
        print('🤖 StudyBot остановлен')
