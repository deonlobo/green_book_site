from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Project
import os

@receiver(post_delete, sender=Project)
def delete_associated_file(sender, instance, **kwargs):
    if instance.img_1:
        if os.path.isfile(instance.img_1.path):
            os.remove(instance.img_1.path)
    if instance.img_2:
        if os.path.isfile(instance.img_2.path):
            os.remove(instance.img_2.path)