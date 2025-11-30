from django.views.decorators.cache import cache_page
from django.shortcuts import render
from messaging.models import Message

@cache_page(60)
def conversation_messages(request, user):
    msgs = Message.objects.filter(receiver=user).select_related("sender")
    return render(request, "conversation.html", {"messages": msgs})
