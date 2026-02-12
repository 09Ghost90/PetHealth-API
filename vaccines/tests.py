import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pets.models import Pet
from .models import Vaccine


class VaccineAccessTests(APITestCase):
	def setUp(self):
		self.tutor_user = User.objects.create_user(
			username="tutor",
			password="pass12345!",
		)
		self.other_tutor_user = User.objects.create_user(
			username="tutor2",
			password="pass12345!",
		)
		self.staff_user = User.objects.create_user(
			username="staff",
			password="pass12345!",
			is_staff=True,
		)

		self.pet_own = Pet.objects.create(
			name="Rex",
			especie="Cachorro",
			raca="Vira-lata",
			data_nascimento=datetime.date(2020, 1, 1),
			tutor=self.tutor_user.tutor,
		)
		self.pet_other = Pet.objects.create(
			name="Mia",
			especie="Gato",
			raca="Siamês",
			data_nascimento=datetime.date(2021, 6, 1),
			tutor=self.other_tutor_user.tutor,
		)

		self.vaccine = Vaccine.objects.create(
			pet=self.pet_own,
			name="V10",
			applied_at=datetime.date(2025, 1, 1),
			next_dose=datetime.date(2026, 1, 1),
			notes="Ok",
		)

	def test_tutor_can_list_vaccines_for_own_pet(self):
		self.client.force_authenticate(user=self.tutor_user)
		url = reverse("pet-vaccines", kwargs={"pet_id": self.pet_own.id})
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		returned_ids = {item["id"] for item in response.data}
		self.assertIn(self.vaccine.id, returned_ids)

	def test_tutor_listing_other_pets_vaccines_returns_empty(self):
		self.client.force_authenticate(user=self.tutor_user)
		url = reverse("pet-vaccines", kwargs={"pet_id": self.pet_other.id})
		response = self.client.get(url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(list(response.data), [])

	def test_tutor_cannot_create_vaccine(self):
		self.client.force_authenticate(user=self.tutor_user)
		url = reverse("pet-vaccines", kwargs={"pet_id": self.pet_own.id})
		payload = {
			"name": "Raiva",
			"applied_at": "2025-02-01",
			"next_dose": "2026-02-01",
			"notes": "",
		}

		response = self.client.post(url, payload, format="json")
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_staff_can_create_vaccine_for_pet(self):
		self.client.force_authenticate(user=self.staff_user)
		url = reverse("pet-vaccines", kwargs={"pet_id": self.pet_own.id})
		payload = {
			"name": "Raiva",
			"applied_at": "2025-02-01",
			"next_dose": "2026-02-01",
			"notes": "Dose anual",
		}

		response = self.client.post(url, payload, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertTrue(
			Vaccine.objects.filter(pet=self.pet_own, name="Raiva").exists()
		)
