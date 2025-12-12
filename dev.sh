#!/bin/bash
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=mysite.settings.dev
python manage.py runserver
