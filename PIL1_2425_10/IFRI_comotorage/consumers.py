import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from IFRI_comotorage.models import RideChat, ChatMessage # Import des nouveaux modèles
from asgiref.sync import sync_to_async
from django.utils import timezone # Pour l'horodatage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Le modèle d'URL pour ce consommateur devrait maintenant inclure un chat_id
        # Exemple: ws/chat/<int:chat_id>/
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        # Ajouter l'utilisateur au groupe de chat
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Supprimer l'utilisateur du groupe de chat
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        chat_id = text_data_json['chat_id'] # Obtenir chat_id du message reçu

        # Enregistrer le message dans la base de données
        await self.save_chat_message(username, message, chat_id)

        # Envoyer le message au groupe WebSocket
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message', # Méthode à appeler sur les consommateurs du groupe
                'message': message,
                'username': username,
                'timestamp': str(timezone.now()), # Envoyer l'horodatage du serveur
            }
        )

    # Recevoir le message du groupe de chat
    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']

        # Envoyer le message au WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp,
        }))

    @sync_to_async
    def save_chat_message(self, username, message_content, chat_id):
        # Obtenir l'instance de l'utilisateur
        try:
            sender_user = User.objects.get(username=username)
        except User.DoesNotExist:
            print(f"L'utilisateur '{username}' n'a pas été trouvé. Message non enregistré.")
            return

        # Obtenir l'instance de RideChat
        try:
            ride_chat = RideChat.objects.get(id=chat_id)
        except RideChat.DoesNotExist:
            print(f"RideChat avec l'ID '{chat_id}' non trouvé. Message non enregistré.")
            return
        
        # Créer et enregistrer le ChatMessage
        ChatMessage.objects.create(
            chat=ride_chat,
            sender=sender_user,
            message=message_content
        )