from rest_framework import permissions, status


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_admin()


class IsAuthorizedUser(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.method != 'delete':
            return obj.author == request.user
