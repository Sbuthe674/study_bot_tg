"""bot/admin.py — регистрируем модели в Django-админке"""
from django.contrib import admin
from django.utils.html import format_html

from .models import UserQuery


@admin.register(UserQuery)
class UserQueryAdmin(admin.ModelAdmin):
    list_display = ('display_user', 'telegram_id', 'command', 'query_text', 'display_time')
    list_filter = ('command', 'created_at')
    search_fields = ('username', 'query_text')
    readonly_fields = ('telegram_id', 'username', 'command', 'query_text', 'response_text', 'created_at')
    ordering = ('-created_at',)

    @admin.display(description='Пользователь')
    def display_user(self, obj):
        name = obj.username or '—'
        return format_html('<strong>{}</strong>', name)

    @admin.display(description='Время')
    def display_time(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M')


admin.site.site_header = 'Уроки, запросы пользователей и настройки бота'
admin.site.site_title = 'StudyBot'
admin.site.index_title = 'Панель управления'
