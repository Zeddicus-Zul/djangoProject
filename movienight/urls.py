from django.urls import path
from . import views

app_name = "movienight"

urlpatterns = [
    path("", views.movie_night, name="movie_night"),
    path("add/", views.add_suggestion, name="add_suggestion"),
    path("edit/<int:pk>/", views.edit_suggestion, name="edit_suggestion"),
    path("delete/<int:pk>/", views.delete_suggestion, name="delete_suggestion"),
    path("generate/", views.trigger_generation, name="trigger_generation"),
]
