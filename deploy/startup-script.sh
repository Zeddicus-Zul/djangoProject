#!/bin/bash
# startup-script.sh — Instance template startup script for MIG VMs
# Attach this as the startup-script in your instance template metadata.
set -e

APP_DIR="/opt/huntProject"
REPO_URL="https://github.com/YOUR_USER/huntProject.git"  # <-- update this
BRANCH="main"

echo "=== Startup script begin ==="

# Install system deps
apt-get update -y
apt-get install -y python3 python3-venv python3-pip git

# Clone or pull latest code
if [ -d "$APP_DIR/.git" ]; then
  cd "$APP_DIR" && git fetch origin && git reset --hard "origin/$BRANCH"
else
  git clone --branch "$BRANCH" "$REPO_URL" "$APP_DIR"
fi

cd "$APP_DIR"

# Create venv and install deps
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# Run migrations
DJANGO_SETTINGS_MODULE=mysite.settings.prod ./venv/bin/python manage.py migrate --noinput

# Collect static (uploads to GCS via prod settings)
DJANGO_SETTINGS_MODULE=mysite.settings.prod ./venv/bin/python manage.py collectstatic --noinput

# Install and enable the systemd service
cp deploy/gunicorn.service /etc/systemd/system/gunicorn.service
systemctl daemon-reload
systemctl enable gunicorn
systemctl restart gunicorn

echo "=== Startup script done ==="
