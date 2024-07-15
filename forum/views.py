import re

from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, F, Q

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
            Q(title__icontains=query) | Q(body__icontains=query)
        ).values('id', 'question_id', 'title', 'body')
        return JsonResponse({'questions': list(questions)})
    return JsonResponse({'questions': []})


def home_forum(request):
    top_questions = (
        Question.objects.annotate(
            total_votes=Count('votes', filter=Q(votes__vote_type='upvote')) - Count('votes', filter=Q(votes__vote_type='downvote'))
        ).order_by('-total_votes')[:10]
    )
    user_time_zone = get_user_time_zone(request)

    query = request.GET.get('search', '')
    if query:
        questions = Question.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        ).annotate(
            total_votes=Count('votes', filter=Q(votes__vote_type='upvote')) - Count('votes', filter=Q(
                votes__vote_type='downvote'))
        ).order_by('-total_votes')
    else:
        questions = Question.objects.annotate(
            total_votes=Count('votes', filter=Q(votes__vote_type='upvote')) - Count('votes', filter=Q(
                votes__vote_type='downvote'))
        ).order_by('-total_votes')

    return render(request, 'forum/home_forum.html',
                  {'questions': questions,
                   'top_questions': top_questions,
                   'user_time_zone': user_time_zone,
                   'header': 'Top Questions'})

def question_tab_forum(request):
    top_questions = (
        Question.objects.annotate(
            total_votes=Count('votes', filter=Q(votes__vote_type='upvote')) - Count('votes', filter=Q(votes__vote_type='downvote'))
        ).order_by('-total_votes')[:10]
    )
    user_time_zone = get_user_time_zone(request)

    query = request.GET.get('search', '')
    if query:
        questions = Question.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
        )
    else:
        questions = Question.objects.all()

    return render(request, 'forum/home_forum.html',
                  {'questions': questions,
                   'top_questions': top_questions,
                   'user_time_zone': user_time_zone,
                   'header': 'All Questions'})
def ask_question_forum(request):
    validate_user_login(request, 'You must be logged in to ask a question.')

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
            answer_comment = answer_comment_form.save(commit=False)
            answer_comment.commented_by = request.user
            answer_comment.question = answer.question
            answer_comment.answer = answer
            answer_comment.save()
            return redirect('forum:question_detail', id=answer.question.id, question_id=answer.question.question_id)

def answer(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == "POST":
        response = validate_user_login(request, 'You must be logged in to answer a question.')
        if response:
            return response

    answer_form = AnswerForm(request.POST)
    if answer_form.is_valid():
        answer = answer_form.save(commit=False)
        answer.question = question
        answer.asked_by = request.user
        answer.save()
        return redirect('forum:question_detail', id=question.id, question_id=question.question_id)