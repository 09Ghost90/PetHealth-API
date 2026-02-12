from rest_framework.test import APITestCase
from django.contrib.auth.models import User

class AuthTests(APITestCase):
    def test_register_creates_user_and_tutor(self):
        payload = {
            "username": "tutor_teste",
            "email": "tutor_teste@email.com",
            "password": "StrongPass123!@#",
            "telefone": "31999999999",
            "endereco": "Rua ABC, 123",
        }

        res = self.client.post("/api/auth/register/", payload, format="json")
        self.assertEqual(res.status_code, 201)

        user = User.objects.get(username="tutor_teste")
        
        # A partir disso signal cria o Tutor automaticamente

        self.assertTrue(hasattr(user, "tutor"))
        self.assertEqual(user.tutor.telefone, "31999999999")

    def test_login_returns_tokens(self):
        User.objects.create_user(username="t1", email="t1@email.com", password="StrongPass123!@#")

        res = self.client.post("/api/auth/login/", {"username": "t1", "password": "StrongPass123!@#"}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertIn("access", res.data)
        self.assertIn("refresh", res.data)