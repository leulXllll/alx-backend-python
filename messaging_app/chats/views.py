from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import CustomUser, Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Extract participant user_ids and title
        participant_ids = request.data.get('participants', [])
        if not participant_ids:
            return Response({"error": "At least one participant is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate participants exist
        participants = CustomUser.objects.filter(user_id__in=participant_ids)
        if len(participants) != len(participant_ids):
            return Response({"error": "One or more participant IDs are invalid."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create conversation
        conversation = serializer.save()
        # Add authenticated user and other participants
        participants = participants | CustomUser.objects.filter(user_id=request.user.user_id)
        conversation.participants.set(participants)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Ensure the sender is the authenticated user
        conversation_id = request.data.get('conversation')
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response({"error": "Conversation does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verify user is a participant in the conversation
        if not conversation.participants.filter(user_id=request.user.user_id).exists():
            return Response({"error": "User is not a participant in this conversation."}, status=status.HTTP_403_FORBIDDEN)
        
        # Save message with sender set to authenticated user
        message = serializer.save(sender=request.user)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)