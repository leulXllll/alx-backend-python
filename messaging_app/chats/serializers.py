from rest_framework import serializers
from .models import CustomUser, Conversation, Message

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_id', 'email', 'username', 'first_name', 'last_name', 'phone_number', 'bio']
        read_only_fields = ['user_id']

class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'body', 'sent_at']
        read_only_fields = ['id', 'sent_at']

class ConversationSerializer(serializers.ModelSerializer):
    participants = CustomUserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']