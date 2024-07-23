from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.db.models import Q, Exists, OuterRef
from .models import *
from .forms import *
import base64
from base64 import b64encode
from django.contrib import messages

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
    active_step2_subquery = ProductStep2.objects.filter(product_step1=OuterRef('pk'), is_active=True)
    products = (ProductStep1.objects.filter(
        status=1
    )
    .exclude(user=get_object_or_404(UserProfile, user=request.user))
    .filter(
        Exists(active_step2_subquery)
    ))
    # products = ProductStep1.objects.filter(status=1).filter(category=category).filter(product_step2__is_active=True)
    return render(request, 'category.html', {'category': category,'products':products})

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
    if not request.user.is_authenticated:
        messages.success(request, 'You must be logged in to add a product.')
        return render(request, 'add-product-step-one.html', {'form': ProductStep1Form()})

    if request.method == 'POST':
        form = ProductStep1Form(request.POST)
        if form.is_valid():
            productStep1 = form.save(commit=False)
            productStep1.user =  get_object_or_404(UserProfile, user=request.user)
            productStep1.save()
            messages.success(request, 'Your product has been added.')
            productStep1 = ProductStep1.objects.get(id=productStep1.id)
            return redirect('marketplace:add_product_step_two', product_id=productStep1.id)
    else:
        form = ProductStep1Form()
    return render(request, 'add-product-step-one.html', {'form' : form})

def modify_add_product_step_one(request,product_id):
    product = get_object_or_404(ProductStep1, id=product_id)
    if request.method == 'POST':
        form = ProductStep1Form(request.POST, instance=product)
        if form.is_valid():
            form.save()
            if ProductStep2.objects.filter(product_step1=product).exists():
                messages.success(request, 'Your product has been updated.')
                return redirect('marketplace:modify_add_product_step_two', product_id=product.id)
            else:
                messages.success(request, 'Your product has been updated.')
                return redirect('marketplace:add_product_step_two', product_id=product.id)

    else:
        form = ProductStep1Form(instance=product)

    return render(request, 'add-product-step-one.html', {'form': form})

def modify_add_product_step_two(request,product_id):
    if request.method == 'POST':
        form = ProductStep2Form(request.POST,request.FILES)
        if form.is_valid():
            product_step1 = get_object_or_404(ProductStep1, pk=product_id)
            if ProductStep2.objects.filter(product_step1=product_step1, is_active=True).count() > 0:
                ProductStep2.objects.filter(product_step1=product_step1).update(is_active=False)
            imageform = form.save(commit=False)
            imageform.product_step1 = product_step1
            imageform.is_active = True
            imageform.save()
            if ProductStep3.objects.filter(product_step1=product_step1, is_active=True).count() > 0:
                messages.success(request,"Your images have been updated")
                return redirect('marketplace:modify_add_product_step_three', product_id=product_id)
            else:
                messages.success(request,"Your images have been uploaded")
                return redirect('marketplace:add_product_step_three', product_id=product_id)
        else:
            images = ProductStep2.objects.all().filter(product_step1__id=product_id).filter(is_active=True)
            imageList = []
            for image in images:
                imageList.append(base64.b64encode(image.image_upload1).decode('utf-8'))
                imageList.append(base64.b64encode(image.image_upload2).decode('utf-8'))
                imageList.append(base64.b64encode(image.image_upload3).decode('utf-8'))
                imageList.append(base64.b64encode(image.image_upload4).decode('utf-8'))

            context = {
                'form': form,
                'product_id': product_id,
                'images': imageList
            }
            return render(request, 'add-product-step-two.html', context)
    else:
        form = ProductStep2Form()
        images = ProductStep2.objects.all().filter(product_step1__id=product_id).filter(is_active=True)
        imageList = []
        for image in images:
            imageList.append(base64.b64encode(image.image_upload1).decode('utf-8'))
            imageList.append(base64.b64encode(image.image_upload2).decode('utf-8'))
            imageList.append(base64.b64encode(image.image_upload3).decode('utf-8'))
            imageList.append(base64.b64encode(image.image_upload4).decode('utf-8'))

        context = {
            'form': form,
            'product_id': product_id,
            'images': imageList
        }
        return render(request,'add-product-step-two.html',context)


def add_category(request):
    if not request.user.is_authenticated:
        messages.success(request, 'You must be logged in to add a category.')
        return render(request, 'add-category.html', {'form': CategoryForm(), 'categories': Category.objects.all()})
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            messages.success(request, 'Category added successfully')
            return  render(request, 'add-category.html', {'form':form,'categories':Category.objects.all()})
        else:
            return render(request, 'add-category.html', {'form': form, 'categories': Category.objects.all()})
    else:
        return render(request, 'add-category.html', {'form': CategoryForm(), 'categories': Category.objects.all()})


def modify_category(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category {category.category_name} has been updated')
            return redirect('marketplace:add_category')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'add-category.html', {
        'form': form,
        'categories': Category.objects.all(),
        'editing': True
    })


def activate_category(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)
    if category is not None:
        category.activate()
        category.save()
        messages.success(request, f'Category {category.category_name} activated')
        return redirect('marketplace:add_category')
    else:
        messages.success(request, 'Category does not exist')
        return render(request,'add-category.html', {'form': CategoryForm(), 'categories': Category.objects.all()})


def delete_category(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)
    if category is not None:
        category.delete()
        messages.success(request, 'Category deleted successfully')
        return redirect('marketplace:add_category')
    else:
        messages.success(request, 'Category does not exist')
        return render(request,'add-category.html', {'form': CategoryForm(), 'categories': Category.objects.all()})

def add_product_step_two(request, product_id):
    if not request.user.is_authenticated:
        messages.success(request, 'You must be logged in to upload images.')
        return render(request,'add-product-step-two.html',{'form':ProductStep2Form(),'product_id':product_id})

    if request.method == 'POST':
        form = ProductStep2Form(request.POST,request.FILES)
        if form.is_valid():
            imageform = form.save(commit=False)
            productstep1 = ProductStep1.objects.get(id=product_id)
            imageform.product_step1 = productstep1
            imageform.save()
            messages.success(request, 'Your images have been uploaded.')
            return redirect('marketplace:add_product_step_three', product_id=product_id)
        else:
            return render(request, 'add-product-step-two.html', {'form': form, 'product_id': product_id})
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
            'images': imageList
        }
        return render(request,'add-product-step-two.html',context)


def add_product_step_three(request, product_id):
    if request.method == 'POST':
        form = ProductStep3Form(request.POST)
        if form.is_valid():
            product_step1 = get_object_or_404(ProductStep1, pk=product_id)
            if ProductStep3.objects.filter(product_step1=product_step1, is_active=True).count() > 0:
                ProductStep3.objects.filter(product_step1=product_step1, is_active=True).update(is_active=False)
            new_description = form.save(commit=False)
            new_description.product_step1 = product_step1
            new_description.is_active = True
            new_description.save()
            messages.success(request, 'Your description have been uploaded.')
            return redirect('marketplace:add_product_step_four',product_id=product_id)
        else:
            return render(request, 'add-product-step-three.html', {'form': form,'product_id':product_id})
    else:
        form = ProductStep3Form()
        return render(request, 'add-product-step-three.html', {'form':form,'product_id':product_id})

def modify_add_product_step_three(request, product_id):
    product_step1 = get_object_or_404(ProductStep1, pk=product_id)
    if request.method == 'POST':
        form = ProductStep3Form(request.POST)
        if form.is_valid():
            if ProductStep3.objects.filter(product_step1=product_step1, is_active=True).count() > 0:
                ProductStep3.objects.filter(product_step1=product_step1, is_active=True).update(is_active=False)
            new_description = form.save(commit=False)
            new_description.product_step1 = product_step1
            new_description.is_active = True
            new_description.save()
            messages.success(request, 'Your description have been uploaded.')
            return redirect('marketplace:add_product_step_four',product_id=product_id)
        else:
            return render(request, 'add-product-step-three.html', {'form': form,'product_id':product_id})
    else:
        productStep3 = ProductStep3.objects.get(product_step1=product_step1, is_active=True)
        form = ProductStep3Form(instance=productStep3)
        return render(request, 'add-product-step-three.html', {'form':form,'product_id':product_id})


def add_product_step_four(request, product_id):
    if request.method == 'POST':
        product = ProductStep1.objects.get(id=product_id)
        product.status = 1
        product.save()
        messages.success(request, 'Your product has been created')
        return redirect('marketplace:manage_products')
    else:
        product = ProductStep1.objects.get(id=product_id)
        product_description = ProductStep3.objects.get(product_step1=product, is_active=True).textarea;
        images = ProductStep2.objects.all().filter(product_step1__id=product_id).order_by('-pk')
        imageList = []
        for image in images:
            imageList.append(base64.b64encode(image.image_upload1).decode('utf-8'))
            imageList.append(base64.b64encode(image.image_upload2).decode('utf-8'))
            imageList.append(base64.b64encode(image.image_upload3).decode('utf-8'))
            imageList.append(base64.b64encode(image.image_upload4).decode('utf-8'))
        return render(request, 'add-product-step-four.html', {'product': product, 'images': imageList,'product_description':product_description})

def manage_products(request):
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

            products = products.objects.filter(user=get_object_or_404(UserProfile, user=request.user))
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

