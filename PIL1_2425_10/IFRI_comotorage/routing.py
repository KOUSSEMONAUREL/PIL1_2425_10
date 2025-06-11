from django.urls import path , include
from IFRI_comotorage.consumers import ChatConsumer


websocket_urlpatterns = [
    path("" , ChatConsumer.as_asgi()) , 
]