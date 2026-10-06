from drf_spectacular.contrib.rest_framework_simplejwt import SimpleJWTScheme
from api.routes import PUBLIC_PATH_PREFIX


class RouteAwareJWTScheme(SimpleJWTScheme):
    """
    OpenAPI security for RouteAwareJWTAuthentication (extensions do not match
    subclasses). Token is optional on public routes and required elsewhere.
    """

    target_class = "api.authentication.RouteAwareJWTAuthentication"

    def get_security_requirement(self, auto_schema):
        requirement = super().get_security_requirement(auto_schema)
        if auto_schema.path.startswith(PUBLIC_PATH_PREFIX):
            # {} means "no authentication" is also accepted
            return [requirement, {}]
        return requirement
