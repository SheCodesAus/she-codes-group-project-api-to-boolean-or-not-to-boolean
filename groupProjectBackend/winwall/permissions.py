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

class IsUserAnApprover(permissions.BasePermission):
    def has_permission(self, request, view):
        # logged_in_user = SheCodesUser.objects.get(pk=request.user)
        return bool(request.user and request.user.is_approver)


# Detailed Authentication - Based on User ID that is associated with task
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
    # must be an owner of the winwall to "do something"
    message = "Editing Win Wall data is restricted to the administrators & approvers of this site only."

    def has_object_permission(self, request, view, obj):
        # GET_METHOD is a tuple that contains get, options and head
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user