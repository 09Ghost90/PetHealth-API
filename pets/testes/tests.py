import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Pet


class PetAccessTests(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="u1", password="pass12345!")
        self.user2 = User.objects.create_user(username="u2", password="pass12345!")
        self.staff = User.objects.create_user(
            username="admin",
            password="pass12345!",
            is_staff=True,
        )

        self.pet1 = Pet.objects.create(
            name="Rex",
            especie="Cachorro",
            raca="Vira-lata",
            data_nascimento=datetime.date(2020, 1, 1),
            tutor=self.user1.tutor,
        )
        self.pet2 = Pet.objects.create(
            name="Mia",
            especie="Gato",
            raca="Siamês",
            data_nascimento=datetime.date(2021, 6, 1),
            tutor=self.user2.tutor,
        )

    def test_unauthenticated_cannot_access_pets(self):
        url = reverse("pets-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_tutor_lists_only_own_pets(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse("pets-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = {item["id"] for item in response.data}
        self.assertIn(self.pet1.id, returned_ids)
        self.assertNotIn(self.pet2.id, returned_ids)

    def test_tutor_cannot_retrieve_other_users_pet(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse("pets-detail", kwargs={"pk": self.pet2.id})
        response = self.client.get(url)
        # queryset filtrado -> DRF tende a responder 404
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_staff_sees_all_pets(self):
        self.client.force_authenticate(user=self.staff)
        url = reverse("pets-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = {item["id"] for item in response.data}
        self.assertIn(self.pet1.id, returned_ids)
        self.assertIn(self.pet2.id, returned_ids)

    def test_pet_create_is_bound_to_authenticated_tutor(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse("pets-list")
        payload = {
            "name": "Bolt",
            "especie": "Cachorro",
            "raca": "Labrador",
            "data_nascimento": "2019-05-20",
        }

        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        pet = Pet.objects.get(id=response.data["id"])
        self.assertEqual(pet.tutor, self.user1.tutor)
