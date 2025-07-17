from django.db import models

class UnreadMessagesManager(models.Manager):
    def unread_for_user(self, user):
        return self.get_queryset().filter(
            receiver=user,
            read=False
        ).select_related('sender', 'receiver').only('id', 'sender', 'receiver', 'content', 'timestamp')
