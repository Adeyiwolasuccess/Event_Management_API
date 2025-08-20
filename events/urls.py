from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import (
    EventCategoryViewSet,
    EventViewSet,
    TicketPricingViewSet,
    RegistrationViewSet,
)

# Main router
router = DefaultRouter()
router.register(r'categories', EventCategoryViewSet, basename='category')
router.register(r'events', EventViewSet, basename='event')

# Nested routers
events_router = NestedDefaultRouter(router, r'events', lookup='event')
events_router.register(r'tickets', TicketPricingViewSet, basename='event-tickets')
events_router.register(r'registrations', RegistrationViewSet, basename='event-registrations')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(events_router.urls)),
]
