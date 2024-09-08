from rest_framework.permissions import BasePermission
class IsAdminOrReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'DELETE','PATCH','PUT']:
            return request.user.is_superuser
        return True