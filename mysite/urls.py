from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect

def redirect_root(request):
    return redirect('/gunSounds/')


urlpatterns = [
    path("", redirect_root),
    path("gunSounds/", include("gunSounds.urls")),
    path("admin/", admin.site.urls),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

