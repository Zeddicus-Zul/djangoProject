from .base import *
import os

ENV_NAME = "prod"  

DEBUG = os.getenv("DJANGO_DEBUG", "").lower() in {"1", "true", "yes"}


# For local VM testing, allow your external IP and localhost
ALLOWED_HOSTS = [
    "136.118.95.21",
    "localhost",
    "127.0.0.1",
    "gun-sounds-app-1096649553455.us-west1.run.app",
]

# --- Use SQLite for local VM testing ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

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
