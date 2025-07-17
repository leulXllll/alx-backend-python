from django.urls import path
from .views import UnreadMessagesView

urlpatterns = [
    path('unread/', UnreadMessagesView.as_view(), name='unread-messages'),
]
