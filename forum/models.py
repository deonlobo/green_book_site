from django.contrib.auth.models import User
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field

from accounts.models import UserProfile


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name


class Question(models.Model):
    question_id = models.CharField(max_length=500, default='DEFAULT_ID')
    title = models.CharField(max_length=500)
    body = CKEditor5Field('Text', config_name='body_config')
    tags = models.ManyToManyField(Tag, related_name='questions')
    created_ts = models.DateTimeField(auto_now_add=True)
    asked_by = models.ForeignKey(User, related_name='questions_asked', on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class QuestionComment(models.Model):
    question = models.ForeignKey(Question, related_name='comments', on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    body = CKEditor5Field('Text', config_name='comment_config')
    created_ts = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_ts']  # Orders comments by the 'created_ts' field

    def __str__(self):
        return f"Comment {self.id} on {self.question.title}"
