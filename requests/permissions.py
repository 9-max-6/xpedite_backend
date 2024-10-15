
from rest_framework.permissions import BasePermission

class IsSupervisor(BasePermission):
    """
    Custom permission for the manager
    """
    def has_permission(self, request, view):
        if request.user.is_sup:
            return True
        
class IsManagement(BasePermission):
    """
    Custom permission for the manager
    """
    def has_permission(self, request, view):
        if request.user.is_jet or request.user.is_sup:
            return False
        return True
