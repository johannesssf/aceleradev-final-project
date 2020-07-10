from django.contrib import admin

from .models import User, Record


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'password')


def _short_message(obj):
    return f'"{obj.message[:15]}..."'


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        'origin',
        'environment',
        'level',
        _short_message,
        'date',
        'is_archived',
        'user_id',
    )
