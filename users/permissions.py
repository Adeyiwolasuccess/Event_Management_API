from rest_framework import permissions

class IsSelfOrAdmin(permissions.BasePermission):
    """
    Allow users to edit their own profile, admins can edit anyone.
    """
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user
