from rest_framework.authtoken.admin import User
from rest_framework.permissions import BasePermission


class IsOwnerOrAdminOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == "GET":
            return True
        if request.user.is_staff:
            return True
        return request.user == obj.creator





