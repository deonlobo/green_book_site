from django import forms
from .models import Product
from django.utils.html import mark_safe
from django.contrib import admin

class ProductForm(forms.ModelForm):
    image_upload = forms.ImageField(required=False, label='Upload Image')

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