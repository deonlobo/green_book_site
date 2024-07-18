from django.urls import path, include
from . import views

app_name = 'DIYProject'

urlpatterns = [
path('categories', views.categoriesView, name='categories'),
path('feed', views.feedView, name='feed'),
path('search', views.SearchProjectView, name='search'),
path('my-projects', views.myProjectView, name='myprojects'),
path('new-project', views.newProjectView, name='newproject'),
path('edit-project/<int:project_id>/',views.editProjectView, name='editproject'),
path('delete-project/<int:project_id>/',views.deleteProjectView, name='deleteproject'),
path('filter/<int:category_id>/',views.filterCategoryView, name='filtercategory'),
path('view-project/<int:id>/',views.projectView, name='viewproject'),
]