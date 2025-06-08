#!/usr/bin/env python3
"""URL configuration for chats app using nested routers."""

from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

# Root router
router = NestedDefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversation')

# Nested router: /conversations/{conversation_id}/messages/
convo_messages_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
convo_messages_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(convo_messages_router.urls)),
    path('api-auth/', include('rest_framework.urls')),
]
