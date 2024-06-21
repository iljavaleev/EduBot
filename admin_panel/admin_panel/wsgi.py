import os

from configurations.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin_panel.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Prod")

application = get_wsgi_application()
