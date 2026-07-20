from django.db import models


class MovieSuggestion(models.Model):
    title = models.CharField(max_length=200)
    session_key = models.CharField(max_length=40)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class MovieNightImage(models.Model):
    image = models.ImageField(upload_to="movienight/generated/")
    prompt_used = models.TextField()
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Movie night image ({self.generated_at:%Y-%m-%d %H:%M})"
