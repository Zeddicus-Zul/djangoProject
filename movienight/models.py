from django.db import models


class MovieSuggestion(models.Model):
    title = models.CharField(max_length=200)
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
