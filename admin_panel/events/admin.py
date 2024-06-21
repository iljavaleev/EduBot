from django.contrib import admin, messages
from notifications.admin import FieldFormatter, NotificationAdmin

from .models import Event, EventNotification


@admin.register(EventNotification)
class EventNotificationAdmin(FieldFormatter, NotificationAdmin):
    fields = ["event", "text", "notification_type", "preview"]
    list_display = ["_text", "event", "updated_at"]

    def event(self, event_not: EventNotification) -> str:
        return event_not.event.title


@admin.register(Event)
class EventAdmin(FieldFormatter, admin.ModelAdmin):
    list_display = ["title", "date", "is_complete", "do_broadcast"]

    def save_model(self, request, obj, form, change):
        if obj.do_broadcast:
            messages.add_message(request, messages.INFO, 'Link has been sent')
        super(EventAdmin, self).save_model(request, obj, form, change)
