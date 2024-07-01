# chat/urls.py
from django.urls import path

from . import views


urlpatterns = [
    path("", views.messenger_home, name="messenger_home"),
    path("<str:param_conversation_uuid>/", views.messenger_home, name="messenger_home"),
]