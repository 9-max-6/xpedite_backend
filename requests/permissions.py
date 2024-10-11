
from rest_framework.permissions import BasePermission

class IsSupervisor(BasePermission):
    """
    Custom permission for the manager
    """
    def has_permission(self, request, view):
        if request.user.designation == 'SUP':
            return True
        
class IsManagement(BasePermission):
    """
    Custom permission for the manager
    """
    def has_permission(self, request, view):
        if request.user.designation == 'STAFF' or request.user.designation == 'MAN':
            return True