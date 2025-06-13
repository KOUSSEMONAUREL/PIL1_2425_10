from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # À adapter plus tard
    else:
        form = CustomUserCreationForm()
    return render(request, 'mon_app/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # À adapter
    else:
        form = CustomAuthenticationForm()
    return render(request, 'mon_app/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    return render(request, 'mon_app/home.html', {'user': request.user})
from .forms import RideOfferForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

@login_required
def publish_offer_view(request):
    if request.user.role != 'conducteur':
        return HttpResponseForbidden("Seuls les conducteurs peuvent publier une offre.")
    
    if request.method == 'POST':
        form = RideOfferForm(request.POST)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.driver = request.user
            offer.save()
            return redirect('home')
    else:
        form = RideOfferForm()
    
    return render(request, 'mon_app/publish_offer.html', {'form': form})
from .models import RideOffer

from django.db.models import Q
from .models import Offre

def list_offers_view(request):
    query = request.GET.get('q')

    if query:
        offres = Offre.objects.filter(
            Q(depart__icontains=query) | Q(arrivee__icontains=query)
        )
    else:
        offres = Offre.objects.all()

    return render(request, 'mon_app/list_offers.html', {'offres': offres, 'query': query})

@login_required
def profil_view(request):
    return render(request, 'mon_app/profil.html', {'user': request.user})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserUpdateForm

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
from .models import Message
from .forms import MessageForm
from django.contrib.auth.models import User  # ou ton CustomUser

@login_required
def conversation_view(request, user_id):
    other_user = CustomUser.objects.get(id=user_id)
    messages_list = Message.objects.filter(
        sender__in=[request.user, other_user],
        receiver__in=[request.user, other_user]
    )

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.sender = request.user
            msg.receiver = other_user
            msg.save()
            return redirect('conversation', user_id=other_user.id)
    else:
        form = MessageForm()

    return render(request, 'mon_app/conversation.html', {
        'form': form,
        'messages': messages_list,
        'other_user': other_user
    })
from django.db.models import Q, Max

@login_required
def conversations_view(request):
    # Récupère tous les messages où l'utilisateur est soit l'expéditeur soit le destinataire
    messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('timestamp')

    conversations = {}
    for msg in messages:
        other_user = msg.receiver if msg.sender == request.user else msg.sender
        conversations[other_user] = msg  # Chaque nouvelle occurrence écrase l’ancienne (donc on garde la + récente)

    return render(request, 'mon_app/listes_conversation.html', {'conversations': conversations.items()})
@login_required
def creer_offre_view(request):
    # Affiche un formulaire ou une page temporaire
    return render(request, 'mon_app/creer_offre.html')
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('offres/', views.list_offers_view, name='list_offers'),
    path('offre/nouvelle/', views.creer_offre_view, name='creer_offre'),
    path('conversations/', views.conversations_view, name='conversations'),
    path('profil/', views.profil_view, name='profil'),
    path('logout/', views.logout_view, name='logout'),
]
@login_required
def conversation_view(request, destinataire_id):
    destinataire = get_object_or_404(CustomUser, id=destinataire_id)
    messages = Message.objects.filter(
        models.Q(expediteur=request.user, destinataire=destinataire) |
        models.Q(expediteur=destinataire, destinataire=request.user)
    ).order_by('date')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.expediteur = request.user
            msg.destinataire = destinataire
            msg.save()
            return redirect('conversation', destinataire_id=destinataire.id)
    else:
        form = MessageForm()

    return render(request, 'core/conversation.html', {
        'form': form,
        'messages': messages,
        'destinataire': destinataire
    })
from .forms import OffreForm

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