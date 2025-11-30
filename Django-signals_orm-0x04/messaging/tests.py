from django.test import TestCase
from django.contrib.auth.models import User
from .models import Message, Notification, MessageHistory


class MessagingTests(TestCase):
    def setUp(self):
        self.u1 = User.objects.create(username="A")
        self.u2 = User.objects.create(username="B")

    def test_notification_created(self):
        msg = Message.objects.create(sender=self.u1, receiver=self.u2, content="Hi")
        self.assertEqual(Notification.objects.filter(user=self.u2).count(), 1)

    def test_edit_logging(self):
        msg = Message.objects.create(sender=self.u1, receiver=self.u2, content="Hello")
        msg.content = "Edited text"
        msg.save()
        self.assertTrue(MessageHistory.objects.filter(message=msg).exists())
