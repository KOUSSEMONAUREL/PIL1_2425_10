# views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Location, UserProfile, RideOffer
import json
from . import forms
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
# Import the new RideOfferFormSet
from .forms import RegisterForm, UserProfileForm, UserUpdateForm, RideOfferFormSet
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone


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


@login_required
def Publier(request):
    if request.user.userprofile.type_utilisateur != 'conducteur':
        messages.warning(request, "Seuls les conducteurs peuvent publier des offres de trajets. Veuillez mettre à jour votre profil.")
        return redirect('profile_config')

    # Initialize a list to hold successfully published rides for display
    published_rides_summary = []

    if request.method == 'POST':
        formset = RideOfferFormSet(request.POST, prefix='ride') # Use a prefix
        if formset.is_valid():
            for form in formset:
                # Check if the form is not marked for deletion and has data
                if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                    try:
                        ride_offer = form.save(commit=False) # Don't save yet
                        ride_offer.driver = request.user # Assign the current user as the driver
                        ride_offer.save() # Now save
                        published_rides_summary.append(ride_offer) # Add to summary list
                    except Exception as e:
                        messages.error(request, f"Erreur lors de l'enregistrement d'un trajet: {e}")
            
            if published_rides_summary:
                messages.success(request, "Vos trajets ont été publiés avec succès!")
                # After successful publication, re-initialize an empty formset for new additions
                formset = RideOfferFormSet(prefix='ride') 
            else:
                messages.info(request, "Aucun nouveau trajet n'a été enregistré.")
        else:
            # If formset is not valid, messages will be displayed for each form's errors
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
            # The formset with errors will be passed to the template automatically
            
    else: # GET request
        formset = RideOfferFormSet(prefix='ride') # Initial empty formset

    context = {
        'formset': formset,
        'published_rides_summary': published_rides_summary, # Pass the list of published rides
    }
    return render(request, 'IFRI_comotorage/Publier.html', context)


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