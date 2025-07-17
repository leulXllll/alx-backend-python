from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer

class UnreadMessageViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        #  Uses custom manager and .only()
        unread_messages = Message.unread.for_user(request.user)
        serializer = MessageSerializer(unread_messages, many=True)
        return Response(serializer.data)
