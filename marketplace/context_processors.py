from .models import Category,ProductStep1

def categories_processor(request):
    categories = Category.objects.filter(is_active=True)
    return {'product_categories': categories}

def products_processor(request):
    products = ProductStep1.objects.filter(status=1).count()
    return {'product_count': products}