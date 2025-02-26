from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrModeratorOrReadOnly(BasePermission):
    """
    Grant full access to admins and moderators. Other users can only read.
    """
    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) for all authenticated users
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated

        # Allow full access to admins and moderators
        user_role = getattr(request.user, 'role', None)
        return request.user.is_authenticated and user_role in ['admin', 'moderator']