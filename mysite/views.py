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
        "description": "Suggest movies for movie night.",
        "url": "/movienight/",
        "available": True,
    },
]


def landing(request):
    return render(request, "landing.html", {"projects": PROJECTS})


def healthz(request):
    """Lightweight health-check endpoint for GCP load-balancer probes."""
    return HttpResponse("ok", content_type="text/plain", status=200)
