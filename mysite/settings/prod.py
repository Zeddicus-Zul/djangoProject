from .base import *
import os

ENV_NAME = "prod"  

DEBUG = os.getenv("DJANGO_DEBUG", "").lower() in {"1", "true", "yes"}


# For local VM testing, allow your external IP and localhost
ALLOWED_HOSTS = [
    "136.118.95.21",
    "localhost",
    "127.0.0.1",
]

# --- Use SQLite for local VM testing ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- Cloud SQL config (commented out for now) ---
# DB_NAME = os.getenv("DB_NAME", "gun_sounds_db")
# DB_USER = os.getenv("DB_USER", "gun_sounds_user")
# DB_PASSWORD = os.getenv("DB_PASSWORD", "")
# INSTANCE = os.getenv(
#     "CLOUD_SQL_CONNECTION_NAME",
#     os.getenv("INSTANCE_CONNECTION_NAME", "portfoliosite-468605:us-west1:portfoliosite-database")
# )
# USE_UNIX_SOCKET = os.getenv("DB_USE_SOCKET", "1") == "1"
# if USE_UNIX_SOCKET:
#     DB_SOCKET_DIR = os.getenv("DB_SOCKET_DIR", "/cloudsql")
#     DATABASES = { ... }
# else:
#     DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
#     DB_PORT = int(os.getenv("DB_PORT", "6543"))
#     DATABASES = { ... }

# --- Use local storage for static and media files for testing ---
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": BASE_DIR / "media",
        },
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

# --- GCS storage config (commented out for now) ---
# GS_PROJECT_ID = "portfoliosite-468605"
# GS_STATIC_BUCKET_NAME = "portfoliosite_static_bucket"
# GS_MEDIA_BUCKET_NAME = "portfoliosite_media_bucket"
# GS_QUERYSTRING_AUTH = False
# STORAGES = { ... }
