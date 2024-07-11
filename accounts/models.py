from datetime import timezone, datetime

from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)  # Automatically set the field to now when the object is first created
    time_zone = models.CharField(max_length=50, default='America/Toronto')  # Default time zone as Toronto
    def __str__(self):
        return self.user.username