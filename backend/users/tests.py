from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class UserAuthTests(APITestCase):

    def setUp(self):
        # Create a test user for login/profile/logout tests
        self.user_password = "testpassword123"
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password=self.user_password,
            role="User"
        )

    def get_token_for_user(self, user):
        """Helper to generate JWT token for authenticated requests."""
        refresh = RefreshToken.for_user(user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }

    def test_register_user(self):
        url = reverse("register")
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "newpassword123",
            "role": "User"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(email="newuser@example.com").exists())

    def test_login_user(self):
        url = reverse("login")
        data = {
            "email": self.user.email,
            "password": self.user_password
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_profile_view_authenticated(self):
        url = reverse("get_profile")
        tokens = self.get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["email"], self.user.email)

    def test_profile_view_unauthenticated(self):
        url = reverse("get_profile")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_profile_update(self):
        url = reverse("update_profile")
        tokens = self.get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        new_data = {"username": "updateduser"}
        response = self.client.put(url, new_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, "updateduser")

    def test_logout_user(self):
        url = reverse("logout")
        tokens = self.get_token_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {tokens['access']}")
        response = self.client.post(url, {"refresh": tokens["refresh"]}, format="json")
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_reset_password(self):
        url = reverse("reset-password")
        data = {
            "email": self.user.email,
            "new_password": "newsecurepassword123"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Ensure password was actually updated
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newsecurepassword123"))

