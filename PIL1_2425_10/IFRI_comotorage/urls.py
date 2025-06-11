from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('accueil/', views.Accueil, name='Accueil'),
    path('rechercher/', views.Rechercher, name='Rechercher'),
    path('Login/', views.Login, name='Login'),
    path('publier/', views.Publier, name='Publier'),
    path('messagerie/', views.Messagerie, name='Messagerie'),
    path('profil/', views.Profil, name='Profil'),
    path('save_location/', views.save_location, name='save_location'),
    # path("auth/login/", LoginView.as_view(template_name="IFRI_comotorage/Login.html"), name="login-user"),
    path("auth/logout/", LogoutView.as_view(), name="logout-user"),
]