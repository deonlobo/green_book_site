from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import now

from accounts.models import UserProfile
from marketplace.models import Category


def get_user_time_zone(request):
    if request.user.is_authenticated:
        # Get user's profile
        user_profile = get_object_or_404(UserProfile, user=request.user)

        # Get user's time zone
        return user_profile.time_zone
    else:
        return "America/Toronto"

def calculate_duration(created_date):
    now_date = now()
    delta = now_date - created_date
    years = delta.days // 365
    months = (delta.days % 365) // 30
    days = (delta.days % 365) % 30
    return f"{years} years, {months} month{'s' if months != 1 else ''}, {days} day{'s' if days != 1 else ''}"

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

    # middle ware to track user history
    visited_pages = request.session.get('visited_pages', {})

    # Sort pages by visit count
    sorted_pages = sorted(visited_pages.items(), key=lambda x: x[1], reverse=True)

    # Get top 3 visited pages
    top_visited_pages = sorted_pages[:5]

    membership_duration = ""
    if request.user.is_authenticated:
        membership_duration = calculate_duration(user_profile.created_at)

    return render(request, "green_book_app/home.html", {
        "date": date_str,
        "time": time_str,
        "user_profile": user_profile,
        "categories":categories,
        'top_visited_pages': top_visited_pages,
        "membership_duration": membership_duration
    })
