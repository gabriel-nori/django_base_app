from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

UserModel = get_user_model()

SIGNUP_URL = "/api/public/users/signup/"
TOKEN_URL = "/api/public/token/"
ME_URL = "/api/private/users/me/"


class PublicPrivateRoutesTestCase(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            username="jane", email="jane@example.com", password="S3cure-pass!"
        )

    def get_access_token(self):
        response = self.client.post(
            TOKEN_URL, {"email": "jane@example.com", "password": "S3cure-pass!"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data["access"]

    def test_signup_is_public(self):
        response = self.client.post(
            SIGNUP_URL,
            {"username": "john", "email": "john@example.com", "password": "An0ther-pass!"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", response.data)
        self.assertTrue(UserModel.objects.get(email="john@example.com").check_password("An0ther-pass!"))

    def test_signup_rejects_weak_password(self):
        response = self.client.post(
            SIGNUP_URL, {"username": "john", "email": "john@example.com", "password": "123"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_uses_email(self):
        self.get_access_token()

    def test_private_route_requires_authentication(self):
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_private_route_with_token(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.get_access_token()}")
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], "jane@example.com")

    def test_invalid_token_is_ignored_on_public_route(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid.token.value")
        response = self.client.post(
            SIGNUP_URL,
            {"username": "john", "email": "john@example.com", "password": "An0ther-pass!"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_token_is_rejected_on_private_route(self):
        self.client.credentials(HTTP_AUTHORIZATION="Bearer invalid.token.value")
        response = self.client.get(ME_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
