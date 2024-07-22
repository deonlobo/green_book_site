# myapp/subapp/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

urlpatterns = [
    path('challenge1/', views.challenge1, name='challenge1'),
    path('accept_challenge/<int:pk>/', views.accept_challenge_view, name='accept_challenge'),
    path('challenges/accepted/', views.accepted_challenges_list_view, name='accepted_challenges_list'),
    path('submit_completed_task/', views.submit_completed_task_view, name='submit_completed_task'),

]
# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
