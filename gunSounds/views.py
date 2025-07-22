from django.shortcuts import render

def sound_list(request):
    # Prepare all 10 increments for Frontier 73C
    sounds = [
        {
            "title": "Frontier 73C",
            "img": "gunSounds/images/Frontier_73C.jpg",
            "audio_clips": [
                {"label": "100m", "path": "gunSounds/audio/Frontier73C_100.wav"},
                {"label": "200m", "path": "gunSounds/audio/Frontier73C_200.wav"},
                {"label": "300m", "path": "gunSounds/audio/Frontier73C_300.wav"},
                {"label": "400m", "path": "gunSounds/audio/Frontier73C_400.wav"},
                {"label": "500m", "path": "gunSounds/audio/Frontier73C_500.wav"},
                {"label": "600m", "path": "gunSounds/audio/Frontier73C_600.wav"},
                {"label": "700m", "path": "gunSounds/audio/Frontier73C_700.wav"},
                {"label": "800m", "path": "gunSounds/audio/Frontier73C_800.wav"},
                {"label": "900m", "path": "gunSounds/audio/Frontier73C_900.wav"},
                {"label": "1000m", "path": "gunSounds/audio/Frontier73C_1000.wav"},
            ],
        }
    ]
    return render(request, "gunSounds/list.html", {"sounds": sounds})
