from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from gunSounds import views as gunSounds_views

def redirect_root(request):
    return redirect('/gunSounds/')


urlpatterns = [
    path("", redirect_root),
    path("gunSounds/", include("gunSounds.urls")),
    path("admin/", admin.site.urls),
    path("server_info/", gunSounds_views.server_info),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

