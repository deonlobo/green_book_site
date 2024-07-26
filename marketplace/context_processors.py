from .models import Category

def categories_processor(request):
    categories = Category.objects.filter(is_active=True)
    return {'categories': categories}