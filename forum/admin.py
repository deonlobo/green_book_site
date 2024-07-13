from django.contrib import admin

from .models import Question, Vote, QuestionComment
from .models import Tag

# Register your models here.

admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Vote)
admin.site.register(QuestionComment)