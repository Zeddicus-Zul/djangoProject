import os
from pathlib import Path

# --- Base ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# Security
SECRET_KEY = os.getenv("django_settings", "dev-insecure-change-me")
DEBUG = os.getenv("DJANGO_DEBUG", "0") not in ("0", "false", "False")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", ".run.app,.a.run.app,localhost,127.0.0.1").split(",")

# Cloud Run sits behind a proxy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_TRUSTED_ORIGINS = [
    "https://*.run.app",
    "https://*.a.run.app",
]

# --- Applications -----------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",  # keep this for collectstatic
    "storages",                    # django-storages (GCS)
    # your app(s)
    "gunSounds",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mysite.urls"
WSGI_APPLICATION = "mysite.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]

# --- Database ---------------------------------------------------------------
DB_NAME = os.getenv("DB_NAME", "gun_sounds_db")
DB_USER = os.getenv("DB_USER", "gun_sounds_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Cloud SQL instance connection name (used for Unix socket)
INSTANCE_CONNECTION_NAME = os.getenv(
    "INSTANCE_CONNECTION_NAME",
    "portfoliosite-468605:us-west2:portfoliosite-database",
)

# If you're on your laptop and set LOCAL_DB_HOST/PORT, use those.
# Otherwise (in Cloud Run/Jobs), use the Unix socket path /cloudsql/<instance>.
LOCAL_DB_HOST = os.getenv("LOCAL_DB_HOST")
LOCAL_DB_PORT = os.getenv("LOCAL_DB_PORT", "5432")

if LOCAL_DB_HOST:
    DB_HOST = LOCAL_DB_HOST
    DB_PORT = LOCAL_DB_PORT
else:
    DB_HOST = f"/cloudsql/{INSTANCE_CONNECTION_NAME}"
    DB_PORT = ""  # not needed when using Unix socket

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

# --- Password validation ---------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Internationalization --------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static & Media via Google Cloud Storage -------------------------
GS_PROJECT_ID = "portfoliosite-468605"
GS_STATIC_BUCKET_NAME = "portfoliosite_static_bucket"
GS_MEDIA_BUCKET_NAME = "portfoliosite_media_bucket"

# Use public, unsigned URLs for GCS objects (avoids signing in Cloud Run)
GS_QUERYSTRING_AUTH = False

# Django 5+ STORAGES API
STORAGES = {
    # Default file storage (user uploads / media)
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "project_id": GS_PROJECT_ID,
            "bucket_name": GS_MEDIA_BUCKET_NAME,
            # critical: return plain public URLs, don’t try to sign
            "querystring_auth": False,
            "default_acl": None,
            # "file_overwrite": False,  # uncomment if you want to avoid overwriting same-name files
        },
    },
    # Static files storage (for collectstatic)
    "staticfiles": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
        "OPTIONS": {
            "project_id": GS_PROJECT_ID,
            "bucket_name": GS_STATIC_BUCKET_NAME,
        },
    },
}

# Public URLs served from GCS (static bucket should be public-read)
STATIC_URL = f"https://storage.googleapis.com/{GS_STATIC_BUCKET_NAME}/"
MEDIA_URL  = f"https://storage.googleapis.com/{GS_MEDIA_BUCKET_NAME}/"

# If you keep extra app-level static dirs (e.g., BASE_DIR / "static")
STATICFILES_DIRS = [BASE_DIR / "static"] if (BASE_DIR / "static").exists() else []

# --- Logging (simple) ------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": os.getenv("DJANGO_LOG_LEVEL", "INFO")},
}

# --- Default primary key type ----------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
