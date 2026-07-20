import logging
import threading

from django.shortcuts import get_object_or_404, redirect, render

from .models import MovieNightImage, MovieSuggestion

logger = logging.getLogger(__name__)


def _get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def _generate_image_safely():
    from .services import generate_movie_night_image
    try:
        generate_movie_night_image()
    except Exception:
        logger.exception("Movie night image generation failed")


def movie_night(request):
    session_key = request.session.session_key
    suggestions = [
        {"obj": s, "is_owner": s.session_key == session_key}
        for s in MovieSuggestion.objects.order_by("-created_at")
    ]
    movie_image = MovieNightImage.objects.order_by("-generated_at").first()
    return render(request, "movienight/movie_night.html", {"suggestions": suggestions, "movie_image": movie_image})


def add_suggestion(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title:
            MovieSuggestion.objects.create(title=title[:200], session_key=_get_session_key(request))
            threading.Thread(target=_generate_image_safely, daemon=True).start()
    return redirect("movienight:movie_night")


def edit_suggestion(request, pk):
    suggestion = get_object_or_404(MovieSuggestion, pk=pk)
    if suggestion.session_key != request.session.session_key:
        return redirect("movienight:movie_night")
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title:
            suggestion.title = title[:200]
            suggestion.save()
        return redirect("movienight:movie_night")
    return render(request, "movienight/edit_suggestion.html", {"suggestion": suggestion})


def delete_suggestion(request, pk):
    suggestion = get_object_or_404(MovieSuggestion, pk=pk)
    if request.method == "POST" and suggestion.session_key == request.session.session_key:
        suggestion.delete()
    return redirect("movienight:movie_night")
