import os

from configurations.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin_panel.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Prod")

application = get_asgi_application()
