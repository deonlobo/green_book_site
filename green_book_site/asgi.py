"""
ASGI config for green_book_site project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import green_book_messenger.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'green_book_site.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            green_book_messenger.routing.websocket_urlpatterns
        )
    ),
})
