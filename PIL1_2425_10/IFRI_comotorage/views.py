from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Location, UserProfile
import json
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .forms import RegisterForm, UserProfileForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def index(request):
    return render(request, 'IFRI_comotorage/index.html')

def Accueil(request):
    return render(request, 'IFRI_comotorage/Accueil.html')

def Login(request):
    form = forms.LoginForm()
    reg_form = forms.RegisterForm()
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
        'reg_form': reg_form,
        'message': message
    })

def register(request):
    if request.method == 'POST':
        form = forms.RegisterForm(request.POST)
        login_form = forms.LoginForm()
                 
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

@login_required
def Profil(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    context = {
        'user': request.user,
        'profile': profile
    }
    return render(request, 'IFRI_comotorage/Profil.html', context)

@login_required
def profile_config(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès!')
            return redirect('Profil')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': request.user,
        'profile': profile
    }
    return render(request, 'IFRI_comotorage/profile_config.html', context)

def save_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        lat = data.get('lat')
        lon = data.get('lon')
        Location.objects.create(name=name, latitude=lat, longitude=lon)
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)