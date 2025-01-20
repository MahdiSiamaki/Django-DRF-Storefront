from rest_framework import permissions
from rest_framework.permissions import BasePermission

class IsAdminUserOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff

class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self):
        self.perms_map = {
            'GET': ['%(app_label)s.view_%(model_name)s']
        }

class ViewCustomerHistoryPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == 'history':
            return request.user.is_staff
        return True