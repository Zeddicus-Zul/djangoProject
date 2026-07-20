from django.shortcuts import get_object_or_404, redirect, render

from .models import MovieSuggestion


def _get_session_key(request):
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key


def movie_night(request):
    session_key = request.session.session_key
    suggestions = [
        {"obj": s, "is_owner": s.session_key == session_key}
        for s in MovieSuggestion.objects.order_by("-created_at")
    ]
    return render(request, "movienight/movie_night.html", {"suggestions": suggestions})


def add_suggestion(request):
    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        if title:
            MovieSuggestion.objects.create(title=title[:200], session_key=_get_session_key(request))
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
