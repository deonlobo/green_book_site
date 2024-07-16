# myapp/subapp/views.py

from django.shortcuts import render

from accounts.models import UserProfile
from .forms import ChallengeForm
from .models import SubModel


def challenge1(request):
    form = ChallengeForm()

    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            # Process form data (save to database, send email, etc.)
            # For demonstration, print cleaned data
            print(form.cleaned_data)
            # Redirect to a success page or render the home page again
            return render(request, 'green_book_challenges/home.html', {'form': form})

    return render(request, 'green_book_challenges/home.html', {'form': form})
