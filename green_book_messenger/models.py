from django.db import models
from django.contrib.auth.models import User
import uuid 

class Conversation(models.Model):
    conversation_uuid = models.UUIDField(default= uuid.uuid4, unique=True, editable = False)
    conversation_logo = models.URLField(default="")
    conversation_name = models.TextField(default="")
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} from {self.sender}"
    
    
    
# django-admin startproject mysite
# python manage.py runserver
# python manage.py startapp polls
# python manage.py makemigrations myapp
# python manage.py migrate
# python manage.py sqlmigrate app 0003
# python manage.py createsuperuser
# python manage.py shell