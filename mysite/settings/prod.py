from .base import *
import os

ENV_NAME = "prod"  

DEBUG = os.getenv("DJANGO_DEBUG", "").lower() in {"1", "true", "yes"}

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS", ".run.app,.a.run.app,localhost,127.0.0.1"
).split(",")

# --- Cloud SQL (socket by default; TCP optional) ---
DB_NAME = os.getenv("DB_NAME", "gun_sounds_db")
DB_USER = os.getenv("DB_USER", "gun_sounds_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
INSTANCE = os.getenv(
    "CLOUD_SQL_CONNECTION_NAME",
    os.getenv("INSTANCE_CONNECTION_NAME", "portfoliosite-468605:us-west2:portfoliosite-database")
)

USE_UNIX_SOCKET = os.getenv("DB_USE_SOCKET", "1") == "1"

if USE_UNIX_SOCKET:
    DB_SOCKET_DIR = os.getenv("DB_SOCKET_DIR", "/cloudsql")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASSWORD,
            "HOST": f"{DB_SOCKET_DIR}/{INSTANCE}",
            "PORT": "",
            "CONN_MAX_AGE": int(os.getenv("DB_CONN_MAX_AGE", "60")),
        }
    }
else:
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = int(os.getenv("DB_PORT", "6543"))
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
            "CONN_MAX_AGE": int(os.getenv("DB_CONN_MAX_AGE", "60")),
        }
    }

# --- GCS storages (same as your current config) ---
GS_PROJECT_ID = "portfoliosite-468605"
GS_STATIC_BUCKET_NAME = "portfoliosite_static_bucket"
GS_MEDIA_BUCKET_NAME = "portfoliosite_media_bucket"
GS_QUERYSTRING_AUTH = False

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "project_id": GS_PROJECT_ID,
            "bucket_name": GS_MEDIA_BUCKET_NAME,
            "querystring_auth": False,
            "default_acl": None,
        },
    },
    "staticfiles": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "project_id": GS_PROJECT_ID,
            "bucket_name": GS_STATIC_BUCKET_NAME,
        },
    },
}

STATIC_URL = f"https://storage.googleapis.com/{GS_STATIC_BUCKET_NAME}/"
MEDIA_URL  = f"https://storage.googleapis.com/{GS_MEDIA_BUCKET_NAME}/"
