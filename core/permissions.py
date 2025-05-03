from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or request.user.is_staff

class IsAdminOrAccountant(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name__in=['admin','accountant']).exists()

class IsAuditorReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name='auditor').exists()
        return False 