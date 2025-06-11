from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('Accueil/', views.Accueil, name='Accueil'),
    path('Login/', views.Login, name='Login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('Rechercher/', views.Rechercher, name='Rechercher'),
    path('Publier/', views.Publier, name='Publier'),
    path('Messagerie/', views.Messagerie, name='Messagerie'),
    path('Profil/', views.Profil, name='Profil'),
    path('save_location/', views.save_location, name='save_location'),
]