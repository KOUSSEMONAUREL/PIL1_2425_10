import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db import transaction 
from django.db import models
from .forms import RegisterForm, LoginForm, UserProfileForm, UserUpdateForm, RideOfferFormSet, RechercheForm
from .models import Location, UserProfile, RideOffer, RideRequest, RideChat, ChatMessage
from django.db.models import F
from django.db.models import Q
import math
from django.utils import timezone
from datetime import datetime, time, date

# Fonction de calcul de distance Haversine
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon de la Terre en kilomètres

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def index(request):
    return render(request, 'IFRI_comotorage/index.html')

def Login(request):
    form = LoginForm()
    reg_form = RegisterForm()
    message = ''

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Bonjour, {user.username}! Vous êtes connecté.')
                return redirect('Accueil')
            else:
                messages.error(request, 'Identifiants invalides.')
        else:
            messages.error(request, 'Erreur de validation du formulaire.')

    return render(request, 'IFRI_comotorage/Login.html', context={
        'form': form,
        'reg_form': reg_form,
        'message': message
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        login_form = LoginForm()

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie et connexion automatique !")
            return redirect('Accueil')
        else:
            messages.error(request, "Erreur lors de l'inscription. Veuillez corriger les champs.")
            return render(request, 'IFRI_comotorage/Login.html', {
                'reg_form': form,
                'form': login_form,
            })
    else:
        form = RegisterForm()
        login_form = LoginForm()

    return render(request, 'IFRI_comotorage/Login.html', {
        'reg_form': form,
        'form': login_form
    })

def user_logout(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('Login')

@login_required
def Accueil(request):
    return render(request, 'IFRI_comotorage/Accueil.html')

@login_required
def Rechercher(request):
    rides = RideOffer.objects.all()
    form = RechercheForm(request.GET or None)
    
    search_radius_km = 10 # Rayon de recherche de 10 km

    # Filtrer les trajets déjà passés (date et heure)
    today = timezone.now().date()
    current_time = timezone.now().time()
    rides = rides.filter(
        Q(departure_date__gt=today) |
        Q(departure_date=today, departure_time__gte=current_time)
    )

    if form.is_valid():
        search_location_text = form.cleaned_data.get('search_location')
        search_lat = form.cleaned_data.get('search_latitude')
        search_lon = form.cleaned_data.get('search_longitude')

        if search_location_text or (search_lat and search_lon):
            filtered_rides = []
            for ride in rides:
                keep_ride = False
                
                # Prioriser la recherche par coordonnées GPS si disponibles
                if search_lat and search_lon:
                    # Vérifier si le point de départ du trajet est proche
                    if ride.departure_latitude and ride.departure_longitude:
                        distance_dep = haversine_distance(
                            search_lat, search_lon,
                            ride.departure_latitude, ride.departure_longitude
                        )
                        if distance_dep <= search_radius_km:
                            keep_ride = True
                    
                    # Si pas encore gardé, vérifier si le point d'arrivée du trajet est proche
                    if not keep_ride and ride.arrival_latitude and ride.arrival_longitude:
                        distance_arr = haversine_distance(
                            search_lat, search_lon,
                            ride.arrival_latitude, ride.arrival_longitude
                        )
                        if distance_arr <= search_radius_km:
                            keep_ride = True
                
                # Sinon, si seulement le texte est fourni, faire une recherche textuelle
                elif search_location_text:
                    if (search_location_text.lower() in ride.departure_location.lower() or
                        search_location_text.lower() in ride.arrival_location.lower()):
                        keep_ride = True
                
                if keep_ride:
                    filtered_rides.append(ride)
            
            rides = filtered_rides
        
        # Convertir la liste en QuerySet si nécessaire pour les filtres suivants
        if not isinstance(rides, models.QuerySet):
            rides = RideOffer.objects.filter(id__in=[ride.id for ride in rides])
        
    # Exclure les trajets du conducteur actuel
    if request.user.is_authenticated:
        rides = rides.exclude(driver=request.user)
    
    # Filtrer uniquement les trajets avec des places restantes
    rides = rides.filter(available_seats__gt=models.F('seats_taken'))

    context = {
        'form': form,
        'rides': rides,
        # 'has_searched' est vrai si au moins un champ de recherche a été rempli et est valide
        'has_searched': request.method == 'GET' and form.is_valid() and (form.cleaned_data.get('search_location') or form.cleaned_data.get('search_latitude') is not None),
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
            newly_published_rides = []
            for form in formset:
                if form.cleaned_data and not form.cleaned_data.get('DELETE'):
                    if all(form.cleaned_data.get(f) is not None for f in ['departure_location', 'arrival_location', 'departure_date', 'departure_time', 'available_seats']):
                        try:
                            ride_offer = form.save(commit=False)
                            ride_offer.driver = request.user
                            ride_offer.save()
                            newly_published_rides.append(ride_offer)
                        except Exception as e:
                            messages.error(request, f"Erreur lors de l'enregistrement d'un trajet: {e}")
                elif form.cleaned_data.get('DELETE') and form.instance.pk:
                    form.instance.delete()
                    messages.success(request, "Un trajet a été supprimé avec succès.")

            if newly_published_rides:
                messages.success(request, "Vos trajets ont été publiés avec succès!")
            elif not formset.is_valid():
                 messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
            else:
                messages.info(request, "Aucun nouveau trajet n'a été enregistré.")

            return redirect('Publier')
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")

    published_rides_summary = RideOffer.objects.filter(driver=request.user).order_by('-created_at')
    
    pending_requests = RideRequest.objects.filter(
        ride_offer__driver=request.user,
        status='pending'
    ).select_related('passenger', 'ride_offer').order_by('-created_at')

    formset = RideOfferFormSet(prefix='ride')

    context = {
        'formset': formset,
        'published_rides_summary': published_rides_summary,
        'pending_requests': pending_requests,
    }
    return render(request, 'IFRI_comotorage/Publier.html', context)


@login_required
def request_ride(request, ride_id):
    ride_offer = get_object_or_404(RideOffer, id=ride_id)

    if ride_offer.driver == request.user:
        messages.error(request, "Vous ne pouvez pas demander à rejoindre votre propre trajet.")
        return redirect('Rechercher')

    if ride_offer.remaining_seats <= 0:
        messages.error(request, "Désolé, il n'y a plus de places disponibles pour ce trajet.")
        return redirect('Rechercher')

    existing_request = RideRequest.objects.filter(
        ride_offer=ride_offer,
        passenger=request.user
    ).first()

    if existing_request:
        if existing_request.status == 'accepted':
            messages.info(request, "Vous avez déjà été accepté pour ce trajet.")
        elif existing_request.status == 'pending':
            messages.info(request, "Votre demande pour ce trajet est déjà en attente.")
        elif existing_request.status == 'rejected':
            messages.warning(request, "Votre précédente demande pour ce trajet a été rejetée.")
        return redirect('pre_messagerie')
    
    with transaction.atomic():
        RideRequest.objects.create(
            ride_offer=ride_offer,
            passenger=request.user,
            status='pending'
        )
        messages.success(request, f"Votre demande de place pour le trajet de {ride_offer.departure_location} à {ride_offer.arrival_location} a été envoyée au conducteur.")
    
    return redirect('pre_messagerie')


@login_required
def pre_messagerie(request):
    passenger_requests = RideRequest.objects.filter(
        passenger=request.user
    ).select_related('ride_offer__driver').order_by('-created_at')

    driver_posted_rides = RideOffer.objects.filter(driver=request.user).prefetch_related('requests').order_by('-created_at')

    accessible_chats = []

    for ride_offer in driver_posted_rides:
        accessible_chats.append({
            'ride_id': ride_offer.id,
            'departure_location': ride_offer.departure_location,
            'arrival_location': ride_offer.arrival_location,
            'is_driver': True,
            'chat_ready': True,
            'associated_request_id': None,
        })

    for req in passenger_requests:
        if req.status == 'accepted' and req.chat_access_granted:
            if not any(chat['ride_id'] == req.ride_offer.id for chat in accessible_chats):
                accessible_chats.append({
                    'ride_id': req.ride_offer.id,
                    'departure_location': req.ride_offer.departure_location,
                    'arrival_location': req.ride_offer.arrival_location,
                    'is_driver': False,
                    'chat_ready': True,
                    'associated_request_id': req.id,
                })

    context = {
        'passenger_requests': passenger_requests,
        'driver_posted_rides': driver_posted_rides,
        'accessible_chats': accessible_chats,
    }
    return render(request, 'IFRI_comotorage/pre-Messagerie.html', context)


@login_required
def approve_ride_request(request, request_id):
    ride_request = get_object_or_404(RideRequest, id=request_id)

    if ride_request.ride_offer.driver != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à approuver cette demande.")
        return redirect('pre_messagerie')

    if ride_request.status == 'pending':
        with transaction.atomic():
            ride_offer = ride_request.ride_offer
            if ride_offer.remaining_seats > 0:
                ride_offer.seats_taken = models.F('seats_taken') + 1
                ride_offer.save()
                ride_request.status = 'accepted'
                ride_request.chat_access_granted = True
                ride_request.save()
                messages.success(request, f"La demande de {ride_request.passenger.username} pour votre trajet a été acceptée et l'accès au chat a été accordé.")
            else:
                messages.error(request, "Impossible d'accepter: plus de places disponibles pour ce trajet.")
    else:
        messages.info(request, f"La demande est déjà au statut '{ride_request.get_status_display()}'.")

    return redirect('pre_messagerie')


@login_required
def reject_ride_request(request, request_id):
    ride_request = get_object_or_404(RideRequest, id=request_id)

    if ride_request.ride_offer.driver != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à rejeter cette demande.")
        return redirect('pre_messagerie')

    if ride_request.status == 'pending':
        ride_request.status = 'rejected'
        ride_request.chat_access_granted = False
        ride_request.save()
        messages.info(request, f"La demande de {ride_request.passenger.username} pour votre trajet a été rejetée.")
    else:
        messages.info(request, f"La demande est déjà au statut '{ride_request.get_status_display()}'.")

    return redirect('pre_messagerie')


@login_required
def cancel_ride_request(request, request_id):
    ride_request = get_object_or_404(RideRequest, id=request_id)

    if ride_request.passenger != request.user:
        messages.error(request, "Vous n'êtes pas autorisé à annuler cette demande.")
        return redirect('pre_messagerie')

    if ride_request.status == 'pending' or ride_request.status == 'accepted':
        with transaction.atomic():
            if ride_request.status == 'accepted':
                ride_offer = ride_request.ride_offer
                if ride_offer.seats_taken > 0:
                    ride_offer.seats_taken = models.F('seats_taken') - 1
                    ride_offer.save()
            ride_request.status = 'cancelled'
            ride_request.chat_access_granted = False
            ride_request.save()
            messages.success(request, f"Votre demande pour le trajet de {ride_request.ride_offer.departure_location} à {ride_request.ride_offer.arrival_location} a été annulée.")
    else:
        messages.info(request, f"La demande est déjà au statut '{ride_request.get_status_display()}'.")
    
    return redirect('pre_messagerie')


@login_required
def messagerie(request, ride_id):
    ride_offer = get_object_or_404(RideOffer, id=ride_id)
    chat = get_object_or_404(RideChat, ride_offer=ride_offer)

    is_driver = (ride_offer.driver == request.user)

    is_passenger_with_chat_access = RideRequest.objects.filter(
        ride_offer=ride_offer,
        passenger=request.user,
        status='accepted',
        chat_access_granted=True
    ).exists()

    if not is_driver and not is_passenger_with_chat_access:
        messages.error(request, "Vous n'avez pas accès à ce chat de trajet.")
        return redirect('pre_messagerie')

    messages_list = ChatMessage.objects.filter(chat=chat).order_by('timestamp')

    context = {
        'ride_offer': ride_offer,
        'chat_id': chat.id,
        'messages': messages_list,
        'current_user_username': request.user.username,
    }
    return render(request, "IFRI_comotorage/Messagerie.html", context)


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
        try:
            data = json.loads(request.body)
            name = data.get('name')
            lat = data.get('lat')
            lon = data.get('lon')
            print(f"Données de localisation reçues : Nom : {name}, Lat : {lat}, Lon : {lon}")
            return JsonResponse({'status': 'ok', 'message': 'Données de localisation reçues.'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'JSON invalide.'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Seules les requêtes POST sont autorisées.'}, status=405)