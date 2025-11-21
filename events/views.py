from rest_framework import viewsets
from django.utils import timezone
from .models import Event
from .serializers import EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer

    def get_queryset(self):
        now = timezone.now()

        queryset = Event.objects.filter(is_deleted=False)

        queryset = queryset.exclude(
            end_date__lt=now
        ).exclude(
            end_date__isnull=True,
            start_date__lt=now
        )

        if self.request.query_params.get('upcoming') == 'true':
            queryset = queryset.filter(start_date__gte=now)

        if category := self.request.query_params.get('category'):
            queryset = queryset.filter(category=category)

        return queryset

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
