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

    def total_votes(self):
        return self.votes.filter(vote_type='upvote').count() - self.votes.filter(vote_type='downvote').count()


class Vote(models.Model):
    UPVOTE = 'upvote'
    DOWNVOTE = 'downvote'
    VOTE_TYPES = [
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
    ]

    question = models.ForeignKey(Question, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='votes', on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=8, choices=VOTE_TYPES)
    created_ts = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('question', 'user')

    def __str__(self):
        return f'{self.vote_type.capitalize()} by {self.user.username} on {self.question.title}'


class QuestionComment(models.Model):
    question = models.ForeignKey(Question, related_name='comments', on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    body = CKEditor5Field('Text', config_name='comment_config')
    created_ts = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_ts']  # Orders comments by the 'created_ts' field

    def __str__(self):
        return f"Comment {self.id} on {self.question.title}"


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    body = CKEditor5Field('Text', config_name='comment_config')
    created_ts = models.DateTimeField(auto_now_add=True)
    asked_by = models.ForeignKey(User, related_name='answered_by', on_delete=models.CASCADE)

    def __str__(self):
        return f"Answer {self.id} on {self.question.title}"

    def total_votes(self):
        return self.answer_votes.filter(vote_type='upvote').count() - self.answer_votes.filter(vote_type='downvote').count()


class AnswerVote(models.Model):
    UPVOTE = 'upvote'
    DOWNVOTE = 'downvote'
    VOTE_TYPES = [
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote'),
    ]

    answer = models.ForeignKey(Answer, related_name='answer_votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='answer_votes', on_delete=models.CASCADE)
    vote_type = models.CharField(max_length=8, choices=VOTE_TYPES)
    created_ts = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('answer', 'user')

    def __str__(self):
        return f'{self.vote_type.capitalize()} by {self.user.username}'


class AnswerComment(models.Model):
    answer = models.ForeignKey(Answer, related_name='answer_comments', on_delete=models.CASCADE)
    commented_by = models.ForeignKey(User, on_delete=models.CASCADE)
    body = CKEditor5Field('Text', config_name='comment_config')
    created_ts = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_ts']  # Orders comments by the 'created_ts' field

    def __str__(self):
        return f"Comment {self.id} on {self.answer_id}"


