from rest_framework import serializers
from django.utils import timezone
from .models import EventCategory
from .models import Event
from .models import TicketPricing

class EventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        models = EventCategory
        fields = [
            'id', 'name', 'description']

class EventSerializer(serializers.ModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'date', 'location',
            'category', 'capacity', 'created_by', 'created_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at']

    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Event date must be in the future.")
        return value

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class TicketPricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = TicketPricing
        fields = ['id', 'event', 'ticket_type', 'price', 'currency']
        read_only_fields = ['id', 'event']