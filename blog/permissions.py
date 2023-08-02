from rest_framework.permissions import BasePermission, SAFE_METHODS


class PostPermission(BasePermission):
    """
    Custom permission class for blog post views.

    This permission class defines the permissions required to access blog post views.
    It allows all SAFE_METHODS (GET, HEAD, OPTIONS) for any user, even unauthenticated users.
    For other methods (POST, PUT, PATCH, DELETE), it requires the user to be authenticated.

    In addition, it checks object-level permissions for specific methods (PUT, PATCH, DELETE).
    For these methods, it only allows users to modify or delete their own posts (if they are the post's author).

    Usage:
    - Assign this permission class to views that handle blog posts to enforce access control.

    """

    def has_permission(self, request, view):
        """
        Check if the user has permission to access the view.

        For SAFE_METHODS (GET, HEAD, OPTIONS), allow all users (including unauthenticated).
        For other methods, require the user to be authenticated.

        """
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """
        Check if the user has permission to access the object (post).

        For SAFE_METHODS (GET, HEAD, OPTIONS), allow all users (including unauthenticated).
        For PUT, PATCH, DELETE methods, only allow the user if they are the post's author.

        """
        if request.method in SAFE_METHODS:
            return True

        # Check if the user is the author of the post
        return obj.author == request.user
