from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        # Register the OpenAPI extension for the JWT authentication
        import api.schema  # noqa: F401
