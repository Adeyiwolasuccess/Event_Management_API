from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import EventCategoryViewSet, EventViewSet, TicketPricingViewSet

router = DefaultRouter()
router.register(r'categories', EventCategoryViewSet, basename='category')
router.register(r'events', EventViewSet, basename='event')

# Nested router for tickets under events
events_router = routers.NestedDefaultRouter(router, r'events', lookup='event')
events_router.register(r'tickets', TicketPricingViewSet, basename='event-tickets')

urlpatterns  = [
    path('', include(router.urls)),
    path('', include(events_router.urls)),
]
