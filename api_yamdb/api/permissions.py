from rest_framework import permissions, status

class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_admin()
