from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.db.models import Q, Exists, OuterRef,Count
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
import base64
from base64 import b64encode
from django.contrib import messages
from datetime import datetime, time

from green_book_messenger.models import *

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

@login_required(login_url='login')
def category(request, category_id ):
    category = Category.objects.get(category_id=category_id)
    active_step2_subquery = ProductStep2.objects.filter(product_step1=OuterRef('pk'), is_active=True)
    products = (ProductStep1.objects.filter(
        status=1,
        category=category
    )
    .exclude(user=get_object_or_404(UserProfile, user=request.user))
    .filter(
        Exists(active_step2_subquery)
    ))
    # products = ProductStep1.objects.filter(status=1).filter(category=category).filter(product_step2__is_active=True)
    return render(request, 'category.html', {'category': category,'products':products})
@login_required(login_url='login')
def view_products(request, category_id, product_id):
    product = ProductStep1.objects.get(id=product_id)
    product_description = ProductStep3.objects.get(product_step1=product, is_active=True).textarea;
    images = ProductStep2.objects.all().filter(product_step1__id=product_id).filter(is_active=True)
    imageList = []
    for image in images:
        imageList.append(base64.b64encode(image.image_upload1).decode('utf-8'))
        imageList.append(base64.b64encode(image.image_upload2).decode('utf-8'))
        imageList.append(base64.b64encode(image.image_upload3).decode('utf-8'))
        imageList.append(base64.b64encode(image.image_upload4).decode('utf-8'))
    category = Category.objects.get(category_id=category_id)
    return render(request, 'view-product.html', {'product':product,'category':category,'images':imageList,'product_description':product_description})


@login_required(login_url='login')
def add_product_step_one(request):
    if not request.user.is_authenticated:
        messages.success(request, 'You must be logged in to add a product.')
        return render(request, 'add-product-step-one.html', {'form': ProductStep1Form()})

    if request.method == 'POST':
        form = ProductStep1Form(request.POST)
        if form.is_valid():
            productStep1 = form.save(commit=False)
            productStep1.user = get_object_or_404(UserProfile, user=request.user)
            productStep1.save()
            messages.success(request, 'Your product has been added.')
            productStep1 = ProductStep1.objects.get(id=productStep1.id)
            return redirect('marketplace:add_product_step_two', product_id=productStep1.id)
    else:
        form = ProductStep1Form()
    return render(request, 'add-product-step-one.html', {'form' : form})

@login_required(login_url='login')
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

@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def delete_category(request, category_id):
    category = get_object_or_404(Category, category_id=category_id)
    if category is not None:
        category.delete()
        messages.success(request, 'Category deleted successfully')
        return redirect('marketplace:add_category')
    else:
        messages.success(request, 'Category does not exist')
        return render(request,'add-category.html', {'form': CategoryForm(), 'categories': Category.objects.all()})

@login_required(login_url='login')
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


@login_required(login_url='login')
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

@login_required(login_url='login')
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


@login_required(login_url='login')
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

@login_required(login_url='login')
def manage_products(request):
    if request.method == "POST":
        searchProduct = SearchProductForm(request.POST)
        if searchProduct.is_valid():
            search_text = searchProduct.cleaned_data['search_text']
            from_date = searchProduct.cleaned_data['from_date']
            to_date = searchProduct.cleaned_data['to_date']
            if search_text and from_date and to_date:
                from_date = datetime.combine(from_date, time.min)
                to_date = datetime.combine(to_date, time.max)

                products = (ProductStep1.objects.filter(user=get_object_or_404(UserProfile, user=request.user),name__icontains=searchProduct.cleaned_data['search_text'] , created_at__gte=from_date,created_at__lte=to_date) |
                        ProductStep1.objects.filter(user=get_object_or_404(UserProfile, user=request.user),description__icontains=searchProduct.cleaned_data['search_text'] , created_at__gte=from_date,created_at__lte=to_date) |
                        ProductStep1.objects.filter(user=get_object_or_404(UserProfile, user=request.user),category__category_name__icontains=searchProduct.cleaned_data['search_text'], created_at__gte=from_date,created_at__lte=to_date) |
                        # ProductStep1.objects.filter(status__icontains=searchProduct.cleaned_data['search_text']) |
                        # ProductStep1.objects.filter(quality__icontains=searchProduct.cleaned_data['search_text']) |
                        ProductStep1.objects.filter(user=get_object_or_404(UserProfile, user=request.user),price__icontains=searchProduct.cleaned_data['search_text'],created_at__gte=from_date,created_at__lte=to_date) |
                        ProductStep1.objects.filter(user=get_object_or_404(UserProfile, user=request.user),stock__icontains=searchProduct.cleaned_data['search_text'],created_at__gte=from_date,created_at__lte=to_date)

                        )
            elif from_date and to_date:
                from_date = datetime.combine(from_date, time.min)
                to_date = datetime.combine(to_date, time.max)
                products = (ProductStep1.objects.filter(user=get_object_or_404(UserProfile, user=request.user),
                                                        created_at__gte=from_date, created_at__lte=to_date))

            else:

                products = (ProductStep1.objects.filter(user=get_object_or_404(UserProfile, user=request.user),name__icontains=searchProduct.cleaned_data['search_text']) |
                        ProductStep1.objects.filter(user=get_object_or_404(UserProfile, user=request.user),description__icontains=searchProduct.cleaned_data['search_text']) |
                        ProductStep1.objects.filter(user=get_object_or_404(UserProfile, user=request.user),category__category_name__icontains=searchProduct.cleaned_data['search_text']) |
                        # ProductStep1.objects.filter(status__icontains=searchProduct.cleaned_data['search_text']) |
                        # ProductStep1.objects.filter(quality__icontains=searchProduct.cleaned_data['search_text']) |
                        ProductStep1.objects.filter(user=get_object_or_404(UserProfile, user=request.user),price__icontains=searchProduct.cleaned_data['search_text']) |
                        ProductStep1.objects.filter(user=get_object_or_404(UserProfile, user=request.user),stock__icontains=searchProduct.cleaned_data['search_text']))
            print(products)
            return render(request, "manage-product.html", {'form': searchProduct, 'products': products})
        else:
            return render(request,"manage-product.html",{'form': searchProduct, 'products' : ProductStep1.objects.filter(user=get_object_or_404(UserProfile, user=request.user))})

    else:
        form = SearchProductForm()
        # messages.success(request, 'Product updated successfully!')
        products = ProductStep1.objects.filter(user=get_object_or_404(UserProfile, user=request.user))
        return render(request,"manage-product.html", {'form':form,'products':products})

@login_required(login_url='login')
def delete_product(request,product_step1_id):
    product_step1 = get_object_or_404(ProductStep1, pk=product_step1_id)
    if product_step1_id is not None:
        product_step1.delete()
        messages.success(request, "Product deleted successfully")
        return redirect('marketplace:manage_products')
    else:
        messages.success(request, "Product not deleted successfully")
        return redirect('marketplace:manage_products')



@login_required(login_url='login')
def create_chat(request, product_step1_id):
    product_step1 = get_object_or_404(ProductStep1, pk=product_step1_id)
    # existing_conversation = Conversation.objects.filter(
    #     conversation_type="private",
    #     participants__in=[product_step1.user.user, request.user],
    # )
    existing_conversation = (Conversation.objects.annotate(num_participants=Count('participants')).
                             filter(conversation_type="private", num_participants=2, participants=product_step1.user.user)).filter(participants=request.user)

    if len(existing_conversation) >0:
        return redirect("/messenger/{}".format(existing_conversation[0].conversation_uuid))
    conversation = Conversation.objects.create(
        conversation_type = "private",
        conversation_name = product_step1.user.user.first_name + " " + product_step1.user.user.last_name,
    )
    conversation.participants.add(request.user, product_step1.user.user)
    conversation.save()
    conversation_id = conversation.conversation_uuid
    return redirect("/messenger/{}".format(conversation_id))


