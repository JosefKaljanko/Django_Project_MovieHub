import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumers(AsyncWebsocketConsumer):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(args, kwargs)
    #     self.room_group_name = None

    async def connect(self):
        self.room_group_name = "test_room"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        await self.send(text_data=json.dumps({"type": "system", "message": "Connected"}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """kdyz klient posle zpravu, posleme ji do skupiny"""
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chat.message", "message": text_data}
        )

    async def chat_message(self, event):
        """zprava ktera prisla ze skupiny se posle zpet klientovi"""
        await self.send(text_data=event["message"])