FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN python -m pip install --upgrade pip && \   
    python -m pip install -r requirements.txt

COPY . /app

EXPOSE 8080
CMD ["sh","-c","exec gunicorn --bind 0.0.0.0:${PORT:-8080} mysite.wsgi:application --workers 3 --chdir /app"]
