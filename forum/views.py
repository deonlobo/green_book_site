from django.shortcuts import render, redirect
from .forms import QuestionForm

def home_forum(request):
    return render(request,
                  'forum/home_forum.html',
                  {

                  })

def ask_question_forum(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirect to home or another page
    else:
        form = QuestionForm()

    return render(request,
                  'forum/question_forum.html',
                  {'form': form
                   })

