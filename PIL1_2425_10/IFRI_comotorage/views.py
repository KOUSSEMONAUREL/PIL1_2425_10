from django.shortcuts import render
from django.http import JsonResponse
from .models import Location
import json 
from . import forms
from django.contrib.auth import login, authenticate 

def index (request):
    return render(request, 'IFRI_comotorage/index.html')

def Accueil (request):
    return render(request, 'IFRI_comotorage/Accueil.html')

def Login (request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                message = f'Bonjour, {user.username}! Vous êtes connecté.'
            else:
                message = 'Identifiants invalides.'
    return render(request, 'IFRI_comotorage/Login.html', context={'form': form, 'message': message})

def Rechercher (request):
    return render(request, 'IFRI_comotorage/Rechercher.html')

def Publier (request):
    return render(request, 'IFRI_comotorage/Publier.html')

def Messagerie (request):
    return render(request, 'IFRI_comotorage/Messagerie.html')

def Profil (request):
    return render(request, 'IFRI_comotorage/Profil.html')

def save_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        lat = data.get('lat')
        lon = data.get('lon')
        Location.objects.create(name=name, latitude=lat, longitude=lon)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)