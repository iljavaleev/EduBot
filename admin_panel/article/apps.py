from django.apps import AppConfig


class ArticleConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "article"
    verbose_name = "article notifications"

    def ready(self):
        import article.signals
