from .base import *
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# SQLite for quick local dev (inherits STORAGES for locall filess)
DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": BASE_DIR / "db.sqlite3"}
}


ENV_NAME = "dev" 


# If you prefer local Postgres in dev, swap the block above for this:
# import os
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": os.getenv("PGDATABASE", "gun_sounds_db"),
#         "USER": os.getenv("PGUSER", "postgres"),
#         "PASSWORD": os.getenv("PGPASSWORD", ""),
#         "HOST": os.getenv("PGHOST", "127.0.0.1"),
#         "PORT": int(os.getenv("PGPORT", "5432")),
#         "CONN_MAX_AGE": 0,
#     }
# }
