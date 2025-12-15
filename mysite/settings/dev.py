from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "gun-sounds-app-1096649553455.us-west1.run.app", "zeddstudy.dev", "www.zeddstudy.dev"]

# SQLite for quick local dev
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
}

ENV_NAME = "dev"

# --- Google Cloud Storage Configuration for dev ---
GS_PROJECT_ID = "portfoliosite-468605"
GS_STATIC_BUCKET_NAME = "portfoliosite-static-files"
GS_MEDIA_BUCKET_NAME = "portfoliosite-media-files"
GS_QUERYSTRING_AUTH = False
GS_DEFAULT_ACL = None
GS_FILE_OVERWRITE = True

# Use GCS for media/static files in Cloud Run, local storage when running locally
if os.getenv("RUNNING_IN_CLOUD_RUN", "false").lower() == "true":
    # Cloud Run: use GCS
    STATIC_URL = f"https://storage.googleapis.com/{GS_STATIC_BUCKET_NAME}/"
    MEDIA_URL = f"https://storage.googleapis.com/{GS_MEDIA_BUCKET_NAME}/"
    
    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
            "OPTIONS": {
                "bucket_name": GS_MEDIA_BUCKET_NAME,
                "project_id": GS_PROJECT_ID,
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
            "OPTIONS": {
                "bucket_name": GS_STATIC_BUCKET_NAME,
                "project_id": GS_PROJECT_ID,
            },
        },
    }
else:
    # Local development: use local storage
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

