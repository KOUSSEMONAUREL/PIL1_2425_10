from django.urls import path , include
from IFRI_comotorage.consumers import ChatConsumer


websocket_urlpatterns = [
    path("ws/chat/<int:chat_id>/" , ChatConsumer.as_asgi()) , # Nouvelle URL de chat spécifique au trajet
]