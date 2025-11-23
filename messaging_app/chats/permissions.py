from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "user"):
            return obj.user == request.user
        if hasattr(obj, "users"):
            return request.user in obj.users.all()
        return False
