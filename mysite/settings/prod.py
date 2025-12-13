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

# Database - use Cloud SQL connector in production
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "postgres"),
        "USER": os.getenv("DB_USER", "postgres"),
        "PASSWORD": os.getenv("DB_PASSWORD", ""),
        "HOST": os.getenv("DB_HOST", "127.0.0.1"),
        "PORT": os.getenv("DB_PORT", "5432"),
    }
}

# --- Google Cloud Storage Configuration ---
GS_PROJECT_ID = "portfoliosite-468605"
GS_STATIC_BUCKET_NAME = "portfoliosite-static-files"
GS_MEDIA_BUCKET_NAME = "portfoliosite-media-files"
GS_QUERYSTRING_AUTH = False  # Don't require signed URLs for public files
GS_DEFAULT_ACL = None  # Use bucket-level permissions (uniform bucket-level access)
GS_FILE_OVERWRITE = True  # Overwrite files with same name

# Static and Media URLs from GCS
STATIC_URL = f"https://storage.googleapis.com/{GS_STATIC_BUCKET_NAME}/"
MEDIA_URL = f"https://storage.googleapis.com/{GS_MEDIA_BUCKET_NAME}/"

# Configure storage backends to use GCS
STORAGES = {
    "default": {  # For media files (user uploads, images, audio)
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "bucket_name": GS_MEDIA_BUCKET_NAME,
            "project_id": GS_PROJECT_ID,
        },
    },
    "staticfiles": {  # For static files (CSS, JS)
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "bucket_name": GS_STATIC_BUCKET_NAME,
            "project_id": GS_PROJECT_ID,
        },
    },
}
