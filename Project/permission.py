from rest_framework.permissions import BasePermission, SAFE_METHODS

class HasPermission(BasePermission):
    def __init__(self, permission_name):
        self.permission_name = permission_name

    def has_permission(self, request, view):
        return request.user.has_perm(self.permission_name)