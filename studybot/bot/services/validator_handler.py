"""
bot/services/validator_handler.py
Regex — Lab 4: обработчик команды /validate

Использует regex_helpers.py для проверки форматов.
"""
from .base_handler import BaseHandler
from ..utils.regex_helpers import validate, DESCRIPTIONS


class ValidatorHandler(BaseHandler):
    """Валидирует текст через регулярные выражения."""

    HELP_TEXT = (
        '❗ Использование: /validate <тип> <текст>\n\n'
        'Доступные типы:\n'
        '  email — адрес эл. почты\n'
        '  phone — номер телефона\n'
        '  url   — ссылка\n'
        '  ip    — IP-адрес\n'
        '  num   — числовое значение\n'
        '  color — HEX-цвет (#FF0000)\n\n'
        'Пример: /validate email test@mail.com'
    )

    def handle(self, message):
        parts = message.text.strip().split(maxsplit=2)

        if len(parts) < 3:
            self._bot.reply_to(message, self.HELP_TEXT)
            return

        type_  = parts[1].lower()
        text   = parts[2]
        result = validate(type_, text)

        if result['ok']:
            response = (
                f'✅ *{result["type"]} найден!*\n\n'
                f'Найдено: `{result["found"]}`\n'
                f'Паттерн: `{result["pattern"]}`'
            )
        else:
            response = (
                f'❌ *Не найдено*\n\n'
                f'{result.get("msg", "Совпадений нет")}\n'
                f'Паттерн: `{result.get("pattern", "—")}`'
            )

        self._bot.reply_to(message, response, parse_mode='Markdown')
