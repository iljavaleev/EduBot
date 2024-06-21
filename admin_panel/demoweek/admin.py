from django.contrib import admin
from notifications.admin import FieldFormatter, NotificationAdmin

from .models import DemoDay


@admin.register(DemoDay)
class DemoDayAdmin(FieldFormatter, NotificationAdmin):
    list_display = ['weekday', '_text']
    fields = ['weekday', 'text', 'preview']

    def _text(self, day: DemoDay) -> str:
        return f"{day.text[:50]}..."
