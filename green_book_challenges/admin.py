from django.contrib import admin
from .models import Challenge, AcceptedChallenge, CompletedTask, Points
from accounts.models import UserProfile

admin.site.register(Challenge)
admin.site.register(AcceptedChallenge)
admin.site.register(CompletedTask)
admin.site.register(Points)