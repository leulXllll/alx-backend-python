from rest_framework import serializers
from .models import CustomUser, Conversation, Message

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['user_id', 'email', 'username', 'first_name', 'last_name', 'phone_number', 'bio', 'password', 'full_name']
        read_only_fields = ['user_id']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()

    def validate(self, data):
        if 'email' in data and not data['email']:
            raise serializers.ValidationError("Email cannot be empty.")
        return data

class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer(read_only=True)
    body = serializers.CharField()
    sender_email = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'body', 'sent_at', 'sender_email']
        read_only_fields = ['id', 'sent_at', 'sender']

    def get_sender_email(self, obj):
        return obj.sender.email

    def validate_body(self, value):
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value

class ConversationSerializer(serializers.ModelSerializer):
    participants = CustomUserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    title = serializers.CharField(required=False, allow_blank=True)
    participant_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at', 'updated_at', 'title', 'participant_count']
        read_only_fields = ['id', 'created_at', 'updated_at', 'participants', 'messages']

    def get_participant_count(self, obj):
        return obj.participants.count()

    def validate_title(self, value):
        if value and len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long if provided.")
        return value