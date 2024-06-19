from django.shortcuts import render
from django.shortcuts import render
from django.utils import timezone
from accounts.models import UserProfile
from marketplace.models import Category


# Create your views here.
def home(request):
    # current date and time
    now = timezone.now()
    date_str = now.strftime("%A, %B %d, %Y")
    time_str = now.strftime("%I:%M %p")

    user_profile = None
    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user_profile = None

    categories = Category.objects.all()
    return render(request, "green_book_app/home.html", {
        "date": date_str,
        "time": time_str,
        "user_profile": user_profile,
        "categories":categories
    })
