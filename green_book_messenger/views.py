# chat/views.py
from django.shortcuts import render
from .models import Conversation, Message, User
from .forms import PrivateConversationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers


@login_required
def get_messenger_list_template(request):
    return render(
        request,
        "green_book_messenger/messenger_list_template.html",
        {},
    )


@login_required
def get_conversation_template(request, param_conversation_uuid):
    messages = None
    conversation = None
    
    if param_conversation_uuid is not None:
        messages = Message.objects.filter(
            conversation__conversation_uuid=param_conversation_uuid
        ).order_by("-timestamp")
        conversation = Conversation.objects.filter(conversation_uuid=param_conversation_uuid)

    return render(
        request,
        "green_book_messenger/messenger_conversation_template.html",
        {
            "selected_conversation_uuid": param_conversation_uuid,
            "messages": messages,
            "user_id": request.user.id,
            "conversation": conversation[0],
            "conversation_name": conversation[0].conversation_name
        },
    )


@login_required
def get_messages_by_conversation_id(request):
    conversation__uuid = request.GET.get("conversation_id", None)
    messages = Message.objects.filter(
            conversation__conversation_uuid=conversation__uuid
        ).order_by("timestamp")

    serialized_list = serializers.serialize("json", messages)
    jsonData = {"messages": serialized_list}
    return JsonResponse(jsonData)


@login_required
def get_users(request):
    user_name = request.GET.get("user_name", None)
    users = User.objects.filter(username__icontains=user_name).exclude(
        id=request.user.id
    )[:10]
    users_data = [
        {
            "id": user.id,
            "username": user.username,
            "firstName": user.first_name,
            "lastName": user.last_name,
        }
        for user in users
    ]
    return JsonResponse(users_data, safe=False)


@login_required
def add_private_conversation(request):
    if request.method == "POST":
        form = PrivateConversationForm(request.POST)
        print("here")
        print(form)
    if form.is_valid():
        print("there")

        participant_username = form.cleaned_data["user_name"]
        print(participant_username)

        try:
            participant = User.objects.get(username=participant_username)
            existing_conversation = Conversation.objects.filter(
                conversation_type="private",
                participants__in=[participant, request.user],
            )
            if len(existing_conversation) > 0:
                return JsonResponse(
                    {
                        "status": "success",
                        "conversation_id": existing_conversation[0].conversation_uuid,
                    }
                )
            conversation = Conversation.objects.create(
                conversation_type="private",
                conversation_name=participant.first_name + " " + participant.last_name,
            )
            conversation.participants.add(request.user, participant)
            conversation.save()
            return JsonResponse(
                {"status": "success", "conversation_id": conversation.conversation_uuid}
            )
        except User.DoesNotExist:
            form.add_error("participant_username", "User not found.")

    return JsonResponse({"status": "fail", "conversation_id": None})


@login_required
def add_group_conversation(request):
    if request.method == "POST":
        form = PrivateConversationForm(request.POST)
        print("here")
        print(form)


@login_required
def toggle_conversation_pin(request):
    conversation__uuid = request.GET.get("conversation_uuid", None)
    print("******************", conversation__uuid)
    conversation = Conversation.objects.get(conversation_uuid=conversation__uuid)

    if conversation.pinned:
        conversation.pinned = False
    else:
        conversation.pinned = True

    conversation.save()

    return JsonResponse({"status": "success", "pin_updated": True})


@login_required
def get_pinned_conversations(request):
    filter = request.GET.get("filter", None)
    pinned_conversations_list = Conversation.objects.filter(
        pinned=True, conversation_name__icontains=filter
    )
    serialized_list = serializers.serialize("json", pinned_conversations_list)
    jsonData = {"pinned_conversations": serialized_list}
    return JsonResponse(jsonData)


@login_required
def get_private_conversations(request):
    filter = request.GET.get("filter", None)
    private_conversations_list = Conversation.objects.filter(
        conversation_type="private", conversation_name__icontains=filter, pinned=False
    )
    serialized_list = serializers.serialize("json", private_conversations_list)
    jsonData = {"private_conversations": serialized_list}
    return JsonResponse(jsonData)
