from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('save/', views.save, name='save'),
    path('category/<int:category_id>/', views.category, name='category'),
    path('category/<int:category_id>/product/<int:product_id>/',views.view_products, name='view_products'),
    path('addproduct/', views.add_product, name='addproduct'),
]