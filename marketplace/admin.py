from django.contrib import admin
from green_book_challenges.models import SubModel
# Register your models here.
from .models import *
admin.site.register(Category)

# myapp/admin.py



admin.site.register(SubModel)

