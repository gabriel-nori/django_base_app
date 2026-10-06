from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework.exceptions import AuthenticationFailed
from api.routes import is_public_route


class RouteAwareJWTAuthentication(JWTAuthentication):
    """
    JWT authentication that does not reject public routes when the client
    sends an expired or invalid token: the request continues as anonymous.
    Private routes keep the default behaviour (401).
    """

    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except (InvalidToken, AuthenticationFailed):
            if is_public_route(request):
                return None
            raise
