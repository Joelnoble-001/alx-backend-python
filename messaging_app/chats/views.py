from django.shortcuts import render
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer,
    MessageSerializer,
)

# Create your views here.




# Conversation ViewSet

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    # POST /api/conversations/
    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get("participants", [])

        if not participant_ids or len(participant_ids) < 2:
            return Response(
                {"error": "A conversation needs at least 2 participants."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        participants = User.objects.filter(id__in=participant_ids)
        conversation.participants.add(*participants)

        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED
        )



# Message ViewSet

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    # POST /api/messages/
    # Expected body:
    # { "conversation": "<id>", "sender": "<id>", "message_body": "Hello" }
    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get("conversation")
        sender_id = request.data.get("sender")
        message_body = request.data.get("message_body")

        if not conversation_id or not sender_id or not message_body:
            return Response(
                {"error": "conversation, sender, and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            conversation = Conversation.objects.get(id=conversation_id)
            sender = User.objects.get(id=sender_id)
        except (Conversation.DoesNotExist, User.DoesNotExist):
            return Response(
                {"error": "Invalid conversation or sender ID."},
                status=status.HTTP_404_NOT_FOUND
            )

        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )
