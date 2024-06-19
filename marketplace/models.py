from django.db import models

# Create your models here.

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    creation_time = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.category_name
