from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from notifications.admin import FieldFormatter, NotificationAdmin

from .models import ArticleNotification


@admin.register(ArticleNotification)
class ArticleNotificationAdmin(
    FieldFormatter,
    ImportExportModelAdmin,
    NotificationAdmin
):
    fields = [
        "title",
        "text",
        "comment",
        "message_time",
        "preview",
        "notify_immediately",
        "is_complete",
    ]
    list_display = ["title", "is_complete", "updated_at"]
