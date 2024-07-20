from django.forms import *
from .models import *


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
        }

class ProductStep1Form(ModelForm):
    class Meta:
        model = ProductStep1
        fields = ['name', 'description', 'quality', 'price', 'stock','category','discounted','percent']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'description': Textarea(attrs={'class': 'form-control'}),
            'quality': Select(attrs={'class': 'form-control'}),
            'price': NumberInput(attrs={'class': 'form-control'}),
            'stock': NumberInput(attrs={'class': 'form-control'}),
            'category': Select(attrs={'class': 'form-control'}),
            'discounted': Select(attrs={'class': 'form-control'}),
            'percent': NumberInput(attrs={'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        stock = cleaned_data.get('stock')
        percent = cleaned_data.get('percent')
        discounted = cleaned_data.get('discounted')
        if price is not None and price < 0:
            self.add_error('price', 'Price cannot be negative.')

        if stock is not None and stock < 0:
            self.add_error('stock', 'Stock cannot be negative.')

        if discounted is not None and discounted == True and percent == 0 :
            self.add_error('percent', 'Percent cannot be zero')

        if percent is not None and (percent < 0 or percent > 100):
            self.add_error('percent', 'Percent must be between 0 and 100.')

        return cleaned_data

class ProductStep2Form(ModelForm):
    image1 = ImageField(
        widget=ClearableFileInput(attrs={'class': 'form-control'}),
        required=False,
        label='Upload Image 1'
    )
    image2 = ImageField(
        widget=ClearableFileInput(attrs={'class': 'form-control'}),
        required=False,
        label='Upload Image 2'
    )
    image3 = ImageField(
        widget=ClearableFileInput(attrs={'class': 'form-control'}),
        required=False,
        label='Upload Image 3'
    )
    image4 = ImageField(
        widget=ClearableFileInput(attrs={'class': 'form-control'}),
        required=False,
        label='Upload Image 4'
    )

    class Meta:
        model = ProductStep2
        fields = ['image1', 'image2', 'image3', 'image4']

    def save(self, commit=True):
        productStep2 = super().save(commit=False)
        if self.cleaned_data.get('image1') and self.cleaned_data.get('image2') and self.cleaned_data.get('image3') and self.cleaned_data.get('image4'):
            productStep2.image_upload1 = self.cleaned_data['image1'].read()
            productStep2.image_upload2 = self.cleaned_data['image2'].read()
            productStep2.image_upload3 = self.cleaned_data['image3'].read()
            productStep2.image_upload4 = self.cleaned_data['image4'].read()
        if commit:
            productStep2.save()
        return productStep2


class ProductStep3Form(ModelForm):
    class Meta:
        model = ProductStep3
        fields = ['textarea']
        widgets = {
            'textarea': Textarea(attrs={'class': 'form-control'}),
        }

class CategoryForm(ModelForm):

    class Meta:
        model = Category
        fields = ['category_name','is_active']
        widgets = {
            'category_name': TextInput(attrs={'class': 'form-control'}),
            'is_active': Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'category_name': 'Category',
            'is_active': 'Is Active?',
        }

class SearchProductForm(ModelForm):
    class Meta:
        model = SearchProduct
        fields = ['search_text','from_date','to_date']
        widgets = {
            'search_text': TextInput(attrs={'class': 'form-control'}),
            'from_date': DateInput(attrs={'class': 'form-control'}),
            'to_date': DateInput(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        from_date = cleaned_data.get('from_date')
        to_date = cleaned_data.get('to_date')
        if from_date and to_date:
            if from_date > to_date:
                self.add_error('from_date', 'From date cannot be greater than to date.')
        else:
            if not from_date:
                self.add_error('from_date', 'This field is required.')
            if not to_date:
                self.add_error('to_date', 'This field is required.')
        return cleaned_data