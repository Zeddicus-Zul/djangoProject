from django.shortcuts import render

def sound_list(request):
    sounds = [
        {"title": "Picard Song", "path": "gunSounds/audio/picard.mp3"},
    ]
    return render(request, "gunSounds/list.html", {"sounds": sounds})
