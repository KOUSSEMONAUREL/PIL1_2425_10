from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max
from .models import CustomUser, Offre, PrivateMessage
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    CustomUserUpdateForm,
    OffreForm,
    PrivateMessageForm,
)

# --- Authentification ---
def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'mon_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'mon_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')


# --- Pages principales ---
@login_required
def home_view(request):
    return render(request, 'mon_app/home.html', {'user': request.user})

@login_required
def profil_view(request):
    return render(request, 'mon_app/profil.html', {'user': request.user})

@login_required
def modifier_profil_view(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès.")
            return redirect('profil')
    else:
        form = CustomUserUpdateForm(instance=request.user)
    return render(request, 'mon_app/modifier_profil.html', {'form': form})


# --- Offres de covoiturage ---
@login_required
def creer_offre_view(request):
    if request.method == 'POST':
        form = OffreForm(request.POST)
        if form.is_valid():
            offre = form.save(commit=False)
            offre.utilisateur = request.user
            offre.save()
            return redirect('list_offers')
    else:
        form = OffreForm()
    return render(request, 'mon_app/creer_offre.html', {'form': form})

def list_offers_view(request):
    query = request.GET.get('q')

    if query:
        offres = Offre.objects.filter(
            Q(depart__icontains=query) | Q(arrivee__icontains=query),
            utilisateur__isnull=False
        )
    else:
        offres = Offre.objects.filter(utilisateur__isnull=False)

    return render(request, 'mon_app/list_offers.html', {'offres': offres, 'query': query})



# --- Messagerie ---
from django.db.models import Q, Max
from .models import PrivateMessage
from django.contrib.auth.decorators import login_required

@login_required
def conversations_box_view(request):
    messages = PrivateMessage.objects.filter(
        Q(sender=request.user) | Q(recipient=request.user)
    ).order_by('-timestamp')

    latest_messages = {}
    for msg in messages:
        user = msg.recipient if msg.sender == request.user else msg.sender
        if user not in latest_messages:
            latest_messages[user] = msg

    return render(request, 'mon_app/messaging/conversations_box.html', {
        'conversations': latest_messages
    })
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import PrivateMessage, CustomUser
from .forms import PrivateMessageForm

@login_required
def chat_with_user_view(request, uid):
    contact = get_object_or_404(CustomUser, id=uid)

    messages_qs = PrivateMessage.objects.filter(
        Q(sender=request.user, recipient=contact) |
        Q(sender=contact, recipient=request.user)
    ).order_by('timestamp')

    if request.method == 'POST':
        form = PrivateMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.recipient = contact
            msg.save()
            return redirect('chat_with_user', uid=contact.id)
    else:
        form = PrivateMessageForm()

    return render(request, 'mon_app/messaging/chat.html', {
        'contact': contact,
        'messages': messages_qs,
        'form': form
    })


