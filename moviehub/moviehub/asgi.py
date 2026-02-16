"""
ASGI config for moviehub project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moviehub.settings')

from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

django_asgi_app = get_asgi_application()

import chat.routing

print("ASGI LOADED: moviehub.asgi")



"""Hybrid at django umi Http i Websocket"""
application = ProtocolTypeRouter(
    {
        "http" : django_asgi_app,
        "websocket" : AllowedHostsOriginValidator(
            AuthMiddlewareStack(
            URLRouter(chat.routing.websocket_urlpatterns)
            )
        ),
    }
)

#  static file servirovani
from django.conf import settings
if settings.DEBUG:
    from django.contrib.staticfiles.handlers import ASGIStaticFilesHandler
    application = ASGIStaticFilesHandler(application)