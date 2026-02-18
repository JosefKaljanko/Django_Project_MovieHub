import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Conversation, Message
from movies.models import Movie


class ChatConsumers(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope.get("user")
        # if not user or isinstance(user, AnonymousUser) or not user.is_authenticated:
        if not user or not getattr(user, "is_authenticated", False):
            await self.close(code=4401) # Unautorized
            return

        self.user = user
        self.conversation = None

        # MOVIE CHAT/CONVERSATION CHAT
        movie_id = self.scope["url_route"]["kwargs"].get("movie_id")
        if movie_id:
            self.conversation = await self.get_or_create_movie_conversation(movie_id)
        else:
            conversation_id = self.scope["url_route"]["kwargs"].get("conversation_id")
            self.conversation = await self.get_conversation_if_member(conversation_id)

        if not self.conversation:
            await self.close(code=4403) # Forbiden / not found
            return

        self.group_name = f"chat_{self.conversation.id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # po připojení pošli posledních N zpráv
        last_messages = await self.get_last_messages(self.conversation.id, limit=30)
        await self.send(text_data=json.dumps(
            {
                "type": "history",
                "messages": last_messages,
            }
        ))

    async def disconnect(self, close_code):

        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):

        payload = None
        try:
            payload = json.loads(text_data)
            if isinstance(payload, str):
                payload = {"text": payload}
            elif not isinstance(payload, dict):
                payload = {}
        except Exception:
            payload = {"text": text_data}

        text = (payload.get("text") or "").strip()
        if not text:
            return

        msg = await self.create_message(self.conversation.id, self.user.id, text)

        event = {
            "type": "chat.message",
                "id": msg["id"],
                "sender": msg["sender"],
                "text": msg["text"],
                "created_at": msg["created_at"],
        }

        await self.channel_layer.group_send(self.group_name, event)

    async def chat_message(self, event):
        """zprava ktera prisla ze skupiny se posle zpet klientovi"""
        event.pop("type", None)     # odstraní interní channels type
        await self.send(text_data=json.dumps(
            {
                "type": "message",
                **event,
            }
        ))

    # utils
    @database_sync_to_async
    def get_or_create_movie_conversation(self, movie_id: int):
        movie = Movie.objects.filter(id=movie_id).first()
        if not movie:
            return None
        conv, _ = Conversation.get_or_create_movie(movie)
        return conv


    @database_sync_to_async
    def get_conversation_if_member(self, conversation_id: int):
        if not conversation_id:
            return None
        conv = Conversation.objects.filter(id=conversation_id).first()
        if not conv:
            return None
        # pro PRIVATE: uživatel musí být participant
        if conv.type == Conversation.Type.PRIVATE and not conv.participants.filter(id=self.user.id).exists():
            return None
        return conv

    @database_sync_to_async
    def create_message(self, conversation_id: int, sender_id: int, text: str):
        msg = Message.objects.create(
            conversation_id=conversation_id,
            sender_id=sender_id,
            content=text
        )
        return{
            "id": msg.id,
            "sender": msg.sender.username,
            "text": msg.content,
            "created_at": msg.created_at.isoformat(),
        }

    @database_sync_to_async
    def get_last_messages(self, conversation_id: int, limit: int = 30):
        qs = (
            Message.objects.filter(conversation_id=conversation_id)
            .select_related("sender")
            .order_by("-created_at")[:limit]
        )
        #otočíme na chronologické pořadí
        msgs = list(reversed(list(qs)))
        return [
            {
                "id": m.id,
                "sender": m.sender.username,
                "text": m.content,
                "created_at": m.created_at.isoformat(),
            }
            for m in msgs
        ]