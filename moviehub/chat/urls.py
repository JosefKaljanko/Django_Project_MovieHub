from django.urls import path
from .views import (conversation_detail, movie_chat, start_private_chat,
                    chat_home,
                    )

app_name = "chat"
urlpatterns = [
    path("", chat_home, name="chat_home"),
    path("conversation/<int:conversation_id>/", conversation_detail, name="conversation_detail"),
    path("movie/<int:movie_id>/", movie_chat, name="movie_chat"),
    path("start/<int:user_id>/", start_private_chat, name="start_private_chat"),
]