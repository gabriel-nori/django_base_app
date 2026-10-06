from apps.users.serializers import SignUpSerializer, UserSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView


class SignUpView(CreateAPIView):
    """Public: create a new account."""

    serializer_class = SignUpSerializer


class MeView(RetrieveUpdateAPIView):
    """Private: read or update the authenticated user."""

    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
