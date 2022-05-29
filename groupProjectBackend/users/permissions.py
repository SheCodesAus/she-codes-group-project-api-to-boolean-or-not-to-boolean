from rest_framework import permissions
from .models import SheCodesUser

# User Types used to convert SheCodesUsers to the right access levels:
class IsSuperUser(permissions.IsAdminUser):
    # Checks that the user performing the task is the SuperUser only
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class IsSuperUserOrAdmin(permissions.BasePermission):
    # Checks that the user performing the task is either the SuperUser or Admin
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_superuser or request.user.is_shecodes_admin))

# Object Level Permission for Editing Profile info
class IsProfileOwnerOrAdminOrSuperUserOrReadOnly(permissions.BasePermission):
    # Only the owner of the Profile or the Admin/SuperUser can edit/delete User profile details
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user or bool(request.user.is_superuser or request.user.is_shecodes_admin)