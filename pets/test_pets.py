from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from pets.models import Pet

'''
    Teste básico de permissão e associação de Pets a Tutors.
'''

class PetTests(APITestCase):
    def login_and_set_token(self, username, password):
        res = self.client.post("/api/auth/login/", {"username": username, "password": password}, format="json")
        self.assertEqual(res.status_code, 200)
        token = res.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_tutor_creates_pet_and_it_is_linked(self):
        user = User.objects.create_user(username="tutorA", email="a@email.com", password="123456")

        '''
            Garantir tutor existe (signal cria automaticamente)
        '''

        _ = user.tutor

        self.login_and_set_token("tutorA", "123456")

        payload = {
            "name": "Luna",
            "especie": "Cachorro",
            "raca": "Vira-lata",
            "data_nascimento": "2021-06-15"
        }
        res = self.client.post("/api/pets/", payload, format="json")
        self.assertEqual(res.status_code, 201)

        pet_id = res.data["id"]
        pet = Pet.objects.get(id=pet_id)
        self.assertEqual(pet.tutor.user.username, "tutorA")

    def test_tutor_only_sees_own_pets(self):
        userA = User.objects.create_user(username="tutorA", email="a@email.com", password="123456")
        userB = User.objects.create_user(username="tutorB", email="b@email.com", password="123456")

        Pet.objects.create(name="PetA", especie="Cachorro", raca="X", data_nascimento="2021-01-01", tutor=userA.tutor)
        Pet.objects.create(name="PetB", especie="Cachorro", raca="Y", data_nascimento="2021-01-01", tutor=userB.tutor)

        self.login_and_set_token("tutorA", "123456")
        res = self.client.get("/api/pets/")
        self.assertEqual(res.status_code, 200)

        names = [p["name"] for p in res.data]
        self.assertIn("PetA", names)
        self.assertNotIn("PetB", names)

    def test_tutor_cannot_access_other_tutor_pet_detail(self):
        userA = User.objects.create_user(username="tutorA", email="a@email.com", password="123456")
        userB = User.objects.create_user(username="tutorB", email="b@email.com", password="123456")

        petB = Pet.objects.create(name="PetB", especie="Cachorro", raca="Y", data_nascimento="2021-01-01", tutor=userB.tutor)

        self.login_and_set_token("tutorA", "123456")
        res = self.client.get(f"/api/pets/{petB.id}/")
        # Normalmente retorna 404 quando queryset filtra (bom pra segurança)
        self.assertIn(res.status_code, [404, 403])
