# IFRI_comotorage/views.py
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.db import transaction # Import transaction pour les opérations atomiques
# Import de toutes les classes de formulaire directement
from .forms import RegisterForm, LoginForm, UserProfileForm, UserUpdateForm, RideOfferFormSet
from .models import Location, UserProfile, RideOffer, RideRequest, RideChat, ChatMessage # Import des nouveaux modèles
from django.db.models import F
from django.db.models import Q
from math import radians, sin, cos, sqrt, atan2
from django.utils import timezone

# Fonction utilitaire pour la distance de Haversine (recherche de proximité simple)
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Rayon de la Terre en kilomètres

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def index(request):
    return render(request, 'IFRI_comotorage/index.html')

def Login(request):
    # Instancier les formulaires directement en utilisant leurs noms de classe
    form = LoginForm()
    reg_form = RegisterForm()
    message = ''

    if request.method == 'POST':
        form = LoginForm(request.POST) # Utiliser LoginForm directement
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
        form = RegisterForm(request.POST) # Utiliser RegisterForm directement
        login_form = LoginForm() # Utiliser LoginForm directement

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
        form = RegisterForm() # Utiliser RegisterForm directement
        login_form = LoginForm() # Utiliser LoginForm directement

    return render(request, 'IFRI_comotorage/Login.html', {
        'reg_form': form,
        'form': login_form
    })

def user_logout(request):
    logout(request)
    return redirect('Login')

@login_required
def Accueil(request):
    return render(request, 'IFRI_comotorage/Accueil.html')

@login_required
def Rechercher(request):
    search_query = request.GET.get('search', '').strip().lower()

    all_ride_offers = []
    if search_query:
        # On filtre les trajets si le champ de recherche n'est pas vide
        all_ride_offers = RideOffer.objects.filter(
            Q(departure_location__icontains=search_query) |
            Q(arrival_location__icontains=search_query)
        ).order_by('-created_at')
        messages.info(request, f"Résultats pour : « {search_query} »")
    else:
        messages.info(request, "Veuillez entrer une adresse de départ ou d'arrivée.")

    ride_offers_data = []
    for ride in all_ride_offers:
        # Vérifier si l'utilisateur actuel a déjà demandé ce trajet
        has_requested = RideRequest.objects.filter(
            ride_offer=ride,
            passenger=request.user
        ).exists()
        
        ride_offers_data.append({
            'id': ride.id,
            'driver': ride.driver.username,
            'departure_location': ride.departure_location,
            'departure_latitude': ride.departure_latitude,
            'departure_longitude': ride.departure_longitude,
            'arrival_location': ride.arrival_location,
            'arrival_latitude': ride.arrival_latitude,
            'arrival_longitude': ride.arrival_longitude,
            'departure_time': ride.departure_time.strftime('%H:%M'),
            'remaining_seats': ride.remaining_seats, # Utilisation de la propriété du modèle
            'has_requested': has_requested,
            'is_driver_of_this_ride': ride.driver == request.user
        })

    context = {
        'ride_offers_json': json.dumps(ride_offers_data),
        'search_query': search_query,
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
                    if form.cleaned_data.get('departure_location') and \
                       form.cleaned_data.get('arrival_location') and \
                       form.cleaned_data.get('departure_time') and \
                       form.cleaned_data.get('available_seats') is not None:
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
    
    # Obtenir les demandes en attente pour les trajets de ce conducteur
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

    if ride_offer.remaining_seats <= 0: # Utilisation de la propriété du modèle
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
            if ride_offer.remaining_seats > 0: # Utilisation de la propriété du modèle
                ride_offer.seats_taken = F('seats_taken') + 1
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
                    ride_offer.seats_taken = F('seats_taken') - 1
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