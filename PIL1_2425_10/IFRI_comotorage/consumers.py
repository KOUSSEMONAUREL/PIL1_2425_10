import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from IFRI_comotorage.models import RideChat, ChatMessage # Import des nouveaux modèles
from asgiref.sync import sync_to_async
from django.utils import timezone # Pour l'horodatage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
      
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
     
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        username = text_data_json['username']
        chat_id = text_data_json['chat_id'] 

  
        await self.save_chat_message(username, message, chat_id)

      
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message', 
                'message': message,
                'username': username,
                'timestamp': str(timezone.now()), 
            }
        )


    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        timestamp = event['timestamp']


        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'timestamp': timestamp,
        }))

    @sync_to_async
    def save_chat_message(self, username, message_content, chat_id):
        
        try:
            sender_user = User.objects.get(username=username)
        except User.DoesNotExist:
            print(f"L'utilisateur '{username}' n'a pas été trouvé. Message non enregistré.")
            return

        try:
            ride_chat = RideChat.objects.get(id=chat_id)
        except RideChat.DoesNotExist:
            print(f"RideChat avec l'ID '{chat_id}' non trouvé. Message non enregistré.")
            return
        
        ChatMessage.objects.create(
            chat=ride_chat,
            sender=sender_user,
            message=message_content
        )