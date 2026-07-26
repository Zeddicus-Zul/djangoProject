from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import requests

from .forms import JoinForm, LoginForm
from .models import Gun, AudioClip, MapMarker

def home(request):
    return render(request, 'gunSounds/home.html')

def about(request):
    return render(request, 'gunSounds/about.html')

def contact(request):
    return render(request, 'gunSounds/contact.html')

def map(request):
    context = {
        'is_admin': request.user.is_authenticated and request.user.is_staff
    }
    return render(request, 'gunSounds/map.html', context)

def quiz(request):
    import random
    from .models import Score
    
    selected_distance = request.GET.get('distance')
    selected_ammo_type = request.GET.get('ammo_type')
    selected_size = request.GET.get('size')
    
    valid_distances = ['100m', '200m', '320m', '400m', '490m']
    all_ammo_types = Gun.objects.values_list('ammo_type', flat=True).distinct().order_by('ammo_type')
    all_sizes = Gun.objects.values_list('size', flat=True).distinct().order_by('size')
    
    current_audio = None
    correct_gun = None
    guns_at_distance = []
    user_high_score = 0
    
    # Get user's high score if logged in
    if request.user.is_authenticated:
        try:
            score = Score.objects.get(user=request.user)
            user_high_score = score.high_score
        except Score.DoesNotExist:
            user_high_score = 0
    
    if selected_distance and selected_distance in valid_distances:
        guns_query = Gun.objects.filter(audio_clips__distance=selected_distance).distinct()
        
        if selected_ammo_type:
            guns_query = guns_query.filter(ammo_type__iexact=selected_ammo_type)
        if selected_size:
            guns_query = guns_query.filter(size__iexact=selected_size)
        
        guns_at_distance = guns_query
        audio_clips = AudioClip.objects.filter(distance=selected_distance, gun__in=guns_at_distance)
        
        if audio_clips.exists():
            current_audio = random.choice(audio_clips)
            correct_gun = current_audio.gun.id
    
    context = {
        'distances': valid_distances,
        'selected_distance': selected_distance,
        'ammo_types': all_ammo_types,
        'selected_ammo_type': selected_ammo_type,
        'sizes': all_sizes,
        'selected_size': selected_size,
        'guns': guns_at_distance,
        'current_audio': current_audio,
        'correct_gun_id': correct_gun,
        'user_high_score': user_high_score,
    }
    return render(request, 'gunSounds/quiz.html', context)

def sound_list(request):
    # All guns are always sent to the page; filtering happens client-side in
    # JS so switching filters doesn't need a full page reload. The GET params
    # still set the initial active filter (so a shared/bookmarked filtered
    # URL still opens correctly).
    guns = Gun.objects.all()

    selected_ammo_type = request.GET.get('ammo_type')
    selected_size = request.GET.get('size')

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

def join(request):
    if (request.method == "POST"):
        join_form = JoinForm(request.POST)
        if (join_form.is_valid()):
            # Save form data to DB
            user = join_form.save()
            # Encrypt the password
            user.set_password(user.password)
            # Save encrypted password to DB
            user.save()
            # Success! Redirect to home page.
            return redirect("/")
        else:
            # Form invalid, print errors to console
            page_data = { "join_form": join_form }
            return render(request, 'gunSounds/join.html', page_data)
    else:
        join_form = JoinForm()
        page_data = { "join_form": join_form }
        return render(request, 'gunSounds/join.html', page_data)

def user_login(request):
    if (request.method == 'POST'):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # First get the username and password supplied
            username = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            # Django's built-in authentication function:
            user = authenticate(username=username, password=password)
            # If we have a user
            if user:
                #Check it the account is active
                if user.is_active:
                    # Log the user in.
                    login(request,user)
                    # Send the user back to homepage
                    return redirect('home')
                else:
                    # If account is not active:
                    return HttpResponse("Your account is not active.")
            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(username,password))
                return render(request, 'gunSounds/login.html', {"login_form": LoginForm})
    else:
        #Nothing has been provided for username or password.
        return render(request, 'gunSounds/login.html', {"login_form": LoginForm})

@login_required(login_url='/gunSounds/login/')
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return redirect('home')


@login_required(login_url='/gunSounds/login/')
def save_score(request):
    from django.http import JsonResponse
    from .models import Score
    
    if request.method == 'POST':
        score = request.POST.get('score', 0)
        try:
            score = int(score)
        except (ValueError, TypeError):
            return JsonResponse({'error': 'Invalid score'}, status=400)
        
        # Get or create user's score record
        user_score, created = Score.objects.get_or_create(user=request.user)
        
        # Check if this is a new high score
        is_new_high = score > user_score.high_score
        
        # Update high score if new score is better
        if is_new_high:
            user_score.high_score = score
            user_score.save()
        
        return JsonResponse({
            'success': True,
            'high_score': user_score.high_score,
            'is_new_high': is_new_high
        })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def server_info(request):
    server_geodata = requests.get('https://ipwhois.app/json/').json()
    settings_dump = settings.__dict__
    return HttpResponse("{}{}".format(server_geodata, settings_dump))


@csrf_exempt
def save_marker(request):
    if request.method == 'POST':
        if not (request.user.is_authenticated and request.user.is_staff):
            return JsonResponse({'success': False, 'error': 'Not authorized'}, status=403)
        try:
            marker = MapMarker.objects.create(
                name=request.POST['name'],
                map_name=request.POST.get('map_name', 'stillwater'),
                latitude=request.POST['latitude'],
                longitude=request.POST['longitude'],
                marker_type=request.POST.get('marker_type', 'spawn'),
                photo=request.FILES.get('photo'),
            )
            return JsonResponse({
                'success': True,
                'id': marker.id,
                'photo_url': marker.photo.url if marker.photo else None,
                'message': 'Marker saved successfully'
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


def get_markers(request):
    map_name = request.GET.get('map_name', 'stillwater')
    markers = MapMarker.objects.filter(map_name=map_name)
    data = [
        {
            'id': m.id,
            'name': m.name,
            'latitude': m.latitude,
            'longitude': m.longitude,
            'marker_type': m.marker_type,
            'photo_url': m.photo.url if m.photo else None,
        }
        for m in markers
    ]
    return JsonResponse(data, safe=False)


@csrf_exempt
def delete_marker(request, marker_id):
    if request.method == 'DELETE':
        if not (request.user.is_authenticated and request.user.is_staff):
            return JsonResponse({'success': False, 'error': 'Not authorized'}, status=403)
        try:
            marker = MapMarker.objects.get(id=marker_id)
            marker.delete()
            return JsonResponse({'success': True, 'message': 'Marker deleted'})
        except MapMarker.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Marker not found'}, status=404)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
