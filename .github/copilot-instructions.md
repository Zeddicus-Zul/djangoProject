# Copilot Instructions for AI Agents

## Project Overview
- **Type:** Django web application for gun sound recognition and management
- **Main app:** `gunSounds` (models: `Gun`, `AudioClip`)
- **Purpose:** Serve and filter gun audio clips, with metadata and images, for in-game or reference use

## Architecture & Structure
- **Apps:**
  - `gunSounds/`: Core app with models, views, templates, static files
  - `mysite/`: Project settings, URLs, WSGI/ASGI
- **Settings:**
  - Modular: `mysite/settings/base.py`, `dev.py`, `prod.py`
  - Local dev uses SQLite; production uses Postgres (Cloud SQL) and Google Cloud Storage for static/media
- **Templates:** Located in `templates/gunSounds/` (e.g., `list.html`)
- **Static/media:**
  - Static: `static/gunSounds/`
  - Media: `media/images/` (for uploaded images)

## Developer Workflows
- **Run locally:**
  - `python3 manage.py runserver` (uses `dev.py` settings)
- **Build/Deploy (Cloud Run):**
  - Dockerfile provided; entrypoint uses Gunicorn and `mysite.wsgi:application`
  - Exposes port 8080 by default
- **Testing:**
  - Tests in `gunSounds/tests.py` (currently empty)
  - Run: `python3 manage.py test gunSounds`
- **Migrations:**
  - `python3 manage.py makemigrations gunSounds`
  - `python3 manage.py migrate`

## Patterns & Conventions
- **Model relationships:**
  - `Gun` has many `AudioClip` (via ForeignKey)
- **Filtering:**
  - Views filter `Gun` objects by `ammo_type` and `size` via GET params
- **Settings selection:**
  - Use `DJANGO_SETTINGS_MODULE` env var to pick settings (default: `mysite.settings`)
  - For production, override with `mysite.settings.prod` and set required env vars
- **Static/media in prod:**
  - Use Google Cloud Storage buckets (see `prod.py` for bucket names and config)

## External Integrations
- **Google Cloud Storage:**
  - For static and media files in production
- **Cloud SQL (Postgres):**
  - For production database
- **Dependencies:**
  - See `requirements.txt` (notably: `Django`, `pillow`, `django-storages`, `google-cloud-storage`, `gunicorn`, `psycopg`)

## Examples
- **Filtering guns in view:**
  ```python
  guns = Gun.objects.all()
  if selected_ammo_type:
      guns = guns.filter(ammo_type=selected_ammo_type)
  ```
- **Serving static/media in dev:**
  - Files are served from local `static/` and `media/` directories

## Key Files
- `gunSounds/models.py`, `views.py`, `templates/gunSounds/list.html`
- `mysite/settings/base.py`, `dev.py`, `prod.py`
- `Dockerfile`, `requirements.txt`, `manage.py`

---
For new features, follow the patterns in `gunSounds/` and update settings/migrations as needed. For deployment, ensure all required environment variables are set for production.
