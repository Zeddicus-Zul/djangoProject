from django.contrib import admin
from .models import MovieSuggestion, MovieNightImage


class MovieSuggestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'session_key', 'created_at')
    search_fields = ('title',)


class MovieNightImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'generated_at')
    readonly_fields = ('prompt_used',)


admin.site.register(MovieSuggestion, MovieSuggestionAdmin)
admin.site.register(MovieNightImage, MovieNightImageAdmin)
