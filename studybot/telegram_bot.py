"""
bot/telegram_bot.py — онбординговый Telegram-бот с inline-кнопками

Новое:
  - /progress и кнопка 📝 Прогресс — сколько уроков прошёл пользователь
  - /help и кнопка ❓ Помощь — красивое меню всех команд
  - Навигация между уроками (кнопки ⬅️ Пред / След ➡️)
  - Умное приветствие: новый vs вернувшийся пользователь
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studybot.settings')
django.setup()

import telebot
from telebot.types import Message, CallbackQuery
from django.conf import settings
from django.db.models import Count

from bot.models import BotUser, Lesson, LessonView
from bot.services.keyboards import (
    main_menu, lessons_menu, lesson_nav, back_to_main,
    ask_city, ask_country, validate_menu, benchmark_kb,
)
from bot.services.api_services import get_weather, get_country, get_jobs
from bot.utils.regex_helpers import validate
from bot.utils.sort_utils import benchmark, merge_sort

bot = telebot.TeleBot(settings.TELEGRAM_TOKEN)

# Состояния ожидания текстового ввода
waiting = {}


# ── Вспомогательные функции ───────────────────────────────────

def get_or_create_user(from_user):
    user, created = BotUser.objects.update_or_create(
        telegram_id=from_user.id,
        defaults={
            'username':   from_user.username or '',
            'first_name': from_user.first_name or '',
        }
    )
    return user, created


def get_all_lesson_numbers():
    """Все номера активных уроков отсортированные — для навигации."""
    return list(Lesson.objects.filter(is_active=True).values_list('number', flat=True).order_by('number'))


def get_user_progress(telegram_id: int) -> dict:
    """Считает прогресс пользователя по урокам."""
    total   = Lesson.objects.filter(is_active=True).count()
    viewed  = LessonView.objects.filter(
        user__telegram_id=telegram_id
    ).values('lesson').distinct().count()

    viewed_nums = list(
        LessonView.objects.filter(user__telegram_id=telegram_id)
        .values_list('lesson__number', flat=True)
        .distinct()
        .order_by('lesson__number')
    )

    return {
        'total':       total,
        'viewed':      viewed,
        'remaining':   total - viewed,
        'percent':     int((viewed / total * 100) if total > 0 else 0),
        'viewed_nums': viewed_nums,
    }


def progress_bar(percent: int) -> str:
    """Текстовый прогресс-бар: ████░░░░ 50%"""
    filled = int(percent / 10)
    empty  = 10 - filled
    return '█' * filled + '░' * empty + f' {percent}%'


# ── Команды ───────────────────────────────────────────────────

@bot.message_handler(commands=['start'])
def cmd_start(message: Message):
    user, created = get_or_create_user(message.from_user)
    name = message.from_user.first_name or 'студент'
    total = Lesson.objects.filter(is_active=True).count()

    if created:
        # Новый пользователь
        text = (
            f'👋 Привет, {name}! Рад видеть тебя впервые!\n\n'
            f'Я StudyBot — твой учебный помощник 🤖\n\n'
            f'📚 Доступно уроков: {total}\n'
            f'Начни с кнопки «Уроки» или посмотри «Помощь».\n\n'
            f'Выбери раздел:'
        )
    else:
        # Вернувшийся пользователь
        progress = get_user_progress(message.from_user.id)
        text = (
            f'С возвращением, {name}! 👋\n\n'
            f'📊 Твой прогресс: {progress["viewed"]}/{progress["total"]} уроков\n'
            f'{progress_bar(progress["percent"])}\n\n'
            f'Выбери раздел:'
        )

    bot.send_message(message.chat.id, text, reply_markup=main_menu())


@bot.message_handler(commands=['help'])
def cmd_help(message: Message):
    get_or_create_user(message.from_user)
    _send_help(message.chat.id)


@bot.message_handler(commands=['progress'])
def cmd_progress(message: Message):
    get_or_create_user(message.from_user)
    _send_progress(message.chat.id, message.from_user.id)


@bot.message_handler(commands=['menu'])
def cmd_menu(message: Message):
    get_or_create_user(message.from_user)
    bot.send_message(message.chat.id, '🏠 Главное меню:', reply_markup=main_menu())


# ── Текстовый ввод (когда бот ждёт ответа) ───────────────────

@bot.message_handler(func=lambda m: m.from_user.id in waiting)
def handle_user_input(message: Message):
    user_id = message.from_user.id
    state   = waiting.pop(user_id, None)
    text    = message.text.strip()

    if state == 'weather':
        _send_weather(message.chat.id, text)
    elif state == 'country':
        _send_country(message.chat.id, text)
    elif state and state.startswith('validate_'):
        _send_validation(message.chat.id, state.replace('validate_', ''), text)
    elif state == 'benchmark':
        try:
            n = min(int(text), 100_000)
        except ValueError:
            n = 1000
        _send_benchmark(message.chat.id, n)


@bot.message_handler(func=lambda m: True)
def handle_unknown(message: Message):
    get_or_create_user(message.from_user)
    bot.send_message(
        message.chat.id,
        '🤷 Не понял команду.\nНажми ❓ Помощь или выбери раздел:',
        reply_markup=main_menu()
    )


# ── Callback обработчики (inline кнопки) ─────────────────────

@bot.callback_query_handler(func=lambda c: True)
def handle_callback(call: CallbackQuery):
    get_or_create_user(call.from_user)
    data    = call.data
    chat_id = call.message.chat.id
    msg_id  = call.message.message_id

    bot.answer_callback_query(call.id)

    # ── Главное меню ──
    if data == 'menu_main':
        bot.edit_message_text(
            '🏠 Главное меню — выбери раздел:',
            chat_id, msg_id,
            reply_markup=main_menu()
        )

    # ── Помощь ──
    elif data == 'menu_help':
        _send_help(chat_id)

    # ── Прогресс ──
    elif data == 'menu_progress':
        _send_progress(chat_id, call.from_user.id)

    # ── Уроки ──
    elif data == 'menu_lessons':
        lessons = Lesson.objects.filter(is_active=True)
        if not lessons:
            bot.send_message(chat_id, '📚 Уроков пока нет. Загляни позже!',
                             reply_markup=back_to_main())
        else:
            progress = get_user_progress(call.from_user.id)
            viewed   = set(progress['viewed_nums'])
            # Помечаем пройденные уроки галочкой
            kb = __lessons_menu_with_progress(lessons, viewed)
            bot.send_message(
                chat_id,
                f'📚 Выбери урок:\n'
                f'Пройдено: {progress["viewed"]}/{progress["total"]} '
                f'({progress["percent"]}%)',
                reply_markup=kb
            )

    elif data.startswith('lesson_'):
        num = int(data.replace('lesson_', ''))
        try:
            lesson      = Lesson.objects.get(number=num, is_active=True)
            all_numbers = get_all_lesson_numbers()

            # Сохраняем просмотр
            try:
                db_user = BotUser.objects.get(telegram_id=call.from_user.id)
                LessonView.objects.get_or_create(user=db_user, lesson=lesson)
            except Exception:
                pass

            text = f'📖 Урок {lesson.number}: {lesson.title}\n\n{lesson.content}'
            bot.send_message(
                chat_id, text,
                reply_markup=lesson_nav(num, all_numbers)
            )
        except Lesson.DoesNotExist:
            bot.send_message(chat_id, f'❌ Урок #{num} не найден.',
                             reply_markup=back_to_main())
        except Exception as e:
            bot.send_message(chat_id, f'❌ Ошибка: {e}',
                             reply_markup=back_to_main())

    # ── Погода ──
    elif data == 'menu_weather':
        bot.send_message(
            chat_id,
            '🌤 Выбери город или напиши своё название:',
            reply_markup=ask_city()
        )

    elif data.startswith('weather_'):
        _send_weather(chat_id, data.replace('weather_', ''))

    # ── Страны ──
    elif data == 'menu_country':
        bot.send_message(
            chat_id,
            '🌍 Выбери страну или напиши название на английском:',
            reply_markup=ask_country()
        )

    elif data.startswith('country_'):
        _send_country(chat_id, data.replace('country_', ''))

    # ── Вакансии ──
    elif data == 'menu_jobs':
        bot.send_message(chat_id, '💼 Парсю вакансии, подожди...')
        jobs = get_jobs()
        if not jobs:
            bot.send_message(chat_id, '❌ Не удалось получить вакансии.',
                             reply_markup=back_to_main())
        else:
            sorted_jobs = merge_sort([j['title'] for j in jobs])[:5]
            lines = ['💼 Топ-5 вакансий:\n']
            for i, title in enumerate(sorted_jobs, 1):
                company = next((j['company'] for j in jobs if j['title'] == title), '—')
                lines.append(f'{i}. {title}\n   🏢 {company}')
            lines.append(f'\nВсего найдено: {len(jobs)}')
            bot.send_message(chat_id, '\n'.join(lines), reply_markup=back_to_main())

    # ── Валидатор ──
    elif data == 'menu_validate':
        bot.send_message(
            chat_id,
            '✅ Что хочешь проверить?',
            reply_markup=validate_menu()
        )

    elif data.startswith('validate_'):
        type_ = data.replace('validate_', '')
        labels = {
            'email': 'email-адрес',
            'phone': 'номер телефона',
            'url':   'ссылку',
            'ip':    'IP-адрес',
            'color': 'HEX-цвет (#FF0000)',
        }
        waiting[call.from_user.id] = f'validate_{type_}'
        bot.send_message(
            chat_id,
            f'✏️ Напиши {labels.get(type_, type_)}:',
            reply_markup=back_to_main()
        )

    # ── Алгоритмы ──
    elif data == 'menu_benchmark':
        bot.send_message(
            chat_id,
            '⚡ Выбери размер массива для теста:',
            reply_markup=benchmark_kb()
        )

    elif data.startswith('bench_'):
        n      = int(data.replace('bench_', ''))
        result = benchmark(n)
        bot.send_message(chat_id, _format_benchmark(result), reply_markup=back_to_main())


# ── Вспомогательные функции отправки ─────────────────────────

def _send_help(chat_id: int):
    text = (
        '❓ Справка — StudyBot\n\n'
        '📚 Уроки\n'
        '  Список всех уроков курса с навигацией\n\n'
        '📝 Прогресс\n'
        '  Сколько уроков ты уже прошёл\n\n'
        '🌤 Погода\n'
        '  Текущая погода для любого города\n\n'
        '🌍 Страны\n'
        '  Данные о стране: столица, население, площадь\n\n'
        '💼 Вакансии\n'
        '  Свежие вакансии (парсинг сайта)\n\n'
        '✅ Валидатор\n'
        '  Проверка email, телефона, URL, IP, HEX-цвета\n\n'
        '⚡ Алгоритмы\n'
        '  Сравнение скорости сортировок и поиска\n\n'
        'Команды: /start /menu /progress /help'
    )
    bot.send_message(chat_id, text, reply_markup=back_to_main())


def _send_progress(chat_id: int, telegram_id: int):
    progress = get_user_progress(telegram_id)

    if progress['total'] == 0:
        bot.send_message(chat_id, '📚 Уроков пока нет.', reply_markup=back_to_main())
        return

    viewed_str = (
        ', '.join(f'#{n}' for n in progress['viewed_nums'])
        if progress['viewed_nums'] else 'ещё ни одного'
    )

    if progress['percent'] == 100:
        emoji = '🏆'
        status = 'Все уроки пройдены! Отличная работа!'
    elif progress['percent'] >= 50:
        emoji = '🔥'
        status = 'Хороший прогресс, продолжай!'
    elif progress['percent'] > 0:
        emoji = '📈'
        status = 'Хорошее начало, не останавливайся!'
    else:
        emoji = '🚀'
        status = 'Начни с первого урока!'

    text = (
        f'{emoji} Твой прогресс\n\n'
        f'{progress_bar(progress["percent"])}\n\n'
        f'Пройдено: {progress["viewed"]} из {progress["total"]} уроков\n'
        f'Осталось: {progress["remaining"]}\n\n'
        f'Пройденные уроки: {viewed_str}\n\n'
        f'{status}'
    )
    bot.send_message(chat_id, text, reply_markup=main_menu())


def _send_weather(chat_id: int, city: str):
    result = get_weather(city, settings.OPENWEATHER_API_KEY)
    if 'error' in result:
        bot.send_message(chat_id, f'❌ {result["error"]}', reply_markup=back_to_main())
    else:
        text = (
            f'🌤 Погода в {result["city"]}:\n\n'
            f'🌡 Температура: {result["temp"]}°C\n'
            f'🤔 Ощущается: {result["feels_like"]}°C\n'
            f'💧 Влажность: {result["humidity"]}%\n'
            f'💨 Ветер: {result["wind"]} м/с\n'
            f'☁️ {result["description"].capitalize()}'
        )
        bot.send_message(chat_id, text, reply_markup=back_to_main())


def _send_country(chat_id: int, name: str):
    result = get_country(name)
    if 'error' in result:
        bot.send_message(chat_id, f'❌ {result["error"]}', reply_markup=back_to_main())
    else:
        text = (
            f'🌍 {result["name"]}\n\n'
            f'🏙 Столица: {result["capital"]}\n'
            f'👥 Население: {result["population"]:,}\n'
            f'🗺 Регион: {result["region"]}\n'
            f'📐 Площадь: {result["area"]:,} км²\n'
            f'💰 Валюта: {result["currency"]}'
        )
        bot.send_message(chat_id, text, reply_markup=back_to_main())


def _send_validation(chat_id: int, type_: str, text: str):
    result = validate(type_, text)
    if result['ok']:
        msg = (
            f'✅ {result["type"]} найден!\n\n'
            f'Значение: {result["found"]}\n'
            f'Паттерн: {result["pattern"]}'
        )
    else:
        msg = (
            f'❌ Не найдено\n\n'
            f'{result.get("msg", "Совпадений нет")}\n'
            f'Паттерн: {result.get("pattern", "—")}'
        )
    bot.send_message(chat_id, msg, reply_markup=back_to_main())


def _send_benchmark(chat_id: int, n: int):
    result = benchmark(n)
    bot.send_message(chat_id, _format_benchmark(result), reply_markup=back_to_main())


def _format_benchmark(result: dict) -> str:
    return (
        f'📊 Сравнение алгоритмов (n={result["n"]:,})\n\n'
        f'🔍 Поиск элемента {result["target"]}:\n'
        f'Linear search: {result["linear_ms"]} мс — O(n)\n'
        f'Binary search: {result["binary_ms"]} мс — O(log n)\n\n'
        f'📦 Сортировка:\n'
        f'Merge sort: {result["merge_ms"]} мс — O(n log n)\n'
        f'Quick sort: {result["quick_ms"]} мс — O(n log n)\n\n'
        f'Чем больше n — тем заметнее разница!'
    )


def __lessons_menu_with_progress(lessons, viewed_nums: set):
    """Список уроков с отметкой пройденных."""
    from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
    kb = InlineKeyboardMarkup(row_width=1)
    for lesson in lessons:
        mark = '✅' if lesson.number in viewed_nums else '📖'
        kb.add(InlineKeyboardButton(
            f'{mark} Урок {lesson.number}: {lesson.title}',
            callback_data=f'lesson_{lesson.number}'
        ))
    kb.add(InlineKeyboardButton('⬅️ Главное меню', callback_data='menu_main'))
    return kb


if __name__ == '__main__':
    print('🤖 StudyBot запущен. Ctrl+C для остановки.')
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
