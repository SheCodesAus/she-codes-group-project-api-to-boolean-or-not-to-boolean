from rest_framework import permissions
from users.models import SheCodesUser
from .models import WinWall
from rest_framework.permissions import SAFE_METHODS

# Authentication from User Model
class IsSuperUser(permissions.IsAdminUser):
    # Ensures the User performing the action is a SuperUser only
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class IsSuperUserOrAdmin(permissions.BasePermission):
    # Ensure the User performing the action is either the SuperUser or an Admin
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_superuser or request.user.is_shecodes_admin))

# Checks if the Logged in User is an Approver
class IsUserAnApprover(permissions.BasePermission):
    # Checks the User performing the object level permission is an Approver
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_approver)
    # Checks the logged in user is an Approver
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_approver)

class IsSuperUserOrAdminOrApprover(permissions.BasePermission):
    # A combined permission that checks either a SuperUser, Admin or Approver is performing the action
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_superuser or request.user.is_shecodes_admin)) or bool(request.user and request.user.is_approver)

# Detailed Authentication - Based on User ID that is associated with task

class IsOwnerOrReadOnly(permissions.BasePermission):
    # The person performing the action/viewing object is the Owner, otherwise only ReadOnly access
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

# Detailed Authentication - Based on User ID that is associated with task
class WinWallOwnerWritePermission(permissions.BasePermission):
    # Added feature enabling owner of the created WinWall to create, put and delete
    message = "Editing Win Wall data is restricted to the specific administrators & approvers of this site only."

    def has_object_permission(self, request, view, obj):
        # GET_METHOD is a tuple that contains get, options and head
        assignments = request.user.assignments.all()
        user_has_assignment = any((assignment.win_wall_id == obj.id  or assignment.collection_id == obj.collection.id) and (assignment.is_admin or assignment.is_approver) for assignment in assignments)
        
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user or user_has_assignment or bool(request.user and (request.user.is_superuser or request.user.is_shecodes_admin))


class WinWallBulkUpdatePermission(permissions.BasePermission):
    # Added feature enabling owner of the created WinWall to create, put and delete
    #updated to allow assignment or approvers or admins to a winwall or collection of winwalls
    message = "Editing Win Wall data is restricted to the administrators & approvers of this site only."

    def has_permission(self, request, view):
        # GET_METHOD is a tuple that contains get, options and head
        obj = WinWall.objects.get(pk=view.kwargs['pk'])
        assignments = request.user.assignments.all()
        user_has_assignment = any((assignment.win_wall_id == obj.id  or assignment.collection_id == obj.collection.id) and (assignment.is_admin or assignment.is_approver) for assignment in assignments)
        
        if request.method in SAFE_METHODS:
            return True

        return obj.owner == request.user or user_has_assignment or bool(request.user and (request.user.is_superuser or request.user.is_shecodes_admin))

class StickyNoteOwnerWritePermission(permissions.BasePermission):
    # Added feature enabling only the admins or the author of the sticky note to edit
    message = "Sticky notes can be edited, approved and archived only by approvers and admins."

    def has_object_permission(self, request, view, obj):

        assignments = request.user.assignments.all()
        user_has_assignment = any((assignment.win_wall_id == obj.win_wall.id  or assignment.collection_id == obj.win_wall.collection.id) and (assignment.is_admin or assignment.is_approver) for assignment in assignments)
        
        if request.method in SAFE_METHODS:
            return True

        return user_has_assignment or bool(request.user and (request.user.is_superuser or request.user.is_shecodes_admin or (request.user.is_approver and obj.win_wall.owner == request.user)))
