import re

from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import localtime

from accounts.models import UserProfile
from .forms import QuestionForm, QuestionCommentForm
from django.http import JsonResponse
from .models import Tag, Question
from django.contrib import messages
import pytz

def home_forum(request):
    questions = Question.objects.all()
    return render(request,
                  'forum/home_forum.html',
                  {
                        'questions' : questions
                  })

def ask_question_forum(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must be logged in to ask a question.')
        return redirect('login')  # Redirect to login or another page

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Save the question
            question = form.save(commit=False)
            question_id = re.sub(r'[^A-Za-z0-9\s]', '', question.title)
            question_id = re.sub(r'\s+', '-', question_id).lower()

            if Question.objects.filter(question_id=question_id).exists():
                messages.success(request, 'This question already exists.')
            else:
                question.question_id = question_id
                question.asked_by = request.user
                # Extract tags from the form
                tags = form.cleaned_data['tags']

                # Create or get existing tags
                tag_objects = []
                for tag_name in tags:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    tag_objects.append(tag)

                # Save the question
                question.save()
                question.tags.set(tag_objects)

                return redirect('home')  # Redirect to home or another page
    else:
        form = QuestionForm()

    return render(request, 'forum/question_forum.html', {'form': form})

def search_tags(request):
    query = request.GET.get('q', '')
    tags = Tag.objects.filter(name__icontains=query).values('name')
    return JsonResponse({'tags': list(tags)})


def get_user_time_zone(request):
    if request.user.is_authenticated:
        # Get user's profile
        user_profile = get_object_or_404(UserProfile, user=request.user)

        # Get user's time zone
        return user_profile.time_zone
    else:
        return "America/Toronto"


def display_question(request, id, question_id):
    question = get_object_or_404(Question, id=id)
    question_comments = question.comments.all()
    user_time_zone = get_user_time_zone(request)
    print(f"User Time Zone: {user_time_zone}")  # Debugging

    if request.method == "POST":
        comment_form = QuestionCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.question = question
            comment.commented_by = request.user
            comment.save()
            return redirect('forum:question_detail', id=question.id, question_id=question_id)
    else:
        comment_form = QuestionCommentForm()

    return render(request,
                  'forum/question_detail.html',
                  {'question': question,
                   'user_time_zone': user_time_zone,
                   'question_comments': question_comments,
                   'comment_form': comment_form})