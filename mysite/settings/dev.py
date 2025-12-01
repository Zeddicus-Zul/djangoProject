from .base import *
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# SQLite for quick local dev (inherits STORAGES for locall filess)
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
}


ENV_NAME = "dev" 
