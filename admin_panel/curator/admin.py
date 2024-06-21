from django.contrib import admin

from .models import CuratorChat


@admin.register(CuratorChat)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['chat_id', 'is_active']
