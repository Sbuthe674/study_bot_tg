"""
bot/models.py — Django ORM модели
"""
from django.db import models


class UserQuery(models.Model):
    telegram_id   = models.BigIntegerField(verbose_name='Telegram ID')
    username      = models.CharField(max_length=100, blank=True, verbose_name='Username')
    first_name    = models.CharField(max_length=100, blank=True, verbose_name='Имя')
    command       = models.CharField(max_length=50, verbose_name='Команда')
    query_text    = models.TextField(verbose_name='Текст запроса')
    response_text = models.TextField(verbose_name='Ответ бота')
    created_at    = models.DateTimeField(auto_now_add=True, verbose_name='Время')

    class Meta:
        verbose_name = 'Запрос пользователя'
        verbose_name_plural = 'Запросы пользователей'
        ordering = ['-created_at']

    def __str__(self):
        name = self.username or self.first_name or str(self.telegram_id)
        return f"{name} — {self.command} ({self.created_at:%d.%m.%Y %H:%M})"


class Lesson(models.Model):
    number     = models.PositiveIntegerField(unique=True, verbose_name='Номер урока')
    title      = models.CharField(max_length=200, verbose_name='Название')
    content    = models.TextField(verbose_name='Содержание (текст для бота)')
    is_active  = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлён')

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['number']

    def __str__(self):
        status = '✅' if self.is_active else '❌'
        return f"{status} Урок {self.number}: {self.title}"
