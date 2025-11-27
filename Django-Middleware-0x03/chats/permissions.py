from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if hasattr(obj, "user"):
            return obj.user == request.user
        if hasattr(obj, "users"):
            return request.user in obj.users.all()
        return False
    

from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    def has_permission(self, request, view):
        # Must be logged in
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow only participants to VIEW or MODIFY (PUT, PATCH, DELETE)

        # Check if updating or deleting
        if request.method in ["PUT", "PATCH", "DELETE"]:
            # Message object
            if hasattr(obj, "conversation"):
                return request.user in obj.conversation.users.all()

            # Conversation object
            if hasattr(obj, "users"):
                return request.user in obj.users.all()

        # Safe methods (GET)
        if hasattr(obj, "conversation"):
            return request.user in obj.conversation.users.all()

        if hasattr(obj, "users"):
            return request.user in obj.users.all()

        return False
