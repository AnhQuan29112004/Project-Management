from rest_framework.permissions import BasePermission, SAFE_METHODS

class HasPermission(BasePermission):
    """
    Custom permission to check if the user has a specific permission.
    """
    def __init__(self, permission_name):
        self.permission_name = permission_name

    def has_permission(self, request, view):
        return request.user.has_perm(self.permission_name) or request.user.is_superuser
    def has_object_permission(self, request, view, obj):
        return request.user.has_perm(self.permission_name, obj) or request.user.is_superuser
    def has_method_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.has_perm(self.permission_name) or request.user.is_superuser