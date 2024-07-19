from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *

# Create your views here.

def index(request):
    return render(request, "index.html")


def save(request):
    response = HttpResponse()
    count = Category.objects.count()
    if count == 0:
        categories = [
            {'category_name': 'Solar Panels'},
            {'category_name': 'Energy-Efficient Refrigerators'},
            {'category_name': 'Energy-Efficient Washing Machines'},
            {'category_name': 'Energy-Efficient Air Conditioners'},
            {'category_name': 'Wind Turbines'},
            {'category_name': 'Hydropower Systems'},
            {'category_name': 'Electric Cars'},
            {'category_name': 'Hybrid Cars'},
            {'category_name': 'Electric Bikes'},
            {'category_name': 'Smart Home Devices'},
            {'category_name': 'Home Battery Systems'},
            {'category_name': 'Low-Flow Showerheads'},
            {'category_name': 'Composters'}
        ]
        for category in categories:
            c = Category(category_name=category['category_name'])
            c.save()

    categories = Category.objects.all()
    for category in categories:
        response.write(category)
    return response

def category(request, category_id ):
    category = Category.objects.get(category_id=category_id)
    categories = Category.objects.all()
    return render(request, 'category.html', {'category': category,'categories':categories})

def view_products(request, category_id, product_id):
    product = Product.objects.get(id=product_id)
    category = Category.objects.get(category_id=category_id)
    return render(request, 'view-product.html', {'product':product,'category':category})

def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            return redirect('view_products', category_id=product.category_id,product_id=product.id)
    else:
         form = AddProductForm()

    return render(request, 'add-product.html', {'form':form})


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return  render(request, 'add-category.html', {'form':form,'categories':Category.objects.all()})
        else:
            return render(request, 'add-category.html', {'form': form, 'categories': Category.objects.all()})
    else:
        return render(request, 'add-category.html', {'form': CategoryForm(), 'categories': Category.objects.all()})


# def dumy(request):
#     if request.method == 'POST':
#         form = ProductStep2Form(request.POST, request.FILES)
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.save()
#             return redirect('view_products', category_id=product.category_id,product_id=product.id)
#     else:
#          form = ProductStep2Form()
#
#     return render(request, 'demo.html', {'form':form})

