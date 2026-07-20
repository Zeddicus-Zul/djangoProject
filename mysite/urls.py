from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path("healthz", views.healthz, name="healthz"),       # MIG health check (intercepted on Cloud Run)
    path("-/health", views.healthz, name="health_alt"),    # Alternative path (works everywhere)
    path("", views.landing, name="landing"),
    path("movienight/", views.movie_night, name="movie_night"),
    path("gunsounds/", include("gunSounds.urls")),
    path("admin/", admin.site.urls),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
