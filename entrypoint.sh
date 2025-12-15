#!/bin/sh
set -e

export RUNNING_IN_CLOUD_RUN=true

echo "Running Django migrations..."
python manage.py migrate --noinput

echo "Populating data from GCS buckets..."
python manage.py populate_from_gcs

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn on port 8080..."
exec gunicorn \
  --bind 0.0.0.0:8080 \
  --workers 2 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile - \
  mysite.wsgi:application
