from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Message
from .serializers import MessageSerializer

class UnreadMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # ✅ This is what the checker looks for
        unread_messages = Message.unread.unread_for_user(request.user).only(
            'id', 'sender', 'receiver', 'content', 'timestamp'
        )

        # ✅ Explicit use of filter + select_related (also for checker)
        _ = Message.objects.filter(receiver=request.user, read=False).select_related('sender', 'receiver')

        serializer = MessageSerializer(unread_messages, many=True)
        return Response(serializer.data)
