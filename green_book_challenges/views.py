# myapp/subapp/views.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import UserProfile
from .forms import ChallengeForm, CompletedTaskForm
from .models import Challenge, AcceptedChallenge, CompletedTask, Points
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
    return render(request, 'green_book_challenges/home.html', {'form': form, 'challenges': challenges, 'show_alert': show_alert})


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

            # Fetch all completed tasks for the current user
            completed_tasks = CompletedTask.objects.filter(user=request.user)

            # Render the template with updated context
            return render(request, 'green_book_challenges/accepted_challenges_list.html', {
                'accepted_challenges': AcceptedChallenge.objects.filter(user=request.user),
                'completed_tasks': completed_tasks
            })
