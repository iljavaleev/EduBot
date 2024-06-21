import os

from celery import Celery
from configurations import importer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin_panel.settings")
os.environ.setdefault('DJANGO_CONFIGURATION', 'Dev')
importer.install()
app = Celery("admin_panel")
app.config_from_object("django.conf:settings", namespace="CELERY")
