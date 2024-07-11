# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/messenger/(?P<param_conversation_uuid>[0-9a-fA-F-]+)/$', consumers.ChatConsumer.as_asgi()),
]