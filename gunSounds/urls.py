from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('map/', views.map, name='map'),
    path('join/', views.join, name='join'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('quiz/', views.quiz, name='quiz'),
    path('save_score/', views.save_score, name='save_score'),
    path('server_info/', views.server_info, name='server_info'),
    path('sounds/', views.sound_list, name='sound_list'),
    path('api/markers/save/', views.save_marker, name='save_marker'),
    path('api/markers/get/', views.get_markers, name='get_markers'),
    path('api/markers/delete/<int:marker_id>/', views.delete_marker, name='delete_marker'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    
    
    
    
    
    
    
    
    
