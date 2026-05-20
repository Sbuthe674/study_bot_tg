"""bot/admin.py — регистрируем модели в Django-админке"""
from django.contrib import admin
from django.utils.html import format_html

from .models import BotUser, Lesson, LessonView, UserQuery


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'telegram_id', 'username', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('username', 'first_name', 'telegram_id')
    readonly_fields = ('telegram_id', 'created_at', 'updated_at')

    @admin.display(description='Имя')
    def get_name(self, obj):
        return obj.first_name or obj.username or '—'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'status', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('number', 'title')
    readonly_fields = ('created_at', 'updated_at')
    fields = ('number', 'title', 'content', 'is_active', 'created_at', 'updated_at')

    @admin.display(description='Статус')
    def status(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green;">✅ Активен</span>')
        return format_html('<span style="color: red;">❌ Неактивен</span>')


@admin.register(LessonView)
class LessonViewAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'created_at')
    list_filter = ('created_at', 'lesson')
    search_fields = ('user__username', 'lesson__title')
    readonly_fields = ('created_at',)


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
