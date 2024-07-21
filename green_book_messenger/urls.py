# chat/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path("", views.get_messenger_list_template, name="messenger_list"),
    path("<str:param_conversation_uuid>/", views.get_conversation_template, name="messenger_conversation"),
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
        name="toggle_conversation_pin",
    ),
    path(
        "ajax/get_pinned_conversations",
        views.get_pinned_conversations,
        name="get_pinned_conversations",
    ),
    path(
        "ajax/get_private_conversations",
        views.get_private_conversations,
        name="get_private_conversations",
    ),
]