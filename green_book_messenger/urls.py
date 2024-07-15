# chat/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path("", views.messenger_home, name="messenger_home"),
    path("<str:param_conversation_uuid>/", views.messenger_home, name="messenger_home"),
    path(
        "ajax/validate_username/",
        views.get_messages_by_conversation_id,
        name="get_messages",
    ),
    path(
        "ajax/get_users/",
        views.get_users,
        name="get_users",
    ),
    path(
        "ajax/add_private_conversation",
        views.add_private_conversation,
        name="add_private_conversation",
    ),
    path(
        "ajax/toggle_conversation_pin",
        views.toggle_conversation_pin,
        name="toggle_conversation_pin"
    )
]