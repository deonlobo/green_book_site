from django.urls import path, include
from . import views

app_name = 'DIYProject'

urlpatterns = [
path('categories', views.categoriesView, name='categories'),
path('feed', views.feedView, name='feed'),
path('new-project', views.newProjectView, name='newproject'),
path('edit-project/<int:project_id>/',views.editProjectView, name='editproject'),
path('filter/<int:category_id>/',views.filterCategoryView, name='filtercategory'),
]