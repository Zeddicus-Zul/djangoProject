#!/bin/bash
set -e

source venv/bin/activate

# Use prod settings; default to local TCP Postgres on 127.0.0.1:5432.
# Set DB_PASSWORD in your shell to avoid the hardcoded default.
export DJANGO_SETTINGS_MODULE=mysite.settings.prod
export DB_HOST=${DB_HOST:-127.0.0.1}
export DB_PORT=${DB_PORT:-5432}
export DB_NAME=${DB_NAME:-gun_sounds_db}
export DB_USER=${DB_USER:-gun_sounds_user}
export DB_PASSWORD=${DB_PASSWORD:-rocklee123}

python manage.py migrate --noinput
python manage.py runserver "$@"
