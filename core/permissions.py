from rest_framework.permissions import BasePermission
from accounts.models import User

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        request.user and request.user.is_authenticated and request.user.role == User.Role.SUPERADMIN

class IsSchoolAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool (
            request.user and request.user.is_authenticated and request.user.role in [User.Role.SUPERADMIN, User.Role.ADMIN]
        )

class IsTeacherOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool (
            request.user and request.user.is_authenticated and request.user.role in [User.Role.SUPERADMIN, User.Role.ADMIN, User.Role.TEACHER]
        )

class IsAccountantOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool (
            request.user and request.user.is_authenticated and request.user.role in [User.Role.SUPERADMIN, User.Role.ADMIN, User.Role.TEACHER, User.Role.ACCOUNTANT]
        )