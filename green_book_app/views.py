from django.shortcuts import render, get_object_or_404
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import now

from accounts.models import UserProfile, User
from green_book_messenger.models import Message
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

    # middle ware to track user history
    visited_pages = request.session.get("visited_pages", {})

    # Sort pages by visit count
    sorted_pages = sorted(visited_pages.items(), key=lambda x: x[1], reverse=True)

    # Get top 3 visited pages
    top_visited_pages = sorted_pages[:5]

    membership_duration = ""
    if request.user.is_authenticated:
        membership_duration = calculate_duration(user_profile.created_at)

    active_users = User.objects.filter(is_active=True).count()
    messages = Message.objects.count()
    return render(
        request,
        "green_book_app/home.html",
        {
            "date": date_str,
            "time": time_str,
            "user_profile": user_profile,
            "top_visited_pages": top_visited_pages,
            "membership_duration": membership_duration,
            "active_users": active_users,
            "message_count": messages,
        },
    )


def contact_page(request):
    team_members = [
        {
            "name": "Deon Victor Lobo",
            "student_id": "110127749",
            "image_url": "green_book_app/assets/deon_lobo.jpg",
        },
        {
            "name": "Zeel Thakkar",
            "student_id": "110125679",
            "image_url": "green_book_app/assets/zeel.jpg",
        },
        {
            "name": "Dekshitha Ravikumar",
            "student_id": "110126006",
            "image_url": "green_book_app/assets/dekshitha.png",
        },
        {
            "name": "Gagandeep Singh",
            "student_id": "110123330",
            "image_url": "green_book_app/assets/gagan.jpg",
        },
        {
            "name": "Kashyap Prajapati",
            "student_id": "110126934",
            "image_url": "green_book_app/assets/gagan.jpg",
        },
        {
            "name": "Sachreet Kaur",
            "student_id": "110122441",
            "image_url": "green_book_app/assets/gagan.jpg",
        },
    ]
    return render(
        request, "green_book_app/contact.html", {"team_members": team_members}
    )
