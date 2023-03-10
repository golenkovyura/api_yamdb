from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка, что админ или суперюзер и безопасный метод"""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and request.user.is_admin))


class IsSuperUserIsAdminIsModeratorIsAuthor(permissions.BasePermission):
    """
    Разрешает анонимному пользователю только безопасные запросы.
    Доступ к запросам PATCH и DELETE предоставляется только
    суперпользователю Джанго, админу Джанго, аутентифицированным пользователям
    с ролью admin или moderator, а также автору объекта.
    """

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.is_admin
                     or request.user.is_moderator
                     or request.user == obj.author))


class IsAdmin(permissions.BasePermission):
    """Проверка, что админ или суперюзер"""

    def has_permission(self, request, view):
        return (request.user.is_authenticated and request.user.is_admin)
