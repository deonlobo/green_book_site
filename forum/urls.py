from django.urls import path, include
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.home_forum, name='home_forum'),
    path('ask/question', views.ask_question_forum, name='ask_question_forum'),
    path('search-tags/', views.search_tags, name='search_tags'),
    path('questions/<int:id>/<str:question_id>/', views.display_question, name='question_detail'),
    path('questions/comment/<int:id>/', views.question_comment, name='question_comment'),
    path('answer/comment/<int:id>/', views.answer_comment, name='answer_comment'),
    path('answer/<int:id>/', views.answer, name='answer'),
    path('question/<int:id>/upvote/', views.upvote_question, name='upvote_question'),
    path('question/<int:id>/downvote/', views.downvote_question, name='downvote_question'),
    path('answer/<int:id>/upvote/', views.upvote_answer, name='upvote_answer'),
    path('answer/<int:id>/downvote/', views.downvote_answer, name='downvote_answer'),
    path('search_questions/', views.search_questions, name='search_questions'),

]