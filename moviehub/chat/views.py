from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Conversation
from movies.models import Movie


User = get_user_model()

@login_required
def chat_home(request):
    """
    Zobrazí seznam konverzací kde je user účastníkem
    """
    conversations = Conversation.objects.filter(participants=request.user).order_by("-updated_at", "-id")

    return render(request, "chat/chat_home.html", {
        "conversations": conversations,
    })

@login_required
def conversation_detail(request, conversation_id: int):
    """
    Detail PRIVATE conv (musi byt participant).
    Historii netaháme přes DB - posílá jí consumer jako 'history'.

    """
    conversation = get_object_or_404(Conversation, id=conversation_id, type=Conversation.Type.PRIVATE)

    if not conversation.participants.filter(id=request.user.id).exists():
        # bezpečnost: cizí konverzaci neuvidí
        return redirect("chat:chat_home")

    # protistrana (pro hezčí nadpis)
    other = conversation.participants.exclude(id=request.user.id).first()


    context = {
        "conversation": conversation,
        "other_user": other,
        "ws_kind": "conversation",
        "ws_id": conversation.id,
    }
    return render(request, "chat/conversation_detail.html", context)

@login_required
def movie_chat(request, movie_id: int):
    """
    Movie chat - najde nebo vytvoří konverzaci pro film
    (Membership se u MOVIE nepoužívá)
    """
    movie = get_object_or_404(Movie, id=movie_id)
    conversation, _ = Conversation.get_or_create_movie(movie)

    context = {
        "movie": movie,
        "conversation": conversation,
        "ws_kind": "movie",
        "ws_id": movie.id, # WS routing má movie_id
    }
    return render(request, "chat/movie_chat.html", context)


@login_required
def start_private_chat(request, user_id: int):
    """
    Startne/najde privatechat se zvolenym userem a redirectne na detail
    """
    other = get_object_or_404(User, id=user_id)
    conversation, _ = Conversation.get_or_create_private(request.user, other)
    return redirect("chat:conversation_detail", conversation_id=conversation.id)
