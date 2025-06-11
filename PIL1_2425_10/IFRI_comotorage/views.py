from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Location
import json
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import RegisterForm

def index(request):
    return render(request, 'IFRI_comotorage/index.html')

def Accueil(request):
    return render(request, 'IFRI_comotorage/Accueil.html')

def Login(request):
    form = forms.LoginForm()
    reg_form = forms.RegisterForm()  # Ajouter le formulaire d'inscription
    message = ''
    
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username_or_email, password=password)
            
            if user is None:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is not None:
                login(request, user)
                message = f'Bonjour, {user.username}! Vous êtes connecté.'
                return redirect('Accueil')
            else:
                message = 'Identifiants invalides.'
        else:
            message = 'Erreur de validation du formulaire.'
    
    return render(request, 'IFRI_comotorage/Login.html', context={
        'form': form, 
        'reg_form': reg_form,  # Passer les deux formulaires
        'message': message
    })

def register(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        login_form = forms.LoginForm()  # Pour l'affichage
        
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Accueil')
        else:
            return render(request, 'IFRI_comotorage/Login.html', {
                'reg_form': form, 
                'form': login_form,
                'message': 'Erreur lors de l\'inscription.'
            })
    else:
        form = forms.RegisterForm()
        login_form = forms.LoginForm()
        
    return render(request, 'IFRI_comotorage/Login.html', {
        'reg_form': form,
        'form': login_form
    })

def user_logout(request):
    logout(request)
    return redirect('Login')

def Rechercher(request):
    return render(request, 'IFRI_comotorage/Rechercher.html')

def Publier(request):
    return render(request, 'IFRI_comotorage/Publier.html')

def Messagerie(request, *args, **kwargs):
    return render(request, "IFRI_comotorage/Messagerie.html", context={})

def Profil(request):
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