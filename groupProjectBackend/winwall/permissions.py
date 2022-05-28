from rest_framework import permissions
from users.models import SheCodesUser
from rest_framework.permissions import SAFE_METHODS

# Authentication from User Model
class IsSuperUser(permissions.IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class IsSuperUserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_superuser or request.user.is_shecodes_admin))

# Checks if the Logged in User is an Approver
class IsUserAnApprover(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

# Detailed Authentication - Based on User ID that is associated with task
class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class WinWallOwnerWritePermission(permissions.BasePermission):
    # Added feature enabling owner of the created WinWall to create, put and delete
    message = "Editing Win Wall data is restricted to the administrators & approvers of this site only."

    def has_object_permission(self, request, view, obj):
        # GET_METHOD is a tuple that contains get, options and head
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user