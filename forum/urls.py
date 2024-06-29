from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_forum, name='home_forum'),
    path('ask/question', views.ask_question_forum, name='ask_question_forum'),
]