from django.db import models
from django.contrib.auth.models import User
import uuid
from enum import Enum


class ConversationType(Enum):
    PRIVATE = "private"
    PRIVATE_GROUP = "private_group"
    PUBLIC_GROUP = "public_group"

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]


class Conversation(models.Model):
    conversation_type = models.CharField(
        max_length=15,
        choices=ConversationType.choices(),
        default=ConversationType.PRIVATE.value,
    )
    conversation_uuid = models.UUIDField(
        default=uuid.uuid4, unique=True, editable=False
    )
    conversation_logo = models.URLField(default="")
    conversation_name = models.TextField(default="")
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)
    pinned = models.BooleanField(default=False, blank=True, null=True)

    def get_participants_as_array(self):
        return list(self.participants.all())


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, related_name="messages", on_delete=models.CASCADE
    )
    sender = models.ForeignKey(User, related_name="messages", on_delete=models.CASCADE)
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
