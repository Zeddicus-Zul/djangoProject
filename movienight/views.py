import logging

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import MovieNightImage, MovieSuggestion

logger = logging.getLogger(__name__)


def _get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def _is_ajax(request):
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"


def _generate_image_safely():
    # Run synchronously within the request — Cloud Run throttles CPU once a
    # response is sent, so a background thread here would get starved/killed
    # before finishing (confirmed: zero log output, not even the exception).
    # Called from its own endpoint (trigger_generation) so the page itself
    # can respond instantly and let the client show a spinner while this runs.
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
    # Don't show a stale image once the list it was generated from is empty.
    movie_image = MovieNightImage.objects.order_by("-generated_at").first() if suggestions else None
    return render(request, "movienight/movie_night.html", {"suggestions": suggestions, "movie_image": movie_image})


def add_suggestion(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title:
            suggestion = MovieSuggestion.objects.create(title=title[:200], session_key=_get_session_key(request))
            if _is_ajax(request):
                return JsonResponse({
                    "id": suggestion.pk,
                    "title": suggestion.title,
                    "edit_url": reverse("movienight:edit_suggestion", args=[suggestion.pk]),
                    "delete_url": reverse("movienight:delete_suggestion", args=[suggestion.pk]),
                })
    if _is_ajax(request):
        return JsonResponse({"error": "invalid"}, status=400)
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
        return redirect(reverse("movienight:movie_night") + "?regenerate=1")
    return render(request, "movienight/edit_suggestion.html", {"suggestion": suggestion})


def delete_suggestion(request, pk):
    suggestion = get_object_or_404(MovieSuggestion, pk=pk)
    if request.method == "POST" and suggestion.session_key == request.session.session_key:
        suggestion.delete()
        if _is_ajax(request):
            return JsonResponse({"success": True})
    if _is_ajax(request):
        return JsonResponse({"error": "invalid"}, status=400)
    return redirect("movienight:movie_night")


def trigger_generation(request):
    if request.method != "POST":
        return JsonResponse({"error": "method not allowed"}, status=405)
    _generate_image_safely()
    has_suggestions = MovieSuggestion.objects.exists()
    movie_image = MovieNightImage.objects.order_by("-generated_at").first() if has_suggestions else None
    return JsonResponse({
        "has_suggestions": has_suggestions,
        "image_url": movie_image.image.url if movie_image else None,
    })
