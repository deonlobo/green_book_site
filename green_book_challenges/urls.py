# myapp/subapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('challenge1/', views.challenge1, name='challenge1'),
]
