from django.contrib import admin

from .models import Question, Vote
from .models import Tag

# Register your models here.

admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Vote)