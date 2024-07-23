from django.urls import path
from . import views

app_name = 'marketplace'

urlpatterns = [
    path('', views.index, name='index'),
    path('manage-products/', views.manage_products, name='manage_products'),
    path('add-category/', views.add_category, name='add_category'),
    path('modify-category/<int:category_id>', views.modify_category, name='modify_category'),
    path('activate-category/<int:category_id>', views.activate_category, name='activate_category'),
    path('delete-category/<int:category_id>', views.delete_category, name='delete_category'),
    path('modify-product-step-1/<int:product_id>', views.modify_add_product_step_one, name='modify_add_product_step_one'),
    path('modify-product-step-2/<int:product_id>', views.modify_add_product_step_two, name='modify_add_product_step_two'),
    path('modify-product-step-3/<int:product_id>', views.modify_add_product_step_three, name='modify_add_product_step_three'),
    path('save/', views.save, name='save'),
    path('category/<int:category_id>/', views.category, name='category'),
    path('category/<int:category_id>/product/<int:product_id>/',views.view_products, name='view_products'),
    path('add-product/', views.add_product_step_one, name='add_product'),
    path('add-product-step-2/<int:product_id>/', views.add_product_step_two, name='add_product_step_two'),
    path('add-product-step-3/<int:product_id>/', views.add_product_step_three, name='add_product_step_three'),
    path('add-product-step-4/<int:product_id>/', views.add_product_step_four, name='add_product_step_four')

]