#!/bin/sh
set -e

# Run database migrations
echo "Running Django migrations..."
python manage.py migrate --noinput

# Collect static files (optional, but common in prod)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create superuser if it doesn't exist
echo "Creating superuser if needed..."
python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'rocklee123')
    print('Superuser created')
else:
    print('Superuser already exists')
" || echo "Superuser creation skipped"

# Start Gunicorn
exec gunicorn mysite.wsgi:application --bind 0.0.0.0:8080
