from django.apps import AppConfig


class DemoweekConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "demoweek"
    verbose_name = "Demo week"

    def ready(self):
        import demoweek.signals
