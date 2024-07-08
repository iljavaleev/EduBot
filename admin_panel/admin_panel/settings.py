import os
from pathlib import Path

from configurations import Configuration, values
from dotenv import load_dotenv

load_dotenv()


class Dev(Configuration):
    BASE_DIR = Path(__file__).resolve().parent.parent
    SECRET_KEY = os.environ.get("SECRET_KEY")

    DEBUG = values.BooleanValue(True)

    ALLOWED_HOSTS = ['*']

    INSTALLED_APPS = [
        "django.contrib.admin",
        "django_celery_beat",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "events.apps.EventsConfig",
        "celeryapp.apps.CeleryappConfig",
        "curator.apps.CuratorConfig",
        "demoweek.apps.DemoweekConfig",
        "notifications.apps.NotificationsConfig",
        "article.apps.ArticleConfig",
        "botuser.apps.BotuserConfig",
        "data.apps.DataConfig",
        "phonenumber_field",
        "import_export",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "admin_panel.urls"

    TEMPLATES = [
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [],
            "APP_DIRS": True,
            "OPTIONS": {
                "context_processors": [
                    "django.template.context_processors.debug",
                    "django.template.context_processors.request",
                    "django.contrib.auth.context_processors.auth",
                    "django.contrib.messages.context_processors.messages",
                ],
            },
        },
    ]

    WSGI_APPLICATION = "admin_panel.wsgi.application"

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB', default='postgres'),
            'USER': os.getenv('POSTGRES_USER', default='postgres'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
            'HOST': os.getenv('POSTGRES_HOST', default='db'),
            'PORT': os.getenv('POSTGRES_PORT', default=5432)
        }
    }

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth."
            "password_validation.UserAttributeSimilarityValidator",
        },
        {
            "NAME": "django.contrib.auth."
            "password_validation.MinimumLengthValidator",
        },
        {
            "NAME": "django.contrib.auth."
            "password_validation.CommonPasswordValidator",
        },
        {
            "NAME": "django.contrib.auth."
            "password_validation.NumericPasswordValidator",
        },
    ]

    LANGUAGE_CODE = "en-US"

    TIME_ZONE = "Europe/Moscow"

    USE_I18N = True

    USE_TZ = True

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

    MEDIA_URL = '/bot_media/'

    MEDIA_ROOT = os.path.join(BASE_DIR, 'bot_media')

    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER', 'amqp://guest:guest@rabbitmq:5672/')

    CELERY_TIMEZONE = 'Europe/Moscow'

    CELERY_TASK_DEFAULT_QUEUE = 'demo_week'


class Test(Dev):
    BASE_DIR = Path(__file__).resolve().parent.parent
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    CELERY_TASK_ALWAYS_EAGER = True

    TEST_RUNNER = "djcelery.contrib.test_runner.CeleryTestSuiteRunner"


class Prod(Dev):
    DEBUG = values.BooleanValue(False)
    allowed_hosts: str = os.environ.get("ALLOWED_HOSTS")
    ALLOWED_HOSTS = allowed_hosts.split() if allowed_hosts else "ALLOWED_HOSTS"
    allowed_csrf: str = os.environ.get("CSRF_TRUSTED_ORIGINS")
    CSRF_TRUSTED_ORIGINS = allowed_csrf.split() if allowed_hosts else "CSRF_TRUSTED_ORIGINS"
