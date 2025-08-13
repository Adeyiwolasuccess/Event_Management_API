from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterUserView, CurrentUserView, LogoutUserView, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Auth
    path('auth/register/', RegisterUserView.as_view(), name='user-register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='user-login'),
    path('auth/logout/', LogoutUserView.as_view(), name='user-logout'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    # Profile
    path('users/me/', CurrentUserView.as_view(), name='user-profile'),

    # Router endpoints
    path('', include(router.urls)),
]
