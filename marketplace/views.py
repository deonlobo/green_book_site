from django.shortcuts import render
from django.http import HttpResponse
from .models import *


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
    return render(request, 'view_products.html', {'product':product},{'category':category})
