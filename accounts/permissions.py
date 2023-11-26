from rest_framework import permissions
from .models import UserRole



class AdminPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user_role = UserRole.objects.get(user=request.user).role
            return user_role.name == 'user' or request.user.is_superuser
        except UserRole.DoesNotExist:
            return False


