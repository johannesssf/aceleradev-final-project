from django.contrib import admin

from .models import Record


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = (
        'origin',
        'environment',
        'level',
        'message',
        'date',
        'is_archived',
        'user_id',
    )
