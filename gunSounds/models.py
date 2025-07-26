# gunSounds/models.py
from django.db import models

class Gun(models.Model):
    name = models.CharField(max_length=200)
    audio_file = models.FileField(upload_to='audio/')
    image = models.ImageField(upload_to='images/')
    ammo_type = models.CharField(max_length=10)
    size = models.CharField(max_length=10)

    def __str__(self):
        return self.name

from django.db import models

class Gun(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    ammo_type = models.CharField(max_length=10)
    size = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class AudioClip(models.Model):
    gun = models.ForeignKey(Gun, related_name='audio_clips', on_delete=models.CASCADE)
    label = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='audio/')

    def __str__(self):
        return f"{self.gun.name} - {self.label}"
