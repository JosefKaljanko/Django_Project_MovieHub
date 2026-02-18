from django.utils import timezone
from django.conf import settings
from django.db import models
from movies.models import Movie

User = settings.AUTH_USER_MODEL

class Conversation(models.Model):
    class Type(models.TextChoices):
        PRIVATE = "private", "Private"
        MOVIE = "movie", "Movie"

    type = models.CharField(max_length=20, choices=Type.choices)

    # pro MOVIE konverzaci
    movie = models.ForeignKey(Movie, null=True, blank=True,
                                     on_delete=models.CASCADE,
                                     related_name="conversations"
    )

    participants = models.ManyToManyField(User, through="ConversationParticipant",
                                                related_name="conversations"
    )

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """MOVIE musí mít movie, PRIVATE nikoliv"""
        if self.type == self.Type.MOVIE and not self.movie:
            raise ValueError("Movie conversation must have a movie.")
        if self.type == self.Type.PRIVATE and self.movie_id is not None:
            raise ValueError("Private conversation cannot have a movie.")

    def __str__(self):
        if self.type == self.Type.MOVIE:
            return f"Movie chat: {self.movie_id}"
        return f"Private chat: {self.pk}"

    @staticmethod
    def get_or_create_private(user1, user2):
        """najde nebo vytvoří soukromý chat."""
        if user1.id == user2.id:
            raise ValueError("Conversation with yourself not possible.")

        qs = (
            Conversation.objects.filter(type=Conversation.Type.PRIVATE)
            .filter(participants=user1)
            .filter(participants=user2)
            .distinct()
        )
        conv = qs.first()
        if conv:
            return conv, False
        conv = Conversation.objects.create(type=Conversation.Type.PRIVATE)
        ConversationParticipant.objects.create(conversation=conv, user=user1)
        ConversationParticipant.objects.create(conversation=conv, user=user2)
        return conv, True

    @staticmethod
    def get_or_create_movie(movie):
        """najde nebo vytvoří konverzaci u filmu"""
        conv = Conversation.objects.filter(type=Conversation.Type.MOVIE, movie=movie).first()
        if conv:
            return conv, False
        conv = Conversation.objects.create(type=Conversation.Type.MOVIE, movie=movie)
        return conv, True


class ConversationParticipant(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("conversation", "user")

    def __str__(self):
        return f"{self.conversation_id} - {self.user_id}"


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.conversation_id} {self.sender_id}: {self.content[:30]}..."
