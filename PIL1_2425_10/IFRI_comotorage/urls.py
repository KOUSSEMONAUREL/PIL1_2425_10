from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('accueil/', views.Accueil, name='Accueil'),
    path('rechercher/', views.Rechercher, name='Rechercher'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('publier/', views.Publier, name='Publier'),
    path('messagerie/', views.Messagerie, name='Messagerie'),
    path('profil/', views.Profil, name='Profil'),
]