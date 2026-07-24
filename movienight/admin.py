from django.contrib import admin
from .models import MovieSuggestion, MovieNightImage, PickedMovie


class MovieSuggestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'session_key', 'created_at')
    search_fields = ('title',)


class MovieNightImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'generated_at')
    readonly_fields = ('prompt_used',)


class PickedMovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'mode', 'chosen_at')
    list_filter = ('mode',)
    search_fields = ('title',)


admin.site.register(MovieSuggestion, MovieSuggestionAdmin)
admin.site.register(MovieNightImage, MovieNightImageAdmin)
admin.site.register(PickedMovie, PickedMovieAdmin)
