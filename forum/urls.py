from django.urls import path, include
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.home_forum, name='home_forum'),
    path('ask/question', views.ask_question_forum, name='ask_question_forum'),
    path('search-tags/', views.search_tags, name='search_tags'),
    path('questions/<int:id>/<str:question_id>/', views.display_question, name='question_detail'),
]