from rest_framework import permissions
from .time import active
class TimePermit(permissions.BasePermission):

    def has_permission(self, request, view):
        return active()