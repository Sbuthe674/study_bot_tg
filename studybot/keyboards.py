"""
bot/services/keyboards.py — все inline-клавиатуры бота
"""
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton('📚 Уроки',      callback_data='menu_lessons'),
        InlineKeyboardButton('📝 Прогресс',   callback_data='menu_progress'),
        InlineKeyboardButton('🌤 Погода',      callback_data='menu_weather'),
        InlineKeyboardButton('🌍 Страны',      callback_data='menu_country'),
        InlineKeyboardButton('💼 Вакансии',    callback_data='menu_jobs'),
        InlineKeyboardButton('✅ Валидатор',   callback_data='menu_validate'),
        InlineKeyboardButton('⚡ Алгоритмы',  callback_data='menu_benchmark'),
        InlineKeyboardButton('❓ Помощь',      callback_data='menu_help'),
    )
    return kb


def lessons_menu(lessons) -> InlineKeyboardMarkup:
    """Список уроков с номером и названием."""
    kb = InlineKeyboardMarkup(row_width=1)
    for lesson in lessons:
        kb.add(InlineKeyboardButton(
            f'📖 Урок {lesson.number}: {lesson.title}',
            callback_data=f'lesson_{lesson.number}'
        ))
    kb.add(InlineKeyboardButton('⬅️ Главное меню', callback_data='menu_main'))
    return kb


def lesson_nav(current_number: int, all_numbers: list) -> InlineKeyboardMarkup:
    """
    Навигация внутри урока: кнопки Пред / След + назад к списку.
    all_numbers — список всех номеров активных уроков отсортированный.
    """
    kb = InlineKeyboardMarkup(row_width=2)
    nav_buttons = []

    if current_number in all_numbers:
        idx = all_numbers.index(current_number)

        if idx > 0:
            prev_num = all_numbers[idx - 1]
            nav_buttons.append(
                InlineKeyboardButton(f'⬅️ Урок {prev_num}', callback_data=f'lesson_{prev_num}')
            )

        if idx < len(all_numbers) - 1:
            next_num = all_numbers[idx + 1]
            nav_buttons.append(
                InlineKeyboardButton(f'Урок {next_num} ➡️', callback_data=f'lesson_{next_num}')
            )

    if nav_buttons:
        kb.add(*nav_buttons)

    kb.add(
        InlineKeyboardButton('📚 К урокам',     callback_data='menu_lessons'),
        InlineKeyboardButton('🏠 Главное меню', callback_data='menu_main'),
    )
    return kb


def back_to_main() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('⬅️ Главное меню', callback_data='menu_main'))
    return kb


def ask_city() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    for city in ['Almaty', 'Astana', 'Shymkent', 'Moscow', 'London', 'New York']:
        kb.add(InlineKeyboardButton(city, callback_data=f'weather_{city}'))
    kb.add(InlineKeyboardButton('⬅️ Главное меню', callback_data='menu_main'))
    return kb


def ask_country() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    for c in ['Kazakhstan', 'Russia', 'Germany', 'Japan', 'France', 'USA']:
        kb.add(InlineKeyboardButton(c, callback_data=f'country_{c}'))
    kb.add(InlineKeyboardButton('⬅️ Главное меню', callback_data='menu_main'))
    return kb


def validate_menu() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=2)
    for label, data in [
        ('📧 Email',    'validate_email'),
        ('📱 Телефон',  'validate_phone'),
        ('🔗 URL',      'validate_url'),
        ('🖥 IP-адрес', 'validate_ip'),
        ('🎨 HEX-цвет', 'validate_color'),
    ]:
        kb.add(InlineKeyboardButton(label, callback_data=data))
    kb.add(InlineKeyboardButton('⬅️ Главное меню', callback_data='menu_main'))
    return kb


def benchmark_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(
        InlineKeyboardButton('1 000',  callback_data='bench_1000'),
        InlineKeyboardButton('10 000', callback_data='bench_10000'),
        InlineKeyboardButton('50 000', callback_data='bench_50000'),
    )
    kb.add(InlineKeyboardButton('⬅️ Главное меню', callback_data='menu_main'))
    return kb
