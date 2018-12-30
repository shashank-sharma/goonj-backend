from rest_framework import permissions


class IsVolunteer(permissions.BasePermission):
    """
    Volunteer User permission
    """

    def has_permission(self, request, view):
        return request.user.is_volunteer


class IsSuperUser(permissions.BasePermission):
    """
    Super User permission
    """

    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAdmin(permissions.BasePermission):
    """
    Admin User permission
    """

    def has_permission(self, request, view):
        return request.user.is_admin
