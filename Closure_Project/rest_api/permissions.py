from rest_framework import permissions 

from rest_api.models import CoursePlan
from rest_framework.request import HttpRequest


def request_is_authenticated(request: HttpRequest) -> bool:
    return bool(request.user and request.user.is_authenticated)

class CoursePlanPermission(permissions.BasePermission):
    """ Allows anyone to read the course plan if it is public.
        The owner of the course plan can do anything with it. """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request_is_authenticated(request)

    def has_object_permission(self, request: HttpRequest, view, obj: CoursePlan):
        is_authenticated = request_is_authenticated(request)
        belongs_to_requester = is_authenticated and obj.owner.user == request.user
        if request.method in permissions.SAFE_METHODS:
            return belongs_to_requester or obj.public

        return belongs_to_requester

class IsAdminOrAuthenticatedReadOnly(permissions.IsAdminUser):
    """ Allows read-only access to authenticated users, and update access
        to admins only. """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request_is_authenticated(request)
        
        return super().has_permission(request, view)