from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from django.urls import include, path, re_path
from django.contrib import admin

# Custom
from config.views import spa_index
from config import settings

"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/

Layout:
    admin/            Django admin
    api/public/       Open routes (api/public_urls.py)
    api/private/      Authenticated routes (api/private_urls.py)
    api/schema/       OpenAPI 3 schema (YAML, or JSON with ?format=json)
    api/swagger/      Swagger UI
    api/redoc/        ReDoc
    everything else   SPA index.html, when SERVE_SPA=true
"""

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
    path("api/", include("rest_framework.urls")),
]

if settings.SERVE_SPA:
    # Must be the last pattern: any non backend route falls back to the SPA
    urlpatterns.append(
        re_path(r"^(?!api/|admin/|static/).*$", spa_index, name="spa"),
    )
