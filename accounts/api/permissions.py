from rest_framework import permissions


class IsVolunteer(permissions.BasePermission):
    """
    Volunteer User permission
    """

    def has_permission(self, request, view):
        if hasattr(request.user, 'is_volunteer') and request.user.is_volunteer:
            return True
        else:
            return False


class IsSuperUser(permissions.BasePermission):
    """
    Super User permission
    """

    def has_permission(self, request, view):
        if hasattr(request.user, 'is_superuser') and request.user.is_superuser:
            return True
        else:
            return False


class IsAdmin(permissions.BasePermission):
    """
    Admin User permission
    """

    def has_permission(self, request, view):
        if hasattr(request.user, 'is_admin') and request.user.is_admin:
            return True
        else:
            return False


class IsAdminOrSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if (hasattr(request.user, 'is_admin') and request.user.is_admin) or \
                (hasattr(request.user, 'is_superuser') and request.user.is_superuser):
            return True
        else:
            return False
