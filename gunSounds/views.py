from django.shortcuts import render
from .models import Gun

def sound_list(request):
    guns = Gun.objects.all()

    ammo_type = request.GET.get('ammo_type')
    size = request.GET.get('size')
    # sort is unused, but you can handle it if needed

    if ammo_type:
        guns = guns.filter(ammo_type=ammo_type)
    if size:
        guns = guns.filter(size=size)

    ammo_types = Gun.objects.values_list('ammo_type', flat=True).distinct()
    sizes = Gun.objects.values_list('size', flat=True).distinct()

    return render(request, "gunSounds/list.html", {
        "guns": guns,
        "ammo_types": ammo_types,
        "sizes": sizes,
        "selected_ammo_type": ammo_type,
        "selected_size": size,
    })
