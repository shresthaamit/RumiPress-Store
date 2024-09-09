from rest_framework.permissions import BasePermission
class IsAdminOrReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'DELETE','PATCH','PUT']:
            return request.user.is_superuser
        return True
    
    
class IsStaffOrReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'DELETE','PATCH','PUT']:
            return request.user.is_staff
        return True
    
class IsStaffOrIsAdminPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and(request.user.is_staff or request.user.is_superuser)