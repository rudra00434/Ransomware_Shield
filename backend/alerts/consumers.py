import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # In a real app, use self.scope['user'] to group by user
        if self.scope["user"].is_authenticated:
            self.room_group_name = f'user_alerts_{self.scope["user"].id}'
        else:
            self.room_group_name = 'user_alerts_guest'
            
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from room group
    async def send_alert(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
