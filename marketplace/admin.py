from django.contrib import admin
from .models import *
from django.utils.html import mark_safe
from .forms import  ProductStep2Form



admin.site.register(Category)
admin.site.register(ProductStep1)
admin.site.register(ProductStep3)
admin.site.register(SearchProduct)


@admin.register(ProductStep2)
class ProductStep2Admin(admin.ModelAdmin):
    form = ProductStep2Form
    list_display = ('image_upload1_tag','image_upload2_tag','image_upload3_tag','image_upload4_tag','product_step1','is_active','created_at')
    readonly_fields = ('image_upload1_tag','image_upload2_tag','image_upload3_tag','image_upload4_tag')




