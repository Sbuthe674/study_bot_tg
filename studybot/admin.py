from django.contrib import admin
from django.utils.html import format_html
from .models import UserQuery, Lesson


@admin.register(UserQuery)
class UserQueryAdmin(admin.ModelAdmin):
    list_display   = ('display_user', 'telegram_id', 'command', 'query_text', 'display_time')
    list_filter    = ('command', 'created_at')
    search_fields  = ('username', 'first_name', 'query_text', 'telegram_id')
    readonly_fields = ('telegram_id', 'username', 'first_name', 'command',
                       'query_text', 'response_text', 'created_at')
    ordering = ('-created_at',)

    @admin.display(description='Пользователь')
    def display_user(self, obj):
        name = obj.username or obj.first_name or '—'
        return format_html('<b>{}</b>', name)

    @admin.display(description='Время')
    def display_time(self, obj):
        return obj.created_at.strftime('%d.%m.%Y %H:%M')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return True


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display  = ('number', 'title', 'display_status', 'updated_at')
    list_filter   = ('is_active',)
    search_fields = ('title', 'content')
    ordering      = ('number',)
    list_editable = ('is_active',)

    fieldsets = (
        ('Основное', {
            'fields': ('number', 'title', 'is_active')
        }),
        ('Содержание', {
            'fields': ('content',),
            'description': 'Текст который бот отправит пользователю. '
                           'Можно использовать *жирный* и _курсив_ (Markdown Telegram).'
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    @admin.display(description='Статус')
    def display_status(self, obj):
        if obj.is_active:
            return format_html('<span style="color:green;">✅ Активен</span>')
        return format_html('<span style="color:red;">❌ Скрыт</span>')


admin.site.site_header = '🤖 StudyBot — Панель управления'
admin.site.site_title  = 'StudyBot Admin'
admin.site.index_title = 'Управление ботом'
