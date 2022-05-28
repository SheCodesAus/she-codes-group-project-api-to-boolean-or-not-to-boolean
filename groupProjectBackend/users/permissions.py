from rest_framework import permissions
from .models import SheCodesUser

class IsSuperUser(permissions.IsAdminUser):
    # Checks that the user performing the task is the SuperUser 
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class IsSuperUserOrAdmin(permissions.BasePermission):
    # Checks that the user performing the task is either the SuperUser or Admin
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_superuser or request.user.is_shecodes_admin))

class IsUserAnApprover(permissions.IsAdminUser):
    # Checks the logged in user is an Approver
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_approver)