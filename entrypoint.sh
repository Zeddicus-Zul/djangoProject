#!/bin/sh
set -e

# Run database migrations
echo "Running Django migrations..."
python manage.py migrate --noinput

# Collect static files (optional, but common in prod)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
exec gunicorn mysite.wsgi:application --bind 0.0.0.0:8080
