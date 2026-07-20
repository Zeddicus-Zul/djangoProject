from django.http import HttpResponse
from django.shortcuts import render

PROJECTS = [
    {
        "title": "Gun Sounds Library",
        "description": "Learn every weapon sound in Hunt Showdown.",
        "url": "/gunsounds/",
        "available": True,
    },
    {
        "title": "Movie Night",
        "description": "Vote on movies and get an AI-generated poster for movie night. Coming soon.",
        "url": "/movienight/",
        "available": False,
    },
]


def landing(request):
    return render(request, "landing.html", {"projects": PROJECTS})


def healthz(request):
    """Lightweight health-check endpoint for GCP load-balancer probes."""
    return HttpResponse("ok", content_type="text/plain", status=200)


def movie_night(request):
    return render(request, "movie_night.html")
