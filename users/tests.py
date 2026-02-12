from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Tutor


class AuthTests(APITestCase):
    def test_register_creates_user_and_tutor_profile(self):
        url = reverse("register")
        payload = {
            "username": "tutor_test",
            "email": "tutor_test@email.com",
            "password": "StrongPass123!@#",
            "telefone": "31999999999",
            "endereco": "Rua A, 123",
        }

        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user = User.objects.get(username="tutor_test")
        tutor = Tutor.objects.get(user=user)
        self.assertEqual(tutor.telefone, payload["telefone"])
        self.assertEqual(tutor.endereco, payload["endereco"])

    def test_login_returns_jwt_tokens(self):
        password = "StrongPass123!@#"
        User.objects.create_user(username="login_user", password=password)

        url = reverse("token_obtain_pair")
        response = self.client.post(
            url,
            {"username": "login_user", "password": password},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
