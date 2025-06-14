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
from django.core.serializers import serialize


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
    # Fetch all published ride offers
    all_ride_offers = RideOffer.objects.all()

    # Serialize ride offer data to JSON for use in JavaScript
    # We'll manually build a list of dictionaries for easier JavaScript consumption
    ride_offers_data = []
    for ride in all_ride_offers:
        ride_offers_data.append({
            # 'id': ride.id,
            'driver': ride.driver.username,
            'departure_location': ride.departure_location,
            # 'departure_latitude': ride.departure_latitude,
            # 'departure_longitude': ride.departure_longitude,
            'arrival_location': ride.arrival_location,
            # 'arrival_latitude': ride.arrival_latitude,
            # 'arrival_longitude': ride.arrival_longitude,
            'departure_time': ride.departure_time.strftime('%H:%M'), # Format time
            'available_seats': ride.available_seats,
        })

    context = {
        'ride_offers_json': json.dumps(ride_offers_data) # Convert list of dicts to JSON string
    }
    return render(request, 'IFRI_comotorage/Rechercher.html', context)


@login_required
def Publier(request):
    if request.user.userprofile.type_utilisateur != 'conducteur':
        messages.warning(request, "Seuls les conducteurs peuvent publier des offres de trajets. Veuillez mettre à jour votre profil.")
        return redirect('profile_config')

    if request.method == 'POST':
        formset = RideOfferFormSet(request.POST, prefix='ride')
        if formset.is_valid():
            newly_published_rides = [] # To store rides successfully saved in this request
            for form in formset:
                # Check if the form is not marked for deletion and has data
                if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                    # Check for required fields more explicitly if needed, though form.is_valid() usually handles this
                    if form.cleaned_data.get('departure_location') and \
                       form.cleaned_data.get('arrival_location') and \
                       form.cleaned_data.get('departure_time') and \
                       form.cleaned_data.get('available_seats') is not None: # Use is not None for integer fields
                        try:
                            ride_offer = form.save(commit=False)
                            ride_offer.driver = request.user
                            ride_offer.save()
                            newly_published_rides.append(ride_offer)
                        except Exception as e:
                            messages.error(request, f"Erreur lors de l'enregistrement d'un trajet: {e}")
                elif form.cleaned_data.get('DELETE') and form.instance.pk:
                    # Handle deletion of existing forms
                    form.instance.delete()
                    messages.success(request, "Un trajet a été supprimé avec succès.")

            if newly_published_rides:
                messages.success(request, "Vos trajets ont été publiés avec succès!")
            elif not formset.is_valid(): # If there were validation errors, this message will be more specific
                 messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
            else:
                # This case happens if no new rides were added/saved and no errors
                messages.info(request, "Aucun nouveau trajet n'a été enregistré.")
            
            # After processing, redirect to the same page to show updated list and clear form
            return redirect('Publier')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
            # If formset is not valid, the formset with errors will be passed to context below
            
    # For GET requests or POST requests with invalid formsets
    # Fetch all ride offers for the current user to display them
    published_rides_summary = RideOffer.objects.filter(driver=request.user).order_by('-created_at')
    
    # Initialize an empty formset for new additions on GET or if POST was invalid
    formset = RideOfferFormSet(prefix='ride') 

    context = {
        'formset': formset,
        'published_rides_summary': published_rides_summary,
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