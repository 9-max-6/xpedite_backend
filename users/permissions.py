from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin (staff) users to add or delete users.
    Other authenticated users can view users.
    """

    def has_permission(self, request, view):
        # Allow all authenticated users to perform safe methods (GET, OPTIONS, HEAD)
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return request.user and request.user.is_authenticated
        # Only allow staff (admin) users to perform unsafe methods (POST, DELETE, PUT)
        return request.user and request.user.is_staff
