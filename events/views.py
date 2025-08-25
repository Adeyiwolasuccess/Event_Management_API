from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import EventCategory, Event, TicketPricing, Registration
from .serializers import (
    EventCategorySerializer,
    EventSerializer,
    TicketPricingSerializer,
    RegistrationSerializer,
)

# ------------------------
# Permissions
# ------------------------

class IsAdminOrReadOnly(permissions.BasePermission):
    """Read-only for everyone, write for admin only."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsCreatorOrAdmin(permissions.BasePermission):
    """Allow only event creator or admin to update/delete."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or obj.created_by == request.user


# ------------------------
# ViewSets
# ------------------------

class EventCategoryViewSet(viewsets.ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCreatorOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'location']
    search_fields = ['title', 'location']
    ordering_fields = ['date', 'created_at']

    def get_queryset(self):
        # Default queryset (all events, ordered)
        return Event.objects.all().order_by("date")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=["get"], url_path="upcoming")
    def upcoming_events(self, request):
        """List all upcoming events with optional filters."""
        queryset = Event.objects.filter(date__gte=timezone.now()).order_by("date")

        # Optional query params
        title = request.query_params.get("title")
        location = request.query_params.get("location")
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")

        if title:
            queryset = queryset.filter(title__icontains=title)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(date__lte=end_date)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TicketPricingViewSet(viewsets.ModelViewSet):
    serializer_class = TicketPricingSerializer

    def get_queryset(self):
        return TicketPricing.objects.filter(event_id=self.kwargs["event_pk"])

    def perform_create(self, serializer):
        event = Event.objects.get(pk=self.kwargs["event_pk"])
        user = self.request.user
        if user != event.created_by and not user.is_staff:
            raise PermissionDenied("You are not allowed to add tickets for this event.")
        serializer.save(event=event)

    def perform_update(self, serializer):
        ticket = self.get_object()
        user = self.request.user
        if user != ticket.event.created_by and not user.is_staff:
            raise PermissionDenied("You are not allowed to update tickets for this event.")
        serializer.save()

    def perform_destroy(self, instance):
        user = self.request.user
        if user != instance.event.created_by and not user.is_staff:
            raise PermissionDenied("You are not allowed to delete tickets for this event.")
        instance.delete()




class RegistrationViewSet(viewsets.ModelViewSet):
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        event_id = self.kwargs["event_pk"]
        event = Event.objects.get(pk=event_id)

        if self.request.user == event.created_by or self.request.user.is_staff:
            return Registration.objects.filter(event_id=event_id)

        return Registration.objects.filter(event_id=event_id, user=self.request.user)

    def perform_create(self, serializer):
        event = Event.objects.get(pk=self.kwargs["event_pk"])

        # 🔒 Prevent duplicate registration
        if Registration.objects.filter(event=event, user=self.request.user).exists():
            raise ValidationError("You are already registered for this event.")

        serializer.save(user=self.request.user, event=event)
