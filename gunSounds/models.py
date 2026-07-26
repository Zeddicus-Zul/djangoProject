from django.db import models
from django.contrib.auth.models import User

class Gun(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    ammo_type = models.CharField(max_length=10)
    size = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class AudioClip(models.Model):
    DISTANCE_CHOICES = [
        ('100m', '100m'),
        ('200m', '200m'),
        ('320m', '320m'),
        ('400m', '400m'),
        ('490m', '490m'),
    ]
    
    gun = models.ForeignKey(Gun, related_name='audio_clips', on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='audio/')
    distance = models.CharField(max_length=10, choices=DISTANCE_CHOICES, default='100m')

    def __str__(self):
        return f"{self.gun.name} - {self.label}"


class Score(models.Model):
    user = models.OneToOneField(User, related_name='quiz_score', on_delete=models.CASCADE)
    high_score = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - High Score: {self.high_score}"


class MapMarker(models.Model):
    name = models.CharField(max_length=200)
    map_name = models.CharField(max_length=100, default='stillwater')
    latitude = models.FloatField()
    longitude = models.FloatField()
    marker_type = models.CharField(max_length=50, default='spawn')
    photo = models.ImageField(upload_to='markers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.map_name})"
