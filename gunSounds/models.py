from django.db import models

# Create your models here. A model serves as a table in Django's database. The class is an attribute
# and the "variables" are the attributes (Columns) with their data type. 
class Gun(models.Model):
    gun_name = models.CharField(max_length=200)
    audio_file = models.FileField(upload_to='audio/')
    
    
    #how to store and play sounds in a django app
    #get one gun with one sound to play