# DRF:
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from drf_yasg import openapi

# Django:
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
    api/swagger/      API docs
    everything else   SPA index.html, when SERVE_SPA=true
"""

schema_view = get_schema_view(
    openapi.Info(
        title=settings.APP_NAME,
        default_version="v1",
        description=settings.APP_DESCRIPTION,
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    authentication_classes=(JWTAuthentication,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path(
        "api/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="{}-swagger-ui".format(settings.APP_NAME),
    ),
    path("api/", include("rest_framework.urls")),
]

if settings.SERVE_SPA:
    # Must be the last pattern: any non backend route falls back to the SPA
    urlpatterns.append(
        re_path(r"^(?!api/|admin/|static/).*$", spa_index, name="spa"),
    )
