# myapp/subapp/views.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import UserProfile
from .forms import ChallengeForm, CompletedTaskForm
from .models import Challenge, AcceptedChallenge, CompletedTask, Points, LikedTask
from django.contrib import messages


def challenge1(request):
    form = ChallengeForm()
    show_alert = False

    if request.method == 'POST':
        form = ChallengeForm(request.POST, request.FILES)
        if form.is_valid():
            # Get the user's profile (assuming you have UserProfile linked to User)
            # user_profile = UserProfile.objects.get(user=request.user)

            # Create a new Challenge instance with form data
            new_challenge = Challenge(
                # user_profile=user_profile,
                title=form.cleaned_data['title'],
                task=form.cleaned_data['task'],
                image=request.FILES.get('image'),  # Handle file upload if any
                deadline=form.cleaned_data['deadline']
            )
            # Save the new challenge to the database
            new_challenge.save()

            # Update points
            points_record, created = Points.objects.get_or_create(user=request.user)
            points_record.total_points += 2000
            points_record.save()

            # Set flag to show alert
            show_alert = True

    challenges = Challenge.objects.all()
    return render(request, 'green_book_challenges/home.html',
                  {'form': form, 'challenges': challenges, 'show_alert': show_alert})


def accept_challenge_view(request, pk):
    challenge = get_object_or_404(Challenge, pk=pk)

    if request.user.is_authenticated:
        # Check if the user has already accepted this challenge
        if not AcceptedChallenge.objects.filter(user=request.user, challenge=challenge).exists():
            # Create a new AcceptedChallenge instance
            accepted_challenge = AcceptedChallenge(user=request.user, challenge=challenge)
            accepted_challenge.save()

            # Return success response
            return JsonResponse({'success': True})
        else:
            # If already accepted, return response indicating no action needed
            return JsonResponse({'success': False, 'message': 'Challenge already accepted.'})
    else:
        # Return error response if user is not authenticated
        return JsonResponse({'success': False, 'message': 'User not authenticated.'}, status=401)


def accepted_challenges_list_view(request):
    completed_task_form = CompletedTaskForm()
    if request.user.is_authenticated:
        accepted_challenges = AcceptedChallenge.objects.filter(user=request.user)
        # Fetch all completed tasks for the current user
        completed_tasks = CompletedTask.objects.filter(user=request.user)
        context = {
            'accepted_challenges': accepted_challenges,
            'completed_task_form': completed_task_form,
            'completed_tasks': completed_tasks

        }
        return render(request, 'green_book_challenges/accepted_challenges_list.html', context)
    else:
        return redirect('login')


# def submit_completed_task_view(request):
#     if request.method == 'POST':
#         challenge_id = request.POST.get('challenge')
#         form = CompletedTaskForm(request.POST, request.FILES)
#         if form.is_valid():
#             completed_task = form.save(commit=False)
#             completed_task.user = request.user
#             completed_task.challenge = get_object_or_404(Challenge, id=challenge_id)
#             completed_task.save()
#
#             # Remove the challenge from accepted challenges list
#             AcceptedChallenge.objects.filter(user=request.user, challenge__id=challenge_id).delete()
#
#             # Fetch all completed tasks for the current user
#             completed_tasks = CompletedTask.objects.filter(user=request.user)
#
#             # Render the template with updated context
#             return render(request, 'green_book_challenges/accepted_challenges_list.html', {
#                 'accepted_challenges': AcceptedChallenge.objects.filter(user=request.user),
#                 'completed_tasks': completed_tasks
#             })
def submit_completed_task_view(request):
    if request.method == 'POST':
        challenge_id = request.POST.get('challenge')
        form = CompletedTaskForm(request.POST, request.FILES)
        if form.is_valid():
            completed_task = form.save(commit=False)
            completed_task.user = request.user
            completed_task.challenge = get_object_or_404(Challenge, id=challenge_id)
            completed_task.save()

            # Remove the challenge from accepted challenges list
            AcceptedChallenge.objects.filter(user=request.user, challenge__id=challenge_id).delete()

            # Return success response
            return JsonResponse({'success': True})

    # Return error response if form is not valid
    return JsonResponse({'success': False, 'errors': 'Form is invalid or other error.'})

@login_required
def completed_tasks_list(request):
    # Fetch all completed tasks excluding those that the user has liked and posted
    completed_tasks = CompletedTask.objects.exclude(likedtask__user=request.user).exclude(user=request.user)

    # Render the template with the filtered tasks
    return render(request, 'green_book_challenges/completed_tasks_list.html', {'completed_tasks': completed_tasks})


def like_completed_task(request, task_id):
    show_alert = False
    if request.method == 'POST':
        task = get_object_or_404(CompletedTask, id=task_id)
        # Check if the user has already liked this task
        liked_task = LikedTask.objects.filter(user=request.user, task=task).first()

        if not liked_task:
            # Add points to user
            points_record, created = Points.objects.get_or_create(user=request.user)
            points_record.total_points += 1000
            points_record.save()

            # Increment the likes count
            task.likes += 1
            task.save()

            # Create a LikedTask record
            LikedTask.objects.create(user=request.user, task=task)

            # Set flag to show alert
            show_alert = True

    # Exclude tasks that the user has already liked
    completed_tasks = CompletedTask.objects.exclude(likedtask__user=request.user)

    return render(request, 'green_book_challenges/completed_tasks_list.html', {
        'completed_tasks': completed_tasks,
        'show_alert': show_alert
    })

@login_required
def points_and_coupons_view(request):
    user_points = Points.objects.get(user=request.user)
    leaderboard = Points.objects.order_by('-total_points')[:3]  # Top 3 users
    return render(request, 'green_book_challenges/points.html', {
        'user_points': user_points,
        'leaderboard': leaderboard
    })