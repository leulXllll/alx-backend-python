#!/usr/bin/env python3
"""Custom permissions for the messaging app."""

from rest_framework import permissions
from .models import Conversation, Message
from typing import Any


class IsParticipantOfConversation(permissions.BasePermission):
    """Permission to allow access only to conversation participants with method checks."""

    def has_permission(self, request: Any, view: Any) -> bool:
        """Allow only authenticated users."""
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request: Any, view: Any, obj: Any) -> bool:
        """Check permissions for different HTTP methods and object types."""
        # Allow GET/HEAD/OPTIONS for safe methods if participant
        if request.method in permissions.SAFE_METHODS:
            return self._is_participant(request.user, obj)
        
        # Explicitly handle PUT, PATCH, DELETE
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if isinstance(obj, Message):
                # Only allow message modification by sender
                return obj.sender == request.user and self._is_participant(request.user, obj.conversation)
            return self._is_participant(request.user, obj)
        
        return False

    def _is_participant(self, user, obj) -> bool:
        """Helper method to check if user is a participant."""
        if isinstance(obj, Conversation):
            return user in obj.participants.all()
        elif isinstance(obj, Message):
            return user in obj.conversation.participants.all()
        return False