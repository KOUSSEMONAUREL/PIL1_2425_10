from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home_view, name='home'),
    path('offres/', views.list_offers_view, name='list_offers'),
    path('profil/', views.profil_view, name='profil'),
    path('profil/modifier/', views.modifier_profil_view, name='modifier_profil'),
    path('conversations/', views.conversations_view, name='conversations'),
    path('offre/nouvelle/', views.creer_offre_view, name='creer_offre'),
    path('messages/<int:user_id>/', views.conversation_detail_view, name='conversation_detail'),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
