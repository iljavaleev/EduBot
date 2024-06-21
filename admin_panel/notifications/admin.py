from botuser.models import BotAdmin
from django.contrib import admin, messages
from django.db import models
from django.forms import Textarea

from .models import Notification, NotificationContent


class FieldFormatter:
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }


class NotificationContentAdmin(FieldFormatter, admin.StackedInline):
    model = NotificationContent
    exclude = ["content_type"]
    extra = 0
    max_num = 10


class NotificationAdmin(admin.ModelAdmin):
    inlines = [NotificationContentAdmin]
    ordering = ["-updated_at"]
    date_hierarchy = "created_at"
    search_fields = ["text"]

    def _text(self, notification: Notification) -> str:
        return f"{notification.text[:50]}..."

    def save_model(self, request, obj, form, change):
        if obj.preview:
            if BotAdmin.objects.filter(get_preview=True).exists():
                messages.add_message(request, messages.INFO,
                                     'Preview in admin chat')
            else:
                messages.add_message(request, messages.ERROR,
                                     'Please, create bot admin to get preview')

        super(NotificationAdmin, self).save_model(request, obj, form, change)
