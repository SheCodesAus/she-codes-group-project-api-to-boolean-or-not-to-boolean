from rest_framework import permissions
from .models import SheCodesUser

class IsSuperUser(permissions.IsAdminUser):
    """
    For use with admin-level access views.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class IsSuperUserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        logged_in_user = SheCodesUser.objects.get(pk=request.user)
        return bool(request.user and (request.user.is_superuser or logged_in_user.is_shecodes_admin))

class IsUserAnApprover(permissions.BasePermission):
    def has_permission(self, request, view):
        logged_in_user = SheCodesUser.objects.get(pk=request.user)
        return bool(request.user and logged_in_user.is_approver)