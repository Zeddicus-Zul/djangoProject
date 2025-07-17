from django.urls import path
from . import views

urlpatterns = [
    path('', views.sound_list, name='sound_list'),
]
