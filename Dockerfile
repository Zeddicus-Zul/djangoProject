FROM python:3.12-slim

ENV DJANGO_SETTINGS_MODULE=mysite.settings.prod

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip && \   
    python -m pip install -r requirements.txt

COPY . /app

EXPOSE 80
# Entrypoint script runs migrations, collectstatic, then starts Gunicorn
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "mysite.wsgi:application", "--bind", "0.0.0.0:80"]
