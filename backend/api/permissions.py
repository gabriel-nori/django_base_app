from rest_framework.permissions import BasePermission
from api.routes import is_public_route


class IsPublicRouteOrAuthenticated(BasePermission):
    """
    Default permission: views under api/public/ are open, any other view
    requires an authenticated user. A view can still override it by
    declaring its own permission_classes.
    """

    def has_permission(self, request, view):
        if is_public_route(request):
            return True
        return bool(request.user and request.user.is_authenticated)
