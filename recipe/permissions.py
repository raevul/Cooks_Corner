from rest_framework import permissions
from user.models import AuthorProfile


class IsAuthorOrReadOnly(permissions.BasePermission):
    edit_methods = ("PUT", "PATCH", "DELETE")

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

            # Проверяем, является ли пользователь автором рецепта
        return obj.author == request.user
