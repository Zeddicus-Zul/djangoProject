# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

EXPOSE 8080

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install --upgrade pip && python -m pip install -r requirements.txt

# Set working directory and copy project files
WORKDIR /app
COPY . /app

# Set Python path if needed (optional)
ENV PYTHONPATH=/app

# Run migrations at build time to bake the SQLite database
RUN python manage.py makemigrations
RUN python manage.py migrate

# Collect static files
RUN python manage.py collectstatic --noinput

# Start the Gunicorn server
CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-8080} mysite.wsgi:application --workers 3 --chdir /app"]
