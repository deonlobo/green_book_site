import re
from datetime import timedelta, datetime

from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, F, Q, OuterRef, Subquery, Value
from django.utils import timezone
from django.utils.timezone import now

from accounts.models import UserProfile
from .forms import QuestionForm, QuestionCommentForm, AnswerForm, AnswerCommentForm
from django.http import JsonResponse
from .models import Tag, Question, Vote, Answer, AnswerVote
from django.contrib import messages
import pytz
from django.contrib.auth.decorators import login_required
def validate_user_login(request, message, redirect_url='login'):
    if not request.user.is_authenticated:
        messages.error(request, message)
        return redirect(redirect_url)  # Redirect to login or another page
    return None

def search_questions(request):
    query = request.GET.get('q', '')
    if query:
        questions = Question.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(tags__name__icontains=query)  # Search in tags
        ).annotate(
            total_votes=Count('votes', filter=Q(votes__vote_type='upvote')) - Count('votes', filter=Q(
                votes__vote_type='downvote'))
        ).order_by('-total_votes')[:10].values('id', 'question_id', 'title', 'body')
        return JsonResponse({'questions': list(questions)})
    return JsonResponse({'questions': []})


def home_forum(request):
    header = 'Top Questions'
    top_questions = (
        Question.objects.annotate(
            total_votes=Count('votes', filter=Q(votes__vote_type='upvote')) - Count('votes', filter=Q(votes__vote_type='downvote'))
        ).order_by('-total_votes')[:10]
    )
    user_time_zone = get_user_time_zone(request)

    query = request.GET.get('search', '')
    tag = request.GET.get('tag', '')
    if query:
        header = 'Search Results'
        if tag:
            questions = Question.objects.filter(
                Q(tags__name=query)  # Search in tags
            ).annotate(
                total_votes=Count('votes', filter=Q(votes__vote_type='upvote')) - Count('votes', filter=Q(
                    votes__vote_type='downvote'))
            ).order_by('-total_votes')
        else:
            questions = Question.objects.filter(
                Q(title__icontains=query) |
                Q(body__icontains=query) |
                Q(tags__name__icontains=query)  # Search in tags
            ).annotate(
                total_votes=Count('votes', filter=Q(votes__vote_type='upvote')) - Count('votes', filter=Q(
                    votes__vote_type='downvote'))
            ).order_by('-total_votes')
    else:
        # Calculate the date 30 days ago
        thirty_days_ago = datetime.now() - timedelta(days=30)

        # Filter, annotate, and order the questions
        questions = Question.objects.filter(
            created_ts__gte=thirty_days_ago  # Filter questions from the past 30 days
        ).annotate(
            total_votes=Count('votes', filter=Q(votes__vote_type='upvote')) - Count('votes', filter=Q(
                votes__vote_type='downvote'))
        ).order_by('-total_votes')

    return render(request, 'forum/home_forum.html',
                  {'questions': questions,
                   'top_questions': top_questions,
                   'user_time_zone': user_time_zone,
                   'header': header,
                   'query': query})

def question_tab_forum(request):
    top_questions = (
        Question.objects.annotate(
            total_votes=Count('votes', filter=Q(votes__vote_type='upvote')) - Count('votes', filter=Q(votes__vote_type='downvote'))
        ).order_by('-total_votes')[:10]
    )
    user_time_zone = get_user_time_zone(request)

    questions = Question.objects.all().order_by('-created_ts')

    return render(request, 'forum/home_forum.html',
                  {'questions': questions,
                   'top_questions': top_questions,
                   'user_time_zone': user_time_zone,
                   'header': 'All Questions'})
def ask_question_forum(request):
    response = validate_user_login(request, 'You must be logged in to ask a question.')
    if response:
        return response
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():

            # Extract the cleaned data from the form
            body = form.cleaned_data.get('body', '').strip()
            # Check if the body field is empty or contains only non-visible content
            if is_blank_html(body):
                # Add a form error if body is blank or contains only non-visible content
                messages.error(request, 'The comment cannot be blank')
                return render(request, 'forum/question_forum.html', {'form': form})

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
                messages.success(request, 'Question submitted successfully')
                return redirect('forum:home_forum')  # Redirect to home or another page
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


def upvote_question(request, id):
    question = get_object_or_404(Question, id=id)
    user = request.user

    # Check if the user has already voted on this question
    existing_vote = Vote.objects.filter(question=question, user=user).first()

    if existing_vote:
        if existing_vote.vote_type == Vote.UPVOTE:
            # If the existing vote is an upvote, do nothing
            existing_vote.delete()
            return JsonResponse({'status': 'already_upvoted', 'value': existing_vote.question.total_votes()})
        else:
            # If the existing vote is a downvote, change it to upvote
            existing_vote.vote_type = Vote.UPVOTE
            existing_vote.save()
            return JsonResponse({'status': 'vote_changed', 'value': existing_vote.question.total_votes()})
    else:
        # If no existing vote, create a new upvote
        new_vote = Vote.objects.create(question=question, user=user, vote_type=Vote.UPVOTE)
        return JsonResponse({'status': 'upvoted','value': new_vote.question.total_votes()})

def downvote_question(request, id):
    question = get_object_or_404(Question, id=id)
    user = request.user

    # Check if the user has already voted on this question
    existing_vote = Vote.objects.filter(question=question, user=user).first()

    if existing_vote:
        if existing_vote.vote_type == Vote.DOWNVOTE:
            # If the existing vote is a downvote, delete
            existing_vote.delete()
            return JsonResponse({'status': 'already_downvoted', 'value': existing_vote.question.total_votes()})
        else:
            # If the existing vote is an upvote, change it to downvote
            existing_vote.vote_type = Vote.DOWNVOTE
            existing_vote.save()
            return JsonResponse({'status': 'vote_changed', 'value': existing_vote.question.total_votes()})
    else:
        # If no existing vote, create a new downvote
        new_vote = Vote.objects.create(question=question, user=user, vote_type=Vote.DOWNVOTE)
        return JsonResponse({'status': 'downvoted','value': new_vote.question.total_votes()})

def display_question(request, id, question_id):
    question = get_object_or_404(Question, id=id)
    answers = question.answers.annotate(
        total_votes=Count('answer_votes', filter=Q(answer_votes__vote_type='upvote')) - Count('answer_votes', filter=Q(
            answer_votes__vote_type='downvote'))
    ).order_by('-total_votes')

    question_comments = question.comments.all()
    user_time_zone = get_user_time_zone(request)

    comment_form = QuestionCommentForm()
    answer_form = AnswerForm()
    answer_comment_form = AnswerCommentForm()

    top_questions = (
        Question.objects.annotate(
            total_upvotes=Count('votes', filter=Q(votes__vote_type='upvote')),
            total_downvotes=Count('votes', filter=Q(votes__vote_type='downvote')),
            total_votes=F('total_upvotes') - F('total_downvotes')
        ).order_by('-total_votes')[:10]
    )
    return render(request, 'forum/question_detail.html', {
        'question': question,
        'user_time_zone': user_time_zone,
        'question_comments': question_comments,
        'answers': answers,
        'comment_form': comment_form,
        'answer_form': answer_form,
        'answer_comment_form': answer_comment_form,
        'top_questions': top_questions
    })


def upvote_answer(request, id):
    answer = get_object_or_404(Answer, id=id)
    user = request.user

    # Check if the user has already voted on this answer
    existing_vote = AnswerVote.objects.filter(answer=answer, user=user).first()

    if existing_vote:
        if existing_vote.vote_type == AnswerVote.UPVOTE:
            # If the existing vote is an upvote, do nothing
            existing_vote.delete()
            return JsonResponse({'status': 'already_upvoted', 'value': existing_vote.answer.total_votes()})
        else:
            # If the existing vote is a downvote, change it to upvote
            existing_vote.vote_type = AnswerVote.UPVOTE
            existing_vote.save()
            return JsonResponse({'status': 'vote_changed', 'value': existing_vote.answer.total_votes()})
    else:
        # If no existing vote, create a new upvote
        new_vote = AnswerVote.objects.create(answer=answer, user=user, vote_type=AnswerVote.UPVOTE)
        return JsonResponse({'status': 'upvoted','value': new_vote.answer.total_votes()})

def downvote_answer(request, id):
    answer = get_object_or_404(Answer, id=id)
    user = request.user

    # Check if the user has already voted on this answer
    existing_vote = AnswerVote.objects.filter(answer=answer, user=user).first()

    if existing_vote:
        if existing_vote.vote_type == AnswerVote.DOWNVOTE:
            # If the existing vote is a downvote, delete
            existing_vote.delete()
            return JsonResponse({'status': 'already_downvoted', 'value': existing_vote.answer.total_votes()})
        else:
            # If the existing vote is an upvote, change it to downvote
            existing_vote.vote_type = AnswerVote.DOWNVOTE
            existing_vote.save()
            return JsonResponse({'status': 'vote_changed', 'value': existing_vote.answer.total_votes()})
    else:
        # If no existing vote, create a new downvote
        new_vote = AnswerVote.objects.create(answer=answer, user=user, vote_type=AnswerVote.DOWNVOTE)
        return JsonResponse({'status': 'downvoted','value': new_vote.answer.total_votes()})


def question_comment(request, id):
    question = get_object_or_404(Question, id=id)
    answers = question.answers.all()
    if request.method == "POST":
        response = validate_user_login(request, 'You must be logged in to answer a question.')
        if response:
            return response
        comment_form = QuestionCommentForm(request.POST)

        if comment_form.is_valid():
            # Extract the cleaned data from the form
            body = comment_form.cleaned_data.get('body', '').strip()

            # Check if the body field is empty or contains only non-visible content
            if is_blank_html(body):
                # Add a form error if body is blank or contains only non-visible content
                messages.error(request, 'The comment cannot be blank')
                return redirect('forum:question_detail', id=question.id, question_id=question.question_id)
            comment = comment_form.save(commit=False)
            comment.question = question
            comment.commented_by = request.user
            comment.save()
            return redirect('forum:question_detail', id=question.id, question_id=question.question_id)

def answer_comment(request, id):
    answer = get_object_or_404(Answer, id=id)
    if request.method == "POST":
        response = validate_user_login(request, 'You must be logged in to answer a question.')
        if response:
            return response

        answer_comment_form = AnswerCommentForm(request.POST)
        if answer_comment_form.is_valid():
            # Extract the cleaned data from the form
            body = answer_comment_form.cleaned_data.get('body', '').strip()

            # Check if the body field is empty or contains only non-visible content
            if is_blank_html(body):
                # Add a form error if body is blank or contains only non-visible content
                messages.error(request, 'The comment cannot be blank')
                return redirect('forum:question_detail', id=answer.question.id, question_id=answer.question.question_id)
            answer_comment = answer_comment_form.save(commit=False)
            answer_comment.commented_by = request.user
            answer_comment.question = answer.question
            answer_comment.answer = answer
            answer_comment.save()
            return redirect('forum:question_detail', id=answer.question.id, question_id=answer.question.question_id)

def is_blank_html(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    text = soup.get_text(strip=True)
    return not text

def answer(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == "POST":
        response = validate_user_login(request, 'You must be logged in to answer a question.')
        if response:
            return response

    answer_form = AnswerForm(request.POST)
    if answer_form.is_valid():
        # Extract the cleaned data from the form
        body = answer_form.cleaned_data.get('body', '').strip()

        # Check if the body field is empty or contains only non-visible content
        if is_blank_html(body):
            # Add a form error if body is blank or contains only non-visible content
            messages.error(request, 'The answer cannot be blank')
            return redirect('forum:question_detail', id=question.id, question_id=question.question_id)

        answer = answer_form.save(commit=False)
        answer.question = question
        answer.asked_by = request.user
        answer.save()
        return redirect('forum:question_detail', id=question.id, question_id=question.question_id)


def display_search_tags(request):
    query = request.GET.get('q', '')

    if query:
        tags = Tag.objects.filter(name__icontains=query).annotate(
            question_count=Coalesce(Count('questions'), Value(0))
        ).values('id', 'name', 'question_count')
    else:
        tags = Tag.objects.all().annotate(
            question_count=Coalesce(Count('questions'), Value(0))
        ).values('id', 'name', 'question_count')

    return JsonResponse({'tags': list(tags)})


def forum_tags(request):
    tags = Tag.objects.all()

    return render(request,
                  'forum/tag_page.html',
                  {'tags': tags})


def search_users(request):
    query = request.GET.get('q', '')

    question_subquery = Question.objects.filter(asked_by=OuterRef('pk')).values('asked_by').annotate(count=Count('*')).values('count')
    answer_subquery = Answer.objects.filter(asked_by=OuterRef('pk')).values('asked_by').annotate(count=Count('*')).values('count')

    users = User.objects.annotate(
        question_count=Coalesce(Subquery(question_subquery), Value(0)),
        answer_count=Coalesce(Subquery(answer_subquery), Value(0))
    )

    if query:
        users = users.filter(username__icontains=query)

    users = users.values('id', 'username', 'question_count', 'answer_count')

    return JsonResponse({'users': list(users)})

def user_page(request):
    # Annotate users with their question count and order by question count
    users = User.objects.annotate(
        question_count=Count('questions_asked')
    ).order_by('-question_count')

    return render(request, 'forum/users_forum_page.html', {'users': users})


def user_details(request, id):
    # Fetch the user and their profile
    user = get_object_or_404(User, id=id)
    user_profile = get_object_or_404(UserProfile, user=user)

    # Calculate membership duration
    created_date = user_profile.created_at
    membership_duration = calculate_duration(created_date)

    # Annotate questions and answers with their total votes
    questions = Question.objects.filter(asked_by=user).annotate(
        total_votes=Count('votes', filter=Q(votes__vote_type='upvote')) - Count('votes',
                                                                                filter=Q(votes__vote_type='downvote'))
    ).order_by('-total_votes')

    # Step 1: Compute total votes for each answer
    answers_with_votes = Answer.objects.annotate(
        total_votes=Count('answer_votes', filter=Q(answer_votes__vote_type='upvote')) - Count('answer_votes', filter=Q(
            answer_votes__vote_type='downvote'))
    )

    # Step 2: Find the top-voted answer per question
    top_answer_subquery = answers_with_votes.filter(
        question=OuterRef('question')
    ).order_by('-total_votes').values('id')[:1]

    # Step 3: Filter answers to get only the top-voted answer for each question
    top_answers = answers_with_votes.filter(
        id__in=Subquery(top_answer_subquery)
    ).order_by('-total_votes')

    return render(request, 'forum/user_detail.html', {
        'user': user,
        'questions': questions,
        'questions_count': questions.count(),
        'answers_count': answers_with_votes.count(),
        'answers': top_answers,
        'membership_duration': membership_duration
    })


def calculate_duration(created_date):
    now_date = now()
    delta = now_date - created_date
    years = delta.days // 365
    months = (delta.days % 365) // 30
    days = (delta.days % 365) % 30
    return f"{years} years, {months} month{'s' if months != 1 else ''}, {days} day{'s' if days != 1 else ''}"
