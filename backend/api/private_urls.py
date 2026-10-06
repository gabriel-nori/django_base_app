from django.urls import include, path

# Routes that require authentication.
# Include each app private URLs under the schema api/private/app/action
urlpatterns = [
    path("users/", include("apps.users.private_urls")),
]
