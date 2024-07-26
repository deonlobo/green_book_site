from django.urls import path, include
from . import views

app_name = 'DIYProject'

urlpatterns = [
path('categories', views.categoriesView, name='categories'),
path('feed', views.feedView, name='feed'),
path('', views.indexView, name='home'),
path('sort-ascending', views.sortAscendingView, name='sortascending'),
path('sort-descending', views.sortDescendingView, name='sortdescending'),
path('sort-latest', views.feedView, name='sortlatest'),
path('search', views.SearchProjectView, name='search'),
path('my-projects', views.myProjectView, name='myprojects'),
path('bookmarks', views.bookmarkView, name='bookmarks'),
path('new-project', views.newProjectView, name='newproject'),
path('edit-project/<int:project_id>/',views.editProjectView, name='editproject'),
path('add-favourite/<int:project_id>/',views.addToFavouriteView, name='addfavourite'),
path('upvote/<int:project_id>/',views.upvotesView, name='upvote'),
path('remove-favourite/<int:project_id>/',views.removeFromFavouriteView, name='removefavourite'),
path('delete-project/<int:project_id>/',views.deleteProjectView, name='deleteproject'),
path('filter/<int:category_id>/',views.filterCategoryView, name='filtercategory'),
path('view-project/<int:id>/',views.projectView, name='viewproject'),
path('remove-thought/<int:thought_id>/',views.removeThoughtView, name='removethought'),
]