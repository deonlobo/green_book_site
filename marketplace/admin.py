from django.contrib import admin
from .models import *
from django.utils.html import mark_safe
from .forms import ProductForm , ProductStep2Form

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('name', 'description', 'price', 'stock', 'category', 'created_at', 'updated_at', 'image_tag')
    readonly_fields = ('image_tag',)

admin.site.register(Category)
admin.site.register(ProductStep1)
admin.site.register(ProductStep3)


@admin.register(ProductStep2)
class ProductStep2Admin(admin.ModelAdmin):
    form = ProductStep2Form
    list_display = ('image_upload1_tag','image_upload2_tag','image_upload3_tag','image_upload4_tag','product_step1','is_active','created_at')
    readonly_fields = ('image_upload1_tag','image_upload2_tag','image_upload3_tag','image_upload4_tag')




