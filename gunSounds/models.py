from django.db import models

# Create your models here. A model serves as a table in Django's database. The class is an attribute
# and the "variables" are the attributes (Columns) with their data type. 
class Gun(models.Model):
    gun_name = models.CharField(max_length=200)
    audio_file = models.FileField(upload_to='audio/')
    
    
    #how to store and play sounds in a django app
    #get one gun with one sound to play
    
    
    #Migrations are very powerful and let you change your models over time, as you develop your project, without the need to delete your database or tables and make new ones - it specializes in upgrading your database live, without losing data. We’ll cover them in more depth in a later part of the tutorial, but for now, remember the three-step guide to making model changes:
    #Change your models (in models.py).
    #Run python manage.py makemigrations to create migrations for those changes
    #Run python manage.py migrate to apply those changes to the database.
    #The reason that there are separate commands to make and apply migrations is because you’ll commit migrations to your version control system and ship them with your app; they not only make your development easier, they’re also usable by other developers and in production"""