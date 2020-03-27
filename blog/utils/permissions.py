from rest_framework.permissions import BasePermission


class SVIPPermission(BasePermission):
    message = "SVIP可访问"

    def has_permission(self, request, view):
        if request.user.userType != 3:
            return False
        return True


class OrdinaryPermission(BasePermission):

    def has_permission(self, request, view):
        return True


class VIPPermission(BasePermission):

    def has_permission(self, request, view):
        return True


class LoginPermission(BasePermission):

    def has_permission(self, request, view):
        return True
