"""
bot/management/commands/runbot.py
Запуск бота через: python manage.py runbot
"""
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Запустить Telegram-бота'

    def handle(self, *args, **options):
        self.stdout.write('🤖 Запуск StudyBot...')
        # Импортируем здесь, чтобы Django уже был инициализирован
        from bot.telegram_bot import bot
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
