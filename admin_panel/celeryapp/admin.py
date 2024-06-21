from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_celery_beat.admin import PeriodicTaskAdmin
from django_celery_beat.models import (
    ClockedSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
)


class CustomPeriodicTaskAdmin(PeriodicTaskAdmin):
    fieldsets = (
        (None, {
            'fields': ('name', 'task', 'enabled'),
            'classes': ('extrapretty', 'wide'),
        }),
        (_('Schedule'), {
            'fields': ('crontab', 'crontab_translation', 'start_time',
                       'last_run_at', 'one_off'),
            'classes': ('extrapretty', 'wide'),
        }),
        (_('Arguments'), {
            'fields': ('kwargs', ),
            'classes': ('extrapretty', 'in'),
        }),
    )

    def get_changeform_initial_data(self, request):
        return {
            'task': 'worker.celery.send_demo_day',
            'kwargs': '{"day": 0-6}',
        }


admin.site.unregister(IntervalSchedule)
admin.site.unregister(ClockedSchedule)
admin.site.unregister(SolarSchedule)
admin.site.unregister(PeriodicTask)
admin.site.register(PeriodicTask, CustomPeriodicTaskAdmin)
