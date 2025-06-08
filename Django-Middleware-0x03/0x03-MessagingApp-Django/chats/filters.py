import django_filters
from .models import Message
from django.utils import timezone
from datetime import timedelta

class MessageFilter(django_filters.FilterSet):
    sender = django_filters.CharFilter(field_name='sender__email', lookup_expr='iexact')
    conversation = django_filters.UUIDFilter(field_name='conversation__conversation_id')
    after = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    before = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    last_24h = django_filters.BooleanFilter(method='filter_last_24h')

    class Meta:
        model = Message
        fields = ['sender', 'conversation', 'sent_at']

    def filter_last_24h(self, queryset, name, value):
        if value:
            return queryset.filter(
                sent_at__gte=timezone.now() - timedelta(hours=24)
            )
        return queryset