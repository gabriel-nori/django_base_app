from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.permissions import AllowAny
from django.urls import include, path

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(permission_classes=[AllowAny]), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(permission_classes=[AllowAny]), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(permission_classes=[AllowAny]), name='token_verify')
]