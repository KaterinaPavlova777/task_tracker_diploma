from rest_framework.permissions import BasePermission


class CheckAccessLvl(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or request.user.is_staff or request.user.access_level >= 50


class AccessLvlOrIsPerformer(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_superuser or request.user.is_staff
                or request.user.access_level >= 50)

    def has_object_permission(self, request, view, obj):
        return (request.user.is_superuser or request.user.is_staff
                or request.user.access_level >= 50 or obj.performer == request.user)
