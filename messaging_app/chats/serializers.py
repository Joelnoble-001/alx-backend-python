from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import User, Conversation, Message

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username')  # Optional, shows username

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']

# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    messages = SerializerMethodField() 

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def get_messages(self, obj):
        return MessageSerializer(obj.messages.all(), many=True).data
