from .models import EventCategory
from .models import TicketPricing
from .serializers import EventCategorySerializer
from . serializers import TicketPricingSerializer
from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework import filters
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Read-only for everyone, write for admin only.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class IsCreatorOrAdmin(permissions.BasePermission):
    """
    Allow only event creator or admin to update/delete.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or obj.created_by == request.user


class EventCategoryViewSet(viewsets.ModelViewSet):
    queryset = EventCategory.objects.all()
    serializer_class = EventCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Event
from .serializers import EventSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCreatorOrAdmin]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'location']
    search_fields = ['title', 'location']
    ordering_fields = ['date', 'created_at']


    def get_queryset(self):
        # Base: only upcoming events
        queryset = Event.objects.filter(date__gte=timezone.now()).order_by('date')

        # Optional date range filters
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')

        if start_date and end_date:
            queryset = queryset.filter(date__range=[start_date, end_date])
        elif start_date:
            queryset = queryset.filter(date__gte=start_date)
        elif end_date:
            queryset = queryset.filter(date__lte=end_date)

        return queryset

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)



class TicketPricingViewSet(viewsets.ModelViewSet):
    serializer_class = TicketPricingSerializer
    queryset = TicketPricing.objects.all()

    def get_queryset(self):
        """
        - If listing tickets for an event → only that event’s tickets.
        - Otherwise → all tickets (admin only).
        """
        event_id = self.kwargs.get("event_pk")
        if event_id:
            return TicketPricing.objects.filter(event_id=event_id)
        return TicketPricing.objects.all()

    def perform_create(self, serializer):
        """Only event creator or admin can create ticket pricing"""
        event = Event.objects.get(id=self.kwargs["event_pk"])
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


