from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.index, name='index'),
    path('admin-manage-products/', views.admin_manage_products, name='admin_manage_products'),
    path('add-category/', views.add_category, name='add_category'),
    path('modify-product-step-1/<int:product_id>', views.modify_add_product_step_one, name='modify_add_product_step_one'),
    path('modify-product-step-2/<int:product_id>', views.modify_add_product_step_two, name='modify_add_product_step_two'),
    path('save/', views.save, name='save'),
    path('category/<int:category_id>/', views.category, name='category'),
    path('category/<int:category_id>/product/<int:product_id>/',views.view_products, name='view_products'),
    path('add-product/', views.add_product_step_one, name='add_product'),
    path('add-product-step-2/<int:product_id>/', views.add_product_step_two, name='view_products'),
    # path('dumy', views.dumy, name='dumy'),
    path('add-product-step-3/<int:product_id>/', views.add_product_step_three, name='add_product_step_three'),

]