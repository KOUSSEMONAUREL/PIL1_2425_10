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
    path('Messagerie/', views.pre_messagerie, name='Messagerie'),
    path('Messagerie/<int:ride_id>/', views.messagerie, name='ride_chat'), 
    path('pre-Messagerie/', views.pre_messagerie, name='pre_messagerie'),
    path('request_ride/<int:ride_id>/', views.request_ride, name='request_ride'),
    path('request/<int:request_id>/approve/', views.approve_ride_request, name='approve_ride_request'),
    path('request/<int:request_id>/reject/', views.reject_ride_request, name='reject_ride_request'),
    path('request/<int:request_id>/cancel/', views.cancel_ride_request, name='cancel_ride_request'),
    path('Profil/', views.Profil, name='Profil'),
    path('profil/config/', views.profile_config, name='profile_config'),
    path('save_location/', views.save_location, name='save_location'),
]