from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from messaging.models import Message, Notification, MessageHistory

@receiver(post_delete, sender=User)
def cleanup_user_related_data(sender, instance, **kwargs):
    # Delete messages sent or received by user
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications for the user
    Notification.objects.filter(user=instance).delete()

    # Delete message histories related to user's messages
    MessageHistory.objects.filter(message__sender=instance).delete()
