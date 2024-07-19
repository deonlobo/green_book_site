from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.index, name='index'),
    path('add-category/', views.add_category, name='add_category'),
    path('save/', views.save, name='save'),
    path('category/<int:category_id>/', views.category, name='category'),
    path('category/<int:category_id>/product/<int:product_id>/',views.view_products, name='view_products'),
    path('addproduct/', views.add_product, name='addproduct'),
    # path('dumy', views.dumy, name='dumy'),
]