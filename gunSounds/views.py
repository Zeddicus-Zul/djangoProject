from django.shortcuts import render
from .models import Gun

def sound_list(request):
    guns = Gun.objects.all()

    selected_ammo_type = request.GET.get('ammo_type')
    selected_size = request.GET.get('size')

    if selected_ammo_type:
        guns = guns.filter(ammo_type=selected_ammo_type)
    if selected_size:
        guns = guns.filter(size=selected_size)

    all_ammo_types = Gun.objects.values_list('ammo_type', flat=True).distinct().order_by('ammo_type')
    all_sizes = Gun.objects.values_list('size', flat=True).distinct().order_by('size')

    context = {
        'guns': guns,
        'ammo_types': all_ammo_types,
        'sizes': all_sizes,
        'selected_ammo_type': selected_ammo_type,
        'selected_size': selected_size,
    }
    return render(request, 'gunSounds/list.html', context)