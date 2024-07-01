# chat/views.py
from django.shortcuts import render
from .models import Conversation, Message

def messenger_home(request, param_conversation_uuid=None):
    conversations_list = Conversation.objects.filter(participants=request.user)
    messages=None
    if param_conversation_uuid != None:
        messages = Message.objects.filter(conversation__conversation_uuid=param_conversation_uuid).order_by('timestamp')
        
    return render(request, "green_book_messenger/messenger_home.html", {'conversations_list': 
        conversations_list, 'selected_conversation_uuid': param_conversation_uuid, 'messages': messages, 'user_id': request.user.id})



def get_messages_by_conversation_id(request):
    conversation__uuid = request.GET.get('conversation__uuid', None)
    data = {
        'messages': Message.objects.filter(conversation__conversation_uuid=conversation__uuid).order_by('timestamp')
    }
    return JsonResponse(data)