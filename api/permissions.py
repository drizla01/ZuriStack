from rest_framework import permissions


class IsCreatorOrAdminReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        edit_methods = ("PUT", "PATCH")

        # if its safe method (GET; HEAD; OPTION) allow
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_staff and request.method not in self.edit_methods:
            return True

        if request.user.is_superuser:
            return True

        if request.user == obj:
            return True
