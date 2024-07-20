from django.db import models
from django.utils.html import mark_safe

# Create your models here.

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100)
    is_active = models.BooleanField(choices=[(True,'Yes'),(False,'No')])
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

class ProductStep1(models.Model):
    quality_choices = [('L','Low'),('M','Medium'),('H','High')]
    discounted_choices = [(True,'Yes'),(False,'No')]
    name = models.CharField(max_length=255)
    description = models.TextField()
    quality = models.CharField(choices=quality_choices, max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    category = models.ForeignKey(Category,null=True, related_name='product_category',on_delete=models.CASCADE)
    discounted = models.BooleanField(choices=discounted_choices,default=False)
    percent = models.DecimalField(max_digits=10, decimal_places=2 , blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=[(0 , 'Pending'),(1, 'Active'),(2, 'Out of Stock')], max_length=1)

    def __str__(self):
        return self.name


class ProductStep2(models.Model):
    image_upload1 = models.BinaryField()
    image_upload2 = models.BinaryField()
    image_upload3 = models.BinaryField()
    image_upload4 = models.BinaryField()
    product_step1 = models.ForeignKey(ProductStep1, related_name='product_step2',on_delete=models.CASCADE)

    def image_tag(self, field_name):
        image_field = getattr(self, field_name)
        if image_field:
            # Decode the binary data and encode it as base64
            encoded_image = base64.b64encode(image_field).decode('utf-8')
            print("Hi i am image")
            return mark_safe(f'<img src="data:image/png;base64,{encoded_image}" width="150" height="150" />')
        return "No Image"

    image_tag.short_description = 'Image'

    def image_upload1_tag(self):
        rint("Hi i am image")
        if self.image_upload1:
            from base64 import b64encode
            print("Hi i am image")
            return mark_safe(
                f'<img src="data:image/png;base64,{b64encode(self.image_upload1).decode()}" width="150" height="150" />')
        return "No Image"

    image_upload1_tag.short_description = 'Image'

    def image_upload2_tag(self):
        if self.image_upload2:
            from base64 import b64encode
            return mark_safe(
                f'<img src="data:image/png;base64,{b64encode(self.image_upload2).decode()}" width="150" height="150" />')
        return "No Image"

    image_upload2_tag.short_description = 'Image'

    def image_upload3_tag(self):
        if self.image_upload3:
            from base64 import b64encode
            return mark_safe(
                f'<img src="data:image/png;base64,{b64encode(self.image_upload3).decode()}" width="150" height="150" />')
        return "No Image"

    image_upload3_tag.short_description = 'Image'

    def image_upload4_tag(self):
        if self.image_upload4:
            from base64 import b64encode
            return mark_safe(
                f'<img src="data:image/png;base64,{b64encode(self.image_upload4).decode()}" width="150" height="150" />')
        return "No Image"

    image_upload4_tag.short_description = 'Image'

class ProductStep3(models.Model):
    textarea = models.TextField()
    product_step1 = models.ForeignKey(ProductStep1, related_name='product_step3',on_delete=models.CASCADE)

class SearchProduct(models.Model):
    search_text = models.TextField()
    from_date = models.DateField()
    to_date = models.DateField()
