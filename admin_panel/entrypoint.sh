#!/bin/bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --noinput ||
python manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:8000 admin_panel.wsgi

