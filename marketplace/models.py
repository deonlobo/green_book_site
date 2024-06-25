from django.db import models
from django.utils.html import mark_safe

# Create your models here.

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.category_name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image = models.BinaryField()
    category = models.ForeignKey(Category, related_name='category',on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.name

    def image_tag(self):
        if self.image:
            from base64 import b64encode
            return mark_safe(
                f'<img src="data:image/png;base64,{b64encode(self.image).decode()}" width="150" height="150" />')
        return "No Image"

    image_tag.short_description = 'Image'