from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact_page, name='contact_page'),
    path('ckeditor5/image_upload/', views.upload_file, name='ck_editor_5_upload_file'),

]