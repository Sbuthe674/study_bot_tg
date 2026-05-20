"""
bot/models.py — Django ORM модели
Сохраняем все запросы пользователей в базу данных.
"""
from django.db import models


class BotUser(models.Model):
    telegram_id = models.BigIntegerField(unique=True, verbose_name='Telegram ID')
    username    = models.CharField(max_length=100, blank=True, verbose_name='Username')
    first_name  = models.CharField(max_length=100, blank=True, verbose_name='Имя')
    created_at  = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at  = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Пользователь бота'
        verbose_name_plural = 'Пользователи бота'
        ordering = ['-created_at']

    def __str__(self):
        return self.username or self.first_name or str(self.telegram_id)


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


class LessonView(models.Model):
    user       = models.ForeignKey(BotUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    lesson     = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='Урок')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Просмотрено')

    class Meta:
        verbose_name = 'Просмотр урока'
        verbose_name_plural = 'Просмотры уроков'
        ordering = ['-created_at']
        unique_together = ('user', 'lesson')

    def __str__(self):
        return f"{self.user} — Урок {self.lesson.number}"


class UserQuery(models.Model):
    """Каждый запрос к боту сохраняется сюда."""
    telegram_id   = models.BigIntegerField(verbose_name='Telegram ID')
    username      = models.CharField(max_length=100, blank=True, verbose_name='Username')
    command       = models.CharField(max_length=50, verbose_name='Команда')
    query_text    = models.TextField(verbose_name='Текст запроса')
    response_text = models.TextField(verbose_name='Ответ бота')
    created_at    = models.DateTimeField(auto_now_add=True, verbose_name='Время')

    class Meta:
        verbose_name = 'Запрос пользователя'
        verbose_name_plural = 'Запросы пользователей'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username or self.telegram_id} — {self.command} ({self.created_at:%d.%m.%Y %H:%M})"
