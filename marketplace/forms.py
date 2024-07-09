from django.forms import *
from .models import Product
from django.utils.html import mark_safe
from django.contrib import admin

class ProductForm(ModelForm):
    image_upload = ImageField(required=False, label='Upload Image')

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock', 'image_upload', 'category']

    def save(self, commit=True):
        product = super().save(commit=False)
        if self.cleaned_data.get('image_upload'):
            product.image = self.cleaned_data['image_upload'].read()
        if commit:
            product.save()
        return product

class AddProductForm(ModelForm):
    image_upload = ImageField(
        widget=ClearableFileInput(attrs={'class': 'form-control'}),
        required=False,
        label='Upload Image'
    )
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'stock','category','image_upload']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
            'stock': NumberInput(attrs={'class': 'form-control'}),
            'category': Select(attrs={'class': 'form-control'}),
        }
