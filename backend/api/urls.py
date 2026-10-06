from api.routes import PRIVATE_NAMESPACE, PUBLIC_NAMESPACE
from django.urls import include, path

urlpatterns = [
    # api/public/...  -> no authentication required
    path("public/", include(("api.public_urls", PUBLIC_NAMESPACE))),
    # api/private/... -> authentication required
    path("private/", include(("api.private_urls", PRIVATE_NAMESPACE))),
]
