from django.db import models
from django_ckeditor_5.fields import CKEditor5Field


class Question(models.Model):
    title = models.CharField(max_length=255)
    body = CKEditor5Field('Text', config_name='body_config')

    def __str__(self):
        return self.title
