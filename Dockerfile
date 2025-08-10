# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3-slim

EXPOSE 8080

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app
COPY huntProject/db.sqlite3 /app/huntProject/db.sqlite3
COPY huntProject/media /app/huntProject/media


ENV PYTHONPATH=/app/huntProject

RUN python huntProject/manage.py collectstatic --noinput


CMD ["sh", "-c", "exec gunicorn --bind 0.0.0.0:${PORT:-8080} mysite.wsgi:application --workers 3 --chdir /app/huntProject"]




