from django.contrib import admin
from django.contrib.auth.models import Group, User

from .models import BotAdmin, BotUser

admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        return {}


@admin.register(BotAdmin)
class BotAdminAdmin(admin.ModelAdmin):
    list_display = [
        "chat_id",
        "get_preview",
    ]


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = [
        "username",
        "email",
        "phone",
        "get_articles",
        "get_demo_week",
    ]
    list_filter = [
        "username",
        "email",
        "phone",
    ]
