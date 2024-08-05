from django.shortcuts import render, redirect
from django.db.models import Count
from .models import Conversation, Message, User
from .forms import PrivateConversationForm, GroupConversationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers
from django.contrib import messages
from django.urls import reverse



def get_messenger_list_template(request):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be login to access messenger")
        return redirect("login")
    return render(
        request,
        "green_book_messenger/messenger_list_template.html",
        {},
    )



def get_conversation_template(request, param_conversation_uuid):
    if not request.user.is_authenticated:
        messages.error(request, "You need to be login to access messenger")
        return redirect("login")
    messages = None
    conversation = None

    if param_conversation_uuid is not None:
        messages = Message.objects.filter(
            conversation__conversation_uuid=param_conversation_uuid
        ).order_by("-timestamp")
        conversation = Conversation.objects.filter(
            conversation_uuid=param_conversation_uuid
        )
    peerParticipant = None
    conversation_name = conversation[0].conversation_name
    if conversation[0].conversation_type == "private":
        participants = conversation[0].get_participants_as_array()
        peerParticipant = [participant for participant in participants if participant.id != request.user.id]
        conversation_name = peerParticipant[0].first_name + " " + peerParticipant[0].last_name
    
    return render(
        request,
        "green_book_messenger/messenger_conversation_template.html",
        {
            "selected_conversation_uuid": param_conversation_uuid,
            "messages": messages,
            "user_id": request.user.id,
            "conversation": conversation[0],
            "conversation_name": conversation_name,
        },
    )


@login_required
def get_messages_by_conversation_id(request):
    conversation__uuid = request.GET.get("conversation_id", None)
    messages = Message.objects.filter(
        conversation__conversation_uuid=conversation__uuid
    ).order_by("timestamp")
    serialized_list = serializers.serialize("json", messages)
    print(serialized_list)
    jsonData = {"messages": serialized_list}
    return JsonResponse(jsonData)


@login_required
def delete_conversation(request, conversation_id):

    instance = Conversation.objects.filter(conversation_uuid=conversation_id)
    instance.delete()

    return redirect(reverse("messenger_list"))

@login_required
def get_users(request):
    user_name = request.GET.get("user_name", None)
    if user_name == "" or user_name is None:
        return JsonResponse({"status": "failed"}, safe=False)
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
            existing_conversation = (
                Conversation.objects.annotate(num_participants=Count("participants"))
                .filter(
                    conversation_type="private",
                    num_participants=2,
                    participants=participant,
                )
                .filter(participants=request.user)
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
    print("call came")
    if request.method == "POST":
        form = GroupConversationForm(request.POST)
        print("here")
        print(form)
    if form.is_valid():
        print("there")

        group_name = form.cleaned_data["group_name"]
        participant_ids = form.cleaned_data["participant_ids"]
        participant_ids = participant_ids.split(",")

        try:
            participant_list = User.objects.filter(username__in=participant_ids)
            conversation = Conversation.objects.create(
                conversation_type="private_group",
                conversation_name=group_name,
            )
            conversation.participants.add(*participant_list)
            conversation.participants.add(request.user)
            conversation.save()

            return JsonResponse(
                {"status": "success", "conversation_id": conversation.conversation_uuid}
            )
        except User.DoesNotExist:
            form.add_error("participant_username", "User not found.")

    return JsonResponse({"status": "fail", "conversation_id": None})

@login_required
def toggle_conversation_pin(request):
    conversation_uuid = request.GET.get("conversation_uuid", None)
    user = request.user

    if not conversation_uuid:
        return JsonResponse(
            {"status": "error", "message": "Conversation UUID not provided"}, status=400
        )

    # Retrieve the conversation or return 404 if not found
    conversation = Conversation.objects.get(conversation_uuid=conversation_uuid)

    if conversation.pinned.filter(id=user.id).exists():
        # If the user has already pinned the conversation, remove them from the list
        conversation.pinned.remove(user)
        pin_status = False
    else:
        # If the user has not pinned the conversation, add them to the list
        conversation.pinned.add(user)
        pin_status = True

    return JsonResponse({"status": "success", "pin_updated": pin_status})

@login_required
def get_pinned_conversations(request):
    filter = request.GET.get("filter", "")
    user = request.user

    pinned_conversations_list = Conversation.objects.filter(
        pinned=user,
        conversation_name__icontains=filter,
        participants=user,
    )

    for conversation in pinned_conversations_list:
        peerParticipant = None
        conversation_name = conversation.conversation_name
        if conversation.conversation_type == "private":
            participants = conversation.get_participants_as_array()

            # Find the peer participant (other than the current user)
            peerParticipant = [
                participant for participant in participants if participant.id != user.id
            ]

            if peerParticipant:
                conversation_name = (
                    f"{peerParticipant[0].first_name} {peerParticipant[0].last_name}"
                )
                conversation.conversation_name = conversation_name

    serialized_list = serializers.serialize("json", pinned_conversations_list)

    jsonData = {"pinned_conversations": serialized_list}
    return JsonResponse(jsonData)

@login_required
def get_private_conversations(request):
    filter = request.GET.get("filter", None)
    private_conversations_list = Conversation.objects.filter(
        conversation_type="private",
        conversation_name__icontains=filter,
        participants=request.user,
    )
    for conversation in private_conversations_list:
        peerParticipant = None
        conversation_name = conversation.conversation_name
        participants = conversation.get_participants_as_array()
        peerParticipant = [
            participant
            for participant in participants
            if participant.id != request.user.id
        ]
        conversation_name = (
            peerParticipant[0].first_name + " " + peerParticipant[0].last_name
        )
        conversation.conversation_name = conversation_name
            
    serialized_list = serializers.serialize("json", private_conversations_list)
    jsonData = {"private_conversations": serialized_list}
    return JsonResponse(jsonData)


@login_required
def get_group_conversations(request):
    filter = request.GET.get("filter", None)
    group_conversation_list = Conversation.objects.filter(
        conversation_type="private_group",
        conversation_name__icontains=filter,
        participants=request.user,
    )
    serialized_list = serializers.serialize("json", group_conversation_list)
    jsonData = {"group_conversations": serialized_list}
    return JsonResponse(jsonData)
