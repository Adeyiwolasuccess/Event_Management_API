from rest_framework import serializers
from django.utils import timezone
from .models import EventCategory
from .models import Event, Registration
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
        fields = ['id', 'event', 'ticket_type', 'price', 'currency', 'available_quantity']
        read_only_fields = ['id', 'event']

class RegistrationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    event = serializers.PrimaryKeyRelatedField(queryset=Event.objects.all())

    class Meta:
        model = Registration
        fields = ["id", "user", "event", "status", "registration_date"]
        read_only_fields = ["id", "status", "registration_date"]

    def create(self, validated_data):
        """
        Ensure user is automatically set to the current authenticated user.
        """
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["user"] = request.user
        return super().create(validated_data)