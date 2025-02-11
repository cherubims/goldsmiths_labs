import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from datetime import datetime
from notifications_app.models import Notification
from .models import Message

logger = logging.getLogger(__name__)
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the room name from the URL route
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        # Join the room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()
        logger.info(f"WebSocket connected: {self.room_group_name}")

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logger.info(f"WebSocket disconnected: {self.room_group_name}")

    async def receive(self, text_data):
        # Parse the incoming WebSocket message
        data = json.loads(text_data)
        message = data['message']
        sender_username = data['sender']

        print(f"Received message: {message} from {sender_username}")

        # Get the sender and receiver
        try:
            sender = await sync_to_async(User.objects.get)(username=sender_username)
            # Extract receiver's username from room name (replace the sender's username with "")
            receiver_username = self.room_name.replace(sender_username, "").replace("_", "")
            receiver = await sync_to_async(User.objects.get)(username=receiver_username)
        except User.DoesNotExist:
            # If user doesn't exist, send error back to WebSocket
            await self.send(text_data=json.dumps({'error': 'User not found'}))
            return

        # Save the message to the database
        await sync_to_async(Message.objects.create)(
            sender=sender,
            receiver=receiver,
            content=message
        )

        # Create a notification for the receiver
        await sync_to_async(Notification.objects.create)(
            recipient=receiver,
            message=f"{sender.username} sent you a message: {message[:50]}",
        )

        # Prepare the timestamp for when the message is received
        timestamp = datetime.now().strftime('%H:%M')

        # Send the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender.username,
                'timestamp': timestamp
            }
        )
        logger.info(f"Message broadcasted: {message}")

    async def chat_message(self, event):
        # Extract the message details from the event
        message = event['message']
        sender = event['sender']
        timestamp = event.get('timestamp', '')

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': timestamp
        }))
        logger.info(f"Message sent to WebSocket: {message}")

