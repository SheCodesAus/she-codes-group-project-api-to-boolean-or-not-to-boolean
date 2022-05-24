from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsAdminUserOrReadOnly(permissions.IsAdminUser):
    def has_permission(self, request, view):
        is_admin = super(
            IsAdminUserOrReadOnly, 
            self).has_permission(request, view)
        # Python3: is_admin = super().has_permission(request, view)
        return request.method in SAFE_METHODS or is_admin

class WinWallOwnerWritePermission(permissions.BasePermission):
    message = "Editing Win Wall data is restricted to the administrators & approvers of this site only."

    def has_object_permission(self, request, view, obj):
        # GET_METHOD is a tuple that contains get, options and head
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user