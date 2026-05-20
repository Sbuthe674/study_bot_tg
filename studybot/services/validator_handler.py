from bot.services.base_handler import BaseHandler
from bot.utils.regex_helpers import validate

HELP_TEXT = (
    '❗ Использование: /validate <тип> <текст>\n\n'
    'Типы: email, phone, url, ip, num, color\n\n'
    'Пример: /validate email test@mail.com'
)


class ValidatorHandler(BaseHandler):
    def handle(self, message):
        parts = message.text.strip().split(maxsplit=2)
        if len(parts) < 3:
            self._bot.reply_to(message, HELP_TEXT)
            return
        result = validate(parts[1].lower(), parts[2])
        if result['ok']:
            text = (
                f'✅ *{result["type"]} найден!*\n\n'
                f'Найдено: `{result["found"]}`\n'
                f'Паттерн: `{result["pattern"]}`'
            )
        else:
            text = (
                f'❌ *Не найдено*\n\n'
                f'{result.get("msg", "Совпадений нет")}\n'
                f'Паттерн: `{result.get("pattern", "—")}`'
            )
        self._bot.reply_to(message, text, parse_mode='Markdown')
