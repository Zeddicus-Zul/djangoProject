#!/bin/bash
set -e

source venv/bin/activate
export DJANGO_SETTINGS_MODULE=mysite.settings.prod
export DB_PASSWORD="rocklee123"

python manage.py runserver "$@"
