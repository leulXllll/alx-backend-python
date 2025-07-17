from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
from django.db.models import Prefetch

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Fetch messages where user is sender or receiver
        qs = Message.objects.filter(sender=user).select_related('sender', 'receiver', 'parent_message').prefetch_related(
            Prefetch('replies', queryset=Message.objects.all().select_related('sender', 'receiver'))
        ).order_by('timestamp')
        return qs

    def list(self, request, *args, **kwargs):
        """
        Return messages with their threaded replies recursively.
        """
        messages = self.get_queryset()
        serializer = self.get_serializer(messages, many=True)
        return Response(serializer.data)

    def get_thread(self, message):
        """
        Recursively fetch all replies for a message.
        """
        thread = []
        for reply in message.replies.all():
            thread.append(reply)
            thread.extend(self.get_thread(reply))
        return thread
