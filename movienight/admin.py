from django.contrib import admin
from .models import MovieSuggestion


class MovieSuggestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'session_key', 'created_at')
    search_fields = ('title',)


admin.site.register(MovieSuggestion, MovieSuggestionAdmin)
