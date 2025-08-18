from rest_framework.routers import DefaultRouter
from .views import EventCategoryViewSet, EventViewSet

router = DefaultRouter()
router.register(r'categories', EventCategoryViewSet, basename='category')
router.register(r'events', EventViewSet, basename='event')

urlpatterns = router.urls
