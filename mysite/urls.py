from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.shortcuts import render

def landing(request):
    return render(request, 'landing.html')


urlpatterns = [
    path("", landing),
    path("gunsounds/", include("gunSounds.urls")),
    path("admin/", admin.site.urls),
    path("server_info/", include("gunSounds.urls")),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

