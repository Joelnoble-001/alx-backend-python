from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from .models import Message
from django.views.decorators.cache import cache_page



# --- Recursive threaded reply fetcher ---
def fetch_replies(message):
    """Recursively fetch nested threaded replies"""
    replies = message.replies.all().select_related("sender", "receiver")
    return [
        {"message": reply, "replies": fetch_replies(reply)}
        for reply in replies
    ]


# ───── Inbox (optimized + required .only + select_related) ─────
@login_required
def inbox(request):
    inbox_messages = (
        Message.objects.filter(receiver=request.user)
        .only("content", "timestamp", "sender", "receiver")  
        .select_related("sender", "receiver")                
        .prefetch_related("replies")                   
    )
    return render(request, "inbox.html", {"messages": inbox_messages})


# ───── Unread Messages — MUST use custom manager ✔ ─────
@login_required
def unread_messages(request):
    unread = Message.unread.unread_for_user(request.user)   
    return render(request, "unread.html", {"messages": unread})


# ───── Sent Messages (with optimization) ─────
@login_required
def sent_messages(request):
    sent = (
        Message.objects.filter(sender=request.user)
        .only("content", "timestamp", "receiver")           
        .select_related("sender", "receiver")
        .prefetch_related("replies")
    )
    return render(request, "sent.html", {"messages": sent})


# ───── Threaded conversation view (recursive tree) ─────
@login_required
def thread_view(request, message_id):
    parent = get_object_or_404(
        Message.objects.select_related("sender", "receiver"),
        id=message_id
    )
    parent.replies_list = fetch_replies(parent)              
    return render(request, "thread.html", {"message": parent})
