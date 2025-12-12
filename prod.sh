#!/bin/bash
source venv/bin/activate
export DJANGO_SETTINGS_MODULE=mysite.settings.prod
python manage.py runserver
