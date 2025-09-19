# permissions.py
from rest_framework import permissions

class IsCreditOfficerOrReadOnly(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return hasattr(request.user, 'credit_officer_profile')
    
    def has_object_permission(self, request, view, obj):
        # Allow read-only access for all authenticated users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only the assigned credit officer can modify their clients
        return obj.credit_officer == request.user