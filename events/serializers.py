from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):

    # DRF will validate category because it's a ChoiceField already in the model
    category_display = serializers.CharField(source='get_category_display', read_only=True)

    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ['is_deleted', 'created_at', 'updated_at']
