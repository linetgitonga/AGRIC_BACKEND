import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
            return
            
        self.user_inbox = f"inbox_{self.user.id}"
        
        # Join user's personal inbox group
        await self.channel_layer.group_add(
            self.user_inbox,
            self.channel_name
        )
        
        await self.accept()

    async def disconnect(self, close_code):
        # Leave inbox group
        await self.channel_layer.group_discard(
            self.user_inbox,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_type = data.get('type')
        
        if message_type == 'chat_message':
            receiver_id = data.get('receiver_id')
            content = data.get('content')
            subject = data.get('subject', 'New Message')
            
            # Save message to database
            message = await self.save_message(
                sender=self.user,
                receiver_id=receiver_id,
                subject=subject,
                content=content
            )
            
            # Send message to receiver's group
            receiver_group = f"inbox_{receiver_id}"
            
            await self.channel_layer.group_send(
                receiver_group,
                {
                    "type": "chat.message",
                    "message": {
                        "id": message.id,
                        "sender": self.user.email,
                        "subject": subject,
                        "content": content,
                        "timestamp": message.created_at.isoformat()
                    }
                }
            )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event["message"]))

    @database_sync_to_async
    def save_message(self, sender, receiver_id, subject, content):
        receiver = User.objects.get(id=receiver_id)
        return Message.objects.create(
            sender=sender,
            receiver=receiver,
            subject=subject,
            content=content
        )