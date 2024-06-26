import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Conversation, Message
from django.contrib.auth.models import User
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_uuid = self.scope['url_route']['kwargs']['param_conversation_uuid']
        self.conversation_group_name = f'conversation_{self.conversation_uuid}'
        print(self.conversation_uuid)
        print(self.conversation_group_name)
        # Join room group
        await self.channel_layer.group_add(
            self.conversation_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.conversation_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # user_id = self.scope["user"].id

        # Save message to the database
        # await self.save_message(user_id, self.conversation_id, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                'type': 'chat_message',
                'message': message,
                # 'username': self.scope["user"].username,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        # username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            # 'username': username,
        }))

    @database_sync_to_async
    def save_message(self, user_id, conversation_id, content):
        user = User.objects.get(id=user_id)
        conversation = Conversation.objects.get(id=conversation_id)
        Message.objects.create(conversation=conversation, sender=user, content=content)
