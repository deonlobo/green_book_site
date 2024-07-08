import re

from django.shortcuts import render, redirect
from .forms import QuestionForm
from django.http import JsonResponse
from .models import Tag, Question
from django.contrib import messages

def home_forum(request):
    return render(request,
                  'forum/home_forum.html',
                  {

                  })

def ask_question_forum(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # Save the question
            question = form.save(commit=False)
            question_id = re.sub(r'[^A-Za-z0-9\s]', '', question.title)
            question_id = re.sub(r'\s+', '-', question_id).lower()

            if Question.objects.filter(title=question_id).exists():
                messages.success(request, 'This question already exists.')
            else:
                question.id = question_id
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
