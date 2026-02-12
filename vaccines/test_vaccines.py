from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from pets.models import Pet
from vaccines.models import Vaccine

'''
    Teste básico Tutor vs Staff no acesso a Vacinas de Pets.
'''

class VaccineTests(APITestCase):
    def login_and_set_token(self, username, password):
        res = self.client.post("/api/auth/login/", {"username": username, "password": password}, format="json")
        self.assertEqual(res.status_code, 200)
        token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_tutor_cannot_create_vaccine(self):
        tutor_user = User.objects.create_user(username="tutorA", email="a@email.com", password="123456")
        pet = Pet.objects.create(name="Luna", especie="Cachorro", raca="X", data_nascimento="2021-01-01", tutor=tutor_user.tutor)

        self.login_and_set_token("tutorA", "123456")

        payload = {
            "name": "Antirrábica",
            "applied_at": "2024-02-01",
            "next_dose": "2025-02-01",
            "notes": "Teste"
        }
        res = self.client.post(f"/api/pets/{pet.id}/vaccines/", payload, format="json")
        self.assertEqual(res.status_code, 403)

    def test_staff_can_create_vaccine_and_tutor_can_list(self):
        tutor_user = User.objects.create_user(username="tutorA", email="a@email.com", password="123456")
        pet = Pet.objects.create(name="Luna", especie="Cachorro", raca="X", data_nascimento="2021-01-01", tutor=tutor_user.tutor)

        staff_user = User.objects.create_user(username="adminA", email="admin@email.com", password="123456", is_staff=True)

        '''
            Staff cria vacina para pet do tutor
        '''

        self.login_and_set_token("adminA", "123456")
        payload = {
            "name": "Antirrábica",
            "applied_at": "2024-02-01",
            "next_dose": "2025-02-01",
            "notes": "Aplicada"
        }
        res = self.client.post(f"/api/pets/{pet.id}/vaccines/", payload, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertTrue(Vaccine.objects.filter(pet=pet, name="Antirrábica").exists())

        '''
            Tutor lista vacinas do próprio pet
        '''

        self.login_and_set_token("tutorA", "123456")
        res = self.client.get(f"/api/pets/{pet.id}/vaccines/")
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data), 1)
