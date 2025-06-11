from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import CustomUser, Message, Offre
from .forms import (
    CustomUserCreationForm,
    CustomAuthenticationForm,
    CustomUserUpdateForm,
    MessageForm,
    OffreForm
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
@login_required
def conversations_view(request):
    messages_all = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('timestamp')
    conversations = {}
    for msg in messages_all:
        other_user = msg.receiver if msg.sender == request.user else msg.sender
        conversations[other_user] = msg  # On garde le plus récent
    return render(request, 'mon_app/listes_conversation.html', {'conversations': conversations.items()})

@login_required
def conversation_detail_view(request, user_id):
    other_user = get_object_or_404(CustomUser, pk=user_id)
    messages_list = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    ).order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = other_user
            msg.save()
            return redirect('conversation_detail', user_id=other_user.id)
    else:
        form = MessageForm()

    return render(request, 'mon_app/conversation.html', {
        'messages': messages_list,
        'form': form,
        'other_user': other_user,
    })
