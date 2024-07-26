import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Conversation, Message
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("---------------------", self.scope)
        self.conversation_uuid = self.scope["url_route"]["kwargs"][
            "param_conversation_uuid"
        ]
        self.conversation_group_name = f"conversation_{self.conversation_uuid}"
        print(self.conversation_uuid)
        print(self.conversation_group_name)
        # Join room group
        await self.channel_layer.group_add(
            self.conversation_group_name, self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.conversation_group_name, self.channel_name
        )
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        timestamp = text_data_json["timestamp"]
        user_id = text_data_json["user_id"]
        message = text_data_json["message_content"]
        username = await self.get_user_name(user_id)
        print(username)
        # Save message to the database
        await self.save_message(user_id, self.conversation_uuid, message, timestamp, username)

        # Send message to room group
        await self.channel_layer.group_send(
            self.conversation_group_name,
            {
                "type": "chat_message",
                "timestamp": timestamp,
                "user_id": user_id,
                "message": message,
                "user_name": username,
            },
        )

    async def chat_message(self, event):
        timestamp = event["timestamp"]
        user_id = event["user_id"]
        message = event["message"]
        username = event["user_name"]

        # Send message to WebSocket
        await self.send(
            text_data=json.dumps(
                {
                    "timestamp": timestamp,
                    "user_id": user_id,
                    "message": message,
                    "user_name": username,
                }
            )
        )

    @database_sync_to_async
    def save_message(self, user_id, conversation_uuid, content, timestamp, username):
        print(user_id, conversation_uuid)
        user = User.objects.get(id=user_id)
        conversation = Conversation.objects.get(conversation_uuid=conversation_uuid)
        Message.objects.create(
            conversation=conversation, sender=user, content=content, timestamp=timestamp, username=username
        )

    @database_sync_to_async
    def get_user_name(self, user_id):
        user = User.objects.get(id=user_id)
        return user.get_full_name()
