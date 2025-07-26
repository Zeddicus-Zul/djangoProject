from django.shortcuts import render
from .models import Gun

def sound_list(request):
    # Get all Gun objects from the database
    guns = Gun.objects.all()

    # Pass guns queryset to the template
    # Sends the whole list of gun objects to list.html
    return render(request, "gunSounds/list.html", {"guns": guns})

