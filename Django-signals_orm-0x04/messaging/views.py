from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer
from django.db.models import Prefetch

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter messages where sender is the current user (using literal sender=self.request.user)
        return Message.objects.filter(sender=self.request.user).select_related(
            'sender', 'receiver', 'parent_message'
        ).prefetch_related(
            Prefetch('replies', queryset=Message.objects.all().select_related('sender', 'receiver'))
        ).order_by('timestamp')
