"""
bot/services/lesson_handler.py
Команда /lesson — отправляет урок из базы данных.

Использование:
  /lesson        — список всех уроков
  /lesson 1      — содержание урока №1
"""
import django
from .base_handler import BaseHandler


class LessonHandler(BaseHandler):
    """Достаёт уроки из БД и отправляет пользователю."""

    def handle(self, message):
        parts = message.text.strip().split(maxsplit=1)

        if len(parts) == 1:
            # /lesson — показать список
            self._send_list(message)
        else:
            # /lesson 3 — показать конкретный урок
            try:
                number = int(parts[1])
                self._send_lesson(message, number)
            except ValueError:
                self._bot.reply_to(message, '❗ Укажи номер урока: /lesson 1')

    def _send_list(self, message):
        from bot.models import Lesson
        lessons = Lesson.objects.filter(is_active=True)

        if not lessons.exists():
            self._bot.reply_to(message, '📭 Уроков пока нет. Загляни позже!')
            return

        lines = ['📚 *Доступные уроки:*\n']
        for lesson in lessons:
            lines.append(f'  {lesson.number}. {lesson.title}')
        lines.append('\n_Чтобы открыть урок: /lesson <номер>_')
        lines.append('_Пример: /lesson 1_')

        self._bot.reply_to(message, '\n'.join(lines), parse_mode='Markdown')

    def _send_lesson(self, message, number: int):
        from bot.models import Lesson
        try:
            lesson = Lesson.objects.get(number=number, is_active=True)
        except Lesson.DoesNotExist:
            self._bot.reply_to(
                message,
                f'❌ Урок №{number} не найден.\n\nСписок уроков: /lesson'
            )
            return

        text = (
            f'📖 *Урок {lesson.number}: {lesson.title}*\n'
            f'{"─" * 30}\n\n'
            f'{lesson.content}\n\n'
            f'{"─" * 30}\n'
            f'_/lesson — вернуться к списку_'
        )
        self._bot.reply_to(message, text, parse_mode='Markdown')
