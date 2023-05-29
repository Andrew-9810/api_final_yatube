from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Ограничение автор или только для чтения."""
    message = "Доступ предоставляется только для чтения."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
