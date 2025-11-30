from django.db import models
from django.contrib.auth.models import User
from .managers import UnreadMessagesManager 


class UnreadMessagesManager(models.Manager):
    def for_user(self, user):
        return self.filter(receiver=user, read=False).only("sender", "content", "timestamp")


class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    # fields added also
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey('self', null=True, blank=True, related_name="replies", on_delete=models.CASCADE)
    read = models.BooleanField(default=False)

    objects = models.Manager()
    unread = UnreadMessagesManager()

    def __str__(self):
        return f"{self.sender} → {self.receiver}"



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self):
        return f"Notify {self.user.username} for message {self.message.id}"


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="history")
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)

    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-edited_at']

    def __str__(self):
        return f"History for message {self.message.id}"

    def get_thread(message_id):
        from django.db.models import Prefetch
        return Message.objects.filter(id=message_id).prefetch_related(
            Prefetch("replies", queryset=Message.objects.select_related("sender", "receiver"))
        )
