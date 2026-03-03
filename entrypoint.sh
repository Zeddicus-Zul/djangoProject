#!/bin/sh
set -e

# Detect environment: Cloud Run sets K_SERVICE automatically.
# On Compute Engine / MIG, set DJANGO_SETTINGS_MODULE via instance metadata or env.
if [ -n "$K_SERVICE" ]; then
  export RUNNING_IN_CLOUD_RUN=true
  echo "Detected Cloud Run (service: $K_SERVICE)"
else
  export RUNNING_IN_CLOUD_RUN=false
  echo "Not running in Cloud Run (Compute Engine / local)"
fi

# Use prod settings unless explicitly overridden
export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-mysite.settings.prod}"

echo "Running Django migrations..."
python manage.py migrate --noinput

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
