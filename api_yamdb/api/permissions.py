from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == "admin" or request.user.is_superuser
        return False

    def has_object_permission(self, request, view, obj):
        return request.user.role == "admin" or request.user.is_superuser


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_admin


class IsAuthorOrModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        if request.method == "POST":
            return request.user.is_authenticated
        return (
            obj.author == request.user
            or request.user.role == "moderator"
            or request.user.role == "admin"
        )
