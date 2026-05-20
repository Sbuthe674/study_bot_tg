"""
bot/utils/regex_helpers.py
Regex — Lab 4: валидация разных форматов.

Варианты из задания:
  Variant 1  — email
  Variant 2  — phone
  Variant 5  — URL
  Variant 6  — IP-адрес
  Variant 10 — числа
  Variant 15 — HEX-цвет
"""
import re

# Паттерны по вариантам Lab 4
PATTERNS = {
    'email': r'[\w.+-]+@[\w-]+\.[\w.]+',
    'phone': r'\+?[\d\s\-()\[\]]{7,15}',
    'url':   r'https?://[^\s]+',
    'ip':    r'\b(?:\d{1,3}\.){3}\d{1,3}\b',
    'num':   r'\b\d+(?:\.\d+)?\b',
    'color': r'#[0-9A-Fa-f]{6}\b',
}

DESCRIPTIONS = {
    'email': 'Email-адрес',
    'phone': 'Телефонный номер',
    'url':   'URL-ссылка',
    'ip':    'IP-адрес',
    'num':   'Числовое значение',
    'color': 'HEX-цвет',
}


def validate(type_: str, text: str) -> dict:
    """
    Проверяет текст по паттерну заданного типа.
    Возвращает словарь с результатом.
    """
    pattern = PATTERNS.get(type_)
    if not pattern:
        known = ', '.join(PATTERNS.keys())
        return {'ok': False, 'msg': f'Неизвестный тип. Доступны: {known}'}

    match = re.search(pattern, text)
    if match:
        return {
            'ok':      True,
            'found':   match.group(),
            'type':    DESCRIPTIONS.get(type_, type_),
            'pattern': pattern,
        }
    return {
        'ok':      False,
        'msg':     f'Паттерн {DESCRIPTIONS.get(type_, type_)} не найден в тексте.',
        'pattern': pattern,
    }


def extract_all(type_: str, text: str) -> list:
    """Извлекает ВСЕ совпадения паттерна из текста."""
    pattern = PATTERNS.get(type_)
    if not pattern:
        return []
    return re.findall(pattern, text)
