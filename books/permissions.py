from django.http import HttpRequest
from django.views import View
from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request: HttpRequest, view: View) -> bool:
        return (
            request.method in permissions.SAFE_METHODS
        ) or bool(request.user and request.user.is_staff)
