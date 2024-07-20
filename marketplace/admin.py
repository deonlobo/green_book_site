from django.contrib import admin
from .models import *
from django.utils.html import mark_safe
from .forms import ProductForm

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ('name', 'description', 'price', 'stock', 'category', 'created_at', 'updated_at', 'image_tag')
    readonly_fields = ('image_tag',)

admin.site.register(Category)
admin.site.register(ProductStep1)
admin.site.register(ProductStep3)
admin.site.register(ProductStep2)


