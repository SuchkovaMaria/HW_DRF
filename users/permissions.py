from rest_framework import permissions


class IsModers(permissions.BasePermission):
    """Проверка пользователя на принадлежность к группе модераторов"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    """Проверка пользователя авторство курса или урока"""

    def has_object_permission(self, request, view, obj):

        if obj.owner == request.user:
            return True
        return False
