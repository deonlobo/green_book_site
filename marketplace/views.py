from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from .forms import *
import base64
from base64 import b64encode

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

def add_product_step_one(request):
    if request.method == 'POST':
        form = ProductStep1Form(request.POST)
        if form.is_valid():
            productStep1 = form.save(commit=False)
            productStep1.save()
            test = ProductStep1.objects.get(id=productStep1.id)
            return redirect('marketplace:view_products', product_id=test.id)
    else:
        form = ProductStep1Form()
    return render(request, 'add-product-step-one.html', {'form' : form})

def modify_add_product_step_one(request,product_id):
    product = get_object_or_404(ProductStep1, id=product_id)
    if request.method == 'POST':
        form = ProductStep1Form(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return render(request, 'add-product-step-one.html', {'form': form, 'success': True})
    else:
        form = ProductStep1Form(instance=product)

    return render(request, 'add-product-step-one.html', {'form': form})

def modify_add_product_step_two(request,product_id):
    if request.method == 'POST':
        form = ProductStep2Form(request.POST,request.FILES)
        if form.is_valid():
            imageform = form.save(commit=False)
            productstep1 = ProductStep1.objects.get(id=product_id)
            imageform.product_step1 = productstep1
            imageform.save()
            return render(request,'add-product-step-two.html',{'form':ProductStep2Form(),'product_id':product_id})
    else:
        form = ProductStep2Form()
        images = ProductStep2.objects.all().filter(product_step1__id=product_id).order_by('-pk')
        imageList = []
        for image in images:
            imageList.append(base64.b64encode(image.image_upload1).decode('utf-8'))
            imageList.append(base64.b64encode(image.image_upload2).decode('utf-8'))
            imageList.append(base64.b64encode(image.image_upload3).decode('utf-8'))
            imageList.append(base64.b64encode(image.image_upload4).decode('utf-8'))

        context = {
            'form': form,
            'product_id': product_id,
            'images': imageList # Pass images queryset to the template context
        }
       # // print(images[0].image_upload1)
        return render(request,'add-product-step-two.html',context)


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

def add_product_step_two(request, product_id):
    if request.method == 'POST':
        form = ProductStep2Form(request.POST,request.FILES)
        if form.is_valid():
            imageform = form.save(commit=False)
            productstep1 = ProductStep1.objects.get(id=product_id)
            imageform.product_step1 = productstep1
            imageform.save()
            return render(request,'add-product-step-two.html',{'form':ProductStep2Form(),'product_id':product_id})
    else:
        form = ProductStep2Form()
        images = ProductStep2.objects.all().filter(product_step1__id=product_id).order_by('-pk')
        imageList = []
        for image in images:
            imageList.append(base64.b64encode(image.image_upload1).decode('utf-8'))
            imageList.append(base64.b64encode(image.image_upload2).decode('utf-8'))
            imageList.append(base64.b64encode(image.image_upload3).decode('utf-8'))
            imageList.append(base64.b64encode(image.image_upload4).decode('utf-8'))

        context = {
            'form': form,
            'product_id': product_id,
            'images': imageList # Pass images queryset to the template context
        }
       # // print(images[0].image_upload1)
        return render(request,'add-product-step-two.html',context)

def add_product_step_three(request, product_id):
    if request.method == 'POST':
        # form = ProductStep3Form(request.POST)
        # if form.is_valid():
        #     productStep3 = form.save(commit=False)
        #     productStep3.save()
             return redirect('view_products', product_id=product_id)
    else:
        # form = ProductStep3Form()
        product = ProductStep1.objects.get(id=product_id)
        images = ProductStep2.objects.all().filter(product_step1__id=product_id).order_by('-pk')
        imageList = []
        for image in images:
            imageList.append(base64.b64encode(image.image_upload1).decode('utf-8'))
            imageList.append(base64.b64encode(image.image_upload2).decode('utf-8'))
            imageList.append(base64.b64encode(image.image_upload3).decode('utf-8'))
            imageList.append(base64.b64encode(image.image_upload4).decode('utf-8'))


        return render(request, 'add-product-step-three.html', {'product': product, 'images': imageList})

def admin_manage_products(request):
    if request.method == "POST":
        searchProduct = SearchProductForm(request.POST)
        if searchProduct.is_valid():
            products = (ProductStep1.objects.filter(name__icontains=searchProduct.cleaned_data['search_text']) |
                        ProductStep1.objects.filter(description__icontains=searchProduct.cleaned_data['search_text']) |
                        ProductStep1.objects.filter(category__category_name__icontains=searchProduct.cleaned_data['search_text']) |
                        # ProductStep1.objects.filter(status__icontains=searchProduct.cleaned_data['search_text']) |
                        # ProductStep1.objects.filter(quality__icontains=searchProduct.cleaned_data['search_text']) |
                        ProductStep1.objects.filter(price__icontains=searchProduct.cleaned_data['search_text']) |
                        ProductStep1.objects.filter(stock__icontains=searchProduct.cleaned_data['search_text'])
                        )
            return render(request, "manage-product.html", {'form': searchProduct, 'products': products})
        else:
            return render(request,"manage-product.html",{'form': searchProduct, 'products' : ProductStep1.objects.all()})

    else:
        form = SearchProductForm()
        # messages.success(request, 'Product updated successfully!')
        products = ProductStep1.objects.all()
        return render(request,"manage-product.html", {'form':form,'products':products})

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

