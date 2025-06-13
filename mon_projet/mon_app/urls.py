from django.urls import path
from . import views
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView
)
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('offres/', views.list_offers_view, name='list_offers'),
    path('profil/', views.profil_view, name='profil'),
    path('profil/modifier/', views.modifier_profil_view, name='modifier_profil'),
    path('offre/nouvelle/', views.creer_offre_view, name='creer_offre'),
    path('messagerie/', views.conversations_box_view, name='conversations_box'),
    path('messagerie/<int:uid>/', views.chat_with_user_view, name='chat_with_user'),
    path('mot-de-passe-oublie/', auth_views.PasswordResetView.as_view(template_name='mon_app/password_reset.html'), name='password_reset'),
    path('mot-de-passe-envoye/', auth_views.PasswordResetDoneView.as_view(template_name='mon_app/password_reset_done.html'), name='password_reset_done'),
    path('reinitialiser/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='mon_app/password_reset_confirm.html'), name='password_reset_confirm'),
    path('mot-de-passe-complet/', auth_views.PasswordResetCompleteView.as_view(template_name='mon_app/password_reset_complete.html'), name='password_reset_complete'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
