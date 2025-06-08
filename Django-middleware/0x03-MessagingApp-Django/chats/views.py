# #!/usr/bin/env python3
# """Views for the chats app."""

# from rest_framework import viewsets, filters
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.pagination import PageNumberPagination
# from .models import Message
# from .serializers import MessageSerializer
# from .permissions import IsParticipantOfConversation
# from .filters import MessageFilter


# class MessagePagination(PageNumberPagination):
#     page_size = 20
#     page_size_query_param = 'page_size'
#     max_page_size = 100


# class MessageViewSet(viewsets.ModelViewSet):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#     permission_classes = [IsParticipantOfConversation]
#     pagination_class = MessagePagination
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
#     filterset_class = MessageFilter
#     ordering_fields = ['sent_at']
#     ordering = ['-sent_at']  # Default ordering (newest first)

#     def get_queryset(self):
#         return Message.objects.filter(
#             conversation__participants=self.request.user
#         ).select_related('sender', 'conversation')
#!/usr/bin/env python3
"""Views for the chats app."""

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .pagination import MessagePagination
from .filters import MessageFilter


class ConversationViewSet(viewsets.ModelViewSet):
    """ViewSet for managing conversations."""
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['participants']

    def get_queryset(self):
        """Limit to conversations the authenticated user participates in."""
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """Create a new conversation with participants."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        participant_ids = request.data.get('participants', [])
        if not participant_ids:
            return Response(
                {"error": "At least one participant is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        participants = User.objects.filter(id__in=participant_ids)
        if request.user.id not in participant_ids:
            participants |= User.objects.filter(id=request.user.id)

        conversation = serializer.save()
        conversation.participants.set(participants)

        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class MessageViewSet(viewsets.ModelViewSet):
    """ViewSet for managing messages."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    pagination_class = MessagePagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def get_queryset(self):
        """Return messages only from conversations the user is part of."""
        conversation_id = self.kwargs.get('conversation_id')
        if conversation_id:
            return Message.objects.filter(
                conversation_id=conversation_id,
                conversation__participants=self.request.user
            ).select_related('sender', 'conversation')
        return Message.objects.filter(
            conversation__participants=self.request.user
        ).select_related('sender', 'conversation')

    def create(self, request, *args, **kwargs):
        """Create a new message in a conversation."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        conversation_id = request.data.get('conversation')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation does not exist."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not conversation.participants.filter(id=request.user.id).exists():
            return Response(
                {"error": "User is not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        message = serializer.save(sender=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )