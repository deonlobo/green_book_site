from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class Question(models.Model):
    id = models.CharField(max_length=500, primary_key=True, default='DEFAULT_ID')
    title = models.CharField(max_length=500)
    body = CKEditor5Field('Text', config_name='body_config')
    tags = models.ManyToManyField(Tag, related_name='questions')

    def __str__(self):
        return self.title
