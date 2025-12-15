FROM python:3.12-slim

ENV DJANGO_SETTINGS_MODULE=mysite.settings.prod

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies including netcat for Cloud SQL Proxy check
RUN apt-get update && \
    apt-get install -y netcat-openbsd curl && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    python -m pip install -r requirements.txt

# Copy application code
COPY . /app

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Entrypoint script runs migrations and collectstatic
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
