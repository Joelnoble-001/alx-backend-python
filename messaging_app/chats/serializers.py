from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from .models import Conversation, Message


# User Serializer

class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(source='sender.username')

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']


class ConversationSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    messages = SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'title', 'messages']

    def get_messages(self, obj):
        return MessageSerializer(obj.messages.all(), many=True).data

    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title is too short")
        return value
