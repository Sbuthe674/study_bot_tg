"""
bot/management/commands/runbot.py
Запуск бота через: python manage.py runbot
"""
from django.core.management.base import BaseCommand
import telebot


class Command(BaseCommand):
    help = 'Запустить Telegram-бота'

    def handle(self, *args, **options):
        self.stdout.write('🤖 Запуск StudyBot...')
        # Импортируем здесь, чтобы Django уже был инициализирован
        from telegram_bot import bot
        try:
            bot.infinity_polling(timeout=10, long_polling_timeout=5, logger_level=None)
        except KeyboardInterrupt:
            self.stdout.write('🤖 StudyBot остановлен')
        except telebot.apihelper.ApiTelegramException as exc:
            self.stdout.write(self.style.ERROR(f'Ошибка Telegram API: {exc}'))
