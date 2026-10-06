from api.routes import PRIVATE_NAMESPACE, PUBLIC_NAMESPACE
from django.urls import include, path

urlpatterns = [
    # api/public/...  -> no authentication required
    path(f"{PUBLIC_NAMESPACE}/", include(("api.public_urls", PUBLIC_NAMESPACE))),
    # api/private/... -> authentication required
    path(f"{PRIVATE_NAMESPACE}/", include(("api.private_urls", PRIVATE_NAMESPACE))),
]
