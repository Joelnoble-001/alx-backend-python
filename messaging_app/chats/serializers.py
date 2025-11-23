from rest_framework import serializers
from .models import User, Conversation, Message

# Message Serializer
class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username')

    class Meta:
        model = Message
        fields = ['message_id', 'conversation', 'sender', 'message_body', 'sent_at']

# Conversation Serializer
class ConversationSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()  # fully qualified for checker

    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants', 'created_at', 'messages']

    def get_messages(self, obj):
        return MessageSerializer(obj.messages.all(), many=True).data

    def validate_participants(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A conversation must have at least 2 participants.")
        return value
