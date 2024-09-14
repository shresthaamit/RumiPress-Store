from rest_framework.permissions import BasePermission
from rest_framework import permissions
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
    
    
class ReviewUserOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.rate_user == request.user or request.user.is_staff
             
        
    