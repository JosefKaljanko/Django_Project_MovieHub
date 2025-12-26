from django.urls import re_path
from .consumers import ChatConsumers

websocket_urlpatterns = [
    # PRIVATE
    re_path(r"ws/chat/conversation/(?P<conversation_id>\d+)/$", ChatConsumers.as_asgi()),
    # MOVIE chat
    re_path(r"ws/chat/movie/(?P<movie_id>\d+)/$", ChatConsumers.as_asgi()),
    re_path(r"ws/chat/$", ChatConsumers.as_asgi()),
]