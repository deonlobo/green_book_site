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
    path('question/all', views.question_tab_forum, name='question_tab_forum'),
    path('tags/', views.forum_tags, name='forum_tags'),
    path('display-search-tags/', views.display_search_tags, name='display_search_tags'),
    path('search-users/', views.search_users, name='search_users'),
    path('display-users/', views.user_page, name='user_page'),
    path('user-details/<int:id>/', views.user_details, name='user_details'),
]